# dacomp-019：药品库存积压、断供与质量风险

本次重放 38 条成功数据 SQL。组合方案：**C1**。全部查询与历史结果比较通过：**True**。

数据：`basic_drug_information` 427 行；`inventory_management` 428 行；`pricing_system` 428 行。

[原任务报告](../../reports/dsv4flash-db-first-full-01/tasks/dacomp-019.md) · [返回十题总览](../README.md)

## 先看应当怎么做

当前数据上的数据库执行与取回耗时：原始 **24.96 ms** → 组合方案 **23.71 ms**（计入构建及清理）。这是本机暖缓存小规模测量，不含模型、Python 分析和网络传输，不是整个 Agent 的加速比。

入口：[完整轨迹 SQL](trajectory.sql)；[执行与验证证据](manifest.json)。

## 每个候选如何实现

下表时间只比较该候选**通过验证的查询子集**。不同候选可能覆盖相同查询，时间或覆盖不能相加。

| 候选 | 实际保存的行数 | 验证通过/原覆盖 | 原查询 ms | 建表及索引 ms | 构建+改写 ms | 组合方案采用 |
|---|---:|---:|---:|---:|---:|---|
| [C1](#c1) | 264 | 4/4 | 8.41 | 2.17 | 7.09 | 是，具体查询见后表 |
| [C2](#c2) | 36 | 4/4 | 0.63 | 0.49 | 0.61 | 否 |
| [C3](#c3) | 401 | 4/4 | 0.71 | 1.33 | 1.99 | 否 |

### C1

缓存 S31 的多表 Join 结果（264 行），S32—S34 读取同一结果，保留原结果顺序。

实现对象：`temp."reuse_019_c1"`，264 行、24 列。

**可改写查询：** [S31](C1/S31.sql), [S32](C1/S32.sql), [S33](C1/S33.sql), [S34](C1/S34.sql)。

[建表 SQL](C1/build.sql) · [通过验证的完整执行脚本](C1/approved.sql) · [清理 SQL](C1/cleanup.sql) · [逐查询验证和计时](C1/validation.json)


组合方案实际使用：S31, S32, S33, S34；在 S31 前构建一次。

### C2

药品基本表按来源 × GSP 状态 × 存储条件 × 运输方式联合计数，427 行汇成 36 行，再按单维汇总。

实现对象：`temp."reuse_019_c2"`，36 行、5 列。

**可改写查询：** [S7](C2/S7.sql), [S21](C2/S21.sql), [S22](C2/S22.sql), [S23](C2/S23.sql)。

[建表 SQL](C2/build.sql) · [通过验证的完整执行脚本](C2/approved.sql) · [清理 SQL](C2/cleanup.sql) · [逐查询验证和计时](C2/validation.json)


物化粒度：`"Origin / Tier (Domestic/Imported/JV)"`、`"GSP Certification Status"`、`"Storage conditions (room temperature/cool/refrigerated)"`、`"Transportation mode (land/cold chain)"`。

### C3

库存表按库存状态 × 预警状态 × 差异率保存计数和出入库日期极值。428 行仅压到 401 行。

实现对象：`temp."reuse_019_c3"`，401 行、8 列。

**可改写查询：** [S9](C3/S9.sql), [S10](C3/S10.sql), [S20](C3/S20.sql), [S26](C3/S26.sql)。

[建表 SQL](C3/build.sql) · [通过验证的完整执行脚本](C3/approved.sql) · [清理 SQL](C3/cleanup.sql) · [逐查询验证和计时](C3/validation.json)


物化粒度：`"Inventory Status (Normal/Frozen/Scrapped)"`、`"Inventory Alert Status"`、`"Inventory Discrepancy Rate"`。

## 组合后的执行顺序

只列发生改写的查询；其余成功数据 SQL 原样执行。临时表按第一次使用时构建，任务结束删除。

| SQL | 使用的临时结果 |
|---|---|
| S31 | C1 |
| S32 | C1 |
| S33 | C1 |
| S34 | C1 |

## 执行命令

在仓库根目录运行：

```bash
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/optimization-011-020/replay.py --task 19
```

若要单独检查某个候选，在命令末尾加 `--candidate C1`（按实际编号替换）。该选项只执行验证通过的子集，候选能够执行不代表推荐启用。
