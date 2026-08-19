from pyspark.sql import SparkSession


def get_spark(app_name: str = "spark-learning") -> SparkSession:
    return (
        SparkSession.builder
        .appName(app_name)
        .enableHiveSupport()
        .getOrCreate()
    )
