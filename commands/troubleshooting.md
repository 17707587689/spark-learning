# Spark / Hadoop 问题排查

## Spark

1. 检查 `JAVA_HOME`。
2. 检查 `which pyspark`。
3. 检查 `pyspark --version`。
4. 检查 HDFS 是否可访问。
5. 使用 `explain(True)` 检查执行计划。

## HDFS

```bash
hdfs dfs -ls /
hdfs dfs -ls /user/hive/warehouse
```
