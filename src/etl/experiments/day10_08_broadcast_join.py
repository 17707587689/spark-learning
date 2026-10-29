from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast


def main():
    spark = (
        SparkSession.builder
        .appName("day10_08_broadcast_join")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    # 1. 模拟客户维度表
    customer_data = [
        (1, "张三", "VIP"),
        (2, "李四", "普通"),
        (3, "王五", "VIP"),
    ]

    customer_df = spark.createDataFrame(
        customer_data,
        ["customer_id", "customer_name", "customer_level"],
    )

    # 2. 模拟订单表
    order_data = [
        (101, 1, 100.0),
        (102, 2, 200.0),
        (103, 1, 150.0),
        (104, 3, 300.0),
    ]

    order_df = spark.createDataFrame(
        order_data,
        ["order_id", "customer_id", "amount"],
    )

    # 3. 指定客户表作为广播表
    result_df = order_df.join(
        broadcast(customer_df),
        on="customer_id",
        how="inner",
    )

    # 4. 查看执行计划
    print("========== 执行计划 ==========")
    result_df.explain("formatted")

    # 5. 执行 Action，触发计算
    print("========== Join 结果 ==========")
    result_df.show()

    spark.stop()


if __name__ == "__main__":
    main()