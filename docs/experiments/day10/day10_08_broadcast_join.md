广播变量： 解决的是“如何让多个计算任务共享一份只读数据”。
广播 Join： 解决的是“如何让两张表进行 Join 时，尽量避免大规模数据 Shuffle”。

```python
# 广播变量
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName(
    "BroadcastVariableDemo"
).getOrCreate()

sc = spark.sparkContext

# 一份较小的客户等级字典
customer_level_dict = {
    1001: "VIP",
    1002: "普通",
    1003: "黄金",
}

# 创建广播变量
broadcast_levels = sc.broadcast(customer_level_dict)

# 模拟交易记录
transactions = [
    (1001, 100.0),
    (1002, 200.0),
    (1003, 300.0),
    (1001, 150.0),
]

# 各个 Task 可以读取广播变量中的字典
result = (
    sc.parallelize(transactions, 2)
    .map(
        lambda row: (
            row[0],
            row[1],
            broadcast_levels.value.get(row[0], "未知"),
        )
    )
    .collect()
)

for row in result:
    print(row)

spark.stop()
```
```python
# 广播join
from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast

spark = SparkSession.builder.appName(
    "BroadcastJoinDemo"
).getOrCreate()

# 较小的客户表
customer_df = spark.createDataFrame(
    [
        (1001, "张三", "VIP"),
        (1002, "李四", "普通"),
        (1003, "王五", "黄金"),
    ],
    ["customer_id", "customer_name", "customer_level"],
)

# 较大的交易表
transaction_df = spark.createDataFrame(
    [
        (101, 1001, 100.0),
        (102, 1002, 200.0),
        (103, 1001, 150.0),
        (104, 1003, 300.0),
    ],
    ["order_id", "customer_id", "amount"],
)

# 提示 Spark 将较小的客户表作为广播侧
result_df = transaction_df.join(
    broadcast(customer_df),
    on="customer_id",
    how="inner",
)

result_df.explain("formatted")
result_df.show()

spark.stop()
```

要让自定义计算任务共享一个对象，用广播变量；要让 Spark SQL 更高效地关联两张表，用广播 Join。

选择广播变量
你有一份小型规则表，需要在自定义计算代码中反复查找。
例如：根据错误代码查询错误说明、根据业务编码查询规则、根据客户编号查询一个简单映射值。
常用 API：sc.broadcast(my_dict)

选择广播 Join
你有两张 Spark DataFrame，需要按一个或多个键进行关联，并且其中一侧足够小，适合广播。
例如：用客户维表关联交易明细表，补充客户名称、客户等级、所属地区。
常用 API：transaction_df.join(broadcast(customer_df), ...)

| 对比维度 | 广播变量 `sc.broadcast()` | 广播 Join `broadcast(df)` |
|---|---|---|
| 所属 API | `SparkContext` | `pyspark.sql.functions` |
| 核心目的 | 让分布式任务共享只读数据 | 优化两张表的 Join |
| 输入 | Python 对象，例如字典、列表 | Spark DataFrame |
| 谁负责匹配 | 你编写的业务代码 | Spark SQL 执行引擎 |
| 典型用途 | 查询规则、代码映射、配置参数 | 大表与小表关联 |
| 是否自动执行 Join | 否 | 是，配合 `.join()` 执行 |
| 典型观察方式 | 查看计算代码如何读取 `.value` | `explain("formatted")` 查看物理计划 |

