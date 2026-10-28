04-05 inner join
   │
   ├── ① Join 基本概念       ← 现在
   ├── ② on 关联字段
   ├── ③ 多字段 Join
   ├── ④ 别名 alias
   ├── ⑤ 解决同名字段
   ├── ⑥ Join + filter
   ├── ⑦ Join + 聚合
   └── ⑧ explain 看 Join 执行计划

没有同名字段时，你可以通过字段名称知道来源；有同名字段时，一定要用 alias + col("别名.字段") 明确指定。

```python
o = order_df.alias("o")
c = customer_df.alias("c")

result_df = (
    o.join(
        c,
        col("o.customer_id") == col("c.customer_id"),
        "inner"
    )
    .select(
        col("o.order_id"),
        col("o.amount"),
        col("c.customer_name"),
        col("c.province")
    )
)
```