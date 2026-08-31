```text
Driver 是 Spark Application 的控制与协调中心，负责创建 SparkContext/SparkSession、构建执行计划、将计算划分为 Job/Stage/Task，并协调 Executor 执行任务。

Driver
│
├── 创建 SparkContext / SparkSession
├── 分析用户代码
├── 构建执行计划
├── 生成 Job
├── 划分 Stage
├── 生成 Task
├── 调度 Task 到 Executor
├── 监控执行状态
└── 获取/处理结果

Job / Stage / Task 的划分和调度，是 Driver 的核心职责之一。

Driver 和 Executor 的关系可以进一步理解成：
                  Driver
                    │
             任务调度/协调
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
    Executor 1  Executor 2  Executor 3
        │           │           │
      Task        Task        Task
        │           │           │
        └───────────┼───────────┘
                    │
                 执行结果
                    │
                    ▼
                  Driver

Driver 主要负责控制和调度，不应该承担大规模数据计算。

Driver 的完整生命周期串起来

spark-submit
      │
      ▼
Spark Application
      │
      ▼
    Driver
      │
      ├── 创建 SparkContext
      │
      ├── 创建 SparkSession
      │
      ├── 读取/分析用户代码
      │
      ├── 构建 Logical Plan
      │
      ├── 优化执行计划
      │
      ├── 生成 Physical Plan
      │
      ├── Action 被触发
      │
      ├── 创建 Job
      │
      ├── 划分 Stage
      │
      ├── 创建 Task
      │
      ▼
Cluster Manager
      │
      ▼
分配 Executor
      │
      ├─────────────┬─────────────┐
      ▼             ▼             ▼
 Executor 1    Executor 2    Executor 3
      │             │             │
    Tasks         Tasks         Tasks
      │             │             │
      └─────────────┼─────────────┘
                    ▼
                  执行
                    │
                    ▼
                  Driver
                    │
                    ▼
                  Result

Python代码
   ↓
SparkSession
   ↓
Driver
   ↓
Logical Plan
   ↓
优化
   ↓
Physical Plan
   ↓
Action
   ↓
Job
   ↓
Stage
   ↓
Task
   ↓
Executor
   ↓
真正计算
```
