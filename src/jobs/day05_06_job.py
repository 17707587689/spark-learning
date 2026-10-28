from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import spark_partition_id

def main():
    spark = (
        SparkSession.builder
        .appName("day05_06_order_sort")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    customer_df = spark.table("dim.customer")

    print("=== 原始数据 ===")
    customer_df.select(
        "customer_id",
        "customer_name",
        "age",
        "province"
    ).show(10)

    print("=== ORDER BY age ASC ===")
    customer_df.select(
        "customer_id",
        "customer_name",
        "age",
        "province"
    ).orderBy(
        col("age").asc()
    ).show(20)

    print("=== ORDER BY age DESC ===")
    customer_df.select(
        "customer_id",
        "customer_name",
        "age",
        "province"
    ).orderBy(
        col("age").desc()
    ).show(20)

    print("=== 多字段 ORDER BY ===")
    customer_df.select(
        "customer_id",
        "customer_name",
        "age",
        "province"
    ).orderBy(
        col("province").asc(),
        col("age").desc()
    ).show(30)

    print("=== SORT BY ===")
    customer_df.select(
        "customer_id",
        "customer_name",
        "age",
        "province"
    ).sortWithinPartitions(
        col("age").asc()
    ).show(30)

    sort_df = customer_df.select(
    "customer_id",
    "customer_name",
    "age",
    "province"
    ).sortWithinPartitions(
        col("age").asc()
    )

    sort_df.withColumn(
        "partition_id",
        spark_partition_id()
    ).show(100, truncate=False)

    print("=== ORDER BY explain ===")
    customer_df.orderBy(
        col("age").asc()
    ).explain()

    customer_df.sortWithinPartitions(
        col("age").asc()
    ).explain()

    spark.stop()


if __name__ == "__main__":
    main()