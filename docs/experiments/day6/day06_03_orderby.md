```text
Window.orderBy()
        ↓
服务于窗口函数计算

DataFrame.orderBy()
        ↓
服务于最终结果排序
```
```text
Window
  │
  ├── partitionBy()
  │       ↓
  │    数据分组
  │
  └── orderBy()
          ↓
       组内排序
          ↓
     窗口函数计算
          ↓
     row_number
     rank
     dense_rank
     lag
     lead
```

