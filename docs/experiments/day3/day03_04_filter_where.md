```python
>>> customer_filter_df = customer_df.filter(
...     col("age") > 50
... )
>>> 
>>> customer_filter_df.show()
+-----------+-------------+------+---+--------------+--------+------+-------------+
|customer_id|customer_name|gender|age|customer_level|province|  city|register_date|
+-----------+-------------+------+---+--------------+--------+------+-------------+
|          3|   customer_3|     F| 53|          GOLD|    江苏|江苏市|   2021-04-16|
|          7|   customer_7|     F| 60|        NORMAL|    湖南|湖南市|   2026-02-18|
|          9|   customer_9|     F| 59|        NORMAL|    山东|山东市|   2021-11-17|
|         10|  customer_10|     M| 52|           VIP|    广东|广东市|   2023-04-21|
|         14|  customer_14|     M| 53|          GOLD|    浙江|浙江市|   2025-08-06|
|         20|  customer_20|     M| 54|           VIP|    广东|广东市|   2019-03-31|
|         24|  customer_24|     M| 56|          GOLD|    浙江|浙江市|   2025-10-23|
|         30|  customer_30|     M| 53|           VIP|    广东|广东市|   2018-05-09|
|         33|  customer_33|     F| 52|          GOLD|    江苏|江苏市|   2025-03-08|
|         35|  customer_35|     F| 51|        NORMAL|    四川|四川市|   2018-01-16|
|         36|  customer_36|     M| 55|        NORMAL|    湖北|湖北市|   2017-05-14|
|         43|  customer_43|     F| 51|          GOLD|    江苏|江苏市|   2021-05-11|
|         46|  customer_46|     M| 53|        NORMAL|    湖北|湖北市|   2023-02-06|
|         47|  customer_47|     F| 55|        NORMAL|    湖南|湖南市|   2020-01-17|
|         48|  customer_48|     M| 60|        NORMAL|    福建|福建市|   2025-05-28|
|         50|  customer_50|     M| 56|           VIP|    广东|广东市|   2025-12-22|
|         52|  customer_52|     M| 55|          GOLD|    上海|上海市|   2022-02-03|
|         56|  customer_56|     M| 58|        NORMAL|    湖北|湖北市|   2020-05-14|
|         63|  customer_63|     F| 56|          GOLD|    江苏|江苏市|   2019-05-12|
|         65|  customer_65|     F| 51|        NORMAL|    四川|四川市|   2021-06-17|
+-----------+-------------+------+---+--------------+--------+------+-------------+
only showing top 20 rows

>>> customer_filter_df2 = customer_df.filter(
...     (col("province") == "广东") &
...     (col("age") > 50)
... )
>>> 
>>> customer_filter_df2.show()
+-----------+-------------+------+---+--------------+--------+------+-------------+
|customer_id|customer_name|gender|age|customer_level|province|  city|register_date|
+-----------+-------------+------+---+--------------+--------+------+-------------+
|         10|  customer_10|     M| 52|           VIP|    广东|广东市|   2023-04-21|
|         20|  customer_20|     M| 54|           VIP|    广东|广东市|   2019-03-31|
|         30|  customer_30|     M| 53|           VIP|    广东|广东市|   2018-05-09|
|         50|  customer_50|     M| 56|           VIP|    广东|广东市|   2025-12-22|
|         70|  customer_70|     M| 56|           VIP|    广东|广东市|   2019-01-09|
|        130| customer_130|     M| 57|           VIP|    广东|广东市|   2020-11-30|
|        190| customer_190|     M| 57|           VIP|    广东|广东市|   2026-06-10|
|        220| customer_220|     M| 58|           VIP|    广东|广东市|   2017-09-13|
|        410| customer_410|     M| 54|           VIP|    广东|广东市|   2018-05-13|
|        480| customer_480|     M| 53|           VIP|    广东|广东市|   2023-09-02|
|        490| customer_490|     M| 54|           VIP|    广东|广东市|   2018-01-11|
|        520| customer_520|     M| 51|           VIP|    广东|广东市|   2020-12-10|
|        630| customer_630|     M| 52|           VIP|    广东|广东市|   2020-07-05|
|        660| customer_660|     M| 56|           VIP|    广东|广东市|   2023-06-25|
|        790| customer_790|     M| 59|           VIP|    广东|广东市|   2022-08-11|
|        840| customer_840|     M| 56|           VIP|    广东|广东市|   2018-04-17|
|        850| customer_850|     M| 60|           VIP|    广东|广东市|   2026-07-28|
|       1000|customer_1000|     M| 57|           VIP|    广东|广东市|   2019-06-25|
|       1040|customer_1040|     M| 56|           VIP|    广东|广东市|   2019-01-06|
|       1080|customer_1080|     M| 57|           VIP|    广东|广东市|   2026-02-07|
+-----------+-------------+------+---+--------------+--------+------+-------------+
only showing top 20 rows

>>> customer_filter_df3 = customer_df.filter(
...     (col("province") == "广东") |
...     (col("age") > 50)
... )
>>> 
>>> customer_filter_df3.show()
+-----------+-------------+------+---+--------------+--------+------+-------------+
|customer_id|customer_name|gender|age|customer_level|province|  city|register_date|
+-----------+-------------+------+---+--------------+--------+------+-------------+
|          3|   customer_3|     F| 53|          GOLD|    江苏|江苏市|   2021-04-16|
|          7|   customer_7|     F| 60|        NORMAL|    湖南|湖南市|   2026-02-18|
|          9|   customer_9|     F| 59|        NORMAL|    山东|山东市|   2021-11-17|
|         10|  customer_10|     M| 52|           VIP|    广东|广东市|   2023-04-21|
|         14|  customer_14|     M| 53|          GOLD|    浙江|浙江市|   2025-08-06|
|         20|  customer_20|     M| 54|           VIP|    广东|广东市|   2019-03-31|
|         24|  customer_24|     M| 56|          GOLD|    浙江|浙江市|   2025-10-23|
|         30|  customer_30|     M| 53|           VIP|    广东|广东市|   2018-05-09|
|         33|  customer_33|     F| 52|          GOLD|    江苏|江苏市|   2025-03-08|
|         35|  customer_35|     F| 51|        NORMAL|    四川|四川市|   2018-01-16|
|         36|  customer_36|     M| 55|        NORMAL|    湖北|湖北市|   2017-05-14|
|         40|  customer_40|     M| 49|           VIP|    广东|广东市|   2021-08-03|
|         43|  customer_43|     F| 51|          GOLD|    江苏|江苏市|   2021-05-11|
|         46|  customer_46|     M| 53|        NORMAL|    湖北|湖北市|   2023-02-06|
|         47|  customer_47|     F| 55|        NORMAL|    湖南|湖南市|   2020-01-17|
|         48|  customer_48|     M| 60|        NORMAL|    福建|福建市|   2025-05-28|
|         50|  customer_50|     M| 56|           VIP|    广东|广东市|   2025-12-22|
|         52|  customer_52|     M| 55|          GOLD|    上海|上海市|   2022-02-03|
|         56|  customer_56|     M| 58|        NORMAL|    湖北|湖北市|   2020-05-14|
|         60|  customer_60|     M| 41|           VIP|    广东|广东市|   2017-12-21|
+-----------+-------------+------+---+--------------+--------+------+-------------+
only showing top 20 rows

>>> customer_where_df = customer_df.where(
...     "province = '广东' AND age > 50"
... )
>>> 
>>> customer_where_df.show()
+-----------+-------------+------+---+--------------+--------+------+-------------+
|customer_id|customer_name|gender|age|customer_level|province|  city|register_date|
+-----------+-------------+------+---+--------------+--------+------+-------------+
|         10|  customer_10|     M| 52|           VIP|    广东|广东市|   2023-04-21|
|         20|  customer_20|     M| 54|           VIP|    广东|广东市|   2019-03-31|
|         30|  customer_30|     M| 53|           VIP|    广东|广东市|   2018-05-09|
|         50|  customer_50|     M| 56|           VIP|    广东|广东市|   2025-12-22|
|         70|  customer_70|     M| 56|           VIP|    广东|广东市|   2019-01-09|
|        130| customer_130|     M| 57|           VIP|    广东|广东市|   2020-11-30|
|        190| customer_190|     M| 57|           VIP|    广东|广东市|   2026-06-10|
|        220| customer_220|     M| 58|           VIP|    广东|广东市|   2017-09-13|
|        410| customer_410|     M| 54|           VIP|    广东|广东市|   2018-05-13|
|        480| customer_480|     M| 53|           VIP|    广东|广东市|   2023-09-02|
|        490| customer_490|     M| 54|           VIP|    广东|广东市|   2018-01-11|
|        520| customer_520|     M| 51|           VIP|    广东|广东市|   2020-12-10|
|        630| customer_630|     M| 52|           VIP|    广东|广东市|   2020-07-05|
|        660| customer_660|     M| 56|           VIP|    广东|广东市|   2023-06-25|
|        790| customer_790|     M| 59|           VIP|    广东|广东市|   2022-08-11|
|        840| customer_840|     M| 56|           VIP|    广东|广东市|   2018-04-17|
|        850| customer_850|     M| 60|           VIP|    广东|广东市|   2026-07-28|
|       1000|customer_1000|     M| 57|           VIP|    广东|广东市|   2019-06-25|
|       1040|customer_1040|     M| 56|           VIP|    广东|广东市|   2019-01-06|
|       1080|customer_1080|     M| 57|           VIP|    广东|广东市|   2026-02-07|
+-----------+-------------+------+---+--------------+--------+------+-------------+
only showing top 20 rows

>>> customer_where_df = customer_df.where(
...     "province = '广东' AND age > 50"
... )
>>> customer_filter_df2.explain()
== Physical Plan ==
*(1) Filter (((isnotnull(province#5) AND isnotnull(age#3)) AND (province#5 = 广东)) AND (age#3 > 50))
+- *(1) ColumnarToRow
   +- FileScan parquet [customer_id#0L,customer_name#1,gender#2,age#3,customer_level#4,province#5,city#6,register_date#7] Batched: true, DataFilters: [isnotnull(province#5), isnotnull(age#3), (province#5 = 广东), (age#3 > 50)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [IsNotNull(province), IsNotNull(age), EqualTo(province,广东), GreaterThan(age,50)], ReadSchema: struct<customer_id:bigint,customer_name:string,gender:string,age:int,customer_level:string,provin...


>>> customer_where_df.explain()
== Physical Plan ==
*(1) Filter (((isnotnull(province#5) AND isnotnull(age#3)) AND (province#5 = 广东)) AND (age#3 > 50))
+- *(1) ColumnarToRow
   +- FileScan parquet [customer_id#0L,customer_name#1,gender#2,age#3,customer_level#4,province#5,city#6,register_date#7] Batched: true, DataFilters: [isnotnull(province#5), isnotnull(age#3), (province#5 = 广东), (age#3 > 50)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [IsNotNull(province), IsNotNull(age), EqualTo(province,广东), GreaterThan(age,50)], ReadSchema: struct<customer_id:bigint,customer_name:string,gender:string,age:int,customer_level:string,provin...
```
```python
# DataFrame 风格
df.filter(
    (col("province") == "广东") &
    (col("age") > 50)
)
# 等价于
# SQL 风格
df.where(
    "province = '广东' AND age > 50"
)
```
