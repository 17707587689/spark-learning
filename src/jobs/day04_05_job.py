from pyspark.sql import Row,SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("day04_05_innerjoin")
    .enableHiveSupport()
    .getOrCreate()
)

customer_df = spark.createDataFrame([
    Row(customer_id=1, customer_name="张三", province="广东"),
    Row(customer_id=2, customer_name="李四", province="江苏"),
    Row(customer_id=3, customer_name="王五", province="浙江"),
    Row(customer_id=4, customer_name="赵六", province="广东"),
])

order_df = spark.createDataFrame([
    Row(order_id=1001, customer_id=1, amount=500),
    Row(order_id=1002, customer_id=1, amount=300),
    Row(order_id=1003, customer_id=2, amount=800),
    Row(order_id=1004, customer_id=5, amount=200),
])

result_df = customer_df.join(order_df,on="customer_id",how="inner")
result_df.show()
