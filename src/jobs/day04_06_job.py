from pyspark.sql import SparkSession
from pyspark.sql.functions import col


spark = (
    SparkSession.builder
    .appName("day04_06_left_join")
    .enableHiveSupport()
    .getOrCreate()
)


# 读取订单表
order_df = spark.table("ods.trade_order")

# 读取客户表
customer_df = spark.table("dim.customer")


# Left Join
result_df = order_df.join(
    customer_df,
    on="customer_id",
    how="left"
)

result_df.select(
    "order_id",
    "customer_id",
    "amount",
    "customer_name",
    "province"
).show(20, truncate=False)

order_count = order_df.count()
result_count = result_df.count()

print(f"订单表数量：{order_count}")
print(f"Left Join 后数量：{result_count}")

unmatched_df = result_df.filter(
    col("customer_name").isNull()
)

unmatched_df.select(
    "order_id",
    "customer_id",
    "amount",
    "customer_name"
).show(20, truncate=False)