# Agent 侧 DB Tool 设计

版本：v0.1（设计稿）  
日期：2026-09-09  
范围：Agent 工具接口、未来访问提示、Client 调用与校验流程。本文不定义数据库侧的优化动作或决策算法。

## 1. 目标与边界

为 Agent 提供统一的 `db.query` 工具。Agent 每轮调用时，同时提交当前 SQL 和结构化的未来访问提示（future access）。Client 校验并封装请求，再交给数据库适配层执行。

未来访问提示描述 Agent 根据任务、已有结果和当前规划，预计在当前 SQL 返回后可能发生的数据访问。提示可以包含多个同等重要、发生可能性相近的方向，不要求提前确定完整 SQL。

本设计对应已有研究文档中的 Agent-side foresight：未来查询未知，但生成查询的 Agent 可以暴露部分访问意图。本文只落实这一信息接口，不声称提示一定准确或一定产生优化收益。

基本原则：

- Agent 根据原任务和真实查询结果继续分析；提示不构成后续执行承诺。
- 不要求 Agent 为配合数据库而改变查询、增加查询或维持已放弃的分析方向。
- 未知信息显式留空或说明，不猜测当前 SQL 尚未返回的结果。
- 提示与当前 SQL 在同一次模型调用中生成，默认不增加专门的预测调用。
- JSON 是工具调用参数，不要求 Agent 创建磁盘文件；Client 可将其记录为日志。

## 2. 已确认的设计决策

| 项目 | v0.1 约定 |
|---|---|
| 预测范围 | 当前 SQL 返回后，至当前任务结束 |
| 规划覆盖 | 允许只暴露当前已形成的部分规划，不强迫规划完整任务 |
| 候选粒度 | 表必填；列、过滤、Join、聚合等按已知程度选填 |
| 候选关系 | 默认允许多个候选在同一任务中发生；不建模互斥和依赖图 |
| 数组顺序 | 不代表排名，也不代表执行顺序 |
| 优先级 | `high / medium / low`，表示对完成任务的重要程度 |
| 发生可能性 | 可选 `likelihood: high / medium / low`；未知时省略 |
| 更新 | 随 SQL 调用提交完整的新集合，整体替换上一轮提示 |
| 空提示 | 区分预计无后续访问与暂时无法预测 |
| 候选上限 | 默认最多 8 个，可配置，不要求填满 |
| Client 元数据 | 轨迹、轮次、请求标识由 Client 注入 |
| 错误降级 | 可独立提取有效 SQL 时，提示错误不阻断 SQL；记录并丢弃整份提示 |

`likelihood` 是定性估计，不预设三级对应的数值概率，也不把它当成经过校准的概率。多个候选的可能性不需要归一化。

## 3. 工具、调用参数与请求封装

### 3.1 三个层次

1. **Tool Schema**：开发者提供的参数定义，说明字段格式与含义。
2. **工具调用参数**：Agent 按 Schema 生成的当前 SQL 和未来访问提示。
3. **工具实现**：Client 中的执行逻辑，负责校验、添加元数据、调用数据库适配层、返回结果和记录日志。

工具逻辑名称为 `db.query`。如运行框架对名称有限制，可以映射为 `db_query`，其参数语义保持一致。

### 3.2 Agent 负责的参数

```json
{
  "sql": "SELECT country, SUM(revenue) FROM sales WHERE month = '2026-08' GROUP BY country",
  "future_access": {
    "status": "provided",
    "coverage": "partial_plan",
    "candidates": [
      {
        "tables": ["sales"],
        "columns": ["sales.country", "sales.product_id", "sales.revenue"],
        "filters": [
          {"column": "sales.month", "op": "eq", "value": "2026-08"}
        ],
        "group_by": ["sales.product_id"],
        "aggregations": [
          {"function": "sum", "column": "sales.revenue"}
        ],
        "condition": "若当前结果显示收入下降集中在某个国家",
        "unresolved": ["国家过滤值待当前查询结果确定"],
        "priority": "high",
        "likelihood": "medium"
      },
      {
        "tables": ["sales"],
        "columns": ["sales.country", "sales.customer_type", "sales.revenue"],
        "filters": [
          {"column": "sales.month", "op": "eq", "value": "2026-08"}
        ],
        "group_by": ["sales.customer_type"],
        "aggregations": [
          {"function": "sum", "column": "sales.revenue"}
        ],
        "condition": "若当前结果显示收入下降集中在某个国家",
        "unresolved": ["国家过滤值待当前查询结果确定"],
        "priority": "high",
        "likelihood": "medium"
      }
    ]
  }
}
```

两个候选可以先后都执行，也可以在看到结果后全部放弃。当前 SQL 中出现的 `country` 分组不需要被机械复制为未来候选；候选描述的是后续访问。

### 3.3 Client 注入的请求封装

```json
{
  "schema_version": "0.1",
  "trajectory_id": "task-001",
  "step_id": 3,
  "request_id": "req-003",
  "payload": {
    "sql": "SELECT COUNT(*) FROM sales",
    "future_access": {
      "status": "unknown",
      "candidates": []
    }
  }
}
```

`trajectory_id` 对应一个分析任务，不能直接用长期数据库 session 代替。`step_id` 表示该轨迹中由 Client 接收并编号的逻辑查询调用；新调用递增，传输重试复用原编号与 `request_id`。请求标识用于关联和去重，但本身不保证数据库恰好执行一次。

初版按轨迹串行调用，不定义同一轨迹内多个并发分支的合并语义。任务结束由 Client 的任务生命周期判定，不由某条提示决定。

## 4. Future access 的字段语义

### 4.1 外层状态与覆盖范围

| 字段 | 语义 |
|---|---|
| `status = provided` | 提供至少一个可描述的未来访问候选 |
| `status = unknown` | 当前无法提供可靠候选；不表示任务结束 |
| `status = no_further_access` | 当前预计本任务不再访问数据库；仍允许以后修正 |
| `coverage = remaining_task` | 当前规划已考虑任务的剩余过程；不保证穷举所有未来 SQL |
| `coverage = partial_plan` | 只描述当前已形成的局部规划；未列出不表示不会访问 |

`provided` 必须包含 `coverage` 和非空候选数组。另外两种状态使用空数组，省略 `coverage`。

初版不设置固定步数窗口。所有候选都以任务剩余期间为时间范围，`partial_plan` 只表示信息覆盖不完整，不把概率范围缩成下一轮。若以后加入窗口，应按未来 DB Tool 调用次数计数，并同步修改发生可能性的定义。

### 4.2 候选访问

| 字段 | 必填 | 语义 |
|---|---|---|
| `tables` | 是 | 已知的预计访问表，至少一个 |
| `priority` | 是 | 对完成任务的重要程度 |
| `columns` | 否 | 已知的访问列，包含过滤、连接和聚合所需列，不仅是输出列 |
| `filters` | 否 | 已知的过滤条件；初版仅表达以 AND 连接的简单条件 |
| `joins` | 否 | 已知的等值连接关系 |
| `group_by` | 否 | 已知的分组列 |
| `aggregations` | 否 | 已知的聚合函数及输入列 |
| `condition` | 否 | 该访问方向成立的简短条件说明 |
| `unresolved` | 否 | 尚未确定的表、列、谓词值或其他细节 |
| `likelihood` | 否 | 在当前信息下，任务剩余期间至少发生一次该访问的定性可能性 |

约定：

- 表名使用当前连接可解析的数据库对象名；列使用 `表名.列名` 或适用的更完整限定名，避免 SQL 临时别名。
- 省略字段表示未知或未提供，不能解释成不存在该操作；`columns` 省略不表示读取全表所有列。
- 若没有任何已知表，则不生成该候选，可使用整体 `unknown` 状态。
- 过滤字段仅写已经确定的值。结果依赖的条件写入 `condition` 和 `unresolved`，不使用看似真实的占位值。
- `condition`、`unresolved` 是描述信息，不能直接拼接成 SQL 或当作可执行谓词。
- `likelihood` 是综合考虑触发条件是否成立之后的估计，不是“假设条件成立时”的条件概率。
- 一个模式可对应未来多次查询；初版不估计复用次数，也不要求模式与 SQL 一一对应。

优先级解释：`high` 为直接支撑核心结论或必要验证的访问；`medium` 为有助于主要分析的补充访问；`low` 为可选的扩展探索。它不表达预计访问时间或数据库调度要求。

## 5. 参数 Schema

以下 JSON Schema 是本设计的逻辑契约。具体模型服务支持的 Schema 子集可能不同，工具适配层可以转换表达方式；Client 必须保留这里定义的语义校验。本文不绑定某个模型厂商的严格参数生成能力。

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["sql", "future_access"],
  "properties": {
    "sql": {"type": "string", "minLength": 1},
    "future_access": {"$ref": "#/$defs/futureAccess"}
  },
  "$defs": {
    "names": {
      "type": "array",
      "minItems": 1,
      "uniqueItems": true,
      "items": {"type": "string", "minLength": 1}
    },
    "level": {"enum": ["high", "medium", "low"]},
    "scalar": {"type": ["string", "number", "boolean", "null"]},
    "filter": {
      "type": "object",
      "additionalProperties": false,
      "required": ["column", "op", "value"],
      "properties": {
        "column": {"type": "string", "minLength": 1},
        "op": {"enum": ["eq", "ne", "lt", "le", "gt", "ge", "in", "between", "is_null", "is_not_null"]},
        "value": {
          "anyOf": [
            {"$ref": "#/$defs/scalar"},
            {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/scalar"}}
          ]
        }
      }
    },
    "join": {
      "type": "object",
      "additionalProperties": false,
      "required": ["left_column", "right_column", "type"],
      "properties": {
        "left_column": {"type": "string", "minLength": 1},
        "right_column": {"type": "string", "minLength": 1},
        "type": {"enum": ["inner", "left", "right", "full", "unknown"]}
      }
    },
    "aggregation": {
      "type": "object",
      "additionalProperties": false,
      "required": ["function", "column"],
      "properties": {
        "function": {"enum": ["sum", "count", "avg", "min", "max", "count_distinct"]},
        "column": {"type": "string", "minLength": 1}
      }
    },
    "candidate": {
      "type": "object",
      "additionalProperties": false,
      "required": ["tables", "priority"],
      "properties": {
        "tables": {"$ref": "#/$defs/names"},
        "columns": {"$ref": "#/$defs/names"},
        "filters": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/filter"}},
        "joins": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/join"}},
        "group_by": {"$ref": "#/$defs/names"},
        "aggregations": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/aggregation"}},
        "condition": {"type": "string", "minLength": 1, "maxLength": 200},
        "unresolved": {
          "type": "array", "minItems": 1, "maxItems": 8,
          "items": {"type": "string", "minLength": 1, "maxLength": 200}
        },
        "priority": {"$ref": "#/$defs/level"},
        "likelihood": {"$ref": "#/$defs/level"}
      }
    },
    "futureAccess": {
      "type": "object",
      "additionalProperties": false,
      "required": ["status", "candidates"],
      "properties": {
        "status": {"enum": ["provided", "unknown", "no_further_access"]},
        "coverage": {"enum": ["remaining_task", "partial_plan"]},
        "candidates": {"type": "array", "maxItems": 8, "items": {"$ref": "#/$defs/candidate"}}
      },
      "allOf": [
        {
          "if": {"properties": {"status": {"const": "provided"}}},
          "then": {"required": ["coverage"], "properties": {"candidates": {"minItems": 1}}},
          "else": {"not": {"required": ["coverage"]}, "properties": {"candidates": {"maxItems": 0}}}
        }
      ]
    }
  }
}
```

Client 还需要执行以下语义检查，不能仅依赖上述结构 Schema：

- `sql` 去除空白后非空；SQL 语法、权限和执行范围沿用数据库工具的执行策略。
- `eq / ne / lt / le / gt / ge` 接受非 null 标量；`in` 接受非空非 null 标量数组；`between` 接受恰好两个非 null 标量；`is_null / is_not_null` 的 `value` 必须为 null。
- 聚合输入 `*` 仅用于 `count`；复杂表达式不能伪装成列名。
- 所有已声明列应能关联到候选中的表。能够通过已有 catalog 信息检查时进行检查；无法解析的对象记录为未核验，不额外启动模型调用猜测。
- 无法表达的 OR、非等值 Join、窗口函数等细节可写入 `unresolved`，不把复杂语义强行编码为不等价的简单条件。

Schema 中的数组上限应由同一 Client 配置生成，避免提示说明与实际校验限制不一致。

## 6. Agent 指令模板

以下说明与工具 Schema 一起提供给 Agent：

> 使用 db.query 执行数据库 SQL。每轮提交当前 SQL，同时提交最新的 future_access。
>
> 根据原任务、已观察到的查询结果和当前已经形成的分析计划，描述当前 SQL 返回后至任务结束期间可能发生的访问。可以提供多个同等重要或可能性相近的候选；数组顺序没有排名含义。
>
> 只描述已有规划，不为填满提示而扩展任务或额外制定完整计划。表名必须已知；其余细节按已知程度填写。不要猜测尚未返回的查询结果，未确定条件用 unresolved 表达。
>
> priority 表示访问对完成任务的重要程度，不表示发生概率或执行顺序。likelihood 是可选的定性发生可能性，无法判断时省略。
>
> 每轮给出完整的最新候选集合，它会替换上一轮提示。默认最多 8 个候选，不要求填满；超过上限时，优先保留与核心任务相关且能清楚描述的方向。
>
> 无法提供候选时使用 unknown 和空数组；预计不再需要数据库访问时使用 no_further_access 和空数组。
>
> 继续根据任务和实际结果决定下一步。此前提示不构成承诺，可以修改或放弃，不需要为了匹配提示而执行查询。不要在提示中输出长篇推理。

运行环境将数据库访问入口统一为该工具，数据库连接由 Client 管理。仅写指令不能保证 Agent 不绕过工具；如果实验要求完整记录轨迹，应确保没有其他可用的数据库访问通道。

## 7. Client 执行、更新与错误处理

### 7.1 正常流程

```text
任务与已有查询结果
    → Agent 生成 db.query 参数
    → Client 解析、校验、注入请求元数据
    → 同一请求携带当前 SQL 与最新提示到数据库适配层
    → 适配层执行当前 SQL
    → Client 返回实际结果并记录本轮日志
    → Agent 根据结果继续分析
```

提示描述未来，但在当前 SQL 执行前提交；此时 Agent 只能利用之前已观察到的信息。初版不提供独立的提示更新调用。

每次可执行 SQL 请求到达时，适配层接收一份新的提示快照。有效的 `unknown` 或 `no_further_access` 也会替换上一份快照。缺失或无效提示同样清除旧快照，不能让数据库继续误用上一轮的意图。清除提示快照不规定数据库物理状态如何回收。

如果参数整体不可解析或 SQL 字段不可用，则不提交数据库请求，也不应用该轮提示。数据库实际执行后报错时，提示仍然只是该轮的预测快照，不表示 SQL 已成功；错误状态必须与同一请求一起记录。下一次调用继续完整替换，任务结束时关闭该轨迹的提示生命周期。

### 7.2 分层校验与降级

| 情况 | SQL 行为 | 提示行为 |
|---|---|---|
| JSON 不可解析、未知执行字段或缺少有效 SQL | 不执行，返回参数错误 | 不应用新快照 |
| SQL 字段有效，缺少或格式错误的 future_access | 按正常 SQL 策略执行 | 丢弃整份提示、清除旧快照、记录原因 |
| 提示违反状态约束、超过大小或候选上限 | 按正常 SQL 策略执行 | 同上；不静默截断候选 |
| 提示合法但对象暂时无法核验 | 按正常 SQL 策略执行 | 标记未核验，不宣称语义正确 |
| 数据库语法、权限或执行错误 | 返回真实数据库错误 | 记录本轮预测及执行失败 |
| 超时且是否执行成功不明 | 返回结果不确定状态 | 不自动把未知状态当作未执行后重试 |

实现时必须分离执行参数校验与提示校验，避免整个 Schema 校验失败就一律阻断 SQL。发送给模型的 Schema 仍要求 `future_access` 必填；降级是 Client 处理异常的机制。

仅因提示错误，不启动模型修复调用。真正的执行参数错误最多允许 2 次连续自动修复尝试，超过后交回上层任务错误处理流程；该上限可配置。

### 7.3 返回格式

成功返回示例：

```json
{
  "request_id": "req-003",
  "status": "ok",
  "sql_executed": true,
  "result": {
    "columns": ["country", "total_revenue"],
    "rows": [["Canada", 120000]],
    "returned_row_count": 1,
    "truncated": false
  }
}
```

参数错误示例：

```json
{
  "request_id": "req-004",
  "status": "invalid_arguments",
  "sql_executed": false,
  "errors": [{"path": "sql", "message": "SQL 不能为空"}]
}
```

返回的执行状态至少区分 `ok / invalid_arguments / db_error / execution_unknown`。`sql_executed` 为 true 表示执行已开始，为 false 表示未执行，无法确定时为 null；是否成功由 `status` 判断。

提示校验结果记录在 Client 日志中，默认不作为要求 Agent 纠正规划的反馈。Agent 获取真实查询结果和必要的执行错误，不需要知道数据库是否采用提示。结果截断策略沿用工具配置并显式标记，不能把截断结果当成全部数据。

## 8. 开销控制与观测

初版默认配置：

| 配置 | 默认值或策略 |
|---|---|
| 候选数量 | 最多 8 个 |
| 自然语言字段 | 每条最多 200 个字符；每候选 unresolved 最多 8 条 |
| 提示总大小 | future_access 序列化后 UTF-8 最大 16 KiB，由 Client 校验 |
| 独立预测模型调用 | 0 次 |
| 提示错误重试 | 0 次 |
| 执行参数自动修复 | 最多连续 2 次 |
| 规划覆盖 | 默认 partial_plan；确实考虑剩余任务时使用 remaining_task |

这些上限是可调整的工程初值，不是研究结论。Schema 适配、校验和日志处理均在 Client 中完成。

每轮至少记录：

- 任务、轮次、请求标识，以及模型、指令和 Schema 版本。
- 原始调用参数、规范化提示、校验状态、丢弃原因和接收时间。
- 当前 SQL、数据库执行状态、耗时，以及结果大小和截断标记。
- 模型调用耗时、可获得的输入输出 token 用量、Client 校验耗时和提示字节数。
- 后续实际 SQL 与任务终止状态，用于事后评估；事后信息不回填为当时已知提示。

任务被取消或失败时，不能把所有未发生候选简单算为错误预测，应单独标记观察提前终止。

## 9. 评估与验收

### 9.1 接口验收

实现时应覆盖以下行为：多个同级候选能通过；只有表和优先级的候选能通过；两种空状态可区分；provided 加空数组被拒绝为无效提示；未知字段和越界大小可被发现；坏提示不触发 SQL 重复执行；新快照及空快照正确替换旧快照；超时不被误判为未执行。

### 9.2 提示信息质量

分别评估表、列和更细访问模式的覆盖与命中情况，不要求匹配一条提前生成的完整 SQL。匹配规则需要在实验前固定，尤其要区分“未提供字段”和“明确指定条件”。仅预测一个大表会容易命中，因此同时报告提示具体程度和覆盖情况。

对 likelihood 的三个等级，事后统计各自实际发生比例，检验其是否具有区分度；不提前给三级指定概率。priority 反映任务重要程度，不通过实际出现频率直接判定对错。unknown 应单独报告占比，避免只对容易预测的轮次统计质量。

### 9.3 成本与分析行为

设置只生成 SQL 和生成 SQL 加提示的对照条件，保持任务、数据、模型配置和结果返回策略尽可能一致。比较模型总耗时、token、任务完成质量、实际查询轨迹与查询数量；有随机性时使用重复运行。

联合生成的总耗时不能直接归因于提示，需要通过对照估计增量成本。指令规定提示不影响分析，不代表模型实际行为绝对不变；是否因额外生成提示而改变轨迹，也是需要测量的结果。

## 10. 初版之外的扩展

以下内容暂不加入必需接口：精确数值概率、固定步数窗口、候选互斥组或依赖图、候选复用次数、独立提示更新工具、跨轮候选增量更新、并发多 Agent 轨迹合并，以及复杂 SQL 表达式的完整 AST。

初版交付边界是：Agent 能在每次数据库调用时，以低额外负担提供多个可修正的未来访问候选；Client 能可靠承载、校验和记录这些信息。数据库如何利用提示选择物理准备动作，留给数据库侧设计文档。
