from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import avg, count


def main():
    spark = SparkSession.builder \
        .appName("day06_02_partitionBy") \
        .enableHiveSupport() \
        .getOrCreate()

    df = spark.table("dim.customer")

    # ============================================================
    # 1. 按 province 划分窗口
    # ============================================================
    window = Window.partitionBy("province")

    # ============================================================
    # 2. 每个省份的平均年龄
    # ============================================================
    result = df.withColumn(
        "province_avg_age",
        avg("age").over(window)
    )

    print("========== 每个省份的平均年龄 ==========")

    result.select(
        "customer_id",
        "customer_name",
        "province",
        "age",
        "province_avg_age"
    ).show(20, truncate=False)

    # ============================================================
    # 3. 每个省份的客户数量
    # ============================================================
    result2 = df.withColumn(
        "province_customer_count",
        count("*").over(window)
    )

    print("========== 每个省份的客户数量 ==========")

    result2.select(
        "customer_id",
        "province",
        "province_customer_count"
    ).show(20)

    # ============================================================
    # 4. province + gender
    # ============================================================
    window2 = Window.partitionBy(
        "province",
        "gender"
    )

    result3 = df.withColumn(
        "province_gender_avg_age",
        avg("age").over(window2)
    )

    print("========== 省份 + 性别平均年龄 ==========")

    result3.select(
        "customer_id",
        "province",
        "gender",
        "age",
        "province_gender_avg_age"
    ).show(20)

    df.groupBy("province", "gender") \
        .count() \
        .orderBy("province", "gender") \
        .show(50)

    df.groupBy("province", "gender") \
        .agg(
            avg("age").alias("avg_age")
        ) \
        .orderBy("province", "gender") \
        .show(50)

    spark.stop()


if __name__ == "__main__":
    main()