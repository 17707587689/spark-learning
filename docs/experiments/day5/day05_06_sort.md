| SQL                     | 含义               | 是否全局有序 | 是否产生 Shuffle |
| ----------------------- | ---------------- | -----: | -----------: |
| `ORDER BY`              | 全局排序             |    ✅ 是 |            ✅ |
| `SORT BY`               | 每个 Partition 内排序 |    ❌ 否 |            ✅ |
| `SORT BY` + 单 Partition | 实际上接近全局排序        |      ✅ |      取决于数据处理 |
| `ORDER BY ... LIMIT`    | 全局排序后取 Top N     |      ✅ |        通常会优化 |

ORDER BY：整个结果集有序。
SORT BY：每个 Partition 内部有序，但 Partition 与 Partition 之间不保证有序。

```text
SQL SORT BY
        ↓
每个 Partition 内排序
        ↓
DataFrame sortWithinPartitions()
```
```python
result_df = customer_df.sortWithinPartitions(
    col("age").asc()
)
```
与下面spark.sql表达的核心思想是一致的
```sql
SORT BY age
```
```text
如果我要找最大的 10 个，为什么 Spark 不需要把全部 100 万条数据完整排序？

ORDER BY age DESC
LIMIT 10
与 
ORDER BY age DESC
LIMIT 10
在 Spark 中并不一定采用完全相同的执行策略。

全局排序 ≠ 一定需要把所有数据完整排序后再取 Top N。
```
```text
ORDER BY
全局排序
    ↓
需要重新分区
    ↓
Exchange rangepartitioning
    ↓
Partition 内排序
    ↓
整个结果集有序

SORT BY
Partition 内排序
    ↓
不要求 Partition 之间有序
    ↓
不需要为了排序进行全局 Range Shuffle
    ↓
每个 Partition 自己 Sort
```
