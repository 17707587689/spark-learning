| 执行计划关键词             | 你应该想到               |
| ------------------- | ------------------- |
| `FileScan parquet`  | 从 Parquet 读取数据      |
| `Filter`            | 过滤数据                |
| `BroadcastExchange` | 广播小表                |
| `BroadcastHashJoin` | 使用广播 Hash Join      |
| `Exchange`          | 普通 Shuffle / 数据重新分区 |

>>> spark.conf.get("spark.sql.autoBroadcastJoinThreshold")
>>> 10485760b
>>> 10,485,760 bytes
≈ 10 MB 
表示 Spark 默认允许自动广播一侧大小不超过约 10 MB 的 Join 数据。

```text
原始状态：

trade_order                 customer
Partition 0                 Partition 0
Partition 1                 Partition 1
Partition 2                 Partition 2
    │                            │
    │  两边分区方式可能不同       │
    └──────────┬─────────────────┘
               ▼
          Exchange
               │
       Hash(customer_id)
               │
               ▼
       重新分成 200 个 Partition
               │
               ▼
       相同 customer_id
       → 相同 Partition
               │
               ▼
             Sort
               │
               ▼
        SortMergeJoin
```

Join 前，两边相同 Join Key 不一定位于同一个 Partition；Exchange 会按照 Join Key 对两边数据重新分区，使相同 Join Key 的数据进入相同 Partition，从而可以进行本地 Join。