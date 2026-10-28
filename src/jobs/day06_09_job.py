
from pyspark.sql import SparkSession
from src.etl.experiments.day06_09_window_aggregation import (
    run_window_aggregation,
)


def main():
    spark = (
        SparkSession.builder
        .appName("day06_09_window_aggregation")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        # 读取已有的 Hive/Spark 表
        customer_df = spark.table("dim.customer")

        print("\n========== 客户表基本信息 ==========")
        print(f"客户总数：{customer_df.count()}")

        # 执行窗口聚合
        result_df = run_window_aggregation(customer_df)

        print("\n========== 窗口聚合结果 ==========")
        result_df.select(
            "customer_id",
            "customer_name",
            "province",
            "age",
            "province_customer_count",
            "province_avg_age",
            "province_max_age",
            "province_min_age",
            "province_total_age",
            "running_customer_count",
        ).orderBy(
            "province", "register_date", "customer_id"
        ).show(20, truncate=False)

        print("\n========== 验证客户明细是否保留 ==========")
        print(f"原始行数：{customer_df.count()}")
        print(f"结果行数：{result_df.count()}")

        print("\n========== 执行计划 ==========")
        result_df.explain("formatted")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
