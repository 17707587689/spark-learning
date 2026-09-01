```text
distinct() 和 dropDuplicates() 的区别
distinct() 对所有列去重
dropDuplicates()可以指定列去重，如df.dropDuplicates(["id"])代表根据 id 去重，返回所有列
```
```python
# 所有不同省份
df2 = customer_df.select("province").distinct()
等价
customer_df.dropDuplicates(["province"]).select("province")
```
```python
>>> data = [
...     (1, "张三", "广东"),
...     (2, "李四", "广东"),
...     (1, "张三", "广东"),
...     (3, "王五", "北京"),
...     (2, "李四", "广东"),
...     (4, "赵六", "上海")
... ]
>>> 
>>> df = spark.createDataFrame(
...     data,
...     ["id", "name", "province"]
... )
>>> 
>>> df.count()
6                                                                               
>>> df.distinct().count()
4                                                                               
>>> df.select("province").distinct().show()
+--------+                                                                      
|province|
+--------+
|    广东|
|    北京|
|    上海|
+--------+

>>> df.distinct().explain()
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- HashAggregate(keys=[id#207L, name#208, province#209], functions=[])
   +- Exchange hashpartitioning(id#207L, name#208, province#209, 200), ENSURE_REQUIREMENTS, [plan_id=437]
      +- HashAggregate(keys=[id#207L, name#208, province#209], functions=[])
         +- Scan ExistingRDD[id#207L,name#208,province#209]

# Spark 读取原始 DataFrame → 先按照 id、name、province 做局部去重 → 通过 Shuffle 把相同的 id、name、province 发送到同一个 #Partition → 再做一次全局去重 → 得到 distinct 结果。
```
```text
                distinct()
                    │
                    ▼
             整行去重
                    │
          ┌─────────┴─────────┐
          │                   │
       所有列              指定部分列
          │                   │
   df.distinct()      df.select("province")
          │                   │
          │                distinct()
          │                   │
          ▼                   ▼
 id + name + province      province
          │                   │
          └─────────┬─────────┘
                    ▼
                 Shuffle
                    │
                 Exchange
                    │
          hashpartitioning(...)
                    │
                    ▼
              最终完成去重
```