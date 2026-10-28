from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("Day05-01-TempView")
        .enableHiveSupport()
        .getOrCreate()
    )

    print(
        "catalogImplementation:",
        spark.conf.get("spark.sql.catalogImplementation")
    )

    # 1. 读取 Hive 表
    customer_df = spark.table("dim.customer")

    # 2. 注册临时视图
    customer_df.createOrReplaceTempView("customer")

    # 3. 查看当前 Session 中的对象
    print("=== SHOW TABLES ===")
    spark.sql("SHOW TABLES").show()

    # 4. 查看 dim 数据库中的真实表
    print("=== SHOW TABLES IN dim ===")
    spark.sql("SHOW TABLES IN dim").show()

    # 5. 通过 TempView 查询
    print("=== QUERY TEMP VIEW ===")
    spark.sql("""
        SELECT *
        FROM customer
        LIMIT 10
    """).show()



    # 第一个 DataFrame
    df1 = spark.createDataFrame(
        [
            (1, "张三"),
            (2, "李四"),
        ],
        ["id", "name"]
    )

    df1.createOrReplaceTempView("test")

    print("=== 第一次注册 ===")

    spark.sql("""
        SELECT *
        FROM test
    """).show()

    # 第二个 DataFrame
    df2 = spark.createDataFrame(
        [
            (3, "王五"),
            (4, "赵六"),
        ],
        ["id", "name"]
    )

    df2.createOrReplaceTempView("test")

    print("=== 第二次注册 ===")

    spark.sql("""
        SELECT *
        FROM test
    """).show()

    spark.stop()


if __name__ == "__main__":
    main()