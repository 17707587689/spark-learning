
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.window import Window


def main():
    spark = (
        SparkSession.builder
        .appName("day06_11_window_sql")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        # 1. 读取项目中的客户表
        customer_df = spark.table("dim.customer").select(
            "customer_id",
            "customer_name",
            "province",
            "age",
        )

        print("=" * 60)
        print("一、客户表基本信息")
        print("=" * 60)
        print(f"客户总数：{customer_df.count()}")
        customer_df.show(5, truncate=False)

        # 注册临时视图，供 Spark SQL 查询
        customer_df.createOrReplaceTempView("customer_view")

        # --------------------------------------------------
        # 2. 排名函数：row_number、rank、dense_rank
        # --------------------------------------------------
        print("\n" + "=" * 60)
        print("二、排名函数：DataFrame API")
        print("=" * 60)

        # row_number 使用 customer_id 作为第二排序条件，
        # 确保相同年龄的客户也有稳定的先后顺序。
        row_window = Window.partitionBy("province").orderBy(
            F.col("age").desc(),
            F.col("customer_id").asc(),
        )

        # rank 和 dense_rank 只按年龄排名，保留并列名次。
        rank_window = Window.partitionBy("province").orderBy(
            F.col("age").desc()
        )

        df_result = (
            customer_df
            .withColumn(
                "row_num",
                F.row_number().over(row_window),
            )
            .withColumn(
                "rank_num",
                F.rank().over(rank_window),
            )
            .withColumn(
                "dense_rank_num",
                F.dense_rank().over(rank_window),
            )
        )

        df_result.orderBy(
            "province",
            F.col("age").desc(),
            "customer_id",
        ).show(10, truncate=False)

        # --------------------------------------------------
        # 3. 排名函数：Spark SQL
        # --------------------------------------------------
        print("\n" + "=" * 60)
        print("三、排名函数：Spark SQL")
        print("=" * 60)

        sql_result = spark.sql("""
            SELECT
                customer_id,
                customer_name,
                province,
                age,
                ROW_NUMBER() OVER (
                    PARTITION BY province
                    ORDER BY age DESC, customer_id ASC
                ) AS row_num,
                RANK() OVER (
                    PARTITION BY province
                    ORDER BY age DESC
                ) AS rank_num,
                DENSE_RANK() OVER (
                    PARTITION BY province
                    ORDER BY age DESC
                ) AS dense_rank_num
            FROM customer_view
        """)

        sql_result.orderBy(
            "province",
            F.col("age").desc(),
            "customer_id",
        ).show(10, truncate=False)

        # --------------------------------------------------
        # 4. 比较 DataFrame API 和 Spark SQL 的结果
        # --------------------------------------------------
        print("\n" + "=" * 60)
        print("四、排名结果一致性检查")
        print("=" * 60)

        # exceptAll 会保留重复行语义，适合验证完整结果。
        df_only = df_result.exceptAll(sql_result)
        sql_only = sql_result.exceptAll(df_result)

        df_only_count = df_only.count()
        sql_only_count = sql_only.count()

        print(f"仅存在于 DataFrame 结果中的记录数：{df_only_count}")
        print(f"仅存在于 SQL 结果中的记录数：{sql_only_count}")

        if df_only_count == 0 and sql_only_count == 0:
            print("验证通过：两种写法的排名结果完全一致。")
        else:
            print("验证失败：请检查两种写法的窗口定义。")

        # --------------------------------------------------
        # 5. lag：获取同省份上一条客户记录的年龄
        # --------------------------------------------------
        print("\n" + "=" * 60)
        print("五、lag：DataFrame API 与 Spark SQL")
        print("=" * 60)

        lag_window = Window.partitionBy("province").orderBy(
            "customer_id"
        )

        lag_df = customer_df.withColumn(
            "previous_age",
            F.lag("age", 1).over(lag_window),
        )

        lag_sql = spark.sql("""
            SELECT
                customer_id,
                customer_name,
                province,
                age,
                LAG(age, 1) OVER (
                    PARTITION BY province
                    ORDER BY customer_id
                ) AS previous_age
            FROM customer_view
        """)

        lag_df.orderBy("province", "customer_id").show(10, truncate=False)
        lag_sql.orderBy("province", "customer_id").show(10, truncate=False)

        lag_df_only = lag_df.exceptAll(lag_sql)
        lag_sql_only = lag_sql.exceptAll(lag_df)

        print(
            "lag 结果一致：",
            lag_df_only.count() == 0 and lag_sql_only.count() == 0,
        )

        # --------------------------------------------------
        # 6. 窗口聚合：每个省份的平均年龄
        # --------------------------------------------------
        print("\n" + "=" * 60)
        print("六、窗口聚合：DataFrame API 与 Spark SQL")
        print("=" * 60)

        province_window = Window.partitionBy("province")

        agg_df = customer_df.withColumn(
            "province_avg_age",
            F.avg("age").over(province_window),
        )

        agg_sql = spark.sql("""
            SELECT
                customer_id,
                customer_name,
                province,
                age,
                AVG(age) OVER (
                    PARTITION BY province
                ) AS province_avg_age
            FROM customer_view
        """)

        agg_df.orderBy("province", "customer_id").show(10, truncate=False)
        agg_sql.orderBy("province", "customer_id").show(10, truncate=False)

        agg_df_only = agg_df.exceptAll(agg_sql)
        agg_sql_only = agg_sql.exceptAll(agg_df)

        print(
            "窗口聚合结果一致：",
            agg_df_only.count() == 0 and agg_sql_only.count() == 0,
        )

        # --------------------------------------------------
        # 7. 执行计划对比
        # --------------------------------------------------
        print("\n" + "=" * 60)
        print("七、DataFrame API 执行计划")
        print("=" * 60)
        df_result.explain("extended")

        print("\n" + "=" * 60)
        print("八、Spark SQL 执行计划")
        print("=" * 60)
        sql_result.explain("extended")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
