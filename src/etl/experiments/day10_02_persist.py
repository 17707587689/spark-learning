
from pyspark.sql import SparkSession
from pyspark import StorageLevel


def main():
    spark = (
        SparkSession.builder
        .appName("day10_02_persist")
        .master("local[*]")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        print("========== 1. 读取客户表 ==========")
        df = spark.table("dim.customer")
        print(f"客户总数：{df.count()}")

        print("\n========== 2. 设置 persist ==========")
        cached_df = df.persist(StorageLevel.MEMORY_AND_DISK)
        print(f"StorageLevel：{cached_df.storageLevel}")

        print("\n========== 3. 第一次 Action ==========")
        print(f"客户总数：{cached_df.count()}")

        print("\n========== 4. 第二次 Action ==========")

        guangdong_df = cached_df.filter("province = '广东'")
        print(f"广东客户数：{guangdong_df.count()}")

        print("\n========== 5. 释放缓存 ==========")
        cached_df.unpersist()
        print("已请求释放缓存")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
