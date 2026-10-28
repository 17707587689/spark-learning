
from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("day08_05_parquet_write")
        .master("local[*]")
        .config("spark.sql.catalogImplementation", "hive")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    # 使用独立的 HDFS 实验路径，避免修改现有业务表
    output_path = (
        "hdfs://hadoop1:9000/user/Administrator/"
        "day08_05_parquet_write"
    )

    try:
        # 1. 读取源数据
        print("\n========== 1. 读取 dim.customer ==========")

        source_df = spark.table("dim.customer")

        source_count = source_df.count()
        print(f"源数据总数：{source_count}")

        source_df.printSchema()

        # 2. 写入 Parquet
        print("\n========== 2. 写入 Parquet ==========")

        (
            source_df.write
            .format("parquet")
            .mode("overwrite")
            .save(output_path)
        )

        print(f"写入路径：{output_path}")
        print("Parquet 写入完成")

        # 3. 重新读取 Parquet
        print("\n========== 3. 重新读取 Parquet ==========")

        result_df = spark.read.parquet(output_path)

        result_count = result_df.count()
        print(f"读取数据总数：{result_count}")

        result_df.printSchema()

        # 4. 验证数据量
        print("\n========== 4. 验证数据量 ==========")

        print(f"源数据量：{source_count}")
        print(f"目标数据量：{result_count}")
        print(f"数据量是否一致：{source_count == result_count}")

        # 5. 验证业务数据
        print("\n========== 5. 查看客户数据 ==========")

        result_df.select(
            "customer_id",
            "customer_name",
            "province",
            "age",
            "customer_level",
        ).show(10, truncate=False)

        # 6. 查看输出目录的数据文件
        print("\n========== 6. 查看 Parquet 文件 ==========")

        hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
        jvm = spark.sparkContext._jvm
        path = jvm.org.apache.hadoop.fs.Path(output_path)
        fs = path.getFileSystem(hadoop_conf)

        for status in fs.listStatus(path):
            print(
                f"文件名：{status.getPath().getName()}, "
                f"目录：{status.isDirectory()}, "
                f"大小：{status.getLen()} bytes"
            )

        print("\n========== 实验完成 ==========")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
