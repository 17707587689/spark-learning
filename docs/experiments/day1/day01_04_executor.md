```text
Worker 是机器，Executor 是运行在机器上的进程

Executor 不等于 Task

Task 是计算任务，Executor 是执行这些任务的进程。

Executor 的生命周期
Application 启动
       │
       ▼
Driver 启动
       │
       ▼
申请集群资源
       │
       ▼
启动 Executor
       │
       ▼
Executor 注册到 Driver
       │
       ▼
Executor 等待 Task
       │
       ▼
执行 Task
       │
       ▼
汇报结果
       │
       ▼
继续执行其他 Task
       │
       ▼
Application 结束
       │
       ▼
Executor 退出

Executor 是实际访问数据并执行计算的主要角色。
Driver 通常不会把整个 HDFS 数据先读取到自己的内存里，再计算。

Executor 是 Spark 的执行角色，但在 Local 模式下，它不会按照集群模式那样表现为独立的远程 Executor 进程。

```
```python
>>> print("Spark version:",spark.version)
Spark version: 3.5.6
>>> print("Spark Master:",spark.sparkContext.master)
Spark Master: local[*]
>>> print("Application ID:", spark.sparkContext.applicationId)
Application ID: local-1787226750611
>>> print("App Name:", spark.sparkContext.appName)
App Name: PySparkShell
```

```text
customer_df = spark.read.parquet(
    "hdfs:///user/hive/warehouse/dim/customer_shuffle"
)

print("Partitions:", customer_df.rdd.getNumPartitions())

result = customer_df.groupBy("province").count()

result.show()

Shuffle 把计算拆成两个 Stage

customer_df
    │
    │ 4 partitions
    ▼
Stage 0
    │
    ├── 4 Tasks
    │
    ▼
  Shuffle
    │
    │ 200 shuffle partitions
    ▼
Stage 1
    │
    └── 200 Tasks
```
```text
Spark 最重要的一条执行链
Application
     │
     ▼
   Driver
     │
     │ 生成执行计划
     ▼
    Job
     │
     ├───────────────┐
     ▼               ▼
  Stage 0          Stage 1
     │               │
     ▼               ▼
4 Partitions    200 Shuffle Partitions
     │               │
     ▼               ▼
4 Tasks         200 Tasks
     │               │
     └───────┬───────┘
             ▼
         Executor
             │
             ▼
        执行这些 Task

Task 是 Stage 的执行单位，通常一个 Partition 对应一个 Task。
```
