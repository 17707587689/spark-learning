```python
>>> customer_df.filter(customer_df.province == "广东" & customer_df.age > 50).show()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
# 多个条件组合时，每一个条件都加括号。
>>> customer_df.filter(customer_df.province == "广东").show()
+-----------+-------------+------+---+--------------+--------+------+-------------+
|customer_id|customer_name|gender|age|customer_level|province|  city|register_date|
+-----------+-------------+------+---+--------------+--------+------+-------------+
|         10|  customer_10|     M| 52|           VIP|    广东|广东市|   2023-04-21|
|         20|  customer_20|     M| 54|           VIP|    广东|广东市|   2019-03-31|
```
| 操作             | 行    | 列       | Schema |
| -------------- | ---- | ------- | ------ |
| `filter()`     | 可能减少 | 不变      | 通常不变   |
| `select()`     | 不变   | 可能减少/变化 | 变化     |
| `withColumn()` | 不变   | 新增/替换   | 可能变化   |

```text
filter()
   ↓
Transformation
   ↓
构建计算计划
   ↓
Action
   ↓
真正执行
```
常用写法
```python
# 大于
df.filter(df.age > 30)

# 等于
df.filter(df.age == 30)

# 不等于
df.filter(df.age != 30)

# 字符串
df.filter(df.province == "广东")

# AND
df.filter(
    (df.age > 30) & (df.province == "广东")
)

# OR
df.filter(
    (df.age > 40) | (df.province == "广东")
)

# NULL
df.filter(df.age.isNull())

# 非 NULL
df.filter(df.age.isNotNull())
```
```python
>>> customer_filter_df = customer_df.filter(
...     customer_df.age > 30
... )
```
```text
>>> customer_filter_df.explain(True)
== Parsed Logical Plan ==
Filter (age#3 > 30)
+- Relation [customer_id#0L,customer_name#1,gender#2,age#3,customer_level#4,province#5,city#6,register_date#7] parquet

== Analyzed Logical Plan ==
customer_id: bigint, customer_name: string, gender: string, age: int, customer_level: string, province: string, city: string, register_date: date
Filter (age#3 > 30)
+- Relation [customer_id#0L,customer_name#1,gender#2,age#3,customer_level#4,province#5,city#6,register_date#7] parquet

== Optimized Logical Plan ==
Filter (isnotnull(age#3) AND (age#3 > 30))
+- Relation [customer_id#0L,customer_name#1,gender#2,age#3,customer_level#4,province#5,city#6,register_date#7] parquet

== Physical Plan ==
*(1) Filter (isnotnull(age#3) AND (age#3 > 30))
+- *(1) ColumnarToRow
   +- FileScan parquet [customer_id#0L,customer_name#1,gender#2,age#3,customer_level#4,province#5,city#6,register_date#7] Batched: true, DataFilters: [isnotnull(age#3), (age#3 > 30)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [IsNotNull(age), GreaterThan(age,30)], ReadSchema: struct<customer_id:bigint,customer_name:string,gender:string,age:int,customer_level:string,provin...
```
```text
Python代码
    │
    │
    ▼
customer_df.filter(customer_df.age > 30)
    │
    ▼
Parsed Logical Plan
    │
    │ Filter(age#3 > 30)
    ▼
Analyzed Logical Plan
    │
    │ 确认 age 是哪个字段、类型是什么
    ▼
Optimized Logical Plan
    │
    │ 增加 isnotnull(age)
    ▼
Physical Plan
    │
    ├── FileScan Parquet
    │
    ├── ColumnarToRow
    │
    └── Filter
    │
    ▼
最终结果
```
| 操作       | PySpark       |
| -------- | ------------- |
| 过滤行      | `filter()`    |
| 大于       | `>`           |
| 等于       | `==`          |
| 不等于      | `!=`          |
| AND      | `&`           |
| OR       | `\|`          |
| NOT      | `~`           |
| 判断 NULL  | `isNull()`    |
| 判断非 NULL | `isNotNull()` |
