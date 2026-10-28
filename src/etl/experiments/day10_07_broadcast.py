
from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("day10_07_broadcast")
        .master("local[*]")
        .getOrCreate()
    )

    sc = spark.sparkContext
    sc.setLogLevel("WARN")

    broadcast_region = None

    try:
        # 1. 准备小型省份映射数据
        province_region = {
            "广东": "华南",
            "广西": "华南",
            "浙江": "华东",
            "江苏": "华东",
            "四川": "西南",
        }

        print("========== 1. 原始映射数据 ==========")
        print(province_region)

        # 2. 创建广播变量
        print("\n========== 2. 创建广播变量 ==========")
        broadcast_region = sc.broadcast(province_region)
        print("广播变量已创建")

        # 3. 准备测试数据，分为 3 个分区
        provinces = ["广东", "浙江", "四川", "广西", "江苏", "湖南"]
        province_rdd = sc.parallelize(provinces, 3)

        print("\n========== 3. 查看 RDD 分区 ==========")
        print(f"分区数量：{province_rdd.getNumPartitions()}")

        # 4. 各分区任务通过广播变量查询区域
        def lookup_region(province):
            region = broadcast_region.value.get(province, "未知区域")
            return province, region

        result = province_rdd.map(lookup_region).collect()

        print("\n========== 4. 查询结果 ==========")
        for province, region in result:
            print(f"{province} -> {region}")

        # 5. 验证广播数据是只读共享数据
        print("\n========== 5. 读取广播变量 ==========")
        print(broadcast_region.value["广东"])
        print("任务执行完成")

    finally:
        # 6. 释放广播变量资源
        if broadcast_region is not None:
            broadcast_region.destroy()

        spark.stop()


if __name__ == "__main__":
    main()
