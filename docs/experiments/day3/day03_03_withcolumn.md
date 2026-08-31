```text 
withColumn() = 基于 Column 表达式，生成一个新的 DataFrame；字段不存在就新增，字段存在就替换。
```
```python
>>> from pyspark.sql.functions import lit
>>> 
>>> df1 = customer_df.withColumn(
...     "source",
...     lit("customer")
... )

>>> 
>>> df1.printSchema()
root
 |-- customer_id: long (nullable = true)
 |-- customer_name: string (nullable = true)
 |-- gender: string (nullable = true)
 |-- age: integer (nullable = true)
 |-- customer_level: string (nullable = true)
 |-- province: string (nullable = true)
 |-- city: string (nullable = true)
 |-- register_date: date (nullable = true)
 |-- source: string (nullable = false)

>>> df2 = customer_df.withColumn(
...     "age_plus_10",
...     customer_df.age + 10
... )
>>> 
>>> df2.select(
...     "customer_id",
...     "age",
...     "age_plus_10"
... ).show()

+-----------+---+-----------+                                                   
|customer_id|age|age_plus_10|
+-----------+---+-----------+
|          1| 44|         54|
|          2| 39|         49|
|          3| 53|         63|
|          4| 29|         39|
```
