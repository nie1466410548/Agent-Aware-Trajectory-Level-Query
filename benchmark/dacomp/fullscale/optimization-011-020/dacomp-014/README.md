# dacomp-014：视频榜单与创作者特征

本次重放 49 条成功数据 SQL。组合方案：**保留原查询**。全部查询与历史结果比较通过：**True**。

数据：`sheet1` 5,200 行。

[原任务报告](../../reports/dsv4flash-db-first-full-01/tasks/dacomp-014.md) · [返回十题总览](../README.md)

## 先看应当怎么做

当前数据上的数据库执行与取回耗时：原始 **364.89 ms** → 组合方案 **364.81 ms**（计入构建及清理）。这是本机暖缓存小规模测量，不含模型、Python 分析和网络传输，不是整个 Agent 的加速比。

入口：[完整轨迹 SQL](trajectory.sql)；[执行与验证证据](manifest.json)。

## 每个候选如何实现

下表时间只比较该候选**通过验证的查询子集**。不同候选可能覆盖相同查询，时间或覆盖不能相加。

| 候选 | 实际保存的行数 | 验证通过/原覆盖 | 原查询 ms | 建表及索引 ms | 构建+改写 ms | 组合方案采用 |
|---|---:|---:|---:|---:|---:|---|
| [C1](#c1) | 5200 | 11/11 | 220.23 | 5.77 | 221.73 | 否 |
| [C2](#c2) | 5200 | 19/19 | 73.97 | 55.54 | 151.89 | 否 |

### C1

缓存全量 5,200 行榜单，后续十次完整读取仍需扫描、传输。若希望省去重复传输，应在工具层复用已有结果句柄；这不是本包数据库临时表已实现的收益。

实现对象：`temp."reuse_014_c1"`，5200 行、21 列。

**可改写查询：** [S36](C1/S36.sql), [S40](C1/S40.sql), [S41](C1/S41.sql), [S42](C1/S42.sql), [S43](C1/S43.sql), [S44](C1/S44.sql), [S45](C1/S45.sql), [S46](C1/S46.sql), [S47](C1/S47.sql), [S48](C1/S48.sql), [S49](C1/S49.sql)。

[建表 SQL](C1/build.sql) · [通过验证的完整执行脚本](C1/approved.sql) · [清理 SQL](C1/cleanup.sql) · [逐查询验证和计时](C1/validation.json)


### C2

把视频类别、创作者、日期、排名分段等全部合成聚合粒度，保存播放互动等状态。仍有 5,200 行，列数反而增加，不宜因为覆盖 19 条 SQL 就默认启用。

实现对象：`temp."reuse_014_c2"`，5200 行、55 列。

**可改写查询：** [S4](C2/S4.sql), [S9](C2/S9.sql), [S11](C2/S11.sql), [S12](C2/S12.sql), [S13](C2/S13.sql), [S14](C2/S14.sql), [S15](C2/S15.sql), [S16](C2/S16.sql), [S19](C2/S19.sql), [S23](C2/S23.sql), [S24](C2/S24.sql), [S25](C2/S25.sql), [S27](C2/S27.sql), [S29](C2/S29.sql), [S30](C2/S30.sql), [S31](C2/S31.sql), [S32](C2/S32.sql), [S33](C2/S33.sql), [S50](C2/S50.sql)。

[建表 SQL](C2/build.sql) · [通过验证的完整执行脚本](C2/approved.sql) · [清理 SQL](C2/cleanup.sql) · [逐查询验证和计时](C2/validation.json)


物化粒度：`"Video Category"`、`"Main Category"`、`"Creator Gender"`、`CASE WHEN NOT "Bilibili Personal Verification" IS NULL THEN 'Verified' ELSE 'Not Verified' END`、`"Creator Video Count"`、`CASE WHEN "Rank" <= 10 THEN 'Top 10' WHEN "Rank" <= 30 THEN '11-30' WHEN "Rank" <= 50 THEN '31-50' WHEN "Rank" <= 70 THEN '51-70' ELSE '71-100' END`、`SUBSTRING(_id, 1, 8)`、`SUBSTRING(_id, 1, 4)`、`"Creator"`、`CASE WHEN "Creator Followers" < 10000 THEN '1. <10k' WHEN "Creator Followers" < 100000 THEN '2. 10k-100k' WHEN "Creator Followers" < 1000000 THEN '3. 100k-1M' ELSE '4. >1M' END`、`CASE WHEN "Creator Video Count" = 100 THEN '100 (full)' WHEN "Creator Video Count" < 10 THEN '1-9' WHEN "Creator Video Count" < 50 THEN '10-49' ELSE '50-99' END`。

## 组合后的执行顺序

只列发生改写的查询；其余成功数据 SQL 原样执行。临时表按第一次使用时构建，任务结束删除。

| SQL | 使用的临时结果 |
|---|---|
| — | 当前测量不支持启用这些候选，完整脚本保留原查询 |

## 执行命令

在仓库根目录运行：

```bash
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/optimization-011-020/replay.py --task 14
```

若要单独检查某个候选，在命令末尾加 `--candidate C1`（按实际编号替换）。该选项只执行验证通过的子集，候选能够执行不代表推荐启用。
