
## PySpark

1. 读取 HDFS 数据

```python
customer_df = spark.read.parquet(
    "hdfs:///user/hive/warehouse/dim/customer_shuffle"
)

customer_df.printSchema()

print("count:", customer_df.count())
print("partitions:", customer_df.rdd.getNumPartitions())
```

2. 确认 AQE 当前状态

```python
print(
    "AQE:",
    spark.conf.get("spark.sql.adaptive.enabled")
)

print(
    "shuffle partitions:",
    spark.conf.get("spark.sql.shuffle.partitions")
)
```

3. 先运行 AQE = true

```python
result_aqe = customer_df.groupBy("province").count()

result_aqe.show()

result_aqe.explain(True)
```
```text
重点观察：AdaptiveSparkPlan
以及： Exchange
hashpartitioning(province, 200)
先记住两个数字：
输入 Partition = 4
Shuffle Partition = 200
```

4. 关闭 AQE

```python
spark.conf.set(
    "spark.sql.adaptive.enabled",
    "false"
)

print(
    "AQE after:",
    spark.conf.get("spark.sql.adaptive.enabled")
)

print(
    "shuffle partitions:",
    spark.conf.get("spark.sql.shuffle.partitions")
)
```

5. 重新执行完全相同的 GroupBy

```python
result_no_aqe = customer_df.groupBy("province").count()

result_no_aqe.show()
```

6. 查看执行计划

```python
result_no_aqe.explain(True)
```
```text
这次重点寻找：AdaptiveSparkPlan
AQE 开启
AdaptiveSparkPlan
```

## 结论

```text
实验：Day09-07

数据：
dim.customer_shuffle

数据量：
1,000,000

输入 Partition：
4

GroupBy：
groupBy("province").count()

默认 Shuffle Partition：
200
```
```text
实验 A：
AQE = true
观察：
AdaptiveSparkPlan
Exchange
hashpartitioning(province, 200)
```
```text
实验 B：
AQE = false
观察：
不再出现 AdaptiveSparkPlan
Exchange
hashpartitioning(province, 200)
```
```text
最终结论：
1. AQE 不改变 GroupBy 的业务结果。

2. GroupBy 仍然需要 Shuffle。

3. spark.sql.shuffle.partitions 控制 Shuffle 阶段的默认分区数。

4. AQE 是运行时执行计划优化机制。

5. AQE=true 和 AQE=false 的执行计划存在差异。

6. Input Partition 与 Shuffle Partition 是两个不同概念。
```