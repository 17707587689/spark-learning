from src.common.spark_session import get_spark


def main() -> None:
    spark = get_spark("customer-etl")
    try:
        print("Spark ETL project initialized successfully.")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
