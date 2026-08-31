```text
用户
 ↓
提交 Spark Application
 ↓
Cluster Manager
 ↓
启动 Driver
 ↓
Driver 管理这个 Application
 ↓
Executor 执行任务
```

| 角色              | 主要职责                |
| --------------- | ------------------- |
| User            | 提交 Spark 程序         |
| Application     | 一个完整的 Spark 应用      |
| Cluster Manager | 为 Application 提供资源  |
| Driver          | 管理 Application      |
| Executor        | 执行 Application 中的任务 |

```python
>>> spark = SparkSession.builder \
...     .appName("CustomerETL") \
...     .getOrCreate()
26/08/22 12:42:49 WARN SparkSession: Using an existing Spark session; only runtime SQL configurations will take effect.
>>> 
>>> print(spark.sparkContext.appName)
PySparkShell
>>> 
>>> 
>>> print(spark.sparkContext.applicationId)
local-1787372908527
```
```text
                Spark Application
                       │
                       │
                    Driver
                       │
             ┌─────────┼─────────┐
             ↓         ↓         ↓
            Job       Job       Job
             │
           Stage
             │
           Task
             │
         Executor 执行

Application = 一个完整的 Spark 应用
Driver = Application 的“大脑”
Job = Application 中的一次计算任务
Stage = Job 根据 Shuffle 划分出来的执行阶段
Executor = 执行 Task 的计算进程
```
```text
Spark Application
       │
       └── Driver
             │
             └── SparkContext
                    │
                    └── SparkSession              
```
