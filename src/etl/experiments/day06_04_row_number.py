
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def main():
    spark = (
        SparkSession.builder
        .appName("day06_04_row_number")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        # 1. 读取现有客户维度表
        customer_df = spark.table("dim.customer")

        # 2. 定义窗口：按省份分组，年龄降序排列
        window_spec = (
            Window
            .partitionBy("province")
            .orderBy(
                F.col("age").desc(),
                F.col("customer_id").asc()
            )
        )

        # 3. 生成组内行号
        result_df = customer_df.withColumn(
            "row_num",
            F.row_number().over(window_spec)
        )

        # 4. 查看上海年龄最大的前 10 名客户
        print("========== 上海年龄排名前 10 的客户 ==========")

        (
            result_df
            .filter(F.col("province") == "上海")
            .orderBy("row_num")
            .select(
                "customer_id",
                "customer_name",
                "province",
                "age",
                "row_num"
            )
            .show(10, truncate=False)
        )

        # 5. 查看执行计划
        print("========== 物理执行计划 ==========")
        result_df.explain("formatted")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()

