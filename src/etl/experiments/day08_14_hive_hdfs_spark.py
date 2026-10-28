
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


APP_NAME = "day08_14_hive_hdfs_spark"

DATABASE = "day08_14_demo"
TABLE = "customer_summary"

OUTPUT_PATH = (
    "hdfs://hadoop1:9000/user/Administrator/"
    "day08_14_hive_hdfs_spark/customer_summary_data"
)


def main():
    spark = (
        SparkSession.builder
        .appName(APP_NAME)
        .config(
            "spark.sql.warehouse.dir",
            "hdfs://hadoop1:9000/user/hive/warehouse"
        )
        .config(
            "hive.metastore.uris",
            "thrift://192.168.214.129:9083"
        )
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:

        print(
            "catalogImplementation =",
            spark.conf.get("spark.sql.catalogImplementation")
        )

        print(
            "spark.sql.warehouse.dir =",
            spark.conf.get("spark.sql.warehouse.dir")
        )

        print(
            "hive.metastore.uris =",
            spark.sparkContext._jsc.hadoopConfiguration()
            .get("hive.metastore.uris")
        )

        print("当前数据库：")
        spark.sql("SELECT current_database()").show()
        # 1. 检查 Spark 与 Hive 配置
        print("\n========== 1. 检查环境 ==========")

        print(
            "catalogImplementation =",
            spark.conf.get("spark.sql.catalogImplementation")
        )

        print(
            "hive.metastore.uris =",
            spark.sparkContext._jsc.hadoopConfiguration()
            .get("hive.metastore.uris")
        )

        # 2. 读取 Hive 源表
        print("\n========== 2. 读取 Hive 源表 ==========")

        source_df = spark.table("dim.customer")

        source_count = source_df.count()
        print("源表记录数：", source_count)

        source_df.printSchema()

        # 3. 通过 Spark 执行数据处理
        print("\n========== 3. 生成省份统计 ==========")

        summary_df = (
            source_df
            .groupBy("province")
            .agg(
                F.count("*").alias("customer_count"),
                F.round(F.avg("age"), 2).alias("avg_age"),
                F.min("age").alias("min_age"),
                F.max("age").alias("max_age"),
            )
        )

        summary_df = summary_df.orderBy("province")

        print("统计结果行数：", summary_df.count())
        summary_df.show(20, truncate=False)

        # 4. 将结果写入 HDFS，格式为 Parquet
        print("\n========== 4. 写入 HDFS ==========")

        (
            summary_df.write
            .mode("overwrite")
            .format("parquet")
            .save(OUTPUT_PATH)
        )

        print("数据写入路径：", OUTPUT_PATH)

        # 5. 创建 Hive 数据库
        print("\n========== 5. 创建 Hive 数据库 ==========")

        DATABASE_LOCATION = (
            "hdfs://hadoop1:9000/user/Administrator/"
            "day08_14_hive_hdfs_spark/day08_14_demo.db"
        )

        spark.sql(
            f"""
            CREATE DATABASE IF NOT EXISTS {DATABASE}
            LOCATION '{DATABASE_LOCATION}'
            """
        )

        spark.sql(
            f"DESCRIBE DATABASE EXTENDED {DATABASE}"
        ).show(truncate=False)

        spark.sql(f"SHOW DATABASES LIKE '{DATABASE}'").show(
            truncate=False
        )

        # 6. 注册 Hive 外部表
        print("\n========== 6. 注册 Hive 外部表 ==========")

        full_table_name = f"{DATABASE}.{TABLE}"

        # 本实验允许重复执行：
        # 先删除旧表元数据，再重新注册。
        # 因为本表是外部表，DROP TABLE 不应删除外部数据文件。
        spark.sql(f"DROP TABLE IF EXISTS {full_table_name}")

        spark.sql(
            f"""
            CREATE TABLE {full_table_name}
            USING PARQUET
            LOCATION '{OUTPUT_PATH}'
            """
        )

        print("表结构及元数据信息：")

        spark.sql(
            f"DESCRIBE EXTENDED {full_table_name}"
        ).show(100, truncate=False)

        # 7. 从 Hive 表重新读取结果
        print("\n========== 7. 从 Hive 查询 ==========")

        hive_df = spark.table(full_table_name)

        print("Hive 表记录数：", hive_df.count())
        hive_df.orderBy("province").show(
            20, truncate=False
        )

        # 8. 验证数据一致性
        print("\n========== 8. 验证数据一致性 ==========")

        output_count = hive_df.count()

        print("Spark 统计结果行数：", summary_df.count())
        print("Hive 查询结果行数：", output_count)
        print(
            "记录数是否一致：",
            summary_df.count() == output_count
        )

        print("\n实验完成。")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
