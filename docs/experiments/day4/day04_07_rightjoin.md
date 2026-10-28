```text
A.join(B, how="right")
与
B.join(A, how="left")
等效

Left Join：左边是谁，就保留谁。
Right Join：右边是谁，就保留谁

Inner = A ∩ B

Left  = A ∪ (A ∩ B 中的匹配结果)
        → A 全保留

Right = B 全保留

Full  = A ∪ B

```
```text
                 两边都有？
                    │
          ┌─────────┴─────────┐
         是                   否
         │                    │
      Inner                谁必须保留？
                              │
                    ┌─────────┴─────────┐
                   左                  右
                   │                    │
                 Left                 Right

如果两边都必须保留
        ↓
      Full
```

