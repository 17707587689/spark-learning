
from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("day08_07_partition_parquet")
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

    # 2. 按 province 分区写入
    output_path = (
        "hdfs://hadoop1:9000/user/Administrator/"
        "day08_07_write_parquet/partitioned"
    )

    print("\n========== 2. 按省份分区写入 ==========")
    (
        source_df.write
        .mode("overwrite")
        .partitionBy("province")
        .parquet(output_path)
    )

    print(f"写入路径：{output_path}")

    # 3. 重新读取数据
    print("\n========== 3. 读取分区数据 ==========")
    result_df = spark.read.parquet(output_path)

    result_count = result_df.count()
    print(f"读取记录数：{result_count}")

    result_df.printSchema()

    # 4. 统计各省份记录数
    print("\n========== 4. 各省份记录数 ==========")
    (
        result_df
        .groupBy("province")
        .count()
        .orderBy("province")
        .show(20, truncate=False)
    )

    # 5. 验证广东省数据
    print("\n========== 5. 查询广东省客户 ==========")
    guangdong_df = result_df.filter(
        result_df.province == "广东"
    )

    print(f"广东省客户数：{guangdong_df.count()}")

    guangdong_df.select(
        "customer_id",
        "customer_name",
        "province",
        "city",
        "age",
    ).show(5, truncate=False)

    # 6. 查看物理执行计划
    print("\n========== 6. 查看分区裁剪执行计划 ==========")
    guangdong_df.explain("formatted")

    # 7. 验证总记录数
    print("\n========== 7. 数据验证 ==========")
    if source_count == result_count:
        print("PASS：源表与分区数据记录数一致")
    else:
        print("FAIL：源表与分区数据记录数不一致")

    spark.stop()


if __name__ == "__main__":
    main()
