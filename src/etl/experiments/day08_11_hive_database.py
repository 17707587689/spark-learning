
from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("day08_11_hive_database")
        .master("local[*]")
        .config("spark.sql.catalogImplementation", "hive")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    database_name = "day08_11_demo"

    try:
        # 1. 查看现有数据库
        print("\n========== 1. 查看数据库列表 ==========")
        spark.sql("SHOW DATABASES").show(truncate=False)

        # 2. 创建实验数据库
        print("\n========== 2. 创建实验数据库 ==========")
        spark.sql(
            f"""
            CREATE DATABASE IF NOT EXISTS {database_name}
            COMMENT 'Day08-11 Hive Database learning'
            LOCATION
            'hdfs://hadoop1:9000/user/Administrator/day08_11_demo.db'
            """
        )

        # 3. 查看数据库详细信息
        print("\n========== 3. 查看数据库信息 ==========")
        spark.sql(
            f"DESCRIBE DATABASE EXTENDED {database_name}"
        ).show(truncate=False)

        # 4. 切换数据库
        print("\n========== 4. 切换当前数据库 ==========")
        spark.sql(f"USE {database_name}")

        spark.sql(
            "SELECT current_database() AS current_db"
        ).show(truncate=False)

        # 5. 在实验数据库中创建表
        print("\n========== 5. 创建实验表 ==========")
        spark.sql("""
            CREATE TABLE IF NOT EXISTS demo_customer (
                customer_id BIGINT,
                customer_name STRING,
                age INT
            )
            USING PARQUET
        """)

        # 6. 查看当前数据库中的表
        print("\n========== 6. 查看当前数据库的表 ==========")
        spark.sql("SHOW TABLES").show(truncate=False)

        # 7. 查看表结构
        print("\n========== 7. 查看表结构 ==========")
        spark.sql(
            "DESCRIBE demo_customer"
        ).show(truncate=False)

        # 8. 查看表的实际存储位置
        print("\n========== 8. 查看表存储位置 ==========")
        spark.sql("""
            DESCRIBE EXTENDED demo_customer
        """).show(truncate=False)

        # 9. 再次确认原有数据库仍然存在
        print("\n========== 9. 查看原有维度表 ==========")
        spark.sql("SHOW TABLES IN dim").show(truncate=False)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
