|对比项|Shuffle Join|Broadcast Join|
|---|---|---|
|核心方式|重新分配数据|将较小一侧广播给各个需要参与的执行端|
|大表是否通常需要 Shuffle|两侧通常都需要重新分区（以 Sort Merge Join 为例）|大表通常不需要因该 Join 重新分区|
|网络开销|可能较大，取决于数据量|需要传输被广播的数据|
|内存压力|Shuffle、排序和 Join 仍可能占用资源|广播侧需要占用内存等执行资源|
|常见适用场景|两侧都比较大|一侧较小、适合广播|
|典型物理算子|SortMergeJoin|BroadcastHashJoin|