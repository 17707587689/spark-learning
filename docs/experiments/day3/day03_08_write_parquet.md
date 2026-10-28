```python
>>> customer_df = spark.read.parquet("/user/hive/warehouse/dim/customer_shuffle")
>>>                                                                             
>>> 
>>> 
>>> customer_df.show(5)
+-----------+-------------+------+---+--------------+--------+------+-------------+
|customer_id|customer_name|gender|age|customer_level|province|  city|register_date|
+-----------+-------------+------+---+--------------+--------+------+-------------+
|          1|   customer_1|     F| 44|           VIP|    北京|北京市|   2021-07-09|
|          2|   customer_2|     M| 39|          GOLD|    上海|上海市|   2025-02-16|
|          3|   customer_3|     F| 53|          GOLD|    江苏|江苏市|   2021-04-16|
|          4|   customer_4|     M| 29|          GOLD|    浙江|浙江市|   2017-07-06|
|          5|   customer_5|     F| 46|        NORMAL|    四川|四川市|   2022-08-24|
+-----------+-------------+------+---+--------------+--------+------+-------------+
only showing top 5 rows

>>> customer_df.write.parquet(
...     "/tmp/customer_parquet"
... )
26/09/02 18:42:20 WARN DataStreamer: Slow waitForAckedSeqno took 46052ms (threshold=30000ms). File being written: /tmp/customer_parquet/_temporary/0/_temporary/attempt_202609021841187149771769304958557_0002_m_000000_2/part-00000-3f971e4d-35d3-4eab-9cb0-ef28e7742234-c000.snappy.parquet, block: BP-664328308-192.168.214.129-1738936466212:blk_1073742532_1708, Write pipeline datanodes: [DatanodeInfoWithStorage[192.168.214.129:9866,DS-8647d913-90de-4c07-b280-dea0cfcd98d3,DISK]].
26/09/02 18:42:20 WARN DataStreamer: Slow waitForAckedSeqno took 46474ms (threshold=30000ms). File being written: /tmp/customer_parquet/_temporary/0/_temporary/attempt_202609021841187149771769304958557_0002_m_000001_3/part-00001-3f971e4d-35d3-4eab-9cb0-ef28e7742234-c000.snappy.parquet, block: BP-664328308-192.168.214.129-1738936466212:blk_1073742531_1707, Write pipeline datanodes: [DatanodeInfoWithStorage[192.168.214.129:9866,DS-8647d913-90de-4c07-b280-dea0cfcd98d3,DISK]].
26/09/02 18:42:26 WARN DataStreamer: Slow waitForAckedSeqno took 52390ms (threshold=30000ms). File being written: /tmp/customer_parquet/_temporary/0/_temporary/attempt_202609021841187149771769304958557_0002_m_000003_5/part-00003-3f971e4d-35d3-4eab-9cb0-ef28e7742234-c000.snappy.parquet, block: BP-664328308-192.168.214.129-1738936466212:blk_1073742530_1706, Write pipeline datanodes: [DatanodeInfoWithStorage[192.168.214.129:9866,DS-8647d913-90de-4c07-b280-dea0cfcd98d3,DISK]].
26/09/02 18:42:26 WARN DataStreamer: Slow waitForAckedSeqno took 52491ms (threshold=30000ms). File being written: /tmp/customer_parquet/_temporary/0/_temporary/attempt_202609021841187149771769304958557_0002_m_000002_4/part-00002-3f971e4d-35d3-4eab-9cb0-ef28e7742234-c000.snappy.parquet, block: BP-664328308-192.168.214.129-1738936466212:blk_1073742529_1705, Write pipeline datanodes: [DatanodeInfoWithStorage[192.168.214.129:9866,DS-8647d913-90de-4c07-b280-dea0cfcd98d3,DISK]].
>>>                                                                             
>>> customer_df.write.parquet(
...     "/tmp/customer_parquet"
... )
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/opt/miniconda3/envs/spark-env/lib/python3.10/site-packages/pyspark/sql/readwriter.py", line 1721, in parquet
    self._jwrite.parquet(path)
  File "/opt/miniconda3/envs/spark-env/lib/python3.10/site-packages/pyspark/python/lib/py4j-0.10.9.7-src.zip/py4j/java_gateway.py", line 1322, in __call__
  File "/opt/miniconda3/envs/spark-env/lib/python3.10/site-packages/pyspark/errors/exceptions/captured.py", line 185, in deco
    raise converted from None
pyspark.errors.exceptions.captured.AnalysisException: [PATH_ALREADY_EXISTS] Path hdfs://hadoop1:9000/tmp/customer_parquet already exists. Set mode as "overwrite" to overwrite the existing path.
>>> (
...     customer_df.write
...     .mode("overwrite")
...     .parquet("/tmp/customer_parquet")
... )
>>>                                                                             
>>> 
>>> 
>>> customer_df.write \
...     .mode("append") \
...     .parquet("/tmp/customer_parquet")
>>>                                                                             
>>> 
>>> df = spark.read.parquet(
...     "/tmp/customer_parquet"
... )
>>> df.show(5)
>>> (
...     customer_df.write
...     .mode("overwrite")
...     .partitionBy("province")
...     .parquet("/tmp/customer_partition")
... )
>>>                                                                             
>>> 
>>> customer_partition_df = spark.read.parquet(
...     "/tmp/customer_partition"
... )
>>> 
>>> customer_partition_df.show(5)
+-----------+---------------+------+---+--------------+------+-------------+--------+
|customer_id|  customer_name|gender|age|customer_level|  city|register_date|province|
+-----------+---------------+------+---+--------------+------+-------------+--------+
|     500009|customer_500009|     F| 28|        NORMAL|山东市|   2025-05-03|    山东|
|     500019|customer_500019|     F| 45|        NORMAL|山东市|   2017-02-04|    山东|
|     500029|customer_500029|     F| 59|        NORMAL|山东市|   2026-06-17|    山东|
|     500039|customer_500039|     F| 29|        NORMAL|山东市|   2017-06-24|    山东|
|     500049|customer_500049|     F| 40|        NORMAL|山东市|   2019-05-16|    山东|
+-----------+---------------+------+---+--------------+------+-------------+--------+
only showing top 5 rows

>>> customer_partition_df \
...     .filter(col("province") == "Guangdong") \
...     .explain(True)
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
NameError: name 'col' is not defined
>>> 
>>> from pyspark.sql.functions import col
>>> 
>>> 
>>> 
>>> customer_partition_df \
...     .filter(col("province") == "Guangdong") \
...     .explain(True)
== Parsed Logical Plan ==
'Filter ('province = Guangdong)
+- Relation [customer_id#200L,customer_name#201,gender#202,age#203,customer_level#204,city#205,register_date#206,province#207] parquet

== Analyzed Logical Plan ==
customer_id: bigint, customer_name: string, gender: string, age: int, customer_level: string, city: string, register_date: date, province: string
Filter (province#207 = Guangdong)
+- Relation [customer_id#200L,customer_name#201,gender#202,age#203,customer_level#204,city#205,register_date#206,province#207] parquet

== Optimized Logical Plan ==
Filter (isnotnull(province#207) AND (province#207 = Guangdong))
+- Relation [customer_id#200L,customer_name#201,gender#202,age#203,customer_level#204,city#205,register_date#206,province#207] parquet

== Physical Plan ==
*(1) ColumnarToRow
+- FileScan parquet [customer_id#200L,customer_name#201,gender#202,age#203,customer_level#204,city#205,register_date#206,province#207] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/tmp/customer_partition], PartitionFilters: [isnotnull(province#207), (province#207 = Guangdong)], PushedFilters: [], ReadSchema: struct<customer_id:bigint,customer_name:string,gender:string,age:int,customer_level:string,city:s...

>> customer_partition_df \
...     .filter(
...         (col("province") == "Guangdong") &
...         (col("age") > 30)
...     ) \
...     .explain(True)
== Parsed Logical Plan ==
'Filter (('province = Guangdong) AND ('age > 30))
+- Relation [customer_id#267L,customer_name#268,gender#269,age#270,customer_level#271,city#272,register_date#273,province#274] parquet

== Analyzed Logical Plan ==
customer_id: bigint, customer_name: string, gender: string, age: int, customer_level: string, city: string, register_date: date, province: string
Filter ((province#274 = Guangdong) AND (age#270 > 30))
+- Relation [customer_id#267L,customer_name#268,gender#269,age#270,customer_level#271,city#272,register_date#273,province#274] parquet

== Optimized Logical Plan ==
Filter ((isnotnull(province#274) AND isnotnull(age#270)) AND ((province#274 = Guangdong) AND (age#270 > 30)))
+- Relation [customer_id#267L,customer_name#268,gender#269,age#270,customer_level#271,city#272,register_date#273,province#274] parquet

== Physical Plan ==
*(1) Filter (isnotnull(age#270) AND (age#270 > 30))
+- *(1) ColumnarToRow
   +- FileScan parquet [customer_id#267L,customer_name#268,gender#269,age#270,customer_level#271,city#272,register_date#273,province#274] Batched: true, DataFilters: [isnotnull(age#270), (age#270 > 30)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/tmp/customer_partition], PartitionFilters: [isnotnull(province#274), (province#274 = Guangdong)], PushedFilters: [IsNotNull(age), GreaterThan(age,30)], ReadSchema: struct<customer_id:bigint,customer_name:string,gender:string,age:int,customer_level:string,city:s...

# 已经 PushedFilters 了，为什么下面还要 Filter
# PushedFilters 是“尽可能下推”，不是说 Spark 就完全不需要执行过滤了
# 数据源可能只能支持部分过滤能力，所以 Spark 仍然保留最终过滤逻辑来保证语义正确
```
```shell
[hadoop@hadoop1 ~]$ hdfs dfs -ls /tmp/customer_parquet
Found 5 items
-rw-r--r--   1 hadoop supergroup          0 2026-09-02 18:42 /tmp/customer_parquet/_SUCCESS
-rw-r--r--   1 hadoop supergroup    2855001 2026-09-02 18:42 /tmp/customer_parquet/part-00000-3f971e4d-35d3-4eab-9cb0-ef28e7742234-c000.snappy.parquet
-rw-r--r--   1 hadoop supergroup    2854130 2026-09-02 18:42 /tmp/customer_parquet/part-00001-3f971e4d-35d3-4eab-9cb0-ef28e7742234-c000.snappy.parquet
-rw-r--r--   1 hadoop supergroup    2853917 2026-09-02 18:42 /tmp/customer_parquet/part-00002-3f971e4d-35d3-4eab-9cb0-ef28e7742234-c000.snappy.parquet
-rw-r--r--   1 hadoop supergroup    2853912 2026-09-02 18:42 /tmp/customer_parquet/part-00003-3f971e4d-35d3-4eab-9cb0-ef28e7742234-c000.snappy.parquet
[hadoop@hadoop1 ~]$ 
[hadoop@hadoop1 ~]$ 
[hadoop@hadoop1 ~]$ hdfs dfs -ls /tmp/customer_parquet
Found 5 items
-rw-r--r--   1 hadoop supergroup          0 2026-09-02 18:51 /tmp/customer_parquet/_SUCCESS
-rw-r--r--   1 hadoop supergroup    2855001 2026-09-02 18:51 /tmp/customer_parquet/part-00000-0802706f-a4ca-44e2-95d6-d8c458e96667-c000.snappy.parquet
-rw-r--r--   1 hadoop supergroup    2854130 2026-09-02 18:51 /tmp/customer_parquet/part-00001-0802706f-a4ca-44e2-95d6-d8c458e96667-c000.snappy.parquet
-rw-r--r--   1 hadoop supergroup    2853917 2026-09-02 18:51 /tmp/customer_parquet/part-00002-0802706f-a4ca-44e2-95d6-d8c458e96667-c000.snappy.parquet
-rw-r--r--   1 hadoop supergroup    2853912 2026-09-02 18:51 /tmp/customer_parquet/part-00003-0802706f-a4ca-44e2-95d6-d8c458e96667-c000.snappy.parquet
# append后
[hadoop@hadoop1 ~]$ hdfs dfs -ls /tmp/customer_parquet
Found 9 items
-rw-r--r--   1 hadoop supergroup          0 2026-09-02 18:54 /tmp/customer_parquet/_SUCCESS
-rw-r--r--   1 hadoop supergroup    2855001 2026-09-02 18:51 /tmp/customer_parquet/part-00000-0802706f-a4ca-44e2-95d6-d8c458e96667-c000.snappy.parquet
-rw-r--r--   1 hadoop supergroup    2855001 2026-09-02 18:54 /tmp/customer_parquet/part-00000-887c989b-1512-460b-a441-be9f7697e0d1-c000.snappy.parquet
-rw-r--r--   1 hadoop supergroup    2854130 2026-09-02 18:51 /tmp/customer_parquet/part-00001-0802706f-a4ca-44e2-95d6-d8c458e96667-c000.snappy.parquet
-rw-r--r--   1 hadoop supergroup    2854130 2026-09-02 18:54 /tmp/customer_parquet/part-00001-887c989b-1512-460b-a441-be9f7697e0d1-c000.snappy.parquet
-rw-r--r--   1 hadoop supergroup    2853917 2026-09-02 18:51 /tmp/customer_parquet/part-00002-0802706f-a4ca-44e2-95d6-d8c458e96667-c000.snappy.parquet
-rw-r--r--   1 hadoop supergroup    2853917 2026-09-02 18:54 /tmp/customer_parquet/part-00002-887c989b-1512-460b-a441-be9f7697e0d1-c000.snappy.parquet
-rw-r--r--   1 hadoop supergroup    2853912 2026-09-02 18:51 /tmp/customer_parquet/part-00003-0802706f-a4ca-44e2-95d6-d8c458e96667-c000.snappy.parquet
-rw-r--r--   1 hadoop supergroup    2853912 2026-09-02 18:54 /tmp/customer_parquet/part-00003-887c989b-1512-460b-a441-be9f7697e0d1-c000.snappy.parquet
[hadoop@hadoop1 ~]$ hdfs dfs -ls /tmp/customer_partition
Found 11 items
-rw-r--r--   1 hadoop supergroup          0 2026-09-02 19:06 /tmp/customer_partition/_SUCCESS
drwxr-xr-x   - hadoop supergroup          0 2026-09-02 19:06 /tmp/customer_partition/province=上海
drwxr-xr-x   - hadoop supergroup          0 2026-09-02 19:06 /tmp/customer_partition/province=北京
drwxr-xr-x   - hadoop supergroup          0 2026-09-02 19:06 /tmp/customer_partition/province=四川
drwxr-xr-x   - hadoop supergroup          0 2026-09-02 19:06 /tmp/customer_partition/province=山东
drwxr-xr-x   - hadoop supergroup          0 2026-09-02 19:06 /tmp/customer_partition/province=广东
drwxr-xr-x   - hadoop supergroup          0 2026-09-02 19:06 /tmp/customer_partition/province=江苏
drwxr-xr-x   - hadoop supergroup          0 2026-09-02 19:06 /tmp/customer_partition/province=浙江
drwxr-xr-x   - hadoop supergroup          0 2026-09-02 19:06 /tmp/customer_partition/province=湖北
drwxr-xr-x   - hadoop supergroup          0 2026-09-02 19:06 /tmp/customer_partition/province=湖南
drwxr-xr-x   - hadoop supergroup          0 2026-09-02 19:06 /tmp/customer_partition/province=福建
```
```text
PartitionFilters 和 PushedFilters 的区别
PartitionFilters
        ↓
过滤目录 / 分区
        ↓
少读文件

PushedFilters
        ↓
过滤文件内部的数据
        ↓
少读数据
```
三种 Filter区分

| Plan 项目            | 作用              | 你的实验                   |
| ------------------ | --------------- | ---------------------- |
| `PartitionFilters` | 过滤目录分区          | `province = Guangdong` |
| `PushedFilters`    | 尝试下推到 Parquet   | `age > 30`             |
| `DataFilters`      | Spark 数据层面的过滤条件 | `age > 30`             |
| `Filter`           | Spark 最终执行过滤    | `age > 30`             |


三大优化

```text
                         FileScan parquet
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      PartitionFilters   PushedFilters      ReadSchema
             │                 │                 │
             ▼                 ▼                 ▼
        分区裁剪            谓词下推            列裁剪
             │                 │                 │
             ▼                 ▼                 ▼
        少读目录            少读数据            少读列
```

写 Parquet 时用 partitionBy 设计好物理目录；读 Parquet 时 Spark 会通过 Partition Pruning、Predicate Pushdown、Column Pruning 尽量做到少读目录、少读数据、少读列