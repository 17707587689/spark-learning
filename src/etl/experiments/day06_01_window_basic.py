from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Window


def main():
    spark = (
        SparkSession.builder
        .appName("day06_01_window_basic")
        .enableHiveSupport()
        .getOrCreate()
    )

    customer_df = spark.table("dim.customer")

    # 定义窗口：按照 province 划分窗口
    window_spec = Window.partitionBy("province")

    result_df = (
        customer_df
        .select(
            "customer_id",
            "customer_name",
            "province",
            "age"
        )
        .withColumn(
            "province_max_age",
            F.max("age").over(window_spec)
        )
    )

    result_df.show(20, truncate=False)

    spark.stop()


if __name__ == "__main__":
    main()