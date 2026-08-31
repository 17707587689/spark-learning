```text
在 Spark 中，DataFrame 最常见的来源有三类：
                    DataFrame
                       ▲
          ┌────────────┼────────────┐
          │            │            │
          │            │            │
 createDataFrame     read       spark.sql
          │            │            │
       内存数据      文件/表       SQL结果
```
