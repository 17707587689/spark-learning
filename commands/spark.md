# Spark 常用命令

```bash
pyspark
spark-submit src/jobs/customer_etl.py
```

## PySpark

```python
df.show()
df.printSchema()
df.explain(True)
df.rdd.getNumPartitions()
spark.conf.get("spark.sql.shuffle.partitions")
spark.conf.get("spark.sql.adaptive.enabled")
```
