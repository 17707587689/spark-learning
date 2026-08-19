# ETL 设计

## 第一阶段：核心 Spark ETL

```text
造数 → ODS → DWD → DWS → ADS
          ↑
         DIM
```

## 第二阶段：MySQL 接入

```text
MySQL → ODS
ADS → MySQL
```

## 第三阶段：调度

暂不接入。待核心 ETL 和 MySQL 链路稳定后再增加调度、重试、监控和告警。
