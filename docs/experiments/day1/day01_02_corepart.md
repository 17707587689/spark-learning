```text
一个 Spark 应用运行起来，最核心的是这几个角色
                    Spark Application
                           │
                           ▼
                       ┌───────┐
                       │Driver │
                       └───┬───┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
         Executor 1   Executor 2   Executor 3
              │            │            │
           Task          Task          Task
           Task          Task          Task

另外还有一个负责管理集群资源的角色：

                  Cluster Manager
                 /       |       \
                /        |        \
               ▼         ▼         ▼
          Executor    Executor    Executor

Driver 可以理解成：Spark 应用的大脑。

你的 Spark 程序
      │
      ▼
    Driver
      │
      ├── 分析代码
      ├── 生成执行计划
      ├── 划分 Job
      ├── 划分 Stage
      ├── 生成 Task
      └── 调度 Executor 执行

                    Application
                         │
                         ▼
                      Driver
                    /    │    \
                   /     │     \
                  ▼      ▼      ▼
             Job/Stage/Task 调度
                         │
                         ▼
                Cluster Manager
                         │
              分配计算资源
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Executor 1     Executor 2     Executor 3
          │              │              │
        Tasks          Tasks          Tasks
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                       Result

Driver
  │
  ├──── Task 1 ────> Executor 1
  │
  ├──── Task 2 ────> Executor 2
  │
  ├──── Task 3 ────> Executor 3
  │
  └──── Task 4 ────> Executor 1
```