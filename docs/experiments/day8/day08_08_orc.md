ORC 与 Parquet 的区别
|对比项	|Parquet	|ORC|
|---|---|---|
|存储方式	|列式存储	|列式存储|
|典型应用	|Spark、数据湖、多种分析引擎	|Hive 数据仓库，也支持 Spark|
|内部组织	|Row Group、Column Chunk、Page	|Stripe、列数据流、索引、Footer|
|Schema	|文件元数据记录 Schema|	文件元数据记录 Schema|
|压缩	|支持多种压缩算法|	支持多种压缩算法|
|分区能力|	通常由目录结构实现|	同样通常由目录结构实现|