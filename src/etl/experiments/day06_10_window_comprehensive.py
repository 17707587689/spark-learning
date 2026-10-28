
from pyspark.sql import SparkSession
from pyspark.sql import Window
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("day06_10_window_comprehensive")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        # ==================================================
        # 1. 读取客户表
        # ==================================================
        print("\n========== 1. 读取客户表 ==========")

        customer_df = spark.table("dim.customer")

        print(f"客户总数：{customer_df.count()}")

        customer_df.select(
            "customer_id",
            "customer_name",
            "province",
            "gender",
            "age",
        ).show(5, truncate=False)

        # ==================================================
        # 2. 定义不同用途的窗口
        # ==================================================

        # 窗口 A：按省份分组，不排序
        province_window = (
            Window.partitionBy("province")
        )

        # 窗口 B：同省客户按年龄降序排名
        # 不增加 customer_id 排序条件，才能保留年龄并列排名
        rank_window = (
            Window
            .partitionBy("province")
            .orderBy(F.col("age").desc())
        )

        # 窗口 C：同省客户按年龄降序、客户 ID 升序排列
        # 用于 lag、lead 和累计统计，保证顺序稳定
        ordered_window = (
            Window
            .partitionBy("province")
            .orderBy(
                F.col("age").desc(),
                F.col("customer_id").asc(),
            )
        )

        # 窗口 D：从当前省份的第一行累计到当前行
        running_window = (
            ordered_window
            .rowsBetween(
                Window.unboundedPreceding,
                Window.currentRow,
            )
        )

        # ==================================================
        # 3. 省份窗口聚合
        # ==================================================
        print("\n========== 2. 省份窗口聚合 ==========")

        province_stats_df = (
            customer_df
            .withColumn(
                "province_customer_count",
                F.count("*").over(province_window),
            )
            .withColumn(
                "province_avg_age",
                F.round(F.avg("age").over(province_window), 2),
            )
            .withColumn(
                "province_max_age",
                F.max("age").over(province_window),
            )
        )

        province_stats_df.select(
            "customer_id",
            "customer_name",
            "province",
            "age",
            "province_customer_count",
            "province_avg_age",
            "province_max_age",
        ).filter(
            F.col("province") == "上海"
        ).orderBy(
            F.col("age").desc(),
            F.col("customer_id").asc(),
        ).show(10, truncate=False)

        # ==================================================
        # 4. 对比三种排名函数
        # ==================================================
        print("\n========== 3. row_number / rank / dense_rank ==========")

        ranking_df = (
            customer_df
            .withColumn(
                "row_num",
                F.row_number().over(rank_window),
            )
            .withColumn(
                "rank_num",
                F.rank().over(rank_window),
            )
            .withColumn(
                "dense_rank_num",
                F.dense_rank().over(rank_window),
            )
        )

        ranking_df.filter(
            F.col("province") == "上海"
        ).select(
            "customer_id",
            "customer_name",
            "province",
            "age",
            "row_num",
            "rank_num",
            "dense_rank_num",
        ).orderBy(
            F.col("age").desc(),
            F.col("customer_id").asc(),
        ).show(20, truncate=False)

        # ==================================================
        # 5. 使用 lag 和 lead 获取前后行
        # ==================================================
        print("\n========== 4. lag / lead ==========")

        adjacent_df = (
            customer_df
            .withColumn(
                "previous_age",
                F.lag("age", 1).over(ordered_window),
            )
            .withColumn(
                "next_age",
                F.lead("age", 1).over(ordered_window),
            )
            .withColumn(
                "age_diff_from_previous",
                F.col("age") - F.col("previous_age"),
            )
        )

        adjacent_df.filter(
            F.col("province") == "上海"
        ).select(
            "customer_id",
            "customer_name",
            "province",
            "age",
            "previous_age",
            "next_age",
            "age_diff_from_previous",
        ).orderBy(
            F.col("age").desc(),
            F.col("customer_id").asc(),
        ).show(15, truncate=False)

        # ==================================================
        # 6. 累计客户数、累计平均年龄
        # ==================================================
        print("\n========== 5. 累计窗口统计 ==========")

        running_df = (
            customer_df
            .withColumn(
                "running_customer_count",
                F.count("*").over(running_window),
            )
            .withColumn(
                "running_avg_age",
                F.round(F.avg("age").over(running_window), 2),
            )
            .withColumn(
                "running_max_age",
                F.max("age").over(running_window),
            )
        )

        running_df.filter(
            F.col("province") == "上海"
        ).select(
            "customer_id",
            "customer_name",
            "province",
            "age",
            "running_customer_count",
            "running_avg_age",
            "running_max_age",
        ).orderBy(
            F.col("age").desc(),
            F.col("customer_id").asc(),
        ).show(15, truncate=False)

        # ==================================================
        # 7. 对比窗口函数与 groupBy 聚合
        # ==================================================
        print("\n========== 6. groupBy 聚合结果 ==========")

        group_stats_df = (
            customer_df
            .groupBy("province")
            .agg(
                F.count("*").alias("customer_count"),
                F.round(F.avg("age"), 2).alias("avg_age"),
                F.max("age").alias("max_age"),
            )
            .orderBy("province")
        )

        group_stats_df.show(20, truncate=False)

        # ==================================================
        # 8. 查看执行计划
        # ==================================================
        print("\n========== 7. 窗口函数执行计划 ==========")

        running_df.filter(
            F.col("province") == "上海"
        ).explain(True)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
