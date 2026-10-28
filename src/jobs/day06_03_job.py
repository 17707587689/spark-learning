from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("Day06_03_job") \
    .enableHiveSupport() \
    .getOrCreate()

df = (
    spark.table("dim.customer")
    .select(
        "customer_id",
        "customer_name",
        "province",
        "age"
    )
    .filter(F.col("province").isin("广东", "北京", "上海"))
)

window_spec = (
    Window
    .partitionBy("province")
    .orderBy(F.col("age").desc())
)

result = (
    df
    .withColumn(
        "row_num",
        F.row_number().over(window_spec)
    )
)

result.orderBy("province", "row_num").show(30)