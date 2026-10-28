```text
                    Spark SQL
                       │
                       ▼
                    Catalog
                       │
              ┌────────┴────────┐
              │                 │
       Spark 内置实现       Hive Catalog
                                  │
                                  ▼
                          Hive Metastore
```
Catalog 是 Spark SQL 的目录抽象；Hive Metastore 是其中一种提供持久化表元数据的机制。

customer_df.createOrReplaceTempView("customer")
核心作用：把一个 DataFrame 注册成当前 SparkSession 可以使用的临时 SQL 视图。

createOrReplaceTempView() 不负责读取 Hive，也不负责保存数据；它负责给一个 DataFrame 注册一个当前 SparkSession 内可供 SQL 使用的临时名称

|                  | `dim.customer` | `customer` TempView         |
| ---------------- | -------------- | --------------------------- |
| 类型               | Hive/Spark 表   | 临时视图                        |
| 是否持久             | ✅              | ❌                           |
| 是否需要 Metastore   | ✅              | 当前 Session 内由 Spark 管理      |
| 是否保存数据           | ✅              | ❌                           |
| 是否创建 HDFS 数据     | 已有实际数据         | ❌                           |
| SparkSession 结束后 | 还在             | 消失                          |
| 创建方式             | 建表/写表          | `createOrReplaceTempView()` |

| 特性               | TempView                       | GlobalTempView                         | Hive Table                           |
| ---------------- | ------------------------------ | -------------------------------------- | ------------------------------------ |
| 创建方式             | `df.createOrReplaceTempView()` | `df.createOrReplaceGlobalTempView()`   | `saveAsTable()` / SQL `CREATE TABLE` |
| 是否真正存储数据         | ❌ 不会额外保存                       | ❌ 不会额外保存                               | ✅ 通常有数据文件                            |
| 是否持久化            | ❌                              | ❌                                      | ✅                                    |
| 作用范围             | 当前 SparkSession                | 当前 Spark Application 内的所有 SparkSession | Catalog / Metastore                  |
| SQL 访问方式         | `FROM customer`                | `FROM global_temp.customer`            | `FROM dim.customer`                  |
| 是否需要数据库名         | ❌                              | 必须 `global_temp.`                      | 通常需要/建议使用 `db.table`                 |
| SparkSession 结束后 | 消失                             | 消失                                     | 仍然存在                                 |
| `SHOW TABLES`    | 能看到                            | 在 `global_temp` 下看到                    | 正常数据库下看到                             |
| 是否适合正式数仓表        | ❌                              | ❌                                      | ✅                                    |


