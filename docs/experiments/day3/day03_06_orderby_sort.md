```python 
customer_df.orderBy("age")
customer_df.orderBy(desc("age"))
customer_df.orderBy(col("age").desc())
# 多字段排序
customer_df.orderBy(
    col("province").asc(),
    col("age").desc()
).show()

# 年龄从大到小，如果年龄相同，则 customer_id 从小到大。
customer_df.orderBy(
    col("age").desc(),
    col("customer_id").asc()
).show()
# 等价于
customer_df.sort(
    col("age").desc(),
    col("customer_id").asc()
).show()
```

| 操作           | 是否通常涉及 Shuffle | 主要目的   |
| ------------ | -------------- | ------ |
| `select`     | ❌              | 选择列    |
| `drop`       | ❌              | 删除列    |
| `withColumn` | ❌              | 增加/修改列 |
| `filter`     | ❌              | 过滤数据   |
| `groupBy`    | ✅              | 数据重新分组 |
| `orderBy`    | ✅              | 全局排序   |

```text
>>> customer_df.orderBy("age").explain()
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- Sort [age#3 ASC NULLS FIRST], true, 0
   +- Exchange rangepartitioning(age#3 ASC NULLS FIRST, 200), ENSURE_REQUIREMENTS, [plan_id=345]
      +- FileScan parquet [customer_id#0L,customer_name#1,gender#2,age#3,customer_level#4,province#5,city#6,register_date#7] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [], ReadSchema: struct<customer_id:bigint,customer_name:string,gender:string,age:int,customer_level:string,provin...

FileScan parquet [...] Spark 从 Parquet 文件中读取 customer_df 数据
Exchange rangepartitioning(age#3 ASC NULLS FIRST, 200)  Spark 根据 age 的范围，把数据重新划分到不同 Partition。
这个 200 就是Shuffle 后的 Partition 数量。
Sort [age#3 ASC NULLS FIRST], true, 0 排序
NULLS FIRST 代表 如果 age 存在 NULL，那么升序排序时 NULL 放最前面

实际上执行逻辑就是

① 从 Parquet 读取数据
        ↓
② 根据 age 做 Range Partition
        ↓
③ Shuffle
        ↓
④ 每个 Partition 内进行 Sort
        ↓
⑤ 得到全局有序结果
```
```text
groupBy 和 orderBy 的 Shuffle 有什么区别？
groupBy
   ↓
Exchange hashpartitioning(province, 200)

orderBy
   ↓
Exchange rangepartitioning(age, 200)
```
| 操作                    | Partition 方式        | 目的                           |
| --------------------- | ------------------- | ---------------------------- |
| `groupBy("province")` | `hashpartitioning`  | 相同 province 尽量进入同一 Partition |
| `orderBy("age")`      | `rangepartitioning` | 按 age 范围重新分配，为全局排序做准备        |

```text
Spark 中 orderBy 为什么比较昂贵
orderBy 是全局排序，为了保证整个 DataFrame 的数据有序，需要根据排序字段进行 Range Partition，并发生 Shuffle，然后再进行 Sort。因此全局排序通常会产生较大的网络和磁盘 I/O 开销
```
```text
groupBy 和 orderBy 对比

                 DataFrame
                     │
          ┌──────────┴──────────┐
          │                     │
       groupBy               orderBy
          │                     │
          ↓                     ↓
 hashpartitioning        rangepartitioning
          │                     │
          ↓                     ↓
       Shuffle               Shuffle
          │                     │
          ↓                     ↓
    HashAggregate             Sort
```
```python
>>> customer_df.sortWithinPartitions(
...     col("age").desc()
... ).explain()

# false, 0中的false说明是分区内排序，非全表排序，没有发现Exchange
== Physical Plan ==
*(1) Sort [age#3 DESC NULLS LAST], false, 0
+- *(1) ColumnarToRow
   +- FileScan parquet [customer_id#0L,customer_name#1,gender#2,age#3,customer_level#4,province#5,city#6,register_date#7] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [], ReadSchema: struct<customer_id:bigint,customer_name:string,gender:string,age:int,customer_level:string,provin...
```
```text
                 排序
                  │
        ┌─────────┴─────────┐
        │                   │
     orderBy          sortWithinPartitions
        │                   │
        ↓                   ↓
    全局排序             分区内排序
        │                   │
        ↓                   ↓
     Shuffle              无需
        │                排序 Shuffle
        ↓                   │
RangePartition              │
        │                   │
        ↓                   ↓
      Sort                 Sort
```
```text
1. orderBy() 和 sort() 都可以排序。

2. 默认是升序 ASC。

3. desc() 可以实现降序。

4. orderBy() 是全局排序，通常需要 Shuffle。

5. orderBy() 的 Shuffle 使用 Range Partition。

6. sortWithinPartitions() 只进行 Partition 内排序，不要求全局有序，因此不需要为排序进行 Exchange。
```