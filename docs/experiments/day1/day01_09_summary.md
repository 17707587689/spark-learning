```text
Driver：Spark 的“大脑”
它主要负责：
创建 SparkContext / SparkSession
分析用户代码
构建计算计划
创建 Job
划分 Stage
生成 Task
调度 Task 到 Executor
监控任务执行情况
处理任务失败、重试等

Executor 主要负责：
执行 Task
处理 Partition 数据
内存缓存
Shuffle 数据
向 Driver 汇报执行状态
```
```text
                 Application
                      │
                      ▼
                   Driver
                      │
               生成 / 调度 Job
                      │
              ┌───────┴───────┐
              ▼               ▼
            Job 0           Job 1
              │
          Shuffle 划分
              │
        ┌─────┴─────┐
        ▼           ▼
     Stage 0     Stage 1
        │           │
      Tasks       Tasks
        │           │
        └─────┬─────┘
              ▼
          Executors
              │
              ▼
        处理 Partition
```
```text
Spark 一个程序是怎么运行的？
Spark 程序启动后形成一个 Application，由 Driver 负责解析和调度。遇到 Action 后会触发 Job，Job 根据 Shuffle 边界划分成多个 Stage，每个 Stage 根据 Partition 数量生成多个 Task，Task 被调度到 Executor 上执行。Executor 负责实际计算、缓存和 Shuffle 数据，并向 Driver 汇报执行状态。
```
