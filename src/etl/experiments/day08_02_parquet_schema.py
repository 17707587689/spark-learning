
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("Day08_02_Parquet_Schema")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    # 1. 读取已有的客户维度表
    print("\n========== 1. 读取 dim.customer ==========")

    customer_df = spark.table("dim.customer")

    print(f"客户总数：{customer_df.count()}")

    # 2. 查看 DataFrame Schema
    print("\n========== 2. DataFrame Schema ==========")

    customer_df.printSchema()

    print("\n========== 3. 获取 Schema 对象 ==========")

    print(customer_df.schema)

    # 4. 遍历字段，查看字段名称、类型、可空性
    print("\n========== 4. 遍历 Schema 字段 ==========")

    for field in customer_df.schema.fields:
        print(
            f"字段名：{field.name}, "
            f"数据类型：{field.dataType}, "
            f"是否可空：{field.nullable}"
        )

    # 5. 将数据写入独立的 Parquet 测试目录
    parquet_path = (
        "hdfs://hadoop1:9000/user/Administrator/day08_02_customer_parquet"
    )

    print("\n========== 5. 写入 Parquet ==========")

    (
        customer_df
        .write
        .mode("overwrite")
        .parquet(parquet_path)
    )

    print(f"Parquet 路径：{parquet_path}")

    # 6. 从 Parquet 文件重新读取数据
    print("\n========== 6. 重新读取 Parquet ==========")

    parquet_df = spark.read.parquet(parquet_path)

    print(f"读取记录数：{parquet_df.count()}")

    # 7. 查看 Parquet 读取后的 Schema
    print("\n========== 7. Parquet Schema ==========")

    parquet_df.printSchema()

    # 8. 比较写入前后的 Schema
    print("\n========== 8. Schema 对比 ==========")

    print(f"原始 Schema：{customer_df.schema}")
    print(f"Parquet Schema：{parquet_df.schema}")

    print(
        "Schema 是否完全相同：",
        customer_df.schema == parquet_df.schema
    )

    # 9. 查看读取后的数据
    print("\n========== 9. 查看客户样例 ==========")

    parquet_df.select(
        "customer_id",
        "customer_name",
        "province",
        "age",
        "register_date"
    ).show(10, truncate=False)

    # 10. 查看 Schema 中的字段名
    print("\n========== 10. 字段名称列表 ==========")

    print(parquet_df.schema.fieldNames())

    spark.stop()


if __name__ == "__main__":
    main()
