```txt
withColumn("字段名", Column表达式)：字段不存在就新增，字段存在就替换；并且不会修改原 DataFrame。
```
```python
>>> customer_age_group_of = customer_df.withColumn("age_group",when(customer_df.age < 30,"青年").otherwise("中年"))
>>> 
>>> customer_age_group_of.show()
+-----------+-------------+------+---+--------------+--------+------+-------------+---------+
|customer_id|customer_name|gender|age|customer_level|province|  city|register_date|age_group|
+-----------+-------------+------+---+--------------+--------+------+-------------+---------+
|          1|   customer_1|     F| 44|           VIP|    北京|北京市|   2021-07-09|     中年|
|          2|   customer_2|     M| 39|          GOLD|    上海|上海市|   2025-02-16|     中年|
|          3|   customer_3|     F| 53|          GOLD|    江苏|江苏市|   2021-04-16|     中年|
>>> df2 = customer_df.withColumn("age_group",when(customer_df.age < 30,"青年").when(customer_df.age < 50,"中年").otherwise("老年"))
>>> df2.show()
+-----------+-------------+------+---+--------------+--------+------+-------------+---------+
|customer_id|customer_name|gender|age|customer_level|province|  city|register_date|age_group|
+-----------+-------------+------+---+--------------+--------+------+-------------+---------+
|          1|   customer_1|     F| 44|           VIP|    北京|北京市|   2021-07-09|     中年|
|          2|   customer_2|     M| 39|          GOLD|    上海|上海市|   2025-02-16|     中年|

```