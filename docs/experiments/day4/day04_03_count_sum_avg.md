```text
count("age") 和 count("*") 的区别
count("*") 统计行数，而 count("字段") 不统计 NULL。

sum / avg 对 NULL 的处理
假设有数据
age
---
20
30
NULL
40

sum不会把NULL当成0参与计算，结果相当20 + 30 + 40
avg对NULL的处理，结果相当于(20 + 30 + 40) / 3

```
```text
customer_df.groupBy("province").count("age")代表式有误，
因为其中的count()是DataFrameGrouped API 提供的特殊方法，它不接受字段参数。

```