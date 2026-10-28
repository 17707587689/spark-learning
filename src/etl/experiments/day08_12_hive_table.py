from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("day08_12_hive_table")
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
            "hive.metastore.uris =",
            spark.sparkContext._jvm.org.apache.hadoop.hive.conf.HiveConf()
            .get("hive.metastore.uris")
        )
        
        print("\n========== 1. 查看表是否存在 ==========")
        print(spark.catalog.tableExists("dim.customer"))

        print("\n========== 2. 查看表结构 ==========")
        spark.sql("DESCRIBE TABLE dim.customer").show(
            truncate=False
        )

        print("\n========== 3. 查看表详细信息 ==========")
        spark.sql(
            "DESCRIBE FORMATTED dim.customer"
        ).show(truncate=False)

        print("\n========== 4. 查看表类型 ==========")
        detail = spark.sql(
            "DESCRIBE EXTENDED dim.customer"
        )
        detail.filter(
            "col_name IN ('Type', 'Provider', 'Location', 'Database')"
        ).show(truncate=False)

        print("\n========== 5. 查看数据 ==========")
        customer_df = spark.table("dim.customer")

        print(f"客户数量：{customer_df.count()}")
        customer_df.show(5, truncate=False)

        print("\n========== 6. 查看 Catalog 中的表 ==========")
        spark.sql("SHOW TABLES IN dim").show(
            truncate=False
        )

    finally:
        spark.stop()


if __name__ == "__main__":
    main()