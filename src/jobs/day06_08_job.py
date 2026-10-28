
from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import col, lead


def main():
    spark = (
        SparkSession.builder
        .appName("Day06_08_Lead")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        # 1. 读取现有 Hive 表
        customer_df = spark.table("dim.customer")

        print("=" * 60)
        print("06-08 lead 窗口函数实验")
        print("=" * 60)

        print(f"客户总数：{customer_df.count()}")

        # 2. 定义窗口：按照省份分区，
        #    每个省份内部按 customer_id 升序排列
        window_spec = (
            Window
            .partitionBy("province")
            .orderBy("customer_id")
        )

        # 3. 只取上海客户，方便观察输出
        shanghai_df = customer_df.filter(
            col("province") == "上海"
        )

        # 4. lead 默认偏移量为 1
        result_df = (
            shanghai_df
            .withColumn(
                "next_customer_id",
                lead("customer_id", 1).over(window_spec)
            )
            .withColumn(
                "next_customer_name",
                lead("customer_name", 1).over(window_spec)
            )
            .withColumn(
                "next_age",
                lead("age", 1).over(window_spec)
            )
            .withColumn(
                "next2_age",
                lead("age", 2).over(window_spec)
            )
            .withColumn(
                "next_age_default",
                lead("age", 1, -1).over(window_spec)
            )
        )

        print("\n========== 实验一：获取下一位客户 ==========")
        result_df.select(
            "customer_id",
            "customer_name",
            "age",
            "next_customer_id",
            "next_customer_name",
            "next_age"
        ).orderBy("customer_id").show(10, truncate=False)

        print("\n========== 实验二：获取下两位客户的年龄 ==========")
        result_df.select(
            "customer_id",
            "age",
            "next_age",
            "next2_age"
        ).orderBy("customer_id").show(10)

        print("\n========== 实验三：设置默认值 -1 ==========")

        # 查看上海客户中 customer_id 最大的记录，
        # 验证窗口分区最后一行的默认值
        result_df.orderBy(
            col("customer_id").desc()
        ).select(
            "customer_id",
            "customer_name",
            "age",
            "next_age",
            "next_age_default"
        ).show(5, truncate=False)

        print("\n========== 执行计划 ==========")
        result_df.select(
            "customer_id",
            "age",
            "next_age"
        ).explain("formatted")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
