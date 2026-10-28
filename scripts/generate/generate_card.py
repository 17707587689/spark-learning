from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def main():
    spark = (
        SparkSession.builder
        .appName("Generate Dim Card")
        .enableHiveSupport()
        .getOrCreate()
    )

    print("=" * 60)
    print("开始生成 dim.card")
    print("=" * 60)

    # 1. 读取真实客户
    customer_df = spark.table("dim.customer").select(
        "customer_id"
    )

    customer_count = customer_df.count()

    print(f"当前客户数量：{customer_count}")

    # 2. 约 70% 的客户成为持卡客户
    card_customer_df = (
        customer_df
        .withColumn("_rand", F.rand(seed=42))
        .filter(F.col("_rand") < 0.70)
        .drop("_rand")
    )

    # 3. 每个持卡客户生成 1~3 张卡
    #
    # rand < 0.75  -> 1 张
    # rand < 0.95  -> 2 张
    # 其余         -> 3 张
    card_customer_df = (
        card_customer_df
        .withColumn("_rand", F.rand(seed=43))
        .withColumn(
            "card_count",
            F.when(F.col("_rand") < 0.75, 1)
             .when(F.col("_rand") < 0.95, 2)
             .otherwise(3)
        )
        .drop("_rand")
    )

    # 4. 展开成一行一张卡
    card_df = (
        card_customer_df
        .withColumn(
            "card_no",
            F.explode(
                F.sequence(
                    F.lit(1),
                    F.col("card_count")
                )
            )
        )
        .drop("card_count")
    )

    # 5. 生成唯一 card_id
    #
    # row_number 会产生连续的卡号：
    # 1, 2, 3, ...
    window = Window.orderBy(
        F.col("customer_id"),
        F.col("card_no")
    )

    card_df = card_df.withColumn(
        "card_id",
        F.row_number().over(window).cast("long")
    )

    # 6. 生成卡片属性
    card_df = (
        card_df
        .withColumn(
            "card_type",
            F.when(
                F.rand(seed=44) < 0.80,
                F.lit("CREDIT")
            ).otherwise(
                F.lit("DEBIT")
            )
        )
        .withColumn(
            "credit_limit",
            F.when(
                F.col("card_type") == "CREDIT",
                (
                    F.round(
                        F.rand(seed=45) * 90000 + 10000,
                        2
                    )
                ).cast("decimal(18,2)")
            ).otherwise(
                F.lit(0).cast("decimal(18,2)")
            )
        )
        .withColumn(
            "card_status",
            F.when(
                F.rand(seed=46) < 0.90,
                F.lit("ACTIVE")
            )
            .when(
                F.rand(seed=47) < 0.95,
                F.lit("FROZEN")
            )
            .otherwise(
                F.lit("CANCELLED")
            )
        )
        .withColumn(
            "open_date",
            F.date_sub(
                F.current_date(),
                F.floor(F.rand(seed=48) * 1095).cast("int")
            )
        )
    )

    # 7. 调整字段顺序
    card_df = card_df.select(
        "card_id",
        "customer_id",
        "card_type",
        "credit_limit",
        "card_status",
        "open_date"
    )

    # 8. 查看生成结果
    print("\n生成结果预览：")
    card_df.show(20, truncate=False)

    print(f"\n生成卡片数量：{card_df.count()}")

    # 9. 写入 Hive
    (
        card_df.write
        .mode("overwrite")
        .insertInto("dim.card")
    )

    # 10. 验证
    final_count = spark.table("dim.card").count()

    print("\n" + "=" * 60)
    print("dim.card 写入完成")
    print(f"最终卡片数量：{final_count}")
    print("=" * 60)

    spark.stop()


if __name__ == "__main__":
    main()