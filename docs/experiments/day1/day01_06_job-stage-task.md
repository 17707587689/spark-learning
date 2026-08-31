```text
Application
    │
    │ 一个 Application
    ▼
  Driver
    │
    │ Action 触发
    ▼
   Job
    │
    │ 根据 Shuffle 划分
    ▼
  Stage
    │
    │ 一个 Stage 拆成多个 Task
    ▼
  Task
    │
    │ Task 在 Executor 上执行
    ▼
 Executor

 最核心的一句话：
 Job 是一次 Action 触发的计算任务，Stage 是 Job 根据 Shuffle 划分出来的执行阶段，Task 是 Stage 中针对每个 Partition 的实际计算单元。
```
| 概念          | 含义                        |
| ----------- | ------------------------- |
| Application | 整个 Spark 应用               |
| Driver      | 管理和协调应用                   |
| Executor    | 执行计算的进程                   |
| Job         | 一次 Action 触发的计算           |
| Stage       | Job 中的一个执行阶段              |
| Task        | Stage 中针对一个 Partition 的计算 |
```text
Application
    ↓
多个 Job
    ↓
每个 Job 多个 Stage
    ↓
每个 Stage 多个 Task
    ↓
Task 在 Executor 上执行

例如
Application
│
├── Job 0
│    │
│    ├── Stage 0
│    │    ├── Task 0
│    │    ├── Task 1
│    │    ├── Task 2
│    │    └── Task 3
│    │
│    └── Stage 1
│         ├── Task 0
│         ├── Task 1
│         └── ...
│
└── Job 1
     │
     └── Stage 0
          ├── Task 0
          └── ...

注意：

Job、Stage、Task 都不是 Executor。

Executor 是运行这些 Task 的地方。
```
```text
                 Application
                      │
                      ▼
                    Driver
                      │
                Action 触发
                      │
                      ▼
                     Job
                      │
               根据 Shuffle 划分
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
       Stage 0                 Stage 1
          │                       │
      Partitions              Partitions
          │                       │
        Tasks                   Tasks
          │                       │
          └───────────┬───────────┘
                      ▼
                  Executor

Action 产生 Job，Shuffle 划分 Stage，Partition 决定 Task，Executor 执行 Task。
```

