from pyspark.sql import SparkSession
from pyspark.sql.functions import count,avg,max,min,sum

def main():
    print(f"enter day04_03_job.py main")
    spark = (
        SparkSession.builder
        .appName("day04_03_jobs")
        .enableHiveSupport()
        .getOrCreate()
    )

    customer_df = spark.table("dim.customer")

    customer_df.select(
        count("*").alias("customer_count")
    ).show()

    # customer_df.groupBy("province").agg(
    #     count("*").alias("province_count")
    # ).show()

    result_df = customer_df.groupBy("province") \
    .agg(
        count("*").alias("customer_count"),
        sum("age").alias("total_age"),
        avg("age").alias("avg_age")
    )

    result_df.show()

if __name__ == "__main__":
    main()