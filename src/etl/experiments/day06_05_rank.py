
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def main():
    spark = (
        SparkSession.builder
        .appName("day06_05_rank")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        # 1. 读取客户维度表
        customer_df = spark.table("dim.customer")

        # 2. 按省份分组，年龄从大到小排名
        # 只按 age 排序，确保年龄相同的客户可以并列
        window_spec = (
            Window
            .partitionBy("province")
            .orderBy(F.col("age").desc())
        )

        # 3. 计算排名
        result_df = customer_df.withColumn(
            "age_rank",
            F.rank().over(window_spec)
        )

        # 4. 查看上海年龄排名前 10 的客户
        print("========== 上海年龄排名前 10 的客户 ==========")

        (
            result_df
            .filter(F.col("province") == "上海")
            .filter(F.col("age_rank") <= 10)
            .select(
                "customer_id",
                "customer_name",
                "province",
                "age",
                "age_rank"
            )
            .orderBy(
                F.col("age").desc(),
                F.col("customer_id").asc()
            )
            .show(50, truncate=False)
        )

        # 5. 查看物理执行计划
        print("========== 物理执行计划 ==========")
        result_df.explain("formatted")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()

# 1. 读取客户维度表
# 2. 按省份分组，年龄从大到小排名
# 3. 计算排名