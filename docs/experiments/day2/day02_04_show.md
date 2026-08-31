```text
一个重要误区：show(5) 并不是 limit(5)
customer_df.show(5) 意思是：展示最多 5 行。
df5 = customer_df.limit(5) 是：创建一个新的 DataFrame，只包含最多 5 行。
```
```python
>>> df_age = customer_df.filter(customer_df.age > 30)
>>> df_age.explain()
== Physical Plan ==
*(1) Filter (isnotnull(age#110) AND (age#110 > 30))
+- *(1) ColumnarToRow
   +- FileScan parquet [customer_id#107L,customer_name#108,gender#109,age#110,customer_level#111,province#112,city#113,register_date#114] Batched: true, DataFilters: [isnotnull(age#110), (age#110 > 30)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [IsNotNull(age), GreaterThan(age,30)], ReadSchema: struct<customer_id:bigint,customer_name:string,gender:string,age:int,customer_level:string,provin...


>>> customer_df.show()
+-----------+-------------+------+---+--------------+--------+------+-------------+
|customer_id|customer_name|gender|age|customer_level|province|  city|register_date|
+-----------+-------------+------+---+--------------+--------+------+-------------+
|          1|   customer_1|     F| 44|           VIP|    北京|北京市|   2021-07-09|
|          2|   customer_2|     M| 39|          GOLD|    上海|上海市|   2025-02-16|
|          3|   customer_3|     F| 53|          GOLD|    江苏|江苏市|   2021-04-16|
|          4|   customer_4|     M| 29|          GOLD|    浙江|浙江市|   2017-07-06|
|          5|   customer_5|     F| 46|        NORMAL|    四川|四川市|   2022-08-24|
|          6|   customer_6|     M| 40|        NORMAL|    湖北|湖北市|   2025-08-26|
|          7|   customer_7|     F| 60|        NORMAL|    湖南|湖南市|   2026-02-18|
|          8|   customer_8|     M| 21|        NORMAL|    福建|福建市|   2025-03-18|
|          9|   customer_9|     F| 59|        NORMAL|    山东|山东市|   2021-11-17|
|         10|  customer_10|     M| 52|           VIP|    广东|广东市|   2023-04-21|
|         11|  customer_11|     F| 37|           VIP|    北京|北京市|   2018-02-08|
|         12|  customer_12|     M| 47|          GOLD|    上海|上海市|   2018-12-05|
|         13|  customer_13|     F| 34|          GOLD|    江苏|江苏市|   2022-04-21|
|         14|  customer_14|     M| 53|          GOLD|    浙江|浙江市|   2025-08-06|
|         15|  customer_15|     F| 50|        NORMAL|    四川|四川市|   2016-11-10|
|         16|  customer_16|     M| 49|        NORMAL|    湖北|湖北市|   2019-03-21|
|         17|  customer_17|     F| 18|        NORMAL|    湖南|湖南市|   2023-04-28|
|         18|  customer_18|     M| 45|        NORMAL|    福建|福建市|   2020-08-25|
|         19|  customer_19|     F| 21|        NORMAL|    山东|山东市|   2024-05-27|
|         20|  customer_20|     M| 54|           VIP|    广东|广东市|   2019-03-31|
+-----------+-------------+------+---+--------------+--------+------+-------------+
only showing top 20 rows

>>> customer_df.show(3)
+-----------+-------------+------+---+--------------+--------+------+-------------+
|customer_id|customer_name|gender|age|customer_level|province|  city|register_date|
+-----------+-------------+------+---+--------------+--------+------+-------------+
|          1|   customer_1|     F| 44|           VIP|    北京|北京市|   2021-07-09|
|          2|   customer_2|     M| 39|          GOLD|    上海|上海市|   2025-02-16|
|          3|   customer_3|     F| 53|          GOLD|    江苏|江苏市|   2021-04-16|
+-----------+-------------+------+---+--------------+--------+------+-------------+
only showing top 3 rows

>>> customer_df.show(5,truncate=False)
+-----------+-------------+------+---+--------------+--------+------+-------------+
|customer_id|customer_name|gender|age|customer_level|province|city  |register_date|
+-----------+-------------+------+---+--------------+--------+------+-------------+
|1          |customer_1   |F     |44 |VIP           |北京    |北京市|2021-07-09   |
|2          |customer_2   |M     |39 |GOLD          |上海    |上海市|2025-02-16   |
|3          |customer_3   |F     |53 |GOLD          |江苏    |江苏市|2021-04-16   |
|4          |customer_4   |M     |29 |GOLD          |浙江    |浙江市|2017-07-06   |
|5          |customer_5   |F     |46 |NORMAL        |四川    |四川市|2022-08-24   |
+-----------+-------------+------+---+--------------+--------+------+-------------+
only showing top 5 rows

>>> customer_df.show(2,vertical=True)
-RECORD 0--------------------
 customer_id    | 1          
 customer_name  | customer_1 
 gender         | F          
 age            | 44         
 customer_level | VIP        
 province       | 北京       
 city           | 北京市     
 register_date  | 2021-07-09 
-RECORD 1--------------------
 customer_id    | 2          
 customer_name  | customer_2 
 gender         | M          
 age            | 39         
 customer_level | GOLD       
 province       | 上海       
 city           | 上海市     
 register_date  | 2025-02-16 
only showing top 2 rows

>>> df_age = customer_df.filter(customer_df.age > 30)
>>> 
>>> df_age.show()
+-----------+-------------+------+---+--------------+--------+------+-------------+
|customer_id|customer_name|gender|age|customer_level|province|  city|register_date|
+-----------+-------------+------+---+--------------+--------+------+-------------+
|          1|   customer_1|     F| 44|           VIP|    北京|北京市|   2021-07-09|
|          2|   customer_2|     M| 39|          GOLD|    上海|上海市|   2025-02-16|
|          3|   customer_3|     F| 53|          GOLD|    江苏|江苏市|   2021-04-16|
|          5|   customer_5|     F| 46|        NORMAL|    四川|四川市|   2022-08-24|
|          6|   customer_6|     M| 40|        NORMAL|    湖北|湖北市|   2025-08-26|
|          7|   customer_7|     F| 60|        NORMAL|    湖南|湖南市|   2026-02-18|
|          9|   customer_9|     F| 59|        NORMAL|    山东|山东市|   2021-11-17|
|         10|  customer_10|     M| 52|           VIP|    广东|广东市|   2023-04-21|
|         11|  customer_11|     F| 37|           VIP|    北京|北京市|   2018-02-08|
|         12|  customer_12|     M| 47|          GOLD|    上海|上海市|   2018-12-05|
|         13|  customer_13|     F| 34|          GOLD|    江苏|江苏市|   2022-04-21|
|         14|  customer_14|     M| 53|          GOLD|    浙江|浙江市|   2025-08-06|
|         15|  customer_15|     F| 50|        NORMAL|    四川|四川市|   2016-11-10|
|         16|  customer_16|     M| 49|        NORMAL|    湖北|湖北市|   2019-03-21|
|         18|  customer_18|     M| 45|        NORMAL|    福建|福建市|   2020-08-25|
|         20|  customer_20|     M| 54|           VIP|    广东|广东市|   2019-03-31|
|         21|  customer_21|     F| 38|           VIP|    北京|北京市|   2017-07-15|
|         22|  customer_22|     M| 49|          GOLD|    上海|上海市|   2022-06-27|
|         23|  customer_23|     F| 41|          GOLD|    江苏|江苏市|   2025-07-03|
|         24|  customer_24|     M| 56|          GOLD|    浙江|浙江市|   2025-10-23|
+-----------+-------------+------+---+--------------+--------+------+-------------+
only showing top 20 rows
```