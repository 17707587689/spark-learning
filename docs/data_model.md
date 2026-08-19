# 数据模型与主要表结构

## 1. 分层

- ODS：原始数据层
- DIM：公共维度层
- DWD：明细数据层
- DWS：主题汇总层
- ADS：应用数据层

## 2. 主要表

```text
ODS
├── ods.customer
└── ods.transaction

DIM
├── dim.customer
├── dim.product
└── dim.region

DWD
└── dwd.transaction_detail

DWS
└── dws.customer_trade_summary

ADS
└── ads.customer_trade_report
```

## 3. 当前实验表：dim.customer_shuffle

| 字段 | 类型 | 说明 |
|---|---|---|
| customer_id | BIGINT | 客户 ID |
| customer_name | STRING | 客户名称 |
| gender | STRING | 性别 |
| age | INT | 年龄 |
| customer_level | STRING | 客户等级 |
| province | STRING | 省份 |
| city | STRING | 城市 |
| register_date | DATE | 注册日期 |

当前 AQE / Shuffle / GroupBy 实验使用该表。
