
from pathlib import Path

from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("day08_06_read_parquet")
        .master("local[*]")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    # 1. 读取现有 Hive 客户表
    print("\n========== 1. 读取源表 ==========")
    source_df = spark.table("dim.customer")

    print(f"源表记录数：{source_df.count()}")
    source_df.printSchema()

    # 2. 写入独立的 Parquet 测试目录
    # 使用 HDFS 路径，避免 Windows 本地路径与 HDFS 路径混淆
    parquet_path = (
        "hdfs://hadoop1:9000/user/Administrator/day08_06_customer_parquet"
    )

    print("\n========== 2. 写入测试 Parquet ==========")
    (
        source_df
        .write
        .mode("overwrite")
        .parquet(parquet_path)
    )
    print(f"测试文件路径：{parquet_path}")

    # 3. 使用 parquet() 读取
    print("\n========== 3. 使用 parquet() 读取 ==========")
    df1 = spark.read.parquet(parquet_path)

    print(f"读取记录数：{df1.count()}")
    df1.printSchema()
    df1.show(5, truncate=False)

    # 4. 使用 format().load() 读取
    print("\n========== 4. 使用 format().load() 读取 ==========")
    df2 = (
        spark.read
        .format("parquet")
        .load(parquet_path)
    )

    print(f"读取记录数：{df2.count()}")
    df2.show(5, truncate=False)

    # 5. 过滤数据：验证读取后的 DataFrame 可以继续处理
    print("\n========== 5. 读取后进行过滤 ==========")
    guangdong_df = df1.filter(df1.province == "广东")

    print(f"广东省客户数：{guangdong_df.count()}")
    guangdong_df.select(
        "customer_id",
        "customer_name",
        "province",
        "city",
        "age",
    ).show(10, truncate=False)

    # 6. 查看执行计划
    print("\n========== 6. 查看读取执行计划 ==========")
    df1.explain("formatted")

    spark.stop()


if __name__ == "__main__":
    main()
