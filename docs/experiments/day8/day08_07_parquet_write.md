1. repartition(n)

重新调整 DataFrame 的分区数，通常会触发 Shuffle（数据重新分布）。

适合需要增加并行度、重新均衡数据的场景，也可以减少分区。

2. coalesce(n)

通常用于减少分区，尽量避免完整 Shuffle。

适合数据经过过滤、数量减少后，想减少输出文件的场景。但可能导致分区数据不均衡。

3. Parquet 输出文件

普通的 Parquet 写入中，一个执行写入的 Spark 分区通常会生成一个数据文件。
因此，写入前的分区数通常会影响文件数量，但并非所有情况下都严格一一对应。

|对比项|repartition(n)	|coalesce(n)|
|---|---|---|
|调整分区数量|可以增加或减少|主要用于减少|
|通常是否触发Shuffle|是|否，通常避免完整 Shuffle|
|数据分布|可以重新分配数据|可能不均衡|
|适用场景|重新均衡数据、增加并行度|减少分区、控制输出文件数量|

df.rdd.getNumPartitions() 得到的是这个 DataFrame 转换为 RDD 后对应的 Spark 执行分区数。它不是指 DataFrame 按哪个业务字段分区，也不是指 Parquet 的目录分区数。

