
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

    source_df = spark.table("dim.customer")

    output_path = (
        "hdfs://hadoop1:9000/user/Administrator/"
        "day08_07_write_parquet/append"
    )

    # 第一次：覆盖写入，建立初始数据
    source_df.write.mode("overwrite").parquet(output_path)

    df1 = spark.read.parquet(output_path)
    print(f"第一次写入后：{df1.count()}")

    # 第二次：追加相同数据
    source_df.write.mode("append").parquet(output_path)

    df2 = spark.read.parquet(output_path)
    print(f"第二次追加后：{df2.count()}")

    # 检查重复客户编号
    print(
        "客户编号为 1 的记录数：",
        df2.filter("customer_id = 1").count()
    )

if __name__ == "__main__":
    main()
