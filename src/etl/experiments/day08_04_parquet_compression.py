
from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("day08_04_parquet_compression")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    # 1. 读取已有客户表
    print("\n========== 1. 读取客户表 ==========")

    df = spark.table("dim.customer")

    row_count = df.count()
    print(f"客户总数：{row_count}")
    df.printSchema()

    # 2. 设置实验输出目录
    base_path = (
        "hdfs://hadoop1:9000/user/Administrator/"
        "parquet_compression/day08_04"
    )

    # uncompressed 表示不压缩
    codecs = [
        "uncompressed",
        "snappy",
        "gzip",
        "zstd",
        "lz4",
    ]

    # 3. 通过 Hadoop FileSystem API 获取目录大小
    jvm = spark._jvm
    hadoop_conf = spark._jsc.hadoopConfiguration()
    Path = jvm.org.apache.hadoop.fs.Path

    results = []

    for codec in codecs:
        print(f"\n========== 写入算法：{codec} ==========")

        output_path = f"{base_path}/{codec}"

        # 4. 写入 Parquet
        (
            df.write
            .mode("overwrite")
            .option("compression", codec)
            .parquet(output_path)
        )

        # 5. 统计目录中所有文件的总字节数
        path = Path(output_path)
        fs = path.getFileSystem(hadoop_conf)

        total_bytes = 0
        parquet_files = 0

        iterator = fs.listFiles(path, True)

        while iterator.hasNext():
            file_status = iterator.next()

            if file_status.isFile():
                name = file_status.getPath().getName()

                # 只统计 Parquet 数据文件
                if name.endswith(".parquet"):
                    total_bytes += file_status.getLen()
                    parquet_files += 1

        # 6. 重新读取并验证数据量
        read_df = spark.read.parquet(output_path)
        actual_count = read_df.count()

        size_mb = total_bytes / (1024 * 1024)

        results.append(
            (
                codec,
                parquet_files,
                total_bytes,
                size_mb,
                actual_count,
            )
        )

        print(f"Parquet 文件数：{parquet_files}")
        print(f"数据文件总大小：{size_mb:.2f} MB")
        print(f"读取记录数：{actual_count}")

        if actual_count != row_count:
            raise RuntimeError(
                f"{codec} 数据量不一致："
                f"expected={row_count}, actual={actual_count}"
            )

    # 7. 汇总对比：使用 Python 本地列表打印
    # 避免 spark.createDataFrame(results) 触发额外的 Python Worker

    print("\n========== 7. 压缩效果汇总 ==========")

    print(
        f"{'compression':<15}"
        f"{'file_count':>12}"
        f"{'total_bytes':>15}"
        f"{'size_mb':>12}"
        f"{'read_count':>15}"
    )

    for item in sorted(results, key=lambda x: x[2]):
        codec, file_count, total_bytes, size_mb, read_count = item

        print(
            f"{codec:<15}"
            f"{file_count:>12}"
            f"{total_bytes:>15}"
            f"{size_mb:>12.2f}"
            f"{read_count:>15}"
        )

    print("实验完成：所有算法均已完成写入和读取验证。")

    spark.stop()


if __name__ == "__main__":
    main()
