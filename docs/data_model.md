# 数据模型与主要表结构

## 1. 数据分层

本项目按照典型数仓分层进行 Spark / Hive 学习实验：

* **ODS**：原始数据层（Operational Data Store）
* **DIM**：公共维度层（Dimension）
* **DWD**：明细数据层（Data Warehouse Detail）
* **DWS**：主题汇总层（Data Warehouse Summary）
* **ADS**：应用数据层（Application Data Service）

---

## 2. 当前数据模型

```text
ODS
└── ods.trade_order
    ├── 订单 ID
    ├── 客户 ID
    ├── 订单金额
    ├── 订单日期
    └── 订单状态

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

其中，目前 Spark Day04 的聚合与 Join 实验主要使用：

```text
ods.trade_order
        │
        │ customer_id
        ▼
dim.customer
```

---

# 3. ODS 层

## 3.1 ods.trade_order

`ods.trade_order` 为当前项目的交易订单原始数据表，主要用于 Day04 聚合与 Join 实验。

当前数据规模：

```text
300,000 条
```

其中：

* `customer_id` 为 `1 ~ 100000`：可以匹配 `dim.customer`
* `customer_id` 为 `100001 ~ 110000`：故意设置为不存在的客户，用于 Join 实验

### 表结构

| 字段           | 类型     | 说明    |
| ------------ | ------ | ----- |
| order_id     | BIGINT | 订单 ID |
| customer_id  | BIGINT | 客户 ID |
| amount       | DOUBLE | 订单金额  |
| order_date   | DATE   | 订单日期  |
| order_status | STRING | 订单状态  |

### order_status

当前模拟数据包含：

* `COMPLETED`：已完成
* `PAID`：已支付
* `CANCELLED`：已取消

### 数据关系

```text
ods.trade_order
┌──────────────┐
│ order_id     │
│ customer_id  │──────────────┐
│ amount       │              │
│ order_date   │              │
│ order_status │              │
└──────────────┘              │
                              │ customer_id
                              ▼
                    ┌──────────────────┐
                    │ dim.customer     │
                    │ customer_id      │
                    │ customer_name    │
                    │ customer_level   │
                    │ province         │
                    │ city             │
                    │ ...              │
                    └──────────────────┘
```

该关系用于学习：

* Inner Join
* Left Join
* Right Join
* Full Join
* Join 后聚合
* Join + Filter
* Join + Select

---

# 4. DIM 层

## 4.1 dim.customer

`dim.customer` 为客户公共维度表。

当前实际数据规模：

```text
100,000 条
```

### 表结构

| 字段             | 类型     | 说明    |
| -------------- | ------ | ----- |
| customer_id    | BIGINT | 客户 ID |
| customer_name  | STRING | 客户名称  |
| gender         | STRING | 性别    |
| age            | INT    | 年龄    |
| customer_level | STRING | 客户等级  |
| province       | STRING | 省份    |
| city           | STRING | 城市    |
| register_date  | DATE   | 注册日期  |

### 主要用途

`dim.customer` 当前用于：

* DataFrame 基础操作
* Filter / Where
* Select
* WithColumn
* Parquet 读写
* GroupBy
* Shuffle
* AQE
* Join

其中 Day09 的 AQE / Shuffle / GroupBy 实验使用过：

```text
dim.customer_shuffle
```

---

## 4.2 dim.customer_shuffle

`dim.customer_shuffle` 是针对 Spark Shuffle / AQE 实验准备的客户实验表。

### 当前数据规模

```text
100,000 条
```

### 表结构

| 字段             | 类型     | 说明    |
| -------------- | ------ | ----- |
| customer_id    | BIGINT | 客户 ID |
| customer_name  | STRING | 客户名称  |
| gender         | STRING | 性别    |
| age            | INT    | 年龄    |
| customer_level | STRING | 客户等级  |
| province       | STRING | 省份    |
| city           | STRING | 城市    |
| register_date  | DATE   | 注册日期  |

### 主要用途

主要用于：

* GroupBy
* Shuffle
* `spark.sql.shuffle.partitions`
* Repartition
* AQE
* HashAggregate
* Exchange

例如：

```python
customer_df.groupBy("province").count()
```

可以观察：

```text
HashAggregate
    ↓
Exchange hashpartitioning(province, 200)
    ↓
HashAggregate
```

---

## 4.3 dim.product

产品公共维度表。

当前主要作为后续业务模型预留表。

典型字段包括：

```text
product_id
product_name
category_id
category_name
price
```

后续可以用于：

```text
trade_order
    ↓
product
    ↓
交易明细分析
```

---

## 4.4 dim.region

区域公共维度表。

当前主要作为后续业务模型预留表。

典型字段包括：

```text
region_id
province
city
region_name
```

后续可用于区域维度分析。

---

# 5. DWD 层

## 5.1 dwd.transaction_detail

DWD 层用于保存经过清洗、转换后的交易明细数据。

该表属于后续综合项目使用，目前主要作为目标数据模型设计。

可能的数据来源：

```text
ods.trade_order
        +
dim.customer
        +
dim.product
        +
dim.region
        ↓
dwd.transaction_detail
```

可能包含：

```text
order_id
customer_id
customer_name
customer_level
product_id
product_name
province
city
amount
order_date
order_status
```

---

# 6. DWS 层

## 6.1 dws.customer_trade_summary

DWS 层用于保存客户交易主题汇总数据。

数据来源：

```text
dwd.transaction_detail
        ↓
GROUP BY customer_id
        ↓
dws.customer_trade_summary
```

典型指标包括：

```text
customer_id
order_count
trade_amount
avg_amount
max_amount
min_amount
last_order_date
```

该表主要用于后续学习：

* 多指标聚合
* GroupBy
* Window
* 主题汇总

---

# 7. ADS 层

## 7.1 ads.customer_trade_report

ADS 层用于面向报表 / 应用提供最终数据。

数据来源：

```text
dws.customer_trade_summary
        ↓
ads.customer_trade_report
```

典型字段包括：

```text
customer_id
customer_name
customer_level
province
order_count
trade_amount
avg_amount
customer_rank
```

后续可用于综合报表和 Spark SQL 实战。

---

# 8. 当前 Day04 实验数据关系

Day04 的核心关系如下：

```text
                    customer_id
┌───────────────────────────────┐
│                               │
▼                               ▼

ods.trade_order              dim.customer
300,000 条                   100,000 条
│                             │
│ order_id                    │ customer_name
│ customer_id ────────────────┤ customer_level
│ amount                      │ province
│ order_date                  │ city
│ order_status                │ age
│                             │ ...
└─────────────────────────────┘
```

其中：

```text
约 90%
trade_order.customer_id
        ↓
能够匹配
dim.customer.customer_id
```

以及：

```text
约 10%
trade_order.customer_id
        ↓
无法匹配
dim.customer.customer_id
```

因此该数据模型可以很好地支持 Join 实验。

---

# 9. Day04 学习路径

当前 Day04：

```text
04-01 groupBy          [已完成]
04-02 agg              [已完成]
04-03 count/sum/avg    [已完成]
04-04 多字段聚合       [已完成]
04-05 inner join       [已完成]
04-06 left join        [当前]
04-07 right join       [后续]
04-08 full join        [后续]
```

当前进入：

```text
04-06 Left Join
```

核心实验：

```python
trade_order_df.join(
    customer_df,
    on="customer_id",
    how="left"
)
```

重点理解：

> **Left Join 保留左表 `ods.trade_order` 的全部数据。**

因此即使某些订单的 `customer_id` 在 `dim.customer` 中不存在，这些订单仍然会保留，只是右表的客户信息字段为 `NULL`。

---

# 10. 表命名约定

为了避免与 SQL 关键字或保留字产生歧义，本项目统一避免使用：

```text
order
transaction
```

作为实际实验表名中的优先选择。

当前订单表统一使用：

```text
ods.trade_order
```

Python DataFrame 统一建议使用：

```python
trade_order_df
```

例如：

```python
trade_order_df = spark.table("ods.trade_order")
customer_df = spark.table("dim.customer")
```

这样可以使代码和数据模型更加清晰，并减少 Hive / Spark SQL 解析问题。
