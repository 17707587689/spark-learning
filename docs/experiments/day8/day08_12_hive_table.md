1. Managed Table（托管表）
托管表的元数据和数据生命周期通常由 Spark Catalog / Hive Metastore 所管理的表机制共同维护。
```sql
CREATE TABLE dim.customer_managed_demo
USING PARQUET
AS
SELECT customer_id, customer_name, province
FROM dim.customer;
```
这条语句创建一张托管表，并把查询结果写入该表对应的数据位置。
```sql
DROP TABLE dim.customer_managed_demo;
```
在常见的 Spark Catalog 托管表语义下，删除表时通常也会删除该表管理的数据。

2. External Table（外部表）
外部表通常用于将已有的数据目录注册成一张表。删除表时，一般删除表的元数据，但保留外部数据文件。
```sql
CREATE TABLE dim.customer_external_demo
USING PARQUET
LOCATION 'hdfs://hadoop1:9000/user/Administrator/customer_external_demo';
```
这里需要注意：这条语句要求指定位置已经包含可读取的数据，或者你事先已经把数据写入该目录。它不会自动把 dim.customer 的数据复制到这个位置。
```sql
DROP TABLE dim.customer_external_demo;
```
通常只注销这张表，不会删除指定位置的文件。