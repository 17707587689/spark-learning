```python
>>> data = [
...     (1, "张三", 30),
...     (2, "李四", 25),
...     (3, "王五", 35)
... ]
>>> 
>>> df = spark.createDataFrame(
...     data,
...     ["customer_id", "customer_name", "age"]
... )
>>> 
>>> print(type(df))
<class 'pyspark.sql.dataframe.DataFrame'>
>>> print(df.columns)
['customer_id', 'customer_name', 'age']
>>> df.show()
+-----------+-------------+---+                                                 
|customer_id|customer_name|age|
+-----------+-------------+---+
|          1|         张三| 30|
|          2|         李四| 25|
|          3|         王五| 35|
+-----------+-------------+---+

>>> 
>>> customer_df = spark.read.parquet(
...     "/user/hive/warehouse/dim/customer_shuffle"
... )
>>> 
>>> 
>>> print(type(customer_df))
<class 'pyspark.sql.dataframe.DataFrame'>
>>> print(customer_df.columns)
['customer_id', 'customer_name', 'gender', 'age', 'customer_level', 'province', 'city', 'register_date']
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
```
```python
>>> customer_df = spark.read.parquet(
...     "/user/hive/warehouse/dim/customer_shuffle"
... )
>>> customer_df.schema
StructType([StructField('customer_id', LongType(), True), StructField('customer_name', StringType(), True), StructField('gender', StringType(), True), StructField('age', IntegerType(), True), StructField('customer_level', StringType(), True), StructField('province', StringType(), True), StructField('city', StringType(), True), StructField('register_date', DateType(), True)])
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

>>> customer_df.schema.names
['customer_id', 'customer_name', 'gender', 'age', 'customer_level', 'province', 'city', 'register_date']
>>> len(customer_df.schema.fields)
8
>>> customer_df.schema.fields[0]
StructField('customer_id', LongType(), True)
```
```text
customer_df 是一个 DataFrame，它包含一个 StructType 类型的 Schema，而 StructType 中包含 8 个 StructField，每个 StructField 描述一个字段的名称、数据类型和 nullable 属性
```