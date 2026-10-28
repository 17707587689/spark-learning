from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("day08_01_parquet_basics")
        .enableHiveSupport()
        .getOrCreate()
    )

    try:
        # 1. 读取已有的 Hive 表
        df = spark.table("dim.customer")

        print("\n========== 1. 表结构 Schema ==========")
        df.printSchema()

        print("\n========== 2. 数据总量 ==========")
        print(f"客户总数：{df.count()}")

        print("\n========== 3. 查看样例数据 ==========")
        df.select(
            "customer_id",
            "customer_name",
            "age",
            "province"
        ).show(5, truncate=False)

        print("\n========== 4. 查看表的存储信息 ==========")
        spark.sql("DESCRIBE FORMATTED dim.customer").show(
            100,
            truncate=False
        )

        print("\n========== 5. 检查文件格式 ==========")
        print("DataFrame 数据源格式：")
        df.explain("formatted")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()