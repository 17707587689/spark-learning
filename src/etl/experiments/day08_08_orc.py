
from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("day08_08_orc")
        .master("local[*]")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    orc_path = "hdfs://hadoop1:9000/user/Administrator/day08_08_orc"

    try:
        # 1. 读取源表
        print("\n========== 1. 读取 dim.customer ==========")

        source_df = spark.table("dim.customer")

        source_count = source_df.count()
        print(f"源数据总数：{source_count}")

        source_df.printSchema()

        # 2. 写入 ORC
        print("\n========== 2. 写入 ORC ==========")

        (
            source_df.write
            .format("orc")
            .mode("overwrite")
            .save(orc_path)
        )

        print(f"ORC 写入路径：{orc_path}")

        # 3. 读取 ORC
        print("\n========== 3. 读取 ORC ==========")

        orc_df = spark.read.format("orc").load(orc_path)

        orc_count = orc_df.count()
        print(f"ORC 数据总数：{orc_count}")

        orc_df.printSchema()

        # 4. 验证数据
        print("\n========== 4. 数据验证 ==========")

        print(f"源数据总数：{source_count}")
        print(f"ORC 数据总数：{orc_count}")
        print(f"数量是否一致：{source_count == orc_count}")

        print("\nORC 前 5 条记录：")
        orc_df.show(5, truncate=False)

        # 5. 查看执行计划
        print("\n========== 5. ORC 读取执行计划 ==========")

        (
            orc_df
            .filter(orc_df["province"] == "广东")
            .select("customer_id", "province", "age")
            .explain("formatted")
        )

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
