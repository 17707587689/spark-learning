```python
#  年龄最大的10个人
customer_df \
    .orderBy(col("age").desc()) \
    .limit(10) \
    .show()

# 年龄最小的10个客户
customer_df \
    .orderBy(col("age")) \
    .limit(10) \
    .show()

# 年龄最大的10个客户，而且年龄必须 ≥ 50
customer_df \
    .filter(col("age") >= 50) \
    .orderBy(col("age").desc()) \
    .limit(10) \
    .show()
```
```text
limit() 与 show(n) 的区别
customer_df.show(10) 展示最多 10 行，它是 DataFrame 的显示动作
customer_df.limit(10) 真正创建一个最多包含 10 行的新 DataFrame

df.orderBy(col("age").desc()).limit(10)是Spark DataFrame 中非常典型的 Top-N 写法
```
| 写法                                        | 含义           |
| ----------------------------------------- | ------------ |
| `df.limit(10)`                            | 最多取10行       |
| `df.show(10)`                             | 显示最多10行      |
| `df.orderBy("age").limit(10)`             | 年龄最小的10人     |
| `df.orderBy(col("age").desc()).limit(10)` | 年龄最大的10人     |
| `df.filter(...).limit(10)`                | 满足条件的数据中取10行 |
| `df.select(...).limit(10)`                | 选择列后取10行     |


customer_df.orderBy(col("age").desc()).limit(10).show()