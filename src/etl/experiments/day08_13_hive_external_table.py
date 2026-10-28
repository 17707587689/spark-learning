
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

HDFS_BASE = "hdfs://hadoop1:9000/user/Administrator/day08_13_external"
DATA_PATH = f"{HDFS_BASE}/customer_data"
TABLE_NAME = "default.day08_13_customer_external"


def main():
    spark = (
        SparkSession.builder
        .appName("Day08-13-Hive-External-Table")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        print("\n========== 1. 检查 Hive 配置 ==========")
        print(
            "catalogImplementation =",
            spark.conf.get("spark.sql.catalogImplementation")
        )
        print(
            "hive.metastore.uris =",
            spark.conf.get("hive.metastore.uris", "未配置")
        )

        print("\n========== 2. 准备 Parquet 数据 ==========")

        source_df = spark.table("dim.customer").select(
            "customer_id",
            "customer_name",
            "province",
            "city",
            "age"
        )

        source_count = source_df.count()
        print(f"源表记录数：{source_count}")

        # 为本次实验创建独立的数据目录
        # overwrite 只覆盖本实验的数据路径
        source_df.write.mode("overwrite").parquet(DATA_PATH)

        print(f"数据写入路径：{DATA_PATH}")
        print(
            "写入后记录数：",
            spark.read.parquet(DATA_PATH).count()
        )

        print("\n========== 3. 创建 Hive 外部表 ==========")

        # 如果同名实验表已经存在，先删除其元数据
        # DROP TABLE 对外部表通常不会删除 DATA_PATH
        spark.sql(f"DROP TABLE IF EXISTS {TABLE_NAME}")

        spark.sql(f"""
            CREATE EXTERNAL TABLE {TABLE_NAME} (
                customer_id BIGINT,
                customer_name STRING,
                province STRING,
                city STRING,
                age INT
            )
            STORED AS PARQUET
            LOCATION '{DATA_PATH}'
        """)

        print("外部表创建完成")

        print("\n========== 4. 查看表元数据 ==========")
        spark.sql(
            f"DESCRIBE FORMATTED {TABLE_NAME}"
        ).show(100, truncate=False)

        print("\n========== 5. 查询外部表 ==========")
        external_df = spark.table(TABLE_NAME)

        print(f"外部表记录数：{external_df.count()}")

        external_df.show(10, truncate=False)

        print("\n========== 6. 验证查询结果 ==========")
        external_df.groupBy("province").count().orderBy(
            F.desc("count")
        ).show(10, truncate=False)

        print("\n========== 7. 删除外部表 ==========")
        spark.sql(f"DROP TABLE {TABLE_NAME}")

        exists_after_drop = spark.catalog.tableExists(TABLE_NAME)
        print(f"删除后表是否存在：{exists_after_drop}")

        # 直接读取原来的 HDFS 数据目录
        preserved_df = spark.read.parquet(DATA_PATH)
        preserved_count = preserved_df.count()

        print(f"删除表后，HDFS 数据记录数：{preserved_count}")
        print(f"原始记录数：{source_count}")

        assert not exists_after_drop, "外部表删除后仍然存在"
        assert preserved_count == source_count, "HDFS 数据数量不一致"

        print("\n========== 8. 使用原数据重新注册外部表 ==========")

        spark.sql(f"""
            CREATE EXTERNAL TABLE {TABLE_NAME} (
                customer_id BIGINT,
                customer_name STRING,
                province STRING,
                city STRING,
                age INT
            )
            STORED AS PARQUET
            LOCATION '{DATA_PATH}'
        """)

        restored_count = spark.table(TABLE_NAME).count()
        print(f"重新创建表后的记录数：{restored_count}")

        assert restored_count == source_count

        print("\n实验完成：外部表删除后，数据仍然保留。")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
