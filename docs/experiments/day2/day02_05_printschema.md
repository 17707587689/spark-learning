| 方法              | 作用     | 是否属于 Action |
| --------------- | ------ | ----------- |
| `show()`        | 查看数据   | ✅ 是         |
| `printSchema()` | 查看数据结构 | ❌ 不是        |
| `count()`       | 统计行数   | ✅ 是         |
| `collect()`     | 获取全部数据 | ✅ 是         |
| `explain()`     | 查看执行计划 | ❌ 不是        |

- printSchema() 查看 DataFrame 的 Schema。
- Schema 描述字段名、数据类型和 nullable。
- printSchema() 主要是给人看的。
- df.schema 返回 StructType，方便程序处理。
- printSchema() 不需要像 show() 一样计算数据结果。
- Transformation 可能改变 Schema，例如 withColumn()；也可能不改变，例如 filter()。

| 操作             | 主要影响 | Schema  |
| -------------- | ---- | ------- |
| `filter()`     | 行    | 通常不变    |
| `where()`      | 行    | 通常不变    |
| `select()`     | 列    | 会变      |
| `withColumn()` | 列    | 可能变     |
| `drop()`       | 列    | 会变      |
| `groupBy()`    | 数据结构 | 后续聚合时会变 |
| `orderBy()`    | 行顺序  | 不改变字段结构 |

```python
>>> customer_df = spark.read.parquet("/user/hive/warehouse/dim/customer_shuffle")
>>> customer_df.schema.fields
[StructField('customer_id', LongType(), True), StructField('customer_name', StringType(), True), StructField('gender', StringType(), True), StructField('age', IntegerType(), True), StructField('customer_level', StringType(), True), StructField('province', StringType(), True), StructField('city', StringType(), True), StructField('register_date', DateType(), True)]
>>> for field in customer_df.schema.fields:
...     print(field.name, field.dataType, field.nullable)
... 
customer_id LongType() True
customer_name StringType() True
gender StringType() True
age IntegerType() True
customer_level StringType() True
province StringType() True
city StringType() True
register_date DateType() True
>>> customer_df.printSchema()
root
 |-- customer_id: long (nullable = true)
 |-- customer_name: string (nullable = true)
 |-- gender: string (nullable = true)
 |-- age: integer (nullable = true)
 |-- customer_level: string (nullable = true)
 |-- province: string (nullable = true)
 |-- city: string (nullable = true)
 |-- register_date: date (nullable = true)

>>> 
>>> customer_df.printSchema()
root
 |-- customer_id: long (nullable = true)
 |-- customer_name: string (nullable = true)
 |-- gender: string (nullable = true)
 |-- age: integer (nullable = true)
 |-- customer_level: string (nullable = true)
 |-- province: string (nullable = true)
 |-- city: string (nullable = true)
 |-- register_date: date (nullable = true)

>>> print(customer_df.schema)
StructType([StructField('customer_id', LongType(), True), StructField('customer_name', StringType(), True), StructField('gender', StringType(), True), StructField('age', IntegerType(), True), StructField('customer_level', StringType(), True), StructField('province', StringType(), True), StructField('city', StringType(), True), StructField('register_date', DateType(), True)])
>>> 
>>> for field in customer_df.schema.fields:
...     print(
...         field.name,
...         field.dataType,
...         field.nullable
...     )
... 
customer_id LongType() True
customer_name StringType() True
gender StringType() True
age IntegerType() True
customer_level StringType() True
province StringType() True
city StringType() True
register_date DateType() True
>>> df_age = customer_df.filter(customer_df.age > 30)
>>> df_age.printSchema()
root
 |-- customer_id: long (nullable = true)
 |-- customer_name: string (nullable = true)
 |-- gender: string (nullable = true)
 |-- age: integer (nullable = true)
 |-- customer_level: string (nullable = true)
 |-- province: string (nullable = true)
 |-- city: string (nullable = true)
 |-- register_date: date (nullable = true)

>>> df_new = customer_df.withColumn(
...     "age_double",
...     customer_df.age * 2
... )
>>> df_new.printSchema()
root
 |-- customer_id: long (nullable = true)
 |-- customer_name: string (nullable = true)
 |-- gender: string (nullable = true)
 |-- age: integer (nullable = true)
 |-- customer_level: string (nullable = true)
 |-- province: string (nullable = true)
 |-- city: string (nullable = true)
 |-- register_date: date (nullable = true)
 |-- age_double: integer (nullable = true)
```