from pyspark.sql import SparkSession

from src.etl.experiments.day05_09_sql_comprehensive import (
    run_customer_province_analysis
)


def main():
    spark = (
        SparkSession.builder
        .appName("day05_09_sql_comprehensive")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    # 读取 Hive 表
    customer_df = spark.table("dim.customer")

    print("========== 原始客户数据 ==========")
    customer_df.show(5)

    print("========== SQL 综合分析 ==========")

    result_df = run_customer_province_analysis(
        spark,
        customer_df
    )

    result_df.show()

    print("========== 执行计划 ==========")

    result_df.explain(True)

    spark.stop()


if __name__ == "__main__":
    main()