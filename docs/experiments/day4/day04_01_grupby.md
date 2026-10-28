| DataFrame             | SQL                 |
| --------------------- | ------------------- |
| `groupBy("province")` | `GROUP BY province` |
| `count()`             | `COUNT(*)`          |
| `show()`              | 执行查询并显示结果           |


```text
一个非常重要的区别
customer_df.groupBy("province")结果是GroupedData
customer_df.groupBy("province").count()结果是DataFrame

groupBy
   ↓
定义“怎么分组”
   ↓
聚合函数
   ↓
得到结果 DataFrame
```
```text
DataFrame
   │
   ├── groupBy("province")
   │       ↓
   │    按 province 分组
   │
   ├── count()
   │       ↓
   │    计算每组数量
   │
   └── show()
           ↓
        Action
           ↓
        Job 执行
           ↓
        Shuffle
```
