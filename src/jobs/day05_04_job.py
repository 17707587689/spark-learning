from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("Day05-04-GroupBy")
        .enableHiveSupport()
        .getOrCreate()
    )

    customer_df = spark.table("dim.customer")

    customer_df.createOrReplaceTempView("customer")

    print("=== 1. 按省份统计客户数量 ===")

    spark.sql("""
        SELECT
            province,
            COUNT(*) AS customer_count
        FROM customer
        GROUP BY province
    """).show()

    print("=== 2. 按省份统计平均年龄 ===")

    spark.sql("""
        SELECT
            province,
            AVG(age) AS avg_age
        FROM customer
        GROUP BY province
    """).show()

    print("=== 3. 按省份统计多个指标 ===")

    spark.sql("""
        SELECT
            province,
            COUNT(*) AS customer_count,
            AVG(age) AS avg_age,
            MIN(age) AS min_age,
            MAX(age) AS max_age
        FROM customer
        GROUP BY province
    """).show()

    print("=== 4. 按省份 + 客户等级统计 ===")

    spark.sql("""
        SELECT
            province,
            customer_level,
            COUNT(*) AS customer_count
        FROM customer
        GROUP BY
            province,
            customer_level
    """).show()

    print("=== 5. WHERE + GROUP BY ===")

    spark.sql("""
        SELECT
            customer_level,
            COUNT(*) AS customer_count
        FROM customer
        WHERE province = '广东'
        GROUP BY customer_level
    """).show()

    spark.stop()


if __name__ == "__main__":
    main()