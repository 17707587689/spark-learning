from pyspark.sql import SparkSession
from pyspark.sql.functions import count,avg,max,min

from src.etl.experiments.day03_10_customer_etl import transform_customer

def main():
    print(f"enter day04_10_job.py main")
    spark = (
        SparkSession.builder
        .appName("day04-customer-etl")
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

        # 开发阶段检查
        customer_df.show(20, truncate=False)

        print(f"province group result:{customer_df.groupBy('province').count().show()}")  

        print(customer_df.groupBy("province").count().explain(True))  

        customer_df.groupBy(
            "province",
            "customer_level"
        ).count().show()  

        customer_df.groupBy("province").agg(
            count("*").alias("customer_count"),
            avg("age").alias("avg_age"),
            max("age").alias("max_age"),
            min("age").alias("min_age")
        ).show()

        customer_df.agg(
            count("customer_id").alias("customer_count"),
            avg("age").alias("avg_age"),
            max("age").alias("max_age")
        ).show()

        province_stats = customer_df.groupBy("province").agg(
            count("*").alias("customer_count"),
            avg("age").alias("avg_age"),
            max("age").alias("max_age"),
            min("age").alias("min_age")
        )

        province_stats.show()

        province_stats.explain(True)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()