# Spark 学习路径

> 每完成一个知识点，将 `[ ]` 修改为 `[√]`。该文件是项目唯一的正式学习进度总表。

## Day01：Spark 架构与环境

- [√] 01-01 Spark 是什么
- [√] 01-02 Spark 核心组件
- [√] 01-03 Driver
- [√] 01-04 Executor
- [√] 01-05 Application
- [√] 01-06 Job / Stage / Task
- [√] 01-07 Spark 与 Hadoop / HDFS
- [√] 01-08 第一个 Spark 程序
- [√] 01-09 Day01 总结

## Day02：DataFrame 入门

- [√] 02-01 SparkSession
- [√] 02-02 创建 DataFrame
- [√] 02-03 Schema
- [√] 02-04 show
- [√] 02-05 printSchema
- [√] 02-06 select
- [√] 02-07 filter
- [√] 02-08 withColumn
- [√] 02-09 when / otherwise
- [√] 02-10 Day02 综合实验

## Day03：DataFrame CRUD

- [√] 03-01 select / alias
- [√] 03-02 drop
- [√] 03-03 withColumn
- [√] 03-04 filter / where
- [ ] 03-05 distinct
- [ ] 03-06 orderBy
- [ ] 03-07 limit
- [ ] 03-08 写入 Parquet
- [ ] 03-09 读取 Parquet
- [ ] 03-10 Day03 综合实验

## Day04：聚合与 Join

- [ ] 04-01 groupBy
- [ ] 04-02 agg
- [ ] 04-03 count / sum / avg
- [ ] 04-04 多字段聚合
- [ ] 04-05 inner join
- [ ] 04-06 left join
- [ ] 04-07 right / full join
- [ ] 04-08 多表 Join
- [ ] 04-09 Join 执行计划
- [ ] 04-10 Join 综合实验

## Day05：Spark SQL

- [ ] 05-01 createOrReplaceTempView
- [ ] 05-02 SELECT
- [ ] 05-03 WHERE
- [ ] 05-04 GROUP BY
- [ ] 05-05 HAVING
- [ ] 05-06 JOIN
- [ ] 05-07 ORDER BY
- [ ] 05-08 SQL 与 DataFrame 对应关系
- [ ] 05-09 综合实验

## Day06：窗口函数

- [ ] 06-01 Window 基础
- [ ] 06-02 partitionBy
- [ ] 06-03 orderBy
- [ ] 06-04 row_number
- [ ] 06-05 rank
- [ ] 06-06 dense_rank
- [ ] 06-07 lag
- [ ] 06-08 lead
- [ ] 06-09 窗口聚合
- [ ] 06-10 综合案例

## Day07：综合练习

- [ ] 07-01 综合数据准备
- [ ] 07-02 清洗
- [ ] 07-03 Join
- [ ] 07-04 聚合
- [ ] 07-05 Window
- [ ] 07-06 写入 Parquet
- [ ] 07-07 explain
- [ ] 07-08 综合 ETL

## Day08：Parquet、ORC、Hive

- [ ] 08-01 Parquet 是什么
- [ ] 08-02 Parquet Schema
- [ ] 08-03 Parquet 列式存储
- [ ] 08-04 Parquet 压缩
- [ ] 08-05 Spark 写 Parquet
- [ ] 08-06 Spark 读 Parquet
- [ ] 08-07 ORC
- [ ] 08-08 Parquet 与 ORC 对比
- [ ] 08-09 Hive Metastore
- [ ] 08-10 Hive Database
- [ ] 08-11 Hive Table
- [ ] 08-12 Hive External Table
- [ ] 08-13 Hive + HDFS + Spark
- [ ] 08-14 Day08 综合实验

## Day09：分区与 Shuffle

- [√] 09-01 分区 Partition
- [√] 09-02 repartition
- [√] 09-03 coalesce
- [√] 09-04 Shuffle
- [√] 09-05 GroupBy 与 Shuffle
- [√] 09-06 spark.sql.shuffle.partitions
- [√] 09-07 AQE
- [√] 09-08 AQE 执行计划
- [√] 09-09 关闭 AQE 对照实验
- [√] 09-10 Day09 总结

## Day10：Cache 与 Broadcast

- [ ] 10-01 Cache
- [ ] 10-02 persist
- [ ] 10-03 StorageLevel
- [ ] 10-04 cache 执行机制
- [ ] 10-05 cache 使用场景
- [ ] 10-06 unpersist
- [ ] 10-07 Broadcast
- [ ] 10-08 Broadcast Join
- [ ] 10-09 Shuffle Join
- [ ] 10-10 Broadcast 与 Shuffle 对比
- [ ] 10-11 综合实验

## Day11：spark-submit

- [ ] 11-01 pyspark 与 spark-submit
- [ ] 11-02 第一个 PySpark 脚本
- [ ] 11-03 spark-submit 基础
- [ ] 11-04 master
- [ ] 11-05 deploy-mode
- [ ] 11-06 --conf
- [ ] 11-07 参数传递
- [ ] 11-08 日志
- [ ] 11-09 失败排查
- [ ] 11-10 综合实验

## Day12：核心 ETL（一）

- [ ] 12-01 项目数据模型
- [ ] 12-02 ODS 数据准备
- [ ] 12-03 DIM 数据准备
- [ ] 12-04 ODS → DWD
- [ ] 12-05 DIM Join
- [ ] 12-06 DWD → DWS
- [ ] 12-07 DWS → ADS
- [ ] 12-08 ETL 脚本化
- [ ] 12-09 spark-submit
- [ ] 12-10 核心链路跑通

## Day13：核心 ETL（二）

- [ ] 13-01 ETL 参数化
- [ ] 13-02 分区处理
- [ ] 13-03 增量思路
- [ ] 13-04 数据质量检查
- [ ] 13-05 Join 优化
- [ ] 13-06 Shuffle 优化
- [ ] 13-07 Broadcast 优化
- [ ] 13-08 ETL 日志
- [ ] 13-09 失败重跑
- [ ] 13-10 完整 ETL 项目

## Day14：面试题与调优

- [ ] 14-01 Spark 架构面试题
- [ ] 14-02 DataFrame / SQL
- [ ] 14-03 Shuffle
- [ ] 14-04 AQE
- [ ] 14-05 Join 优化
- [ ] 14-06 数据倾斜
- [ ] 14-07 Cache
- [ ] 14-08 Broadcast
- [ ] 14-09 Spark 参数
- [ ] 14-10 ETL 调优
- [ ] 14-11 项目复盘
