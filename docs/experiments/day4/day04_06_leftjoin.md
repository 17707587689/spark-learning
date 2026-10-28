pyspark 与 spark sql对比
| PySpark            | Spark SQL          |
| ------------------ | ------------------ |
| `join()`           | `JOIN`             |
| `how="left"`       | `LEFT JOIN`        |
| `on="customer_id"` | `ON ...`           |
| `filter()`         | `WHERE`            |
| `groupBy()`        | `GROUP BY`         |
| `agg()`            | `SUM/COUNT/AVG...` |
| `select()`         | `SELECT`           |
