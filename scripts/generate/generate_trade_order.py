from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    rand,
    round as spark_round,
    when,
    to_date,
    expr,
)
from pyspark.sql.types import LongType


ORDER_COUNT = 300_000
CUSTOMER_COUNT = 100_000

DATABASE = "ods"
TABLE = "trade_order"


def create_spark_session():
    return (
        SparkSession.builder
        .appName("GenerateTradeOrder")
        .enableHiveSupport()
        .getOrCreate()
    )


def generate_trade_order_data(spark):
    """
    生成 300,000 条交易订单数据。

    customer_id 设计：
    - 90%：1 ~ 100000，可以匹配 dim.customer
    - 10%：100001 ~ 110000，不存在于 dim.customer
          用于后续学习 inner join / left join
    """

    trade_order_df = (
        spark.range(1, ORDER_COUNT + 1)
        .withColumnRenamed("id", "order_id")
        .withColumn(
            "customer_id",
            when(
                rand(seed=42) < 0.90,
                (rand(seed=43) * CUSTOMER_COUNT)
                .cast(LongType()) + 1
            ).otherwise(
                (rand(seed=44) * 10000)
                .cast(LongType())
                + CUSTOMER_COUNT
                + 1
            )
        )
        .withColumn(
            "amount",
            spark_round(
                rand(seed=45) * 9900 + 100,
                2
            )
        )
        .withColumn(
            "order_date",
            to_date(
                expr(
                    "date_add('2025-01-01', "
                    "cast(rand(46) * 365 as int))"
                )
            )
        )
        .withColumn(
            "order_status",
            when(rand(seed=47) < 0.70, "COMPLETED")
            .when(rand(seed=48) < 0.90, "PAID")
            .otherwise("CANCELLED")
        )
    )

    return trade_order_df


def main():
    spark = create_spark_session()

    try:
        print("=" * 60)
        print("开始生成交易订单数据")
        print("=" * 60)

        trade_order_df = generate_trade_order_data(spark)

        print("\n订单表结构：")
        trade_order_df.printSchema()

        print("\n订单数量：")
        print(trade_order_df.count())

        print("\n订单示例：")
        trade_order_df.show(10, truncate=False)

        # 确保 ods 数据库存在
        spark.sql("CREATE DATABASE IF NOT EXISTS ods")

        # 删除旧的 trade_order 表，保证脚本可以重复执行
        spark.sql("DROP TABLE IF EXISTS ods.trade_order")

        # 写入 Hive
        (
            trade_order_df
            .write
            .mode("overwrite")
            .format("parquet")
            .saveAsTable("ods.trade_order")
        )

        print("\n" + "=" * 60)
        print("ods.trade_order 创建成功")
        print("=" * 60)

        print("\nHive 表信息：")
        spark.sql("DESC ods.trade_order").show(truncate=False)

        print("\n订单数量：")
        spark.sql(
            "SELECT COUNT(*) FROM ods.trade_order"
        ).show()

        print("\n订单数据：")
        spark.sql(
            """
            SELECT *
            FROM ods.trade_order
            LIMIT 10
            """
        ).show(truncate=False)

        print("\ncustomer_id 范围：")
        spark.sql(
            """
            SELECT
                MIN(customer_id) AS min_customer_id,
                MAX(customer_id) AS max_customer_id
            FROM ods.trade_order
            """
        ).show()

    finally:
        spark.stop()


if __name__ == "__main__":
    main()