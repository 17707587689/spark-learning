
import time

from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("day10_04_cache_execution")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        print("\n========== 1. 读取源表 ==========")

        source_df = spark.table("dim.customer")

        # 加入过滤条件，构造本次实验使用的数据集
        df = source_df.filter("province = '广东'")

        print("DataFrame 已创建，尚未执行 Action")

        print("\n========== 2. 调用 cache() ==========")

        cached_df = df.cache()

        print("已调用 cache()")
        print("注意：此时不能认定数据已经全部进入缓存")

        print("\n========== 3. 首次 Action 前的执行计划 ==========")

        cached_df.explain("formatted")

        print("\n========== 4. 第一次执行 count() ==========")

        start_time = time.perf_counter()
        first_count = cached_df.count()
        first_time = time.perf_counter() - start_time

        print(f"第一次查询结果：{first_count}")
        print(f"第一次执行耗时：{first_time:.4f} 秒")

        print("\n========== 5. 首次 Action 后的执行计划 ==========")

        cached_df.explain("formatted")

        print("\n========== 6. 第二次执行 count() ==========")

        start_time = time.perf_counter()
        second_count = cached_df.count()
        second_time = time.perf_counter() - start_time

        print(f"第二次查询结果：{second_count}")
        print(f"第二次执行耗时：{second_time:.4f} 秒")

        print("\n========== 7. 结果检查 ==========")

        print(f"两次结果一致：{first_count == second_count}")
        print(f"第一次耗时：{first_time:.4f} 秒")
        print(f"第二次耗时：{second_time:.4f} 秒")

    finally:
        # 实验结束后释放缓存，避免影响后续实验
        spark.catalog.clearCache()
        spark.stop()


if __name__ == "__main__":
    main()
