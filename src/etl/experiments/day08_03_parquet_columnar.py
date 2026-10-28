
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col


def main():
    spark = (
        SparkSession.builder
        .appName("Day08_03_Parquet_Columnar")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        # 1. 读取已有客户表
        print("\n========== 1. 读取 dim.customer ==========")

        customer_df = spark.table("dim.customer")

        print(f"客户总数：{customer_df.count()}")

        # 2. 查看原始 DataFrame 的全部字段
        print("\n========== 2. 原始 DataFrame Schema ==========")
        customer_df.printSchema()

        # 3. 只选择 age 列
        print("\n========== 3. 只读取 age 列 ==========")

        age_df = customer_df.select("age")

        age_df.explain("formatted")

        print("\n年龄平均值：")
        age_df.agg(avg("age").alias("avg_age")).show()

        # 4. 只选择 age、province 两列
        print("\n========== 4. 只读取 age、province ==========")

        selected_df = customer_df.select(
            "age",
            "province"
        )

        selected_df.explain("formatted")

        print("\n广东省客户年龄统计：")
        (
            selected_df
            .filter(col("province") == "广东")
            .groupBy("province")
            .agg(avg("age").alias("avg_age"))
            .show()
        )

        # 5. 对比：读取全部列与部分列
        print("\n========== 5. 对比读取列 ==========")

        print("读取全部列：")
        customer_df.explain("formatted")

        print("只读取 age 列：")
        customer_df.select("age").explain("formatted")

        print("只读取 age、province 列：")
        customer_df.select(
            "age", "province"
        ).explain("formatted")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
