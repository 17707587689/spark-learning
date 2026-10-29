Broadcast 与 cache / persist 的区别
|对比项|cache() / persist()|broadcast()|
|---|---|---|
|主要目的|缓存计算结果，方便复用|分发共享的只读数据|
|典型对象|DataFrame、RDD|Python 对象等可序列化数据|
|典型场景|多次查询同一份客户数据|多个 Task 查询同一份小型映射表|
|是否改变业务数据|不改变数据内容|不允许通过广播变量修改共享值|
|清理方式|unpersist()|unpersist() 或 destroy()|

cache/persist：计算过的数据，留着以后复用。
broadcast：需要共享的数据，分发出去供多个任务读取。

Broadcast 变量和 Broadcast Join 不是同一个概念。
- 广播变量：通过 sc.broadcast() 创建，在任务代码中通过 .value 读取。
- 广播 Join：Spark SQL 在连接两个表时，可以把较小的一侧广播到各个 Executor，减少大规模 Shuffle。
通常使用 broadcast() 函数或相关 SQL 提示。

Spark 广播变量不应简单理解为“发送给所有计算节点”。
更准确地说，广播数据会在需要使用它的 Executor 上提供副本，而不是保证集群中每个节点都保存一份。

广播变量提供面向分布式任务的共享只读数据访问机制，但不意味着每台服务器、每个 Executor、每个 Task 都必然各自保存一份数据。