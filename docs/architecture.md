# 项目架构

## 1. 总体链路

```text
MySQL → ODS → DWD → DWS → ADS → MySQL
             ↑
            DIM
```

MySQL 接入属于后续阶段；当前先使用造数脚本和 HDFS/Hive 数据完成 Spark 核心 ETL。

## 2. 当前阶段

```text
造数脚本 → HDFS / Hive → Spark ETL → ODS → DWD → DWS → ADS
```

## 3. 技术栈

- Python 3.10.x
- PySpark 3.5.6
- Hadoop / HDFS
- Hive Metastore
- Parquet
- MySQL（后续接入）

## 4. 演进原则

先掌握 Spark，再完成核心 ETL；核心 ETL 稳定后再接 MySQL；最后再引入调度。
