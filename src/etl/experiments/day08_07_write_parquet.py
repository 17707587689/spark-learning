
from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("day08_07_write_parquet")
        .master("local[*]")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    # 1. 读取源表
    print("\n========== 1. 读取源表 ==========")
    source_df = spark.table("dim.customer")

    source_count = source_df.count()
    print(f"源表记录数：{source_count}")
    source_df.printSchema()

    # 2. 定义独立的 HDFS 输出目录
    output_path = (
        "hdfs://hadoop1:9000/user/Administrator/"
        "day08_07_write_parquet/basic"
    )

    # 3. 写入 Parquet
    print("\n========== 2. 写入 Parquet ==========")
    (
        source_df.write
        .mode("overwrite")
        .parquet(output_path)
    )

    print(f"写入路径：{output_path}")
    print("写入完成")

    # 4. 重新读取写入结果
    print("\n========== 3. 重新读取 Parquet ==========")
    result_df = spark.read.parquet(output_path)

    result_count = result_df.count()
    print(f"读取记录数：{result_count}")

    result_df.printSchema()
    result_df.show(5, truncate=False)

    # 5. 验证数据量
    print("\n========== 4. 数据验证 ==========")

    if source_count == result_count:
        print("PASS：源表与写入结果的记录数一致")
    else:
        print("FAIL：源表与写入结果的记录数不一致")

    spark.stop()


if __name__ == "__main__":
    main()
