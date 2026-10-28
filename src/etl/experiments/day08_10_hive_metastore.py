
from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("Day08-10-Hive-Metastore")
        .config("spark.sql.catalogImplementation", "hive")
        .enableHiveSupport()
        .getOrCreate()
    )

    try:
        print("\n========== 1. Catalog 类型 ==========")
        print(
            "spark.sql.catalogImplementation =",
            spark.conf.get("spark.sql.catalogImplementation")
        )

        print("\n========== 2. Metastore 服务地址 ==========")
        print(
            "hive.metastore.uris =",
            spark.sparkContext._jsc.hadoopConfiguration()
            .get("hive.metastore.uris")
        )

        print("\n========== 3. 查看数据库 ==========")
        spark.sql("SHOW DATABASES").show(truncate=False)

        print("\n========== 4. 查看 dim.customer ==========")
        spark.sql("DESCRIBE EXTENDED dim.customer").show(
            100, truncate=False
        )

        print("\n========== 5. 查看表数据 ==========")
        df = spark.table("dim.customer")

        print("记录数：", df.count())
        df.show(5, truncate=False)

        print("\n========== 6. 查看表存储位置 ==========")
        detail = spark.sql(
            "DESCRIBE EXTENDED dim.customer"
        )

        detail.filter(
            "col_name IN ('Location', 'Provider', "
            "'Type', 'Database', 'Table')"
        ).show(truncate=False)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
