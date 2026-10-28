| Spark SQL  | DataFrame API            |
| ---------- | ------------------------ |
| `SELECT`   | `.select()`              |
| `WHERE`    | `.filter()` / `.where()` |
| `ORDER BY` | `.orderBy()`             |
| `LIMIT`    | `.limit()`               |
| `GROUP BY` | `.groupBy()`             |
| `JOIN`     | `.join()`                |

- TempView 是 SQL 的入口
- spark.sql() 返回的仍然是 DataFrame
- SELECT 本质上对应 DataFrame 的 .select()
- SQL 和 DataFrame API 最终都会进入 Spark 的执行计划

```text
DataFrame API ─┐
               ├──> Logical Plan ──> Optimizer ──> Physical Plan
Spark SQL ─────┘
```