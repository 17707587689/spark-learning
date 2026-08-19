# Spark Learning Project

一个用于 **Spark 学习 + 数据工程实践** 的可复现项目。

## 项目目标

按照“先 Spark 核心 → 核心 ETL → MySQL 接入 → 调度”的顺序逐步演进。
当前阶段暂不接入调度，优先把 Spark 核心能力和 ODS → DWD → DWS → ADS 核心链路跑通。

## 文档

- [项目架构](docs/architecture.md)
- [工程目录](docs/directory.md)
- [数据模型](docs/data_model.md)
- [ETL 设计](docs/etl_design.md)
- [Spark 学习路径](docs/learning_path.md)
- [开发规范](docs/development_guide.md)
- [常用 Linux 命令](commands/linux.md)
- [常用 HDFS 命令](commands/hdfs.md)
- [常用 Hive 命令](commands/hive.md)
- [常用 Spark 命令](commands/spark.md)
- [问题排查](commands/troubleshooting.md)

## 当前进度

当前学习节点：**Day09-07：关闭 AQE 对照实验**。

## 基本原则

1. 所有造数脚本进入 `scripts/generate/`。
2. 常用命令进入 `commands/`。
3. 表结构进入 `docs/data_model.md` 和 `sql/ddl/`。
4. Spark 学习进度统一维护在 `docs/learning_path.md`。
5. 每个重要实验可在 `docs/experiments/` 留下记录。
6. 暂不接入调度。
