# dacomp-011：家长教育程度与学生成绩

本次重放 25 条成功数据 SQL。组合方案：**保留原查询**。全部查询与历史结果比较通过：**True**。

数据：`sheet1` 1,000 行。

[原任务报告](../../reports/dsv4flash-db-first-full-01/tasks/dacomp-011.md) · [返回十题总览](../README.md)

## 先看应当怎么做

当前数据上的数据库执行与取回耗时：原始 **24.54 ms** → 组合方案 **24.54 ms**（计入构建及清理）。这是本机暖缓存小规模测量，不含模型、Python 分析和网络传输，不是整个 Agent 的加速比。

入口：[完整轨迹 SQL](trajectory.sql)；[执行与验证证据](manifest.json)。

## 每个候选如何实现

下表时间只比较该候选**通过验证的查询子集**。不同候选可能覆盖相同查询，时间或覆盖不能相加。

| 候选 | 实际保存的行数 | 验证通过/原覆盖 | 原查询 ms | 建表及索引 ms | 构建+改写 ms | 组合方案采用 |
|---|---:|---:|---:|---:|---:|---|
| [C1](#c1) | 1000 | 4/4 | 10.66 | 0.77 | 11.43 | 否 |
| [C2](#c2) | 875 | 18/18 | 11.12 | 6.40 | 17.77 | 否 |

### C1

缓存整张学生明细表。后续仍要返回全部 1,000 行，普通表扫描本来就便宜，数据库内再复制一份通常没有收益。

实现对象：`temp."reuse_011_c1"`，1000 行、15 列。

**可改写查询：** [S25](C1/S25.sql), [S26](C1/S26.sql), [S27](C1/S27.sql), [S28](C1/S28.sql)。

[建表 SQL](C1/build.sql) · [通过验证的完整执行脚本](C1/approved.sql) · [清理 SQL](C1/cleanup.sql) · [逐查询验证和计时](C1/validation.json)


### C2

按家长教育、性别、饮食、网络、活动、学习时间分段等维度联合分组，保存成绩及行为指标的 SUM/COUNT/MIN/MAX，再上卷回答各查询。联合粒度过细：1,000 行仅压到 875 行。

实现对象：`temp."reuse_011_c2"`，875 行、29 列。

**可改写查询：** [S3](C2/S3.sql), [S4](C2/S4.sql), [S6](C2/S6.sql), [S8](C2/S8.sql), [S9](C2/S9.sql), [S13](C2/S13.sql), [S15](C2/S15.sql), [S16](C2/S16.sql), [S17](C2/S17.sql), [S18](C2/S18.sql), [S19](C2/S19.sql), [S20](C2/S20.sql), [S21](C2/S21.sql), [S22](C2/S22.sql), [S23](C2/S23.sql), [S24](C2/S24.sql), [S29](C2/S29.sql), [S30](C2/S30.sql)。

[建表 SQL](C2/build.sql) · [通过验证的完整执行脚本](C2/approved.sql) · [清理 SQL](C2/cleanup.sql) · [逐查询验证和计时](C2/validation.json)


物化粒度：`"Parents' education level"`、`gender`、`"Diet quality"`、`"Internet quality"`、`"Extracurricular activity participation"`、`CASE WHEN "Daily study time" < 2 THEN '<2h' WHEN "Daily study time" < 4 THEN '2-4h' WHEN "Daily study time" < 6 THEN '4-6h' ELSE '6h+' END`、`CASE WHEN "Mental health score" <= 3 THEN 'Low (0-3)' WHEN "Mental health score" <= 6 THEN 'Medium (4-6)' ELSE 'High (7-10)' END`、`CASE WHEN "Attendance rate" < 70 THEN '<70%' WHEN "Attendance rate" < 85 THEN '70-85%' WHEN "Attendance rate" < 95 THEN '85-95%' ELSE '95%+' END`、`"Part-time job"`、`CASE WHEN "Parents' education level" IS NULL THEN 'Missing' ELSE "Parents' education level" END`。

## 组合后的执行顺序

只列发生改写的查询；其余成功数据 SQL 原样执行。临时表按第一次使用时构建，任务结束删除。

| SQL | 使用的临时结果 |
|---|---|
| — | 当前测量不支持启用这些候选，完整脚本保留原查询 |

## 执行命令

在仓库根目录运行：

```bash
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/optimization-011-020/replay.py --task 11
```

若要单独检查某个候选，在命令末尾加 `--candidate C1`（按实际编号替换）。该选项只执行验证通过的子集，候选能够执行不代表推荐启用。
