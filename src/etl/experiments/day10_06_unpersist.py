
from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("day10_06_unpersist")
        .enableHiveSupport()
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    try:
        print("\n========== 1. 读取客户表 ==========")
        df = spark.table("dim.customer")

        print("DataFrame 已创建")
        print(f"初始 StorageLevel：{df.storageLevel}")

        print("\n========== 2. 注册缓存 ==========")
        df.cache()
        print(f"调用 cache() 后：{df.storageLevel}")

        print("\n========== 3. 首次 Action：填充缓存 ==========")
        first_count = df.count()
        print(f"首次查询客户数：{first_count}")
        print(f"首次 Action 后：{df.storageLevel}")

        print("\n========== 4. 释放缓存 ==========")
        df.unpersist(blocking=True)
        print(f"unpersist 后：{df.storageLevel}")

        print("\n========== 5. 再次执行 Action ==========")
        second_count = df.count()
        print(f"再次查询客户数：{second_count}")
        print(f"再次 Action 后：{df.storageLevel}")

        print("\n========== 6. 验证结果 ==========")
        print(f"两次查询结果一致：{first_count == second_count}")
        print("注意：StorageLevel 表示持久化配置，不直接展示实际缓存字节数。")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
