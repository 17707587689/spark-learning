| 知识点          | 记忆                     |
| ------------ | -------------------------- |
| 读取 Parquet   | spark.read.parquet(path)|
| 读取目录         | 可以直接指定 Parquet 目录  |
| Schema       | Parquet 自带 Schema          |
| 列裁剪          | Column Pruning            |
| 谓词下推         | Predicate Pushdown        |
| 物理读取         | FileScan parquet        |
| Spark 常用存储格式 | Parquet                  |

CSV 更像“文本文件”，Parquet 是“带 Schema 的列式数据文件”，Spark 读取 Parquet 时可以利用列裁剪、谓词下推等机制提高性能。

