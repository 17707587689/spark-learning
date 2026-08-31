```python
customer_df.select(
    "customer_id",
    "customer_name",
    "age"
)
```
```text
得到一个新的 DataFrame。
select() 不会修改原来的 customer_df。
DataFrame API 大多数操作都会返回一个新的 DataFrame，而不是修改原对象。
```
```python
>>> customer_df.select(
...     "customer_id",
...     "customer_name",
...     "age"
... ).show(5)
+-----------+-------------+---+
|customer_id|customer_name|age|
+-----------+-------------+---+
|          1|   customer_1| 44|
|          2|   customer_2| 39|
|          3|   customer_3| 53|
|          4|   customer_4| 29|
|          5|   customer_5| 46|
+-----------+-------------+---+
only showing top 5 rows

>>> df_select = customer_df.select(
...     "customer_id",
...     "customer_name",
...     "age"
... )
>>> 
>>> df_select.printSchema()
root
 |-- customer_id: long (nullable = true)
 |-- customer_name: string (nullable = true)
 |-- age: integer (nullable = true)

>>> df_select_age = customer_df.select(
...     "customer_id",
...     "age",
...     (customer_df.age + 1).alias("next_age")
... )
>>> 
>>> df_select_age.show(5)
+-----------+---+--------+
|customer_id|age|next_age|
+-----------+---+--------+
|          1| 44|      45|
|          2| 39|      40|
|          3| 53|      54|
|          4| 29|      30|
|          5| 46|      47|
+-----------+---+--------+
only showing top 5 rows

>>> from pyspark.sql.functions import year
>>> 
>>> df_register_year = customer_df.select(
...     "customer_id",
...     "register_date",
...     year("register_date").alias("register_year")
... )
>>> 
>>> df_register_year.show(5)
+-----------+-------------+-------------+                                       
|customer_id|register_date|register_year|
+-----------+-------------+-------------+
|          1|   2021-07-09|         2021|
|          2|   2025-02-16|         2025|
|          3|   2021-04-16|         2021|
|          4|   2017-07-06|         2017|
|          5|   2022-08-24|         2022|
+-----------+-------------+-------------+
only showing top 5 rows

>>> df_select.explain(True)
== Parsed Logical Plan ==
'Project ['customer_id, 'customer_name, 'age]
+- Relation [customer_id#0L,customer_name#1,gender#2,age#3,customer_level#4,province#5,city#6,register_date#7] parquet

== Analyzed Logical Plan ==
customer_id: bigint, customer_name: string, age: int
Project [customer_id#0L, customer_name#1, age#3]
+- Relation [customer_id#0L,customer_name#1,gender#2,age#3,customer_level#4,province#5,city#6,register_date#7] parquet

== Optimized Logical Plan ==
Project [customer_id#0L, customer_name#1, age#3]
+- Relation [customer_id#0L,customer_name#1,gender#2,age#3,customer_level#4,province#5,city#6,register_date#7] parquet

== Physical Plan ==
*(1) ColumnarToRow
+- FileScan parquet [customer_id#0L,customer_name#1,age#3] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [], ReadSchema: struct<customer_id:bigint,customer_name:string,age:int>

```

