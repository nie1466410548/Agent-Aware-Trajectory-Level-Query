# dacomp-020：学生心理健康与成绩、行为因素

本次重放 15 条成功数据 SQL。组合方案：**保留原查询**。全部查询与历史结果比较通过：**True**。

数据：`sheet1` 1,000 行。

[原任务报告](../../reports/dsv4flash-db-first-full-01/tasks/dacomp-020.md) · [返回十题总览](../README.md)

## 先看应当怎么做

当前数据上的数据库执行与取回耗时：原始 **9.88 ms** → 组合方案 **9.88 ms**（计入构建及清理）。这是本机暖缓存小规模测量，不含模型、Python 分析和网络传输，不是整个 Agent 的加速比。

入口：[完整轨迹 SQL](trajectory.sql)；[执行与验证证据](manifest.json)。

## 每个候选如何实现

下表时间只比较该候选**通过验证的查询子集**。不同候选可能覆盖相同查询，时间或覆盖不能相加。

| 候选 | 实际保存的行数 | 验证通过/原覆盖 | 原查询 ms | 建表及索引 ms | 构建+改写 ms | 组合方案采用 |
|---|---:|---:|---:|---:|---:|---|
| [C1](#c1) | 1000 | 2/2 | 5.29 | 0.73 | 6.02 | 否 |
| [C2](#c2) | 724 | 9/11 | 3.29 | 8.34 | 11.05 | 否 |

### C1

缓存全部 1,000 行学生记录；第二次取明细仍要读取和返回这些行。

实现对象：`temp."reuse_020_c1"`，1000 行、15 列。

**可改写查询：** [S17](C1/S17.sql), [S18](C1/S18.sql)。

[建表 SQL](C1/build.sql) · [通过验证的完整执行脚本](C1/approved.sql) · [清理 SQL](C1/cleanup.sql) · [逐查询验证和计时](C1/validation.json)


### C2

按心理健康分数、性别、兼职、饮食、家长教育、网络、活动联合聚合，保存行为和成绩统计状态。S5、S16 的全局平均值有浮点末位差异，严格口径下不改写。

实现对象：`temp."reuse_020_c2"`，724 行、54 列。

**可改写查询：** [S4](C2/S4.sql), [S7](C2/S7.sql), [S9](C2/S9.sql), [S10](C2/S10.sql), [S11](C2/S11.sql), [S12](C2/S12.sql), [S13](C2/S13.sql), [S14](C2/S14.sql), [S15](C2/S15.sql)。

[建表 SQL](C2/build.sql) · [通过验证的完整执行脚本](C2/approved.sql) · [清理 SQL](C2/cleanup.sql) · [逐查询验证和计时](C2/validation.json)

**回退原查询：** S5, S16。不能执行这些查询对应的试验改写。

- S5：浮点末位差异；本包保留严格无序多重集比较，没有放宽标准。
- S16：浮点末位差异；本包保留严格无序多重集比较，没有放宽标准。

物化粒度：`"Mental health score"`、`"Gender"`、`"Part-time job"`、`"Diet quality"`、`"Parents' education level"`、`"Internet quality"`、`"Extracurricular activity participation"`。

## 组合后的执行顺序

只列发生改写的查询；其余成功数据 SQL 原样执行。临时表按第一次使用时构建，任务结束删除。

| SQL | 使用的临时结果 |
|---|---|
| — | 当前测量不支持启用这些候选，完整脚本保留原查询 |

## 执行命令

在仓库根目录运行：

```bash
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/optimization-011-020/replay.py --task 20
```

若要单独检查某个候选，在命令末尾加 `--candidate C1`（按实际编号替换）。该选项只执行验证通过的子集，候选能够执行不代表推荐启用。
