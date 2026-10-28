from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when


def transform_customer(customer_df: DataFrame) -> DataFrame:
    """
    03-10 Day03 综合实验
    客户数据加工。
    """

    # 1. 过滤广东客户
    df = customer_df.filter(
        col("province") == "广东"
    )

    # 2. 增加年龄分组
    df = df.withColumn(
        "age_group",
        when(col("age") < 35, "青年")
        .when(col("age") < 50, "中年")
        .otherwise("老年")
    )

    # 3. 增加客户类型
    df = df.withColumn(
        "customer_type",
        when(
            col("customer_level").isin("VIP", "SVIP"),
            "高价值客户"
        )
        .otherwise("普通客户")
    )

    # 4. 选择业务需要的字段
    df = df.select(
        "customer_id",
        "customer_name",
        "gender",
        "age",
        "age_group",
        "customer_level",
        "customer_type",
        "province",
        "city",
        "register_date"
    )

    # 5. 去重
    df = df.distinct()

    # 6. 排序
    df = df.orderBy(
        col("age").desc(),
        col("customer_id")
    )

    return df
