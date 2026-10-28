from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("Day05-03-Where")
        .enableHiveSupport()
        .getOrCreate()
    )

    # 读取 Hive 表
    customer_df = spark.table("dim.customer")

    # 注册临时视图
    customer_df.createOrReplaceTempView("customer")

    print("=== 1. 广东客户 ===")

    spark.sql("""
        SELECT
            customer_id,
            customer_name,
            province,
            age
        FROM customer
        WHERE province = '广东'
    """).show(10)

    print("=== 2. 年龄 >= 50 ===")

    spark.sql("""
        SELECT
            customer_id,
            customer_name,
            province,
            age
        FROM customer
        WHERE age >= 50
    """).show(10)

    print("=== 3. 广东且年龄 >= 50 ===")

    spark.sql("""
        SELECT
            customer_id,
            customer_name,
            province,
            age
        FROM customer
        WHERE province = '广东'
          AND age >= 50
    """).show(10)

    print("=== 4. 广东、江苏、浙江 ===")

    spark.sql("""
        SELECT
            customer_id,
            customer_name,
            province,
            age
        FROM customer
        WHERE province IN ('广东', '江苏', '浙江')
    """).show(10)

    print("=== 5. 年龄 30~40 ===")

    spark.sql("""
        SELECT
            customer_id,
            customer_name,
            province,
            age
        FROM customer
        WHERE age BETWEEN 30 AND 40
    """).show(10)

    spark.stop()


if __name__ == "__main__":
    main()