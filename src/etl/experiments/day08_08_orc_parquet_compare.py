
from time import perf_counter

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def get_directory_stats(spark, path):
    """递归统计 HDFS 目录下的数据文件数量和总大小。"""
    jvm = spark._jvm
    hadoop_path = jvm.org.apache.hadoop.fs.Path(path)
    fs = hadoop_path.getFileSystem(
        spark._jsc.hadoopConfiguration()
    )

    total_bytes = 0
    file_count = 0

    iterator = fs.listFiles(hadoop_path, True)

    while iterator.hasNext():
        status = iterator.next()
        name = status.getPath().getName()

        # 排除 _SUCCESS 等标记文件
        if status.isFile() and not name.startswith("_") \
                and not name.startswith("."):
            total_bytes += status.getLen()
            file_count += 1

    return file_count, total_bytes


def format_size(size_bytes):
    return f"{size_bytes / 1024 / 1024:.2f} MB"


def benchmark_query(df):
    """执行相同的过滤与列选择，返回耗时和结果数量。"""
    query_df = (
        df.filter(F.col("province") == "广东")
        .select("customer_id", "province", "age")
    )

    start = perf_counter()
    count = query_df.count()
    elapsed = perf_counter() - start

    return query_df, count, elapsed


def main():
    spark = (
        SparkSession.builder
        .appName("day08_08_orc_parquet_compare")
        .master("local[*]")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    base_path = "hdfs://hadoop1:9000/user/Administrator"
    parquet_path = f"{base_path}/day08_08_customer_parquet"
    orc_path = f"{base_path}/day08_08_customer_orc"

    try:
        # 1. 读取同一份源数据
        print("\n========== 1. 读取源表 ==========")

        source_df = spark.table("dim.customer")
        source_count = source_df.count()

        print(f"源表记录数：{source_count}")
        source_df.printSchema()

        # 2. 分别写入两种格式
        print("\n========== 2. 写入 Parquet ==========")

        (
            source_df.write
            .format("parquet")
            .mode("overwrite")
            .save(parquet_path)
        )

        print(f"Parquet 路径：{parquet_path}")

        print("\n========== 3. 写入 ORC ==========")

        (
            source_df.write
            .format("orc")
            .mode("overwrite")
            .save(orc_path)
        )

        print(f"ORC 路径：{orc_path}")

        # 3. 统计文件数量和总大小
        print("\n========== 4. 文件大小比较 ==========")

        parquet_files, parquet_bytes = get_directory_stats(
            spark, parquet_path
        )
        orc_files, orc_bytes = get_directory_stats(
            spark, orc_path
        )

        print(
            f"Parquet：{parquet_files} 个数据文件，"
            f"{parquet_bytes:,} 字节，"
            f"{format_size(parquet_bytes)}"
        )

        print(
            f"ORC：{orc_files} 个数据文件，"
            f"{orc_bytes:,} 字节，"
            f"{format_size(orc_bytes)}"
        )

        if parquet_bytes > 0:
            ratio = orc_bytes / parquet_bytes
            print(f"ORC / Parquet 大小比例：{ratio:.3f}")

            if orc_bytes < parquet_bytes:
                print("本次结果：ORC 文件更小")
            elif orc_bytes > parquet_bytes:
                print("本次结果：Parquet 文件更小")
            else:
                print("本次结果：两者大小相同")

        # 4. 分别读取文件
        print("\n========== 5. 读取并验证 ==========")

        parquet_df = spark.read.parquet(parquet_path)
        orc_df = spark.read.orc(orc_path)

        parquet_count = parquet_df.count()
        orc_count = orc_df.count()

        print(f"源表记录数：{source_count}")
        print(f"Parquet 记录数：{parquet_count}")
        print(f"ORC 记录数：{orc_count}")

        print(
            "Parquet Schema 是否一致：",
            source_df.schema == parquet_df.schema
        )
        print(
            "ORC Schema 是否一致：",
            source_df.schema == orc_df.schema
        )

        print("\nParquet 前 5 条记录：")
        parquet_df.show(5, truncate=False)

        print("\nORC 前 5 条记录：")
        orc_df.show(5, truncate=False)

        # 5. 相同查询条件下比较读取和过滤耗时
        print("\n========== 6. 查询性能比较 ==========")

        parquet_query, parquet_result_count, parquet_seconds = (
            benchmark_query(parquet_df)
        )
        orc_query, orc_result_count, orc_seconds = (
            benchmark_query(orc_df)
        )

        print(f"Parquet 广东客户数：{parquet_result_count}")
        print(f"Parquet 查询耗时：{parquet_seconds:.3f} 秒")

        print(f"ORC 广东客户数：{orc_result_count}")
        print(f"ORC 查询耗时：{orc_seconds:.3f} 秒")

        # 6. 查看两个查询的执行计划
        print("\n========== 7. Parquet 执行计划 ==========")
        parquet_query.explain("formatted")

        print("\n========== 8. ORC 执行计划 ==========")
        orc_query.explain("formatted")

        # 7. 总结基本验证结果
        print("\n========== 9. 实验总结 ==========")

        print(
            "记录数是否一致：",
            source_count == parquet_count == orc_count
        )
        print(
            "查询结果数量是否一致：",
            parquet_result_count == orc_result_count
        )

        print("\n注意：耗时受缓存、JVM、文件大小和运行顺序影响。")
        print("单次结果不能直接证明某种格式始终更快。")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
