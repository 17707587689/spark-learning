
from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


def run_window_aggregation(customer_df: DataFrame) -> DataFrame:
    """
    06-09 窗口聚合实验。

    在客户明细上增加：
    1. 省份客户数
    2. 省份平均年龄
    3. 省份最大年龄
    4. 省份最小年龄
    5. 省份年龄总和
    6. 省份内按注册日期排序的累计客户数
    """

    # 窗口一：按省份划分，不排序
    province_window = Window.partitionBy("province")

    # 窗口二：按省份划分，并在省份内排序
    # customer_id 用于提供稳定的次级排序条件
    running_window = (
        Window
        .partitionBy("province")
        .orderBy("register_date", "customer_id")
        .rowsBetween(
            Window.unboundedPreceding,
            Window.currentRow
        )
    )

    result_df = (
        customer_df
        .withColumn(
            "province_customer_count",
            F.count("*").over(province_window)
        )
        .withColumn(
            "province_avg_age",
            F.round(F.avg("age").over(province_window), 2)
        )
        .withColumn(
            "province_max_age",
            F.max("age").over(province_window)
        )
        .withColumn(
            "province_min_age",
            F.min("age").over(province_window)
        )
        .withColumn(
            "province_total_age",
            F.sum("age").over(province_window)
        )
        .withColumn(
            "running_customer_count",
            F.count("*").over(running_window)
        )
    )

    return result_df
