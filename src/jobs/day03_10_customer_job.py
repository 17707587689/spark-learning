from pyspark.sql import SparkSession

from src.etl.experiments.day03_10_customer_etl import transform_customer

def main():
    print(f"enter day03_10_customer_job.py main()")
    spark = (
        SparkSession.builder
        .appName("day03-10-customer-etl")
        .enableHiveSupport()
        .getOrCreate()
    )

    print("Spark master:", spark.sparkContext.master)

    print(
        "fs.defaultFS:",
        spark.sparkContext._jsc.hadoopConfiguration().get("fs.defaultFS")
    )

    try:
        customer_df = spark.table("dim.customer")

        result_df = transform_customer(customer_df)

        # 开发阶段检查
        result_df.show(20, truncate=False)

        # 输出 Parquet
        (
            result_df.write
            .mode("overwrite")
            .parquet("hdfs://hadoop1:9000/user/Administrator/day03_10_customer")
        )

        print(f"overwrite day03_10_customer")

        df2 = spark.read.parquet("hdfs://hadoop1:9000/user/Administrator/day03_10_customer")
        print(f"df2.count is {df2.count()}")       

    finally:
        spark.stop()


if __name__ == "__main__":
    main()