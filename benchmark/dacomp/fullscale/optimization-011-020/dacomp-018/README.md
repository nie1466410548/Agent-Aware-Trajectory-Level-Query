# dacomp-018：Fashion 类增长与客户群体

本次重放 55 条成功数据 SQL。组合方案：**M1, M2**。全部查询与历史结果比较通过：**True**。

数据：`customer_information` 51,289 行；`order_information` 51,289 行；`product_browsing` 51,289 行。

[原任务报告](../../reports/dsv4flash-db-first-full-01/tasks/dacomp-018.md) · [返回十题总览](../README.md)

## 先看应当怎么做

当前数据上的数据库执行与取回耗时：原始 **7732.12 ms** → 组合方案 **6814.29 ms**（计入构建及清理）。这是本机暖缓存小规模测量，不含模型、Python 分析和网络传输，不是整个 Agent 的加速比。

入口：[完整轨迹 SQL](trajectory.sql)；[执行与验证证据](manifest.json)。

## 每个候选如何实现

下表时间只比较该候选**通过验证的查询子集**。不同候选可能覆盖相同查询，时间或覆盖不能相加。

| 候选 | 实际保存的行数 | 验证通过/原覆盖 | 原查询 ms | 建表及索引 ms | 构建+改写 ms | 组合方案采用 |
|---|---:|---:|---:|---:|---:|---|
| [C1](#c1) | 795 | 6/6 | 401.57 | 41.14 | 195.27 | 否 |
| [C2](#c2) | 795 | 8/8 | 496.51 | 23.00 | 337.49 | 否 |
| [C3](#c3) | 795 | 5/5 | 232.34 | 22.75 | 143.06 | 否 |
| [C4](#c4) | 795 | 2/2 | 121.06 | 30.27 | 90.20 | 否 |
| [C5](#c5) | 795 | 2/2 | 103.13 | 20.59 | 82.76 | 否 |
| [C6](#c6) | 795 | 11/11 | 852.68 | 29.30 | 554.20 | 否 |
| [C7](#c7) | 795 | 3/3 | 27.67 | 27.06 | 27.67 | 否 |
| [C8](#c8) | 30775 | 4/4 | 62.17 | 20.26 | 73.38 | 否 |
| [C9](#c9) | 30775 | 2/2 | 14.24 | 11.86 | 23.10 | 否 |
| [M1](#m1) | 795 | 19/19 | 1378.18 | 42.19 | 824.15 | 是，具体查询见后表 |
| [M2](#m2) | 795 | 17/17 | 995.97 | 23.47 | 628.33 | 是，具体查询见后表 |

### C1

customer_information 按客户编号去重，保留完整客户属性，后续与订单聚合做 Join。

实现对象：`temp."reuse_018_c1"`，795 行、9 列。

**可改写查询：** [S19](C1/S19.sql), [S20](C1/S20.sql), [S21](C1/S21.sql), [S22](C1/S22.sql), [S23](C1/S23.sql), [S24](C1/S24.sql)。

[建表 SQL](C1/build.sql) · [通过验证的完整执行脚本](C1/approved.sql) · [清理 SQL](C1/cleanup.sql) · [逐查询验证和计时](C1/validation.json)


### C2

Fashion 订单按客户编号汇总订单数、销售、利润；后续按客户群分析。

实现对象：`temp."reuse_018_c2"`，795 行、4 列。

**可改写查询：** [S20](C2/S20.sql), [S21](C2/S21.sql), [S22](C2/S22.sql), [S23](C2/S23.sql), [S24](C2/S24.sql), [S25](C2/S25.sql), [S27](C2/S27.sql), [S28](C2/S28.sql)。

[建表 SQL](C2/build.sql) · [通过验证的完整执行脚本](C2/approved.sql) · [清理 SQL](C2/cleanup.sql) · [逐查询验证和计时](C2/validation.json)


### C3

与 C2 计算相同，只是 sales/profit 的输出顺序不同；在 M2 中统一物化并显式投影回原顺序。

实现对象：`temp."reuse_018_c3"`，795 行、4 列。

**可改写查询：** [S34](C3/S34.sql), [S35](C3/S35.sql), [S46](C3/S46.sql), [S47](C3/S47.sql), [S58](C3/S58.sql)。

[建表 SQL](C3/build.sql) · [通过验证的完整执行脚本](C3/approved.sql) · [清理 SQL](C3/cleanup.sql) · [逐查询验证和计时](C3/validation.json)


### C4

客户去重后只取性别、客户分层，是 C1 的较窄投影；可由 M1 服务。

实现对象：`temp."reuse_018_c4"`，795 行、3 列。

**可改写查询：** [S37](C4/S37.sql), [S38](C4/S38.sql)。

[建表 SQL](C4/build.sql) · [通过验证的完整执行脚本](C4/approved.sql) · [清理 SQL](C4/cleanup.sql) · [逐查询验证和计时](C4/validation.json)


### C5

Fashion 订单按客户求利润，是 C2 的较窄输出；可由 M2 服务。

实现对象：`temp."reuse_018_c5"`，795 行、2 列。

**可改写查询：** [S37](C5/S37.sql), [S56](C5/S56.sql)。

[建表 SQL](C5/build.sql) · [通过验证的完整执行脚本](C5/approved.sql) · [清理 SQL](C5/cleanup.sql) · [逐查询验证和计时](C5/validation.json)


### C6

客户去重后只取性别，是 C1 的较窄投影；可由 M1 服务。

实现对象：`temp."reuse_018_c6"`，795 行、2 列。

**可改写查询：** [S42](C6/S42.sql), [S43](C6/S43.sql), [S45](C6/S45.sql), [S49](C6/S49.sql), [S50](C6/S50.sql), [S51](C6/S51.sql), [S52](C6/S52.sql), [S53](C6/S53.sql), [S54](C6/S54.sql), [S55](C6/S55.sql), [S57](C6/S57.sql)。

[建表 SQL](C6/build.sql) · [通过验证的完整执行脚本](C6/approved.sql) · [清理 SQL](C6/cleanup.sql) · [逐查询验证和计时](C6/validation.json)


### C7

客户表按客户编号统计源记录数，再回答人数/重复记录相关查询。不能替换为去重后的 COUNT(*)，否则会丢失原始重复次数。

实现对象：`temp."reuse_018_c7"`，795 行、2 列。

**可改写查询：** [S5](C7/S5.sql), [S13](C7/S13.sql), [S15](C7/S15.sql)。

[建表 SQL](C7/build.sql) · [通过验证的完整执行脚本](C7/approved.sql) · [清理 SQL](C7/cleanup.sql) · [逐查询验证和计时](C7/validation.json)


物化粒度：`"Customer ID"`。

### C8

物化 Fashion 订单明细子集，服务该类别明细查询。

实现对象：`temp."reuse_018_c8"`，30775 行、13 列。

**可改写查询：** [S8](C8/S8.sql), [S12](C8/S12.sql), [S26](C8/S26.sql), [S44](C8/S44.sql)。

[建表 SQL](C8/build.sql) · [通过验证的完整执行脚本](C8/approved.sql) · [清理 SQL](C8/cleanup.sql) · [逐查询验证和计时](C8/validation.json)


### C9

物化浏览表 Fashion 子集，和订单表 C8 是不同的数据源。

实现对象：`temp."reuse_018_c9"`，30775 行、7 列。

**可改写查询：** [S9](C9/S9.sql), [S30](C9/S30.sql)。

[建表 SQL](C9/build.sql) · [通过验证的完整执行脚本](C9/approved.sql) · [清理 SQL](C9/cleanup.sql) · [逐查询验证和计时](C9/validation.json)


### M1

合并 C1/C4/C6：客户去重只构建一次，795 行；按各 CTE 的原列顺序显式投影，并给 Customer ID 建普通索引。

实现对象：`temp."reuse_018_m1"`，795 行、9 列。包含客户编号索引。

**可改写查询：** [S19](M1/S19.sql), [S20](M1/S20.sql), [S21](M1/S21.sql), [S22](M1/S22.sql), [S23](M1/S23.sql), [S24](M1/S24.sql), [S37](M1/S37.sql), [S38](M1/S38.sql), [S42](M1/S42.sql), [S43](M1/S43.sql), [S45](M1/S45.sql), [S49](M1/S49.sql), [S50](M1/S50.sql), [S51](M1/S51.sql), [S52](M1/S52.sql), [S53](M1/S53.sql), [S54](M1/S54.sql), [S55](M1/S55.sql), [S57](M1/S57.sql)。

[建表 SQL](M1/build.sql) · [通过验证的完整执行脚本](M1/approved.sql) · [清理 SQL](M1/cleanup.sql) · [逐查询验证和计时](M1/validation.json)


组合方案实际使用：S19, S20, S21, S22, S23, S24, S37, S38, S42, S43, S45, S49, S50, S51, S52, S53, S54, S55, S57；在 S19 前构建一次。

### M2

合并 C2/C3/C5：Fashion 订单按客户聚合只构建一次，795 行；显式投影保持列顺序，并给 Customer ID 建普通索引。

实现对象：`temp."reuse_018_m2"`，795 行、4 列。包含客户编号索引。

**可改写查询：** [S20](M2/S20.sql), [S21](M2/S21.sql), [S22](M2/S22.sql), [S23](M2/S23.sql), [S24](M2/S24.sql), [S25](M2/S25.sql), [S27](M2/S27.sql), [S28](M2/S28.sql), [S32](M2/S32.sql), [S34](M2/S34.sql), [S35](M2/S35.sql), [S37](M2/S37.sql), [S46](M2/S46.sql), [S47](M2/S47.sql), [S48](M2/S48.sql), [S56](M2/S56.sql), [S58](M2/S58.sql)。

[建表 SQL](M2/build.sql) · [通过验证的完整执行脚本](M2/approved.sql) · [清理 SQL](M2/cleanup.sql) · [逐查询验证和计时](M2/validation.json)


组合方案实际使用：S20, S21, S22, S23, S24, S25, S27, S28, S32, S34, S35, S37, S46, S47, S48, S56, S58；在 S20 前构建一次。

## 组合后的执行顺序

只列发生改写的查询；其余成功数据 SQL 原样执行。临时表按第一次使用时构建，任务结束删除。

| SQL | 使用的临时结果 |
|---|---|
| S19 | M1 |
| S20 | M1, M2 |
| S21 | M1, M2 |
| S22 | M1, M2 |
| S23 | M1, M2 |
| S24 | M1, M2 |
| S25 | M2 |
| S27 | M2 |
| S28 | M2 |
| S32 | M2 |
| S34 | M2 |
| S35 | M2 |
| S37 | M1, M2 |
| S38 | M1 |
| S42 | M1 |
| S43 | M1 |
| S45 | M1 |
| S46 | M2 |
| S47 | M2 |
| S48 | M2 |
| S49 | M1 |
| S50 | M1 |
| S51 | M1 |
| S52 | M1 |
| S53 | M1 |
| S54 | M1 |
| S55 | M1 |
| S56 | M2 |
| S57 | M1 |
| S58 | M2 |

客户属性约束：本数据快照逐客户检查 gender、Customer Segment、age、Education Level、Marital Status、Region、Country、City，均没有属性冲突（包括 NULL/非 NULL 冲突）。原始 `GROUP BY Customer ID` 携带非分组属性只在这种约束下有明确含义；新数据若出现冲突，必须先规定选择哪条客户记录，再重新验证，不能任意用 MAX 代替。

M1 和 M2 可在同一 SQL 的不同 CTE 同时使用；组合脚本已做合并改写并验证，收益没有重复累加。

## 执行命令

在仓库根目录运行：

```bash
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/optimization-011-020/replay.py --task 18
```

若要单独检查某个候选，在命令末尾加 `--candidate C1`（按实际编号替换）。该选项只执行验证通过的子集，候选能够执行不代表推荐启用。
