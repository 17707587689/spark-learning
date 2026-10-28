from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("Day04-08 Multi Join")
    .enableHiveSupport()
    .getOrCreate()
)

spark.sql("DESCRIBE dim.card").show(truncate=False)
spark.sql("DESCRIBE dim.customer").show(truncate=False)

# 1. 读取三张表
order_df = spark.table("ods.trade_order")
customer_df = spark.table("dim.customer")
card_df = spark.table("dim.card")


# 2. 给 DataFrame 起别名
o = order_df.alias("o")
c = customer_df.alias("c")
card = card_df.alias("card")

spark.conf.set(
    "spark.sql.autoBroadcastJoinThreshold",
    1
)

# 3. 三表 Join
result_df = (
    o
    .join(
        c,
        F.col("o.customer_id") == F.col("c.customer_id"),
        "left"
    )
    .join(
        card,
        F.col("o.customer_id") == F.col("card.customer_id"),
        "left"
    )
)

print("\n========== Execution Plan ==========")

result_df.explain()


print(
    "Broadcast threshold =",
    spark.conf.get("spark.sql.autoBroadcastJoinThreshold")
)

result_df.explain()

print(f"card count:{spark.table('dim.card').count()}")

# 4. 明确选择需要的字段
result_df = result_df.select(
    F.col("o.order_id"),
    F.col("o.customer_id"),
    F.col("o.amount"),
    F.col("o.order_date"),
    F.col("o.order_status"),
    F.col("c.customer_name"),
    F.col("c.customer_level"),
    F.col("c.province"),
    F.col("card.card_id"),
    F.col("card.card_type"),
    F.col("card.credit_limit"),
    F.col("card.card_status")
)


# 5. 查看结果
result_df.show(20, truncate=False)

spark.table("dim.card") \
    .groupBy("customer_id") \
    .count() \
    .orderBy(F.desc("count")) \
    .show(20)

print(spark.conf.get("spark.sql.autoBroadcastJoinThreshold"))

print(f"customer_df count is {customer_df.count()}")
print(f"card_df count is {card_df.count()}")
print(f"order_df count is {order_df.count()}")

spark.stop()
