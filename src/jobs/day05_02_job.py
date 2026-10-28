from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("day05_02_select")
        .enableHiveSupport()
        .getOrCreate()
    )

    customer_df = spark.table("dim.customer")

    customer_df.createOrReplaceTempView("customer")

    result_df = spark.sql("""
        SELECT
            customer_id,
            customer_name,
            province,
            age,
            CASE
                WHEN age >= 60 THEN '老年'
                WHEN age >= 40 THEN '中年'
                ELSE '青年'
            END AS age_group
        FROM customer
        WHERE province = '广东'
        ORDER BY age DESC
        LIMIT 20
    """)

    result_df.show(20, truncate=False)

    print("=== 执行计划 ===")
    result_df.explain()

    spark.stop()


if __name__ == "__main__":
    main()