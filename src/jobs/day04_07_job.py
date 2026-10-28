from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("Day04-07-Join") \
    .enableHiveSupport() \
    .getOrCreate()

customer_df = spark.table("dim.customer")
trade_order_df = spark.table("ods.trade_order")

right_join_df = customer_df.join(
    trade_order_df,
    on="customer_id",
    how="right"
)

right_join_df.show(20, truncate=False)

right_join_df.filter(
    col("customer_name").isNull()
).show(20, truncate=False)

unmatched_order_count =right_join_df.filter(
    col("customer_name").isNull()
).count()

print("没有匹配到客户的订单数量：", unmatched_order_count)

full_join_df = customer_df.join(
    trade_order_df,
    on="customer_id",
    how="full"
)

print(f"Full Join 结果数量：{full_join_df.count()}")

customer_only_df = full_join_df.filter(
    col("order_id").isNull()
)

customer_only_df.show(20, truncate=False)

print(
    "有客户但没有订单：",
    customer_only_df.count()
)

order_only_df = full_join_df.filter(
    col("customer_name").isNull()
)

order_only_df.show(20, truncate=False)

print(
    "有订单但没有客户：",
    order_only_df.count()
)

matched_df = full_join_df.filter(
    col("customer_name").isNotNull() &
    col("order_id").isNotNull()
)

print(
    "客户和订单都存在：",
    matched_df.count()
)

