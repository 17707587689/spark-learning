from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    sum,
    avg
)


spark = (
    SparkSession.builder
    .appName("day04_10_join_comprehensive")
    .enableHiveSupport()
    .getOrCreate()
)


customer_df = spark.table("dim.customer")
order_df = spark.table("ods.trade_order")
card_df = spark.table("dim.card")

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    sum,
    avg
)


spark = (
    SparkSession.builder
    .appName("day04_10_join_comprehensive")
    .enableHiveSupport()
    .getOrCreate()
)


customer_df = spark.table("dim.customer")
order_df = spark.table("ods.trade_order")
card_df = spark.table("dim.card")

print("customer:", customer_df.count())
print("order:", order_df.count())
print("card:", card_df.count())

customer_df.show(5, truncate=False)
order_df.show(5, truncate=False)
card_df.show(5, truncate=False)

customer_order_df = customer_df.join(
    order_df,
    on="customer_id",
    how="left"
)

customer_order_df.show(20, truncate=False)