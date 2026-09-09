# dacomp-017：产品类别年度利润率与家具类问题定位

本次重放 69 条成功数据 SQL。组合方案：**C3, C4, C6, C1, C8, C2, C15, C12**。全部查询与历史结果比较通过：**True**。

数据：`customer_information` 51,289 行；`order_information` 51,289 行；`product_browsing` 51,289 行。

[原任务报告](../../reports/dsv4flash-db-first-full-01/tasks/dacomp-017.md) · [返回十题总览](../README.md)

## 先看应当怎么做

当前数据上的数据库执行与取回耗时：原始 **972.95 ms** → 组合方案 **623.57 ms**（计入构建及清理）。这是本机暖缓存小规模测量，不含模型、Python 分析和网络传输，不是整个 Agent 的加速比。

入口：[完整轨迹 SQL](trajectory.sql)；[执行与验证证据](manifest.json)。

## 每个候选如何实现

下表时间只比较该候选**通过验证的查询子集**。不同候选可能覆盖相同查询，时间或覆盖不能相加。

| 候选 | 实际保存的行数 | 验证通过/原覆盖 | 原查询 ms | 建表及索引 ms | 构建+改写 ms | 组合方案采用 |
|---|---:|---:|---:|---:|---:|---|
| [C1](#c1) | 10309 | 3/3 | 52.84 | 7.66 | 40.92 | 是，具体查询见后表 |
| [C2](#c2) | 10309 | 2/2 | 28.22 | 6.82 | 22.46 | 是，具体查询见后表 |
| [C3](#c3) | 12 | 9/9 | 298.14 | 56.50 | 56.89 | 是，具体查询见后表 |
| [C4](#c4) | 10309 | 19/19 | 187.23 | 9.58 | 132.49 | 是，具体查询见后表 |
| [C5](#c5) | 10259 | 11/13 | 122.64 | 50.13 | 114.19 | 否 |
| [C6](#c6) | 1029 | 6/6 | 26.47 | 5.16 | 8.66 | 是，具体查询见后表 |
| [C7](#c7) | 75 | 4/4 | 21.13 | 5.69 | 6.07 | 否 |
| [C8](#c8) | 1029 | 3/3 | 14.85 | 5.18 | 6.75 | 是，具体查询见后表 |
| [C9](#c9) | 15 | 2/2 | 10.28 | 5.41 | 5.51 | 否 |
| [C10](#c10) | 10309 | 3/3 | 28.08 | 6.00 | 26.48 | 否 |
| [C11](#c11) | 10309 | 6/6 | 104.44 | 9.85 | 93.02 | 否 |
| [C12](#c12) | 1027 | 2/2 | 11.10 | 5.18 | 7.37 | 是，具体查询见后表 |
| [C13](#c13) | 10309 | 3/3 | 39.38 | 10.08 | 41.68 | 否 |
| [C14](#c14) | 10309 | 2/2 | 21.85 | 10.27 | 25.06 | 否 |
| [C15](#c15) | 30 | 2/2 | 21.83 | 17.30 | 17.43 | 是，具体查询见后表 |

### C1

缓存家具类、数量有效订单的年份/产品/数量/销售/利润投影；S51、S52 复用 S50。

实现对象：`temp."reuse_017_c1"`，10309 行、5 列。

**可改写查询：** [S50](C1/S50.sql), [S51](C1/S51.sql), [S52](C1/S52.sql)。

[建表 SQL](C1/build.sql) · [通过验证的完整执行脚本](C1/approved.sql) · [清理 SQL](C1/cleanup.sql) · [逐查询验证和计时](C1/validation.json)


组合方案实际使用：S50, S51, S52；在 S50 前构建一次。

### C2

缓存家具类、数量有效订单的客户/年份/数量投影；S62 复用 S59。

实现对象：`temp."reuse_017_c2"`，10309 行、3 列。

**可改写查询：** [S59](C2/S59.sql), [S62](C2/S62.sql)。

[建表 SQL](C2/build.sql) · [通过验证的完整执行脚本](C2/approved.sql) · [清理 SQL](C2/cleanup.sql) · [逐查询验证和计时](C2/validation.json)


组合方案实际使用：S59, S62；在 S59 前构建一次。

### C3

按年份 × 产品类别保存订单数、销售额、利润、亏损和异常计数，51,289 行汇成 12 行，支持全局、年度和类别上卷。

实现对象：`temp."reuse_017_c3"`，12 行、10 列。

**可改写查询：** [S5](C3/S5.sql), [S8](C3/S8.sql), [S9](C3/S9.sql), [S10](C3/S10.sql), [S13](C3/S13.sql), [S14](C3/S14.sql), [S42](C3/S42.sql), [S57](C3/S57.sql), [S68](C3/S68.sql)。

[建表 SQL](C3/build.sql) · [通过验证的完整执行脚本](C3/approved.sql) · [清理 SQL](C3/cleanup.sql) · [逐查询验证和计时](C3/validation.json)


物化粒度：`SUBSTRING("Order Date", 1, 4)`、`"Product Category"`。

组合方案实际使用：S5, S8, S9, S10, S13, S14, S42, S57, S68；在 S5 前构建一次。

### C4

先筛出 Home & Furniture 的 10,309 行订单，多个后续诊断查询共用；保留各查询原本的分组、排序和后续条件。

实现对象：`temp."reuse_017_c4"`，10309 行、13 列。

**可改写查询：** [S17](C4/S17.sql), [S18](C4/S18.sql), [S19](C4/S19.sql), [S20](C4/S20.sql), [S21](C4/S21.sql), [S22](C4/S22.sql), [S23](C4/S23.sql), [S28](C4/S28.sql), [S29](C4/S29.sql), [S30](C4/S30.sql), [S31](C4/S31.sql), [S43](C4/S43.sql), [S44](C4/S44.sql), [S58](C4/S58.sql), [S61](C4/S61.sql), [S63](C4/S63.sql), [S69](C4/S69.sql), [S70](C4/S70.sql), [S71](C4/S71.sql)。

[建表 SQL](C4/build.sql) · [通过验证的完整执行脚本](C4/approved.sql) · [清理 SQL](C4/cleanup.sql) · [逐查询验证和计时](C4/validation.json)


组合方案实际使用：S17, S18, S19, S20, S21, S22, S23, S28, S29, S30, S31, S43, S44, S58, S61, S63, S69, S70, S71；在 S17 前构建一次。

### C5

对家具订单再按折扣、物流、年份、产品、数量、优先级、客户联合聚合，仅压成 10,259 行。S69、S70 浮点求和顺序变化导致严格比较失败，回退原 SQL。

实现对象：`temp."reuse_017_c5"`，10259 行、16 列。

**可改写查询：** [S17](C5/S17.sql), [S18](C5/S18.sql), [S19](C5/S19.sql), [S20](C5/S20.sql), [S21](C5/S21.sql), [S23](C5/S23.sql), [S29](C5/S29.sql), [S30](C5/S30.sql), [S31](C5/S31.sql), [S58](C5/S58.sql), [S61](C5/S61.sql)。

[建表 SQL](C5/build.sql) · [通过验证的完整执行脚本](C5/approved.sql) · [清理 SQL](C5/cleanup.sql) · [逐查询验证和计时](C5/validation.json)

**回退原查询：** S69, S70。不能执行这些查询对应的试验改写。

- S69：浮点末位差异；本包保留严格无序多重集比较，没有放宽标准。
- S70：浮点末位差异；本包保留严格无序多重集比较，没有放宽标准。

物化粒度：`"Discount"`、`"Shipping Method"`、`SUBSTRING("Order Date", 1, 4)`、`"Product"`、`"Quantity"`、`"Order Priority"`、`"Customer ID"`。

### C6

物化家具类 Beds 订单子集；供明细和销量/折扣/年份等分组使用。

实现对象：`temp."reuse_017_c6"`，1029 行、13 列。

**可改写查询：** [S27](C6/S27.sql), [S32](C6/S32.sql), [S33](C6/S33.sql), [S34](C6/S34.sql), [S35](C6/S35.sql), [S38](C6/S38.sql)。

[建表 SQL](C6/build.sql) · [通过验证的完整执行脚本](C6/approved.sql) · [清理 SQL](C6/cleanup.sql) · [逐查询验证和计时](C6/validation.json)


组合方案实际使用：S27, S32, S33, S34, S35, S38；在 S27 前构建一次。

### C7

将 Beds 订单按数量 × 折扣 × 年份聚合，保存数量、销售和利润状态。与 C6 有覆盖交集，按实际收益择一或分配不同查询。

实现对象：`temp."reuse_017_c7"`，75 行、6 列。

**可改写查询：** [S32](C7/S32.sql), [S34](C7/S34.sql), [S35](C7/S35.sql), [S38](C7/S38.sql)。

[建表 SQL](C7/build.sql) · [通过验证的完整执行脚本](C7/approved.sql) · [清理 SQL](C7/cleanup.sql) · [逐查询验证和计时](C7/validation.json)


物化粒度：`"Quantity"`、`"Discount"`、`SUBSTRING("Order Date", 1, 4)`。

### C8

物化家具类 Umbrellas 订单子集，供三个查询使用。

实现对象：`temp."reuse_017_c8"`，1029 行、13 列。

**可改写查询：** [S36](C8/S36.sql), [S37](C8/S37.sql), [S39](C8/S39.sql)。

[建表 SQL](C8/build.sql) · [通过验证的完整执行脚本](C8/approved.sql) · [清理 SQL](C8/cleanup.sql) · [逐查询验证和计时](C8/validation.json)


组合方案实际使用：S36, S37, S39；在 S36 前构建一次。

### C9

将 Umbrellas 订单按数量 × 年份聚合，供两条汇总查询使用。与 C8 有交集。

实现对象：`temp."reuse_017_c9"`，15 行、5 列。

**可改写查询：** [S37](C9/S37.sql), [S39](C9/S39.sql)。

[建表 SQL](C9/build.sql) · [通过验证的完整执行脚本](C9/approved.sql) · [清理 SQL](C9/cleanup.sql) · [逐查询验证和计时](C9/validation.json)


物化粒度：`"Quantity"`、`SUBSTRING("Order Date", 1, 4)`。

### C10

物化浏览表中的家具类记录；不是订单表的复用，必须独立建表。

实现对象：`temp."reuse_017_c10"`，10309 行、7 列。

**可改写查询：** [S40](C10/S40.sql), [S41](C10/S41.sql), [S64](C10/S64.sql)。

[建表 SQL](C10/build.sql) · [通过验证的完整执行脚本](C10/approved.sql) · [清理 SQL](C10/cleanup.sql) · [逐查询验证和计时](C10/validation.json)


### C11

物化家具类中数量非 NULL 且不是 abc 的订单，多个清洗后分析共用。

实现对象：`temp."reuse_017_c11"`，10309 行、13 列。

**可改写查询：** [S48](C11/S48.sql), [S50](C11/S50.sql), [S51](C11/S51.sql), [S52](C11/S52.sql), [S59](C11/S59.sql), [S62](C11/S62.sql)。

[建表 SQL](C11/build.sql) · [通过验证的完整执行脚本](C11/approved.sql) · [清理 SQL](C11/cleanup.sql) · [逐查询验证和计时](C11/validation.json)


### C12

物化家具类 Sofa Covers 订单子集。

实现对象：`temp."reuse_017_c12"`，1027 行、13 列。

**可改写查询：** [S53](C12/S53.sql), [S55](C12/S55.sql)。

[建表 SQL](C12/build.sql) · [通过验证的完整执行脚本](C12/approved.sql) · [清理 SQL](C12/cleanup.sql) · [逐查询验证和计时](C12/validation.json)


组合方案实际使用：S53, S55；在 S53 前构建一次。

### C13

物化家具类且数量、折扣有效的清洗后订单。与 C14 的条件合取项相同、顺序不同；二者是可替代方案，不应重复保存。

实现对象：`temp."reuse_017_c13"`，10309 行、13 列。

**可改写查询：** [S56](C13/S56.sql), [S60](C13/S60.sql), [S67](C13/S67.sql)。

[建表 SQL](C13/build.sql) · [通过验证的完整执行脚本](C13/approved.sql) · [清理 SQL](C13/cleanup.sql) · [逐查询验证和计时](C13/validation.json)


### C14

与 C13 是条件顺序不同的同一过滤结果；当前独立保留验证证据，组合计划避免重复部署。

实现对象：`temp."reuse_017_c14"`，10309 行、13 列。

**可改写查询：** [S65](C14/S65.sql), [S66](C14/S66.sql)。

[建表 SQL](C14/build.sql) · [通过验证的完整执行脚本](C14/approved.sql) · [清理 SQL](C14/cleanup.sql) · [逐查询验证和计时](C14/validation.json)


### C15

清洗后的家具订单按年份 × 产品汇总折扣和数量乘折扣的 SUM/COUNT，服务 S65、S66。

实现对象：`temp."reuse_017_c15"`，30 行、6 列。

**可改写查询：** [S65](C15/S65.sql), [S66](C15/S66.sql)。

[建表 SQL](C15/build.sql) · [通过验证的完整执行脚本](C15/approved.sql) · [清理 SQL](C15/cleanup.sql) · [逐查询验证和计时](C15/validation.json)


物化粒度：`SUBSTRING("Order Date", 1, 4)`、`"Product"`。

组合方案实际使用：S65, S66；在 S65 前构建一次。

## 组合后的执行顺序

只列发生改写的查询；其余成功数据 SQL 原样执行。临时表按第一次使用时构建，任务结束删除。

| SQL | 使用的临时结果 |
|---|---|
| S5 | C3 |
| S8 | C3 |
| S9 | C3 |
| S10 | C3 |
| S13 | C3 |
| S14 | C3 |
| S17 | C4 |
| S18 | C4 |
| S19 | C4 |
| S20 | C4 |
| S21 | C4 |
| S22 | C4 |
| S23 | C4 |
| S27 | C6 |
| S28 | C4 |
| S29 | C4 |
| S30 | C4 |
| S31 | C4 |
| S32 | C6 |
| S33 | C6 |
| S34 | C6 |
| S35 | C6 |
| S36 | C8 |
| S37 | C8 |
| S38 | C6 |
| S39 | C8 |
| S42 | C3 |
| S43 | C4 |
| S44 | C4 |
| S50 | C1 |
| S51 | C1 |
| S52 | C1 |
| S53 | C12 |
| S55 | C12 |
| S57 | C3 |
| S58 | C4 |
| S59 | C2 |
| S61 | C4 |
| S62 | C2 |
| S63 | C4 |
| S65 | C15 |
| S66 | C15 |
| S68 | C3 |
| S69 | C4 |
| S70 | C4 |
| S71 | C4 |

## 执行命令

在仓库根目录运行：

```bash
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/optimization-011-020/replay.py --task 17
```

若要单独检查某个候选，在命令末尾加 `--candidate C1`（按实际编号替换）。该选项只执行验证通过的子集，候选能够执行不代表推荐启用。
