SparkSession 最重要的几个入口

| API                       | 用途                |
| ------------------------- | ----------------- |
| `spark.read`              | 读取数据              |
| `spark.createDataFrame()` | 创建 DataFrame      |
| `spark.sql()`             | 执行 SQL            |
| `spark.catalog`           | 管理 Catalog        |
| `spark.sparkContext`      | 获取底层 SparkContext |
| `spark.stop()`            | 停止 Spark          |

```python
>>> SparkSession
<class 'pyspark.sql.session.SparkSession'>
>>> print(spark)
<pyspark.sql.session.SparkSession object at 0x7fbce5340af0>
>>> print(type(spark))
<class 'pyspark.sql.session.SparkSession'>
>>> print("Spark version:", spark.version)
Spark version: 3.5.6
>>> print("Spark version:", spark.version)
Spark version: 3.5.6
>>> print("Master:", spark.sparkContext.master)
Master: local[*]
>>> print("App Name:", spark.sparkContext.appName)
App Name: PySparkShell
```

