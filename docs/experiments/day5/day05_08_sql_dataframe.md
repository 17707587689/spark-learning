DataFrame API 没有一个叫 having() 的核心 API，通常是聚合之后再 filter()。
```python
customer_df \
    .groupBy("province") \
    .agg(
        count("*").alias("customer_count")
    ) \
    .filter(
        col("customer_count") > 9000
    )
```

SQL 与 DataFrame 完整对照表

| SQL           | DataFrame API                       |
| ------------- | ----------------------------------- |
| `SELECT`      | `select()`                          |
| `WHERE`       | `filter()` / `where()`              |
| `GROUP BY`    | `groupBy()`                         |
| `COUNT`       | `count()`                           |
| `SUM`         | `sum()`                             |
| `AVG`         | `avg()`                             |
| `MIN`         | `min()`                             |
| `MAX`         | `max()`                             |
| 多个聚合          | `agg()`                             |
| `HAVING`      | 聚合后 `filter()`                      |
| `ORDER BY`    | `orderBy()`                         |
| `SORT BY`     | `sort()` / `sortWithinPartitions()` |
| `LIMIT`       | `limit()`                           |
| `DISTINCT`    | `distinct()`                        |
| `INNER JOIN`  | `join(..., "inner")`                |
| `LEFT JOIN`   | `join(..., "left")`                 |
| `RIGHT JOIN`  | `join(..., "right")`                |
| `FULL JOIN`   | `join(..., "full")`                 |
| `CASE WHEN`   | `when().otherwise()`                |
| `IS NULL`     | `isNull()`                          |
| `IS NOT NULL` | `isNotNull()`                       |
| `IN`          | `isin()`                            |
| `LIKE`        | `like()`                            |
| `AS`          | `alias()`                           |
