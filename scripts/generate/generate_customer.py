from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    concat,
    lit,
    when,
    floor,
    rand,
    current_date,
    date_sub
)


spark = (
    SparkSession.builder
    .appName("GenerateDimCustomer")
    .enableHiveSupport()
    .getOrCreate()
)


# 第一次测试只生成 10 万条
customer_count = 100_000


customer_df = (
    spark.range(1, customer_count + 1)

    # id → customer_id
    .withColumnRenamed(
        "id",
        "customer_id"
    )

    # 客户名称
    .withColumn(
        "customer_name",
        concat(
            lit("customer_"),
            col("customer_id")
        )
    )

    # 性别
    .withColumn(
        "gender",
        when(
            col("customer_id") % 2 == 0,
            "M"
        ).otherwise("F")
    )

    # 年龄：18～60
    .withColumn(
        "age",
        (
            floor(rand(seed=42) * 43) + 18
        ).cast("int")
    )

    # 客户等级
    .withColumn(
        "customer_level",
        when(
            col("customer_id") % 10 < 2,
            "VIP"
        )
        .when(
            col("customer_id") % 10 < 5,
            "GOLD"
        )
        .otherwise("NORMAL")
    )

    # 省份
    .withColumn(
        "province",
        when(col("customer_id") % 10 == 0, "广东")
        .when(col("customer_id") % 10 == 1, "北京")
        .when(col("customer_id") % 10 == 2, "上海")
        .when(col("customer_id") % 10 == 3, "江苏")
        .when(col("customer_id") % 10 == 4, "浙江")
        .when(col("customer_id") % 10 == 5, "四川")
        .when(col("customer_id") % 10 == 6, "湖北")
        .when(col("customer_id") % 10 == 7, "湖南")
        .when(col("customer_id") % 10 == 8, "福建")
        .otherwise("山东")
    )

    # 城市
    .withColumn(
        "city",
        concat(
            col("province"),
            lit("市")
        )
    )

    # 注册日期：最近 10 年
    .withColumn(
        "register_date",
        date_sub(
            current_date(),
            (rand(seed=100) * 3650).cast("int")
        )
    )
)


output_path = (
    "hdfs://hadoop1:9000"
    "/user/hive/warehouse/dim/customer"
)


# 写入 Parquet
(
    customer_df
    .write
    .mode("overwrite")
    .format("parquet")
    .save(output_path)
)


# 统计数据量
count = customer_df.count()


print("====================================")
print("Customer data generated successfully")
print("Count:", count)
print("Path:", output_path)
print("====================================")


spark.stop()

