常见 StorageLevel
|存储级别|内存|磁盘|序列化|说明|
|---|---|---|---|---|
|MEMORY_ONLY|是|否|否|内存放不下的分区不会保留在缓存中，需要时重新计算|
|MEMORY_AND_DISK|是|是|否|内存放不下的分区可以存入磁盘|
|MEMORY_ONLY_SER|是|否|是|序列化后放内存，通常更省空间，但需要反序列化|
|MEMORY_AND_DISK_SER|是|是|是|序列化存储，兼顾内存和磁盘|
|DISK_ONLY|否|是|否|缓存数据只存磁盘|
|MEMORY_AND_DISK_DESER|是|是|否（反序列化存储）|PySpark DataFrame 默认持久化级别|
|OFF_HEAP|堆外内存|否|是|使用堆外内存，需要相应配置支持|

