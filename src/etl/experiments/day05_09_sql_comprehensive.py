from pyspark.sql import DataFrame, SparkSession


def run_customer_province_analysis(
    spark: SparkSession,
    customer_df: DataFrame
) -> DataFrame:

    # 注册临时视图
    customer_df.createOrReplaceTempView("customer")

    result_df = spark.sql("""
        SELECT
            province,
            COUNT(*) AS customer_count,
            ROUND(AVG(age), 2) AS avg_age,
            MIN(age) AS min_age,
            MAX(age) AS max_age
        FROM customer
        WHERE age IS NOT NULL
        GROUP BY province
        HAVING COUNT(*) >= 5000
           AND AVG(age) >= 35
        ORDER BY customer_count DESC, avg_age DESC
    """)

    return result_df