```python
from pyspark.sql.functions import when

customer_level_df = customer_df.withColumn(
    "level_code",
    when(customer_df.customer_level == "普通会员", 1)
    .when(customer_df.customer_level == "白银会员", 2)
    .when(customer_df.customer_level == "黄金会员", 3)
    .when(customer_df.customer_level == "钻石会员", 4)
    .otherwise(0)
)
```
| 省份  |   年龄 | customer_tag |
| --- | ---: | ------------ |
| 广东  | ≥ 50 | 广东重点客户       |
| 广东  | < 50 | 广东普通客户       |
| 非广东 | ≥ 50 | 外省重点客户       |
| 非广东 | < 50 | 普通客户         |
```python
df3 = customer_df.withColumn(
    "customer_tag",
    when((customer_df.province == "广东") & (customer_df.age >= 50),"广东重点客户")
    .when((customer_df.province == "广东") & (customer_df.age < 50),"广东普通客户")
    .when((customer_df.province != "广东") & (customer_df.age >= 50),"外省重点客户")
    .otherwise("普通客户")
)
>>> df3.show()
+-----------+-------------+------+---+--------------+--------+------+-------------+------------+
|customer_id|customer_name|gender|age|customer_level|province|  city|register_date|customer_tag|
+-----------+-------------+------+---+--------------+--------+------+-------------+------------+
|          1|   customer_1|     F| 44|           VIP|    北京|北京市|   2021-07-09|    普通客户|
|          2|   customer_2|     M| 39|          GOLD|    上海|上海市|   2025-02-16|    普通客户|
|          3|   customer_3|     F| 53|          GOLD|    江苏|江苏市|   2021-04-16|外省重点客户|
|          4|   customer_4|     M| 29|          GOLD|    浙江|浙江市|   2017-07-06|    普通客户|
|          5|   customer_5|     F| 46|        NORMAL|    四川|四川市|   2022-08-24|    普通客户|
|          6|   customer_6|     M| 40|        NORMAL|    湖北|湖北市|   2025-08-26|    普通客户|
|          7|   customer_7|     F| 60|        NORMAL|    湖南|湖南市|   2026-02-18|外省重点客户|
|          8|   customer_8|     M| 21|        NORMAL|    福建|福建市|   2025-03-18|    普通客户|
|          9|   customer_9|     F| 59|        NORMAL|    山东|山东市|   2021-11-17|外省重点客户|
|         10|  customer_10|     M| 52|           VIP|    广东|广东市|   2023-04-21|广东重点客户|
|         11|  customer_11|     F| 37|           VIP|    北京|北京市|   2018-02-08|    普通客户|
|         12|  customer_12|     M| 47|          GOLD|    上海|上海市|   2018-12-05|    普通客户|
|         13|  customer_13|     F| 34|          GOLD|    江苏|江苏市|   2022-04-21|    普通客户|
|         14|  customer_14|     M| 53|          GOLD|    浙江|浙江市|   2025-08-06|外省重点客户|
|         15|  customer_15|     F| 50|        NORMAL|    四川|四川市|   2016-11-10|外省重点客户|
|         16|  customer_16|     M| 49|        NORMAL|    湖北|湖北市|   2019-03-21|    普通客户|
|         17|  customer_17|     F| 18|        NORMAL|    湖南|湖南市|   2023-04-28|    普通客户|
|         18|  customer_18|     M| 45|        NORMAL|    福建|福建市|   2020-08-25|    普通客户|
|         19|  customer_19|     F| 21|        NORMAL|    山东|山东市|   2024-05-27|    普通客户|
|         20|  customer_20|     M| 54|           VIP|    广东|广东市|   2019-03-31|广东重点客户|
+-----------+-------------+------+---+--------------+--------+------+-------------+------------+
only showing top 20 rows

>>> df3.select(
...     "customer_id",
...     "province",
...     "age",
...     "customer_tag"
... ).show()
+-----------+--------+---+------------+                                         
|customer_id|province|age|customer_tag|
+-----------+--------+---+------------+
|          1|    北京| 44|    普通客户|
|          2|    上海| 39|    普通客户|
|          3|    江苏| 53|外省重点客户|
|          4|    浙江| 29|    普通客户|
|          5|    四川| 46|    普通客户|
|          6|    湖北| 40|    普通客户|
|          7|    湖南| 60|外省重点客户|
|          8|    福建| 21|    普通客户|
|          9|    山东| 59|外省重点客户|
|         10|    广东| 52|广东重点客户|
|         11|    北京| 37|    普通客户|
|         12|    上海| 47|    普通客户|
|         13|    江苏| 34|    普通客户|
|         14|    浙江| 53|外省重点客户|
|         15|    四川| 50|外省重点客户|
|         16|    湖北| 49|    普通客户|
|         17|    湖南| 18|    普通客户|
|         18|    福建| 45|    普通客户|
|         19|    山东| 21|    普通客户|
|         20|    广东| 54|广东重点客户|
+-----------+--------+---+------------+
only showing top 20 rows

>>> df3.printSchema()
root
 |-- customer_id: long (nullable = true)
 |-- customer_name: string (nullable = true)
 |-- gender: string (nullable = true)
 |-- age: integer (nullable = true)
 |-- customer_level: string (nullable = true)
 |-- province: string (nullable = true)
 |-- city: string (nullable = true)
 |-- register_date: date (nullable = true)
 |-- customer_tag: string (nullable = false)

>>> df3.explain()
== Physical Plan ==
*(1) Project [customer_id#0L, customer_name#1, gender#2, age#3, customer_level#4, province#5, city#6, register_date#7, CASE WHEN ((province#5 = 广东) AND (age#3 >= 50)) THEN 广东重点客户 WHEN ((province#5 = 广东) AND (age#3 < 50)) THEN 广东普通客户 WHEN (NOT (province#5 = 广东) AND (age#3 >= 50)) THEN 外省重点客户 ELSE 普通客户 END AS customer_tag#361]
+- *(1) ColumnarToRow
   +- FileScan parquet [customer_id#0L,customer_name#1,gender#2,age#3,customer_level#4,province#5,city#6,register_date#7] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [], ReadSchema: struct<customer_id:bigint,customer_name:string,gender:string,age:int,customer_level:string,provin...
```
