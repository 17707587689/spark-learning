```text
drop() 用于删除 DataFrame 的列，并且不会修改原 DataFrame，而是返回一个新的 DataFrame
drop() 的语义可以理解为：如果这个列存在，就删除；如果不存在，就保持不变。
DataFrame 是不可变的，drop() 不会修改原 DataFrame，而是返回新的 DataFrame。
```
```python
>>> customer_df = spark.read.parquet("/user/hive/warehouse/dim/customer_shuffle")

[Stage 0:===========================================================(1 + 0) / 1]
>>> 
>>> 
>>> customer_drop_df = customer_df.drop("city")
>>> customer_drop_df.printSchema()
root
 |-- customer_id: long (nullable = true)
 |-- customer_name: string (nullable = true)
 |-- gender: string (nullable = true)
 |-- age: integer (nullable = true)
 |-- customer_level: string (nullable = true)
 |-- province: string (nullable = true)
 |-- register_date: date (nullable = true)

>>> customer_drop_df_2 = customer_drop_df.drop("city")
>>> customer_drop_df_2.printSchema()
root
 |-- customer_id: long (nullable = true)
 |-- customer_name: string (nullable = true)
 |-- gender: string (nullable = true)
 |-- age: integer (nullable = true)
 |-- customer_level: string (nullable = true)
 |-- province: string (nullable = true)
 |-- register_date: date (nullable = true)

>>> customer_drop_df2 = customer_df.drop(
...     "gender",
...     "city"
... )
>>> customer_drop_df2.printSchema
<bound method DataFrame.printSchema of DataFrame[customer_id: bigint, customer_name: string, age: int, customer_level: string, province: string, register_date: date]>
>>> customer_drop_df2.printSchema()
root
 |-- customer_id: long (nullable = true)
 |-- customer_name: string (nullable = true)
 |-- age: integer (nullable = true)
 |-- customer_level: string (nullable = true)
 |-- province: string (nullable = true)
 |-- register_date: date (nullable = true)
```