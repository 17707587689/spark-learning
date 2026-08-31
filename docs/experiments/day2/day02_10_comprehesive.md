```python
from pyspark.sql.functions import col

customer_result_df = (
    customer_df
    .filter(col("age") >= 30)
    .select(
        "customer_id",
        "customer_name",
        "gender",
        "age",
        "province",
        "city"
    )
    .withColumn(
        "age_group",
        when(col("age") < 30, "青年")
        .when(col("age") < 50, "中年")
        .otherwise("老年")
    )
)
```
```text
原始 DataFrame
      │
      ▼
   filter()
      │
      │ 过滤行
      ▼
   select()
      │
      │ 选择列
      ▼
 withColumn()
      │
      │ 新增/修改列
      ▼
 when()
      │
      │ 条件判断
      ▼
 otherwise()
      │
      ▼
最终 DataFrame
```
```text
customer_df
    │
    │ filter(age >= 30)
    ▼
过滤客户
    │
    │ select(...)
    ▼
保留需要字段
    │
    │ withColumn()
    ▼
增加业务字段
    │
    │ when / otherwise
    ▼
生成业务标签
```
```text
withColumn("字段名", "固定字符串") 可以给所有行新增一个相同值的字段。
```
```python
>>> df3 = (
... customer_df
... .filter((customer_df.province == "广东省") & (customer_df.age >=50))
... .select("customer_id","customer_name","age","province","city")
... .withColumn("customer_type","广东重点客户")
... )
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
  File "/opt/miniconda3/envs/spark-env/lib/python3.10/site-packages/pyspark/sql/dataframe.py", line 5172, in withColumn
    raise PySparkTypeError(
pyspark.errors.exceptions.base.PySparkTypeError: [NOT_COLUMN] Argument `col` should be a Column, got str.
```
```text
withColumn() 的基本语法是：
withColumn("字段名", Column表达式)
第一个参数
    ↓
字段名称
    ↓
必须是字符串

第二个参数
    ↓
字段值/计算逻辑
    ↓
必须是 Column

.withColumn(
    "customer_type",       # 字符串：字段名
    "广东重点客户"          # ❌ 字符串：不是 Column
)

修改成
from pyspark.sql.functions import col, lit
...
    .withColumn(
        "customer_type",
        lit("广东重点客户")
    )
lit("广东重点客户")会把普通 Python 字符串："广东重点客户"转换成 Spark 的：Column
```
```python 
>>> df3 = (
... customer_df
... .filter((col("province") == "广东省") & (col("age") >=50))
... .select("customer_id","customer_name","age","province","city")
... .withColumn("customer_type",lit("广东重点客户"))
... )
>>> 
>>> 
>>> df3.show
<bound method DataFrame.show of DataFrame[customer_id: bigint, customer_name: string, age: int, province: string, city: string, customer_type: string]>
```
```text
1.age >= 20
2.只保留 customer_id、customer_name、gender、age、province、city
3.新增 age_group
age < 30：青年
age < 50：中年
其他：老年
4.新增 customer_type
广东省且 age≥50：广东重点客户
广东省且 age<50：广东普通客户
非广东省且 age≥50：外省重点客户
其他：普通客户
```
```python
from pyspark.sql.functions import col,lit,when

customer_df3 = (
customer_df.filter(col("age") >=20)
.select("customer_id","customer_name","gender","age","province","city")
.withColumn(
    "age_group",
	when((col("age") < 30),"青年")
	.when((col("age") < 50),"中年")
	.otherwise("老年")	
)
.withColumn(
    "customer_type",
	when(((col("province") == "广东") & (col("age") >= 50)),"广东重点客户")
	.when(((col("province") == "广东") & (col("age") < 50)),"广东普通客户")
	.when(((col("province") != "广东") & (col("age") >= 50)),"外省重点客户")
	.otherwise("普通客户")	
)
)

>>> customer_df3.explain()
== Physical Plan ==
*(1) Project [customer_id#0L, customer_name#1, gender#2, age#3, province#5, city#6, CASE WHEN (age#3 < 30) THEN 青年 WHEN (age#3 < 50) THEN 中年 ELSE 老年 END AS age_group#80, CASE WHEN ((province#5 = 广东) AND (age#3 >= 50)) THEN 广东重点客户 WHEN ((province#5 = 广东) AND (age#3 < 50)) THEN 广东普通客户 WHEN (NOT (province#5 = 广东) AND (age#3 >= 50)) THEN 外省重点客户 ELSE 普通客户 END AS customer_type#88]
+- *(1) Filter (isnotnull(age#3) AND (age#3 >= 20))
   +- *(1) ColumnarToRow
      +- FileScan parquet [customer_id#0L,customer_name#1,gender#2,age#3,province#5,city#6] Batched: true, DataFilters: [isnotnull(age#3), (age#3 >= 20)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[hdfs://hadoop1:9000/user/hive/warehouse/dim/customer_shuffle], PartitionFilters: [], PushedFilters: [IsNotNull(age), GreaterThanOrEqual(age,20)], ReadSchema: struct<customer_id:bigint,customer_name:string,gender:string,age:int,province:string,city:string>
```
