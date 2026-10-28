```text


========== 物理执行计划 ==========
== Physical Plan ==
AdaptiveSparkPlan (5)
+- Window (4)
   +- Sort (3)
      +- Exchange (2)
         +- Scan parquet spark_catalog.dim.customer (1)


(1) Scan parquet spark_catalog.dim.customer
Output [8]: [customer_id#0L, customer_name#1, gender#2, age#3, customer_level#4, province#5, city#6, register_date#7]
Batched: true
Location: InMemoryFileIndex [hdfs://hadoop1:9000/user/hive/warehouse/dim/customer]
ReadSchema: struct<customer_id:bigint,customer_name:string,gender:string,age:int,customer_level:string,province:string,city:string,register_date:date>

(2) Exchange
Input [8]: [customer_id#0L, customer_name#1, gender#2, age#3, customer_level#4, province#5, city#6, register_date#7]
Arguments: hashpartitioning(province#5, 200), ENSURE_REQUIREMENTS, [plan_id=71]

(3) Sort
Input [8]: [customer_id#0L, customer_name#1, gender#2, age#3, customer_level#4, province#5, city#6, register_date#7]
Arguments: [province#5 ASC NULLS FIRST, age#3 DESC NULLS LAST, customer_id#0L ASC NULLS FIRST], false, 0

(4) Window
Input [8]: [customer_id#0L, customer_name#1, gender#2, age#3, customer_level#4, province#5, city#6, register_date#7]
Arguments: [row_number() windowspecdefinition(province#5, age#3 DESC NULLS LAST, customer_id#0L ASC NULLS FIRST, specifiedwindowframe(RowFrame, unboundedpreceding$(), currentrow$())) AS row_num#25], [province#5], [age#3 DESC NULLS LAST, customer_id#0L ASC NULLS FIRST]

(5) AdaptiveSparkPlan
Output [9]: [customer_id#0L, customer_name#1, gender#2, age#3, customer_level#4, province#5, city#6, register_date#7, row_num#25]
Arguments: isFinalPlan=false
```