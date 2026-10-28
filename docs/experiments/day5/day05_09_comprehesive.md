
```python
result_df = spark.sql("""
        SELECT
            province,
            COUNT(*) AS customer_count,
            ROUND(AVG(age), 2) AS avg_age,
            MIN(age) AS min_age,
            MAX(age) AS max_age
        FROM customer
        WHERE age IS NOT NULL
        GROUP BY province
        HAVING COUNT(*) >= 5000
           AND AVG(age) >= 35
        ORDER BY customer_count DESC, avg_age DESC
```

```text
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- Sort [customer_count#58L DESC NULLS LAST, avg_age#59 DESC NULLS LAST], true, 0
   +- Exchange rangepartitioning(customer_count#58L DESC NULLS LAST, avg_age#59 DESC NULLS LAST, 200), ENSURE_REQUIREMENTS, [plan_id=143]
      +- Project [province#5, customer_count#58L, avg_age#59, min_age#60, max_age#61]
         +- Filter (isnotnull(avg(age#3)#68) AND ((customer_count#58L >= 5000) AND (avg(age#3)#68 >= 35.0)))
            +- HashAggregate(keys=[province#5], functions=[count(1), avg(age#3), min(age#3), max(age#3)], output=[province#5, customer_count#58L, avg_age#59, min_age#60, max_age#61, avg(age#3)#68])
               +- Exchange hashpartitioning(province#5, 200), ENSURE_REQUIREMENTS, [plan_id=138]
                  +- HashAggregate(keys=[province#5], functions=[partial_count(1), partial_avg(age#3), partial_min(age#3), partial_max(age#3)], output=[province#5, count#94L, sum#95, count#96L, min#97, max#98])
                     +- Filter isnotnull(age#3)
                        +- FileScan parquet spark_catalog.dim.customer[age#3,province#5] Batched: true, DataFilters: [isnotnull(age#3)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer], PartitionFilters: [], PushedFilters: [IsNotNull(age)], ReadSchema: struct<age:int,province:string>
```
- ReadSchema: struct<age:int,province:string>  列裁剪（Column Pruning）
- WHERE age IS NOT NULL -> Filter isnotnull(age) DataFilters: [isnotnull(age)] PushedFilters: [IsNotNull(age)] Predicate Pushdown（谓词下推）
- Partial HashAggregate -> 每个 Partition 本地计算
- GROUP BY -> Shuffle
- AVG 为什么看起来比较特殊 -> AVG(age) 本质上可以理解成 SUM(age) / COUNT(age)
- GROUP BY 的 Exchange 和 ORDER BY 的 Exchange 是两个完全不同的 Shuffle。
GROUP BY                ORDER BY
   ↓                        ↓
hashpartitioning        rangepartitioning
- 为什么 ORDER BY 之后还需要 Sort -> 因为Exchange只是把数据按照排序范围重新分区，后面还需要Sort真正把每个 Partition 内的数据排好。
- 完整执行计划可简单理解为
FileScan（从 Parquet 读取 age、province）
        ↓  
Filter isnotnull(age) 执行 WHERE
        ↓ 
Partial HashAggregate 每个 Partition 先局部统计
        ↓ 
Exchange hashpartitioning(province, 200)  GROUP BY province，Shuffle    
        ↓ 
Final HashAggregate 汇总每个 province 的最终 COUNT / AVG / MIN / MAX
        ↓ 
Filter  执行 HAVING
        ↓ 
Exchange rangepartitioning(...) ORDER BY 所需要的全局 Shuffle
        ↓ 
Sort  完成最终排序     

| SQL                 | Physical Plan              |
| ------------------- | -------------------------- |
| `FROM`              | `FileScan`                 |
| `WHERE`             | `Filter`                   |
| `GROUP BY`          | `HashAggregate + Exchange` |
| `COUNT/AVG/MIN/MAX` | `HashAggregate`            |
| `HAVING`            | `Filter`                   |
| `ORDER BY`          | `Exchange + Sort`          |
