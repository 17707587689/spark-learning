from pyspark.sql import SparkSession
from pyspark.sql.functions import count,avg,max,min,sum,col

def main():
    print(f"enter day04_03_job.py main")
    spark = (
        SparkSession.builder
        .appName("day04_03_jobs")
        .enableHiveSupport()
        .getOrCreate()
    )

    customer_df = spark.table("dim.customer")

    result_df = (
        customer_df
        .groupBy("province", "customer_level")
        .agg(
            count("customer_id").alias("customer_count"),
            avg("age").alias("avg_age"),
            max("age").alias("max_age"),
            min("age").alias("min_age")
        )
    )

    result_df2 = (
        customer_df
        .groupBy("province","customer_level")
        .agg(
            count("customer_id").alias("customer_count2"),
            avg("age").alias("age_avg"),
            min("age").alias("age_min"),
            max("age").alias("age_max")
        )
    )

    result_df2.show(30, truncate=False)

    result_df2.explain(True)   

if __name__ == "__main__":
    main()