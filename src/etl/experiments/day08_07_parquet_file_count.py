
from pyspark.sql import SparkSession


def count_parquet_files(spark, output_path):
    """统计 HDFS 目录及其子目录中的 Parquet 数据文件数量。"""
    hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
    path = spark._jvm.org.apache.hadoop.fs.Path(output_path)
    fs = path.getFileSystem(hadoop_conf)

    if not fs.exists(path):
        return 0

    iterator = fs.listFiles(path, True)
    file_count = 0

    while iterator.hasNext():
        file_status = iterator.next()
        if file_status.getPath().getName().endswith(".parquet"):
            file_count += 1

    return file_count


def write_and_check(spark, df, output_path, label):
    print(f"\n========== {label} ==========")
    print(f"写入前 Spark 分区数：{df.rdd.getNumPartitions()}")

    (
        df.write
        .mode("overwrite")
        .parquet(output_path)
    )

    parquet_count = count_parquet_files(spark, output_path)
    result_df = spark.read.parquet(output_path)
    result_count = result_df.count()

    print(f"输出路径：{output_path}")
    print(f"Parquet 文件数：{parquet_count}")
    print(f"读取记录数：{result_count}")

    return result_count


def main():
    spark = (
        SparkSession.builder
        .appName("day08_07_parquet_file_count")
        .master("local[*]")
        .enableHiveSupport()
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    base_path = (
        "hdfs://hadoop1:9000/user/Administrator/"
        "day08_07_write_parquet/file_count"
    )

    try:
        print("\n========== 1. 读取源表 ==========")
        source_df = spark.table("dim.customer")
        source_count = source_df.count()

        print(f"源表记录数：{source_count}")
        print(f"源 DataFrame 分区数：{source_df.rdd.getNumPartitions()}")

        # 实验 A：直接写入
        default_path = f"{base_path}/default"
        count_default = write_and_check(
            spark,
            source_df,
            default_path,
            "2. 默认方式写入"
        )

        # 实验 B：明确重新分为 4 个 Spark 分区
        repartition_df = source_df.repartition(4)
        repartition_path = f"{base_path}/repartition_4"

        count_repartition = write_and_check(
            spark,
            repartition_df,
            repartition_path,
            "3. repartition(4) 后写入"
        )

        # 实验 C：先得到 8 个分区，再减少到 2 个
        coalesce_df = source_df.repartition(8).coalesce(2)
        coalesce_path = f"{base_path}/coalesce_2"

        count_coalesce = write_and_check(
            spark,
            coalesce_df,
            coalesce_path,
            "4. repartition(8).coalesce(2) 后写入"
        )

        print("\n========== 5. 数据验证 ==========")
        if (
            count_default == source_count
            and count_repartition == source_count
            and count_coalesce == source_count
        ):
            print("PASS：三种方式写入后，记录数均与源表一致")
        else:
            print("FAIL：存在记录数不一致，请检查实验输出")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
