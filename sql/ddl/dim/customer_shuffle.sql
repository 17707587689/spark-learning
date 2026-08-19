-- 当前 Spark Shuffle / AQE 实验表
-- 实际建表语句根据当前 Hive 环境调整。

CREATE TABLE IF NOT EXISTS dim.customer_shuffle (
    customer_id BIGINT,
    customer_name STRING,
    gender STRING,
    age INT,
    customer_level STRING,
    province STRING,
    city STRING,
    register_date DATE
)
STORED AS PARQUET;
