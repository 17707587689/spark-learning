"""
Day06-07：lag() 窗口函数实验

学习目标：
1. 使用 lag() 获取前一行的数据
2. 使用不同 offset 获取前几行的数据
3. 使用 default 设置默认值
4. 结合 partitionBy()、orderBy() 理解窗口边界
5. 计算当前客户与上一位客户的年龄差

数据来源：dim.customer
"""

from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F


def main():
    # ==================================================
    # 1. 创建 SparkSession
    # ==================================================
    spark = (
        SparkSession.builder
        .appName("Day06_07_Lag")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        # ==================================================
        # 2. 读取现有客户维度表
        # ==================================================
        customer_df = spark.table("dim.customer")

        print("=" * 60)
        print("========== 客户表基本信息 ==========")
        print(f"客户总数：{customer_df.count()}")

        customer_df.printSchema()

        # ==================================================
        # 3. 定义窗口
        #
        # 每个省份单独计算；
        # 按注册日期升序排列；
        # 注册日期相同时，按 customer_id 升序排列。
        # ==================================================
        window_spec = (
            Window
            .partitionBy("province")
            .orderBy(
                F.col("register_date").asc(),
                F.col("customer_id").asc()
            )
        )

        # ==================================================
        # 4. 使用 lag() 获取上一行的客户信息
        # ==================================================
        result_df = (
            customer_df
            .withColumn(
                "prev_customer_id",
                F.lag("customer_id", 1).over(window_spec)
            )
            .withColumn(
                "prev_register_date",
                F.lag("register_date", 1).over(window_spec)
            )
            .withColumn(
                "prev_age",
                F.lag("age", 1).over(window_spec)
            )
        )

        print("\n========== 每个省份的前一位客户 ==========")

        (
            result_df
            .filter(F.col("province") == "上海")
            .select(
                "customer_id",
                "customer_name",
                "province",
                "register_date",
                "age",
                "prev_customer_id",
                "prev_register_date",
                "prev_age"
            )
            .orderBy(
                F.col("register_date").asc(),
                F.col("customer_id").asc()
            )
            .show(20, truncate=False)
        )

        # ==================================================
        # 5. 对比 lag 的不同 offset
        # ==================================================
        offset_df = (
            customer_df
            .filter(F.col("province") == "上海")
            .withColumn(
                "prev_age_1",
                F.lag("age", 1).over(window_spec)
            )
            .withColumn(
                "prev_age_2",
                F.lag("age", 2).over(window_spec)
            )
            .withColumn(
                "prev_age_default_0",
                F.lag("age", 1, 0).over(window_spec)
            )
        )

        print("\n========== lag 不同 offset 与 default ==========")

        (
            offset_df
            .select(
                "customer_id",
                "register_date",
                "age",
                "prev_age_1",
                "prev_age_2",
                "prev_age_default_0"
            )
            .orderBy(
                F.col("register_date").asc(),
                F.col("customer_id").asc()
            )
            .show(10, truncate=False)
        )

        # ==================================================
        # 6. 计算当前客户与上一位客户的年龄差
        # ==================================================
        diff_df = (
            customer_df
            .filter(F.col("province") == "上海")
            .withColumn(
                "prev_age",
                F.lag("age", 1).over(window_spec)
            )
            .withColumn(
                "age_diff",
                F.col("age") - F.col("prev_age")
            )
        )

        print("\n========== 当前客户与上一位客户的年龄差 ==========")

        (
            diff_df
            .select(
                "customer_id",
                "register_date",
                "age",
                "prev_age",
                "age_diff"
            )
            .orderBy(
                F.col("register_date").asc(),
                F.col("customer_id").asc()
            )
            .show(10, truncate=False)
        )

        # ==================================================
        # 7. 查看执行计划
        # ==================================================
        print("\n========== lag 执行计划 ==========")

        (
            customer_df
            .filter(F.col("province") == "上海")
            .withColumn(
                "prev_age",
                F.lag("age", 1).over(window_spec)
            )
            .explain("formatted")
        )

        print("\nDay06-07 lag 实验完成！")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()