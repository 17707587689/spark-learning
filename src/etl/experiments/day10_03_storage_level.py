
from pyspark import StorageLevel
from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("Day10_03_StorageLevel")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        print("========== 1. 查看常见 StorageLevel ==========")

        levels = [
            ("MEMORY_ONLY", StorageLevel.MEMORY_ONLY),
            ("MEMORY_AND_DISK", StorageLevel.MEMORY_AND_DISK),
            ("DISK_ONLY", StorageLevel.DISK_ONLY),
            ("MEMORY_AND_DISK_DESER",
             StorageLevel.MEMORY_AND_DISK_DESER),
        ]

        for name, level in levels:
            print(f"\n{name}")
            print(f"  useMemory: {level.useMemory}")
            print(f"  useDisk: {level.useDisk}")
            print(f"  useOffHeap: {level.useOffHeap}")
            print(f"  deserialized: {level.deserialized}")
            print(f"  replication: {level.replication}")

        print("\n========== 2. 读取客户表 ==========")
        df = spark.table("dim.customer")
        print(f"客户总数：{df.count()}")

        print("\n========== 3. 指定存储级别 ==========")
        cached_df = df.persist(StorageLevel.MEMORY_AND_DISK)

        # persist 本身是惰性的；用 Action 触发计算和缓存
        print(f"缓存后再次统计：{cached_df.count()}")

        print("\n========== 4. 检查 DataFrame 存储级别 ==========")
        print(cached_df.storageLevel)

        print("\n========== 5. 释放缓存 ==========")
        cached_df.unpersist()
        print("已调用 unpersist()")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
