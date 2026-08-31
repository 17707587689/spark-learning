1. 第一组实验 Shuffle Partition = 200

```python
print(
    "AQE:",
    spark.conf.get("spark.sql.adaptive.enabled")
)

print(
    "shuffle partitions:",
    spark.conf.get("spark.sql.shuffle.partitions")
)

result_200 = customer_df.groupBy("province").count()

result_200.explain(True)
```
```text
result_200.explain(True)
== Parsed Logical Plan ==
'Aggregate ['province], ['province, count(1) AS count#114L]
+- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Analyzed Logical Plan ==
province: string, count: bigint
Aggregate [province#81], [province#81, count(1) AS count#114L]
+- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Optimized Logical Plan ==
Aggregate [province#81], [province#81, count(1) AS count#114L]
+- Project [province#81]
   +- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Physical Plan ==
*(2) HashAggregate(keys=[province#81], functions=[count(1)], output=[province#81, count#114L])
+- Exchange hashpartitioning(province#81, 200), ENSURE_REQUIREMENTS, [plan_id=227]
   +- *(1) HashAggregate(keys=[province#81], functions=[partial_count(1)], output=[province#81, count#119L])
      +- *(1) ColumnarToRow
         +- FileScan parquet [province#81] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [], ReadSchema: struct<province:string>

重点寻找：
Exchange
hashpartitioning(province, 200)

说明
GroupBy
  ↓
Shuffle
  ↓
200 个 Shuffle Partition
```

2. 第二组实验：修改为 10

```python
spark.conf.set(
    "spark.sql.shuffle.partitions",
    "10"
)

print(
    "shuffle partitions:",
    spark.conf.get("spark.sql.shuffle.partitions")
)

result_10 = customer_df.groupBy("province").count()

result_10.explain(True)
```
```text
result_10.explain(True)
== Parsed Logical Plan ==
'Aggregate ['province], ['province, count(1) AS count#129L]
+- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Analyzed Logical Plan ==
province: string, count: bigint
Aggregate [province#81], [province#81, count(1) AS count#129L]
+- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Optimized Logical Plan ==
Aggregate [province#81], [province#81, count(1) AS count#129L]
+- Project [province#81]
   +- Relation [customer_id#76L,customer_name#77,gender#78,age#79,customer_level#80,province#81,city#82,register_date#83] parquet

== Physical Plan ==
*(2) HashAggregate(keys=[province#81], functions=[count(1)], output=[province#81, count#129L])
+- Exchange hashpartitioning(province#81, 10), ENSURE_REQUIREMENTS, [plan_id=259]
   +- *(1) HashAggregate(keys=[province#81], functions=[partial_count(1)], output=[province#81, count#133L])
      +- *(1) ColumnarToRow
         +- FileScan parquet [province#81] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [], ReadSchema: struct<province:string>
```
```text
这一次重点观察：
Exchange
hashpartitioning(province, 10)
```
3. 调整过程

```text
spark.sql.shuffle.partitions = 200

4 Input Partitions
        │
        ▼
     GroupBy
        │
        ▼
     Shuffle
        │
        ├── Partition 0
        ├── Partition 1
        ├── Partition 2
        ├── ...
        └── Partition 199

修改为 10

4 Input Partitions
        │
        ▼
     GroupBy
        │
        ▼
     Shuffle
        │
        ├── Partition 0
        ├── Partition 1
        ├── ...
        └── Partition 9

所以这个参数最核心的作用可以先记成：
控制 Shuffle 阶段默认产生多少个分区。
```

4. 完整代码 

```python
# ==========================================
# Day09-08
# spark.sql.shuffle.partitions 实验
# ==========================================

# 1. 关闭 AQE
spark.conf.set(
    "spark.sql.adaptive.enabled",
    "false"
)

# 2. 查看输入数据
print("count:", customer_df.count())
print(
    "input partitions:",
    customer_df.rdd.getNumPartitions()
)

# ==========================================
# Experiment 1: 200
# ==========================================

spark.conf.set(
    "spark.sql.shuffle.partitions",
    "200"
)

print("\n===== shuffle partitions = 200 =====")

result_200 = customer_df.groupBy("province").count()

result_200.explain(True)


# ==========================================
# Experiment 2: 10
# ==========================================

spark.conf.set(
    "spark.sql.shuffle.partitions",
    "10"
)

print("\n===== shuffle partitions = 10 =====")

result_10 = customer_df.groupBy("province").count()

result_10.explain(True)


# ==========================================
# Experiment 3: 50
# ==========================================

spark.conf.set(
    "spark.sql.shuffle.partitions",
    "50"
)

print("\n===== shuffle partitions = 50 =====")

result_50 = customer_df.groupBy("province").count()

result_50.explain(True)


# ==========================================
# Restore
# ==========================================

spark.conf.set(
    "spark.sql.shuffle.partitions",
    "200"
)

print("\n===== restored =====")
print(
    "shuffle partitions:",
    spark.conf.get("spark.sql.shuffle.partitions")
)
```

5. 执行计划简单理解

```text
customer_df.groupBy("province").count()
↓
Project
只保留 province
↓
FileScan parquet
只读取 province
↓
Partial HashAggregate
先在本地做一次聚合
↓
Exchange
按照 province Hash 重分区
↓
200 / 10 个 Shuffle Partition
↓
Final HashAggregate
完成最终聚合
```

6. 结论

```text

Day09-08：spark.sql.shuffle.partitions 实验

实验条件：

数据：
dim.customer_shuffle

数据量：
1,000,000

Input Partition：
4

GroupBy：
province

AQE：
false

实验一：
spark.sql.shuffle.partitions = 200

Physical Plan：
Exchange hashpartitioning(province#81, 200)

实验二：
spark.sql.shuffle.partitions = 10
Physical Plan：
Exchange hashpartitioning(province#81, 10)

1. GroupBy(province) 会触发 Shuffle。

2. Shuffle 在 Physical Plan 中表现为 Exchange。

3. spark.sql.shuffle.partitions
   控制 Shuffle HashPartitioning 的默认分区数量。

4. 200 → 10 后，Logical Plan 基本不变。

5. 变化主要发生在 Physical Plan：
   hashpartitioning(province, 200)
   →
   hashpartitioning(province, 10)

6. GroupBy 通常会出现 Partial HashAggregate
   和 Final HashAggregate 两阶段聚合。

7. Spark 会进行列裁剪，
   因此 FileScan 最终只读取 province。

还有一个特别重要的认识：
spark.sql.shuffle.partitions = 200
不是说 Spark 永远最终会执行 200 个有效 Task。
特别是我们上一节刚学过：
AQE 可以在运行过程中进一步优化执行计划。
```