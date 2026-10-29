from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("Day10_09_ShuffleJoin")
        .master("local[*]")
        .config("spark.sql.autoBroadcastJoinThreshold", "-1")
        .config("spark.sql.adaptive.enabled", "false")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        customer_df = spark.createDataFrame(
            [
                (1, "张三"),
                (2, "李四"),
                (3, "王五"),
            ],
            ["customer_id", "customer_name"],
        )

        order_df = spark.createDataFrame(
            [
                (101, 2, 300.0),
                (102, 1, 500.0),
                (103, 3, 200.0),
            ],
            ["order_id", "customer_id", "amount"],
        )

        # 模拟两侧具有不同的初始分区分布
        customer_df = customer_df.repartition(2, "customer_id")
        order_df = order_df.repartition(3, "customer_id")

        result_df = customer_df.join(
            order_df,
            on="customer_id",
            how="inner",
        )

        print("========== 1. Join 结果 ==========")
        result_df.orderBy("customer_id").show()

        print("========== 2. 物理执行计划 ==========")
        result_df.explain("formatted")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()