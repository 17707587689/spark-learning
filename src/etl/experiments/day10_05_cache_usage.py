
import time

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def run_statistics(df, label):
    """对同一份 DataFrame 执行多个统计任务。"""
    print(f"\n========== {label} ==========")

    start = time.perf_counter()

    print("客户总数：", df.count())

    df.groupBy("customer_level").count().show()

    df.groupBy("province").count().show()

    elapsed = time.perf_counter() - start
    print(f"{label}耗时：{elapsed:.2f} 秒")


def main():
    spark = (
        SparkSession.builder
        .appName("Day10_05_CacheUsage")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        # 1. 读取源表并构造共享的中间结果
        source_df = spark.table("dim.customer")

        df = source_df.filter(
            F.col("age").isNotNull()
        ).select(
            "customer_id",
            "age",
            "customer_level",
            "province",
        )

        print("========== 实验一：不缓存 ==========")
        run_statistics(df, "不缓存")

        print("\n========== 实验二：使用缓存 ==========")
        cached_df = df.cache()

        # cache() 是惰性操作；
        # 第一次 Action 会触发计算和缓存填充。
        run_statistics(cached_df, "缓存")

        print("\n========== 实验三：释放缓存 ==========")
        cached_df.unpersist()
        print("已调用 unpersist()")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
