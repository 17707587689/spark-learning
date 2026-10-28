from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import (
    col,
    row_number,
    rank,
    dense_rank,
)


def main():
    spark = (
        SparkSession.builder
        .appName("Day06_06_DenseRank")
        .enableHiveSupport()
        .getOrCreate()
    )

    try:
        # 1. 读取现有 Hive Catalog 中的客户表
        customer_df = spark.table("dim.customer")

        print("========== 客户表基本信息 ==========")
        print(f"客户总数：{customer_df.count()}")

        # 2. 筛选上海客户
        shanghai_df = customer_df.filter(
            col("province") == "上海"
        )

        # 3. 定义窗口：按照年龄降序排名
        window_spec = (
            Window
            .partitionBy("province")
            .orderBy(col("age").desc())
        )

        # 4. 同时计算三种排名
        result_df = (
            shanghai_df
            .withColumn(
                "row_num",
                row_number().over(window_spec),
            )
            .withColumn(
                "rank_num",
                rank().over(window_spec),
            )
            .withColumn(
                "dense_rank_num",
                dense_rank().over(window_spec),
            )
        )

        print("\n========== 上海年龄排名前 20 的客户 ==========")

        result_df.orderBy(
            col("age").desc(),
            col("customer_id").asc(),
        ).select(
            "customer_id",
            "customer_name",
            "province",
            "age",
            "row_num",
            "rank_num",
            "dense_rank_num",
        ).show(20, truncate=False)

        # 5. 按年龄汇总，观察不同年龄对应的排名
        print("\n========== 上海各年龄对应的排名 ==========")

        result_df.groupBy(
            "age",
            "rank_num",
            "dense_rank_num",
        ).count().orderBy(
            col("age").desc()
        ).show(30, truncate=False)

        # 6. 查看执行计划
        print("\n========== 执行计划 ==========")
        result_df.explain("formatted")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()