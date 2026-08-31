1. 确认分区数

```python 
print("count:", customer_df.count())

print(
    "input partitions:",
    customer_df.rdd.getNumPartitions()
)
```
```text
>>> print("count:", customer_df.count())

count: 1000000                                                                  
>>> 
>>> print(
...     "input partitions:",
...     customer_df.rdd.getNumPartitions()
... )
input partitions: 4
```

2. 关闭 AQE

```python
spark.conf.set(
    "spark.sql.adaptive.enabled",
    "false"
)
```

3. 实验 A：普通 GroupBy

```python
spark.conf.set(
    "spark.sql.shuffle.partitions",
    "200"
)

result_groupby_200 = (
    customer_df
    .groupBy("province")
    .count()
)

result_groupby_200.explain(True)
```
```text
 result_groupby_200.explain(True)
== Parsed Logical Plan ==
'Aggregate ['province], ['province, count(1) AS count#156L]
+- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Analyzed Logical Plan ==
province: string, count: bigint
Aggregate [province#81], [province#81, count(1) AS count#156L]
+- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Optimized Logical Plan ==
Aggregate [province#81], [province#81, count(1) AS count#156L]
+- Project [province#81]
   +- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Physical Plan ==
*(2) HashAggregate(keys=[province#81], functions=[count(1)], output=[province#81, count#156L])
+- Exchange hashpartitioning(province#81, 200), ENSURE_REQUIREMENTS, [plan_id=321]
   +- *(1) HashAggregate(keys=[province#81], functions=[partial_count(1)], output=[province#81, count#160L])
      +- *(1) ColumnarToRow
         +- FileScan parquet [province#81] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [], ReadSchema: struct<province:string>
```

4. 实验 B：把 shuffle.partitions 改成 10

```python
spark.conf.set(
    "spark.sql.shuffle.partitions",
    "10"
)

result_groupby_10 = (
    customer_df
    .groupBy("province")
    .count()
)

result_groupby_10.explain(True)
```
```text
Exchange hashpartitioning(province#81, 10)
其余与实验 A高度相似
```

5. 实验 C：repartition(10)

```python 
df_repartition_10 = customer_df.repartition(10)

print(
    "before:",
    customer_df.rdd.getNumPartitions()
)

print(
    "after:",
    df_repartition_10.rdd.getNumPartitions()
)
```
```text
>>> df_repartition_10 = customer_df.repartition(10)
>>> print(
...     "before:",
...     customer_df.rdd.getNumPartitions()
... )
before: 4
>>> 
>>> 
>>> print(
...     "after:",
...     df_repartition_10.rdd.getNumPartitions()
... )
after: 10
```
```text
>>> df_repartition_10.explain(True)
== Parsed Logical Plan ==
Repartition 10, true
+- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Analyzed Logical Plan ==
customer_id: bigint, customer_name: string, gender: string, age: int, customer_level: string, province: string, city: string, register_date: date
Repartition 10, true
+- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Optimized Logical Plan ==
Repartition 10, true
+- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Physical Plan ==
Exchange RoundRobinPartitioning(10), REPARTITION_BY_NUM, [plan_id=345]
+- *(1) ColumnarToRow
   +- FileScan parquet [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [], ReadSchema: struct<customer_id:bigint,customer_name:string,gender:string,age:int,customer_level:string,provin.
```

6. 区别

```text
GroupBy

customer_df
4 partitions
     │
     ▼
 groupBy(province)
     │
     ▼
   Shuffle
     │
     │ hash(province)
     ▼
10 Shuffle Partitions
     │
     ▼
Final HashAggregate

repartition(10)

customer_df
4 partitions
     │
     ▼
repartition(10)
     │
     ▼
   Shuffle
     │
     │ RoundRobin
     ▼
10 Partitions

```

7. 再做一个非常重要的实验：repartition + GroupBy

```python
df_repartition_10 = customer_df.repartition(10)

result_repartition_groupby = (
    df_repartition_10
    .groupBy("province")
    .count()
)

result_repartition_groupby.explain(True)
```
```text
result_repartition_groupby.explain(True)
== Parsed Logical Plan ==
'Aggregate ['province], ['province, count(1) AS count#170L]
+- Repartition 10, true
   +- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Analyzed Logical Plan ==
province: string, count: bigint
Aggregate [province#81], [province#81, count(1) AS count#170L]
+- Repartition 10, true
   +- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Optimized Logical Plan ==
Aggregate [province#81], [province#81, count(1) AS count#170L]
+- Repartition 10, true
   +- Project [province#81]
      +- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Physical Plan ==
*(3) HashAggregate(keys=[province#81], functions=[count(1)], output=[province#81, count#170L])
+- Exchange hashpartitioning(province#81, 200), ENSURE_REQUIREMENTS, [plan_id=379]
   +- *(2) HashAggregate(keys=[province#81], functions=[partial_count(1)], output=[province#81, count#174L])
      +- Exchange RoundRobinPartitioning(10), REPARTITION_BY_NUM, [plan_id=375]
         +- *(1) ColumnarToRow
            +- FileScan parquet [province#81] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [], ReadSchema: struct<province:string>
```
```text
Exchange RoundRobinPartitioning(10)
Exchange hashpartitioning(province#81, 200)
为了单纯改变 Partition 数量而提前 repartition()，可能额外增加一次 Shuffle
```

8. 知识点

| 操作                                | 是否可能 Shuffle     | 作用               | Partition           |
| --------------------------------- | ---------------- | ---------------- | ------------------- |
| `customer_df`                     | 否                | 读取数据             | 4                   |
| `spark.sql.shuffle.partitions=10` | 本身不触发            | 控制 Shuffle 默认分区数 | 原 DataFrame 仍为 4    |
| `groupBy("province")`             | **是**            | 按 key 聚合         | Shuffle 可为 10       |
| `repartition(10)`                 | **是**            | 主动重新分区           | 变成 10               |
| `repartition(10).groupBy()`       | **可能两次 Shuffle** | 先重分区，再聚合         | 10 → 再按 key Shuffle |

9. 结论

```text
实验条件
数据：
dim.customer_shuffle

数据量：
1,000,000

输入 Partition：
4

AQE：
false

实验一
repartition(10)
+
shuffle.partitions = 200

得到
Exchange RoundRobinPartitioning(10)
        ↓
Exchange hashpartitioning(province, 200)

实验二
repartition(10)
+
shuffle.partitions = 10

得到
Exchange RoundRobinPartitioning(10)
        ↓
Exchange hashpartitioning(province, 10)

核心结论

1. repartition(10) 本身会触发 Shuffle。

2. repartition(10) 使用 RoundRobinPartitioning。

3. groupBy("province") 会触发基于 province 的 Hash Shuffle。

4. spark.sql.shuffle.partitions 控制 GroupBy Shuffle
   默认的 Shuffle Partition 数量。

5. repartition(10) 和
   spark.sql.shuffle.partitions = 10
   不是一回事。

6. repartition(10) + groupBy()
   可能产生两次 Shuffle。

7. 不必要的 repartition 可能增加 ETL 执行成本。
```
