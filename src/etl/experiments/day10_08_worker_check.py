import os
import sys

from pyspark.sql import SparkSession


def main():
    print("========== Python 环境 ==========")
    print("Python executable:", sys.executable)
    print("Python version:", sys.version)
    print("PYSPARK_PYTHON:", os.environ.get("PYSPARK_PYTHON"))

    spark = (
        SparkSession.builder
        .appName("day10_08_worker_check")
        .master("local[2]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    print(
        "spark.pyspark.python =",
        spark.sparkContext.getConf().get(
            "spark.pyspark.python", "<未显式配置>"
        ),
    )

    print(
        "spark.pyspark.driver.python =",
        spark.sparkContext.getConf().get(
            "spark.pyspark.driver.python", "<未显式配置>"
        ),
    )

    sc = spark.sparkContext

    print("\n========== 测试 1：Python Worker ==========")
    values = sc.parallelize([1, 2, 3], 1).map(
        lambda x: x + 1
    ).collect()
    print("计算结果：", values)

    print("\n========== 测试 2：Python 创建 DataFrame ==========")
    df = spark.createDataFrame(
        [(1, "张三"), (2, "李四")],
        ["id", "name"],
    )
    df.show()

    spark.stop()


if __name__ == "__main__":
    main()