```text
select() 决定“最终输出哪些列”，alias() 决定“这些列最终叫什么名字”。
```
```python
df = customer_df.select(
    customer_df.customer_id.alias("id"),
    customer_df.customer_name.alias("name"),
    "province",
    "age",
    (customer_df.age + 1).alias("next_age")
)

df.show()
df.printSchema()
df.explain()

>>> df.explain()
== Physical Plan ==
*(1) Project [customer_id#0L AS id#265L, customer_name#1 AS name#266, province#5, age#3, (age#3 + 1) AS next_age#267]
+- *(1) ColumnarToRow
   +- FileScan parquet [customer_id#0L,customer_name#1,age#3,province#5] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [], ReadSchema: struct<customer_id:bigint,customer_name:string,age:int,province:string>
```

| 写法                                        | 含义        |
| ----------------------------------------- | --------- |
| `customer_df.customer_id.alias("id")`     | 选择字段 + 改名 |
| `customer_df.customer_name.alias("name")` | 选择字段 + 改名 |
| `"province"`                              | 原样选择      |
| `"age"`                                   | 原样选择      |
| `(customer_df.age + 1).alias("next_age")` | 计算字段 + 改名 |

```text
① select()
   → 决定输出哪些列

② alias()
   → 给字段/表达式重新命名

③ select + 表达式
   → 可以在选择字段的同时进行计算

④ select
   → Physical Plan 中通常体现为 Project

⑤ select
   → 可以触发 Column Pruning，减少 Parquet 实际读取的列
```



