# Agent-Aware Trajectory-Level Query Processing and Optimization  
## Related Work 与研究定位

## 1. 研究定位概述

传统数据库查询优化通常以单条查询为基本优化单元，即针对当前查询 \(q_t\) 搜索代价最低的物理执行计划：

\[
P_t^*=\arg\min_{P\in\mathcal{P}(q_t)} Cost(q_t,P)
\]

然而，在 Data Agent 场景下，一个高层分析任务通常并不会对应单条 SQL，而是形成一个持续演化的查询轨迹：

\[
\tau =
\langle
q_1,r_1,
q_2,r_2,
\dots,
q_T,r_T
\rangle
\]

其中后续查询往往由前序查询结果以及 Agent 当前任务状态共同决定：

\[
q_{t+1}
=
Agent(
Task,
State_t,
q_{\leq t},
r_{\leq t}
)
\]

例如，Agent 为分析“为什么八月份收入下降”可能依次执行：

\[
\text{Country Breakdown}
\rightarrow
\text{Canada Drill-down}
\rightarrow
\text{Product Analysis}
\rightarrow
\text{Temporal Verification}
\]

这些查询在数据范围、谓词、Join、聚合维度以及中间结果方面具有显著相关性。

如果数据库仍然逐条独立优化，就可能错失：

- intermediate-result reuse；
- proactive materialization；
- temporary / ephemeral indexing；
- data prefetching；
- shared computation；
- trajectory-aware caching 与 eviction；
- trajectory-level resource scheduling。

因此，本研究关注的并不是如何帮助 Agent 生成下一条 SQL，而是：

> **数据库能否利用 Agent 查询轨迹及 Agent 可暴露的未来访问意图，在后续 SQL 真正产生之前主动准备跨查询物理状态，从而降低整个 Agent 数据访问轨迹的执行成本。**

这一问题与 Multi-Query Optimization、History-Aware Optimization、Exploratory Data Analysis、Predictive Query Processing、Query-Sequence Optimization 以及近年来的 Agentic Data Systems 均存在联系，但又不完全等同于其中任何一个方向。

---

# 2. Related Work Landscape：六条最相关研究主线

## 2.1 Multi-Query Optimization：从单查询最优到多查询共享

Multi-Query Optimization（MQO）最早解决的核心问题就是：

> 独立优化多个相关查询可能导致重复扫描、重复 Join 和重复计算，因此应当在多个查询之间寻找共享执行机会。

典型方法包括：

\[
Shared\ Scan
\]

\[
Shared\ Sub\text{-}Expression
\]

\[
Common\ Intermediate\ Result
\]

以及：

\[
Materialized\ View\ Reuse
\]

较新的 Hybrid MQO 工作进一步结合 shared sub-expression 与 materialized-view reuse，使 query batch 可以共享执行计划，同时后续到来的查询也能够复用已经保存的中间结果。

因此，本研究不能简单声称：

> “传统数据库只会优化单条查询，无法进行跨查询优化。”

事实上，MQO 已经充分说明：

\[
\sum_i \min Cost(q_i)
\neq
\min Cost(q_1,\ldots,q_n)
\]

### 与本研究的区别

MQO 通常基于一个已经可获得的 query set 或 query batch：

\[
Q=\{q_1,q_2,\dots,q_n\}
\]

也就是说，优化器能够直接观察多个查询并搜索公共计算。

而 Agent trajectory 中：

\[
q_{t+1},q_{t+2},\ldots
\]

在时刻 \(t\) 尚未真正产生。

因此，本研究面对的不是：

\[
\text{Known multi-query workload}
\]

而是：

\[
\text{Evolving and uncertain future workload}
\]

MQO 提供了跨查询共享计算的技术基础，但并没有解决 Agent 场景下“future queries 尚未出现时如何主动进行跨查询优化”的问题。

---

# 2.2 History-Aware Optimization 与 Intermediate Reuse：利用过去帮助未来

第二类工作比传统 MQO 更接近本研究，因为它们已经研究：

> 即使未来查询未知，系统是否可以根据已经观察到的 workload 保存有价值的中间结果，以帮助后续查询？

### HAWC

HAWC（History-Aware Query Optimization with Materialized Intermediate Views）在 cost-based optimizer 中加入历史信息，用过去 workload 判断当前查询计划产生的哪些 intermediate results 值得物化，以便未来查询使用。

其基本逻辑是：

\[
Past\ Queries
\rightarrow
Identify\ Reusable\ Intermediate
\rightarrow
Materialize
\rightarrow
Future\ Reuse
\]

### HashStash

HashStash 进一步研究 DBMS 内部 physical structure 的直接复用。例如，一个 Hash Join 或 Hash Aggregation 本身就会创建 hash table，系统将其保存并 externalize，使之后的查询可以直接利用，而不必重新构建。其 reuse-aware optimizer 会对已有 reusable structure 和普通执行计划进行成本比较。

### SparkCruise

SparkCruise 则从 workload-level optimization 的角度构建在线 feedback loop，根据已经执行的 Spark SQL workload 学习并选择 computation reuse opportunities，以优化后续 workload。

### 与本研究的区别

这一类工作的基本信息流是：

\[
W_{past}
\rightarrow
Estimate\ Reuse\ Value
\rightarrow
Prepare\ for\ Future
\]

它已经具有：

- future unknown；
- online execution；
- intermediate reuse；
- dynamic physical-state management。

因此：

> **仅仅根据 Agent 已经执行过的 SQL 做 reuse/materialization，并不足以构成本研究的核心创新。**

否则本研究很容易被理解为：

\[
History\text{-}Aware\ Optimization
+
Agent\ workload
\]

本研究真正希望引入的是 Agent workload 特有的新信息源：

\[
AgentGoal,
AgentState,
CandidateActions,
FutureIntent
\]

使系统从单纯的：

\[
P(W_{future}\mid W_{past})
\]

进一步发展到：

\[
P(
W_{future}
\mid
W_{past},
R_{past},
AgentContext
)
\]

---

# 2.3 Exploratory / Interactive Data Analysis：结果驱动的在线查询轨迹

Exploratory Data Analysis（EDA）与 Interactive Data Exploration 是另一个必须正面讨论的领域。

SIGMOD 2015 的 Data Exploration tutorial 已经系统总结了数据库如何支持用户在“不知道最终要找什么”的情况下不断探索数据，包括新的 storage、query processing 以及 interaction techniques。

其典型过程本身就是：

\[
Q_1
\rightarrow
R_1
\rightarrow
Human\ Reasoning
\rightarrow
Q_2
\rightarrow
R_2
\rightarrow \cdots
\]

因此 EDA 与 Agent trajectory 有两个非常重要的共同点：

\[
Future\ Query\ Unknown
\]

以及：

\[
Future\ Query\ is\ Result\text{-}Dependent
\]

### ForeCache

ForeCache 是其中与本研究尤其接近的一项工作。它根据用户近期的数据浏览行为预测下一步可能访问的数据 tile，并提前进行 prefetch，从而提高 interactive visualization 的响应速度。

因此：

\[
Past\ Interaction
\rightarrow
Future\ Access\ Prediction
\rightarrow
Prefetch
\]

也并不是 Agent 场景第一次出现。

### 与本研究的区别

真正的区别不应该表述成：

> “EDA 是 Human，而我们是 Agent。”

因为这只是 workload generator 的表面区别。

更本质的区别在于 **workload generator 的可观察性**。

传统 EDA 中：

\[
Human\ Intent
\]

主要存在于人的脑中。

DBMS 只能观察：

\[
Queries + Mouse/Visualization\ Interactions
\]

然后推断：

\[
Future\ Intent
\]

即：

\[
Observed\ Behavior
\rightarrow
Infer\ Future
\]

而 Agent 是程序化的 workload generator，它原则上可以主动向 DBMS 暴露：

\[
Goal
\]

\[
Current\ Stage
\]

\[
Current\ Hypothesis
\]

\[
Candidate\ Future\ Actions
\]

\[
Likely\ Data\ Access
\]

因此 Agent 场景提供了一种 EDA 中很难获得的信息条件：

\[
\boxed{
Future\ query\ unknown,
but\ future\ intent\ partially\ visible
}
\]

此外，传统 interactive exploration 的 action space 往往受到 UI、visualization 或 drill-down 模板限制；Agent 则可以动态生成任意 SQL、Join、schema exploration 和跨表分析，因此 future access space 更开放、更难预测，但同时 Agent 又能够提供更丰富的机器可读 intent。

---

# 2.4 Query-Sequence 与 Procedural SQL Optimization：已知未来条件下的跨查询优化

数据库领域也已经直接研究过 Query-Sequence Optimization。

ReProVide 利用 upcoming query sequence 的知识，在当前查询尚未完成时提前进行 FPGA reconfiguration，并避免覆盖后续查询仍会使用的硬件配置，从而降低整个 query sequence 的执行时间。其核心前提是系统已知 upcoming queries。

2026 年的 AutoCox 则研究 procedural SQL program 中 producer-consumer statements 的跨查询 physical design。它针对 temporary intermediate result 动态创建 intermediate index，并利用 what-if analysis 比较 index creation overhead 与 downstream consumer savings。

其信息条件类似：

\[
Producer
\rightarrow
Consumer_1
\rightarrow
Consumer_2
\]

其中 consumer statements 已经存在于 program 中。

### 与本研究的区别

这一类工作的特点是：

\[
Future\ Workload = Known
\]

因此 optimizer 可以直接计算：

\[
Cost(Build)
+
\sum_i Cost(q_i|Build)
\]

Agent 场景则是：

\[
q_{t+1}
\]

尚未产生，而且取决于：

\[
q_{t+1}
=
Agent(r_t,State_t)
\]

因此本研究关注的是：

\[
\boxed{
Cross\text{-}query\ physical\ optimization
under\ uncertain\ future\ consumers
}
\]

可以把传统 Query-Sequence Optimization 看作一种：

> **Perfect-Foresight Setting**

而 Agent trajectory 对应：

> **Imperfect but Partially Exposed Foresight Setting**

---

# 2.5 Predictive Query Processing / Predictive Physical Design：最直接的竞争方向

这一类工作与本研究在系统机制上最接近。

### PreView

PreView（2026）根据 historical workload 与 live query session 预测 future queries，包括其结构模式、发生概率以及预计到达时间：

\[
Q_{future}
=
\{
(z_j,p_j,\hat{\tau}_j)
\}
\]

然后选择未来收益最大的 materialized views：

\[
M^*
=
\arg\max_M
\sum_j
p_j Gain(z_j|M)
\]

同时考虑 storage budget 和 materialization-time budget，并在后续查询到达时自动 rewrite query 使用已物化结果。

这实际上已经实现了：

\[
Future\ Prediction
\rightarrow
Cost\text{-}Benefit\ Optimization
\rightarrow
Proactive\ Physical\ State
\]

因此，PreView 是目前与本研究“Future Access Estimator + Trajectory Optimizer”架构最直接的传统相关工作之一。

### 与本研究的区别

PreView 的 future information 主要来自：

\[
Historical\ workload
+
Recent\ query\ behavior
\]

本研究希望研究另一种新的 future information source：

\[
\boxed{
Agent\text{-}Side\ Foresight
}
\]

即：

\[
AgentGoal
+
AgentState
+
CandidateActions
+
ObservedResults
+
QueryHistory
\]

因此二者的核心区别不是：

> 一个预测 future，一个不预测 future。

而是：

### Existing Predictive Systems

\[
Observed\ Behavior
\rightarrow
Infer\ Future
\]

### 本研究

\[
Agent\ Exposed\ Intent
+
Observed\ Behavior
\rightarrow
Calibrated\ Future\ Access\ Belief
\]

这使本研究的核心问题从单纯的 **future-query prediction** 转变为：

> **Agent–DB cooperative future-aware optimization。**

---

# 2.6 Agentic Data Systems：知道 Agent，但优化对象不同

近两年已经出现了一批面向 Agentic Analytics / Agentic Query Processing 的系统。

### AgenticData

AgenticData 将自然语言分析问题转换成由 relational operators 与 semantic operators 组成的计划，并通过 multi-agent collaboration 和 semantic optimization 执行 heterogeneous analytics。

### Cost-Aware Optimization for Agentic Query Execution

该工作明确提出 agent workflow optimization 可以成为 classical query optimization 在 Agent 场景下的对应物，并联合优化 LLM-backed operator 的类型、位置、粒度和 execution paradigm，同时考虑 execution cost 与 answer quality。

### Lumilake

Lumilake 更进一步提出：

> 在 agentic analytics 中，fundamental unit of computation 不再是单条 SQL，而是 agentic workflow。

它把 SQL query、object fetch、LLM/VLM invocation 和 sub-agent interaction 组织成 first-class workflow DAG，并优化 KV-cache reuse、heterogeneous scheduling 和 cross-tenant deduplication。

### 与本研究的区别

这些工作认识到了：

\[
Agent
\rightarrow
larger\ optimization\ scope
\]

但其主要优化对象通常是：

\[
One\ Agentic\ Workflow
\]

或者：

\[
Relational/Semantic/LLM\ Operators
\]

本研究则关注一个不同的系统问题：

\[
SQL_1
\rightarrow Agent
\rightarrow SQL_2
\rightarrow Agent
\rightarrow SQL_3
\]

其中 DBMS 希望主动维护：

\[
Cross\text{-}Query\ Physical\ State
\]

包括：

\[
Materialized\ Results,
Cached\ Intermediates,
Prefetched\ Data,
Ephemeral\ Indexes,\ldots
\]

因此本研究并不优化 Agent 应该“想什么”或“执行哪个语义 operator”，而是优化：

> **面对 Agent 可能产生的后续数据访问，DBMS 现在应该准备什么。**

---

# 3. 从 Landscape 进一步抽象：数据库获取“未来信息”的四种优化范式

前述六类工作看起来分散，但如果从一个更本质的问题出发：

> **数据库在做当前决策时，对未来 workload 到底知道什么？**

它们可以统一成四种范式。

---

## 3.1 Current-Query Optimization：无 Future Information

传统 query optimizer 的输入主要是：

\[
Current\ Query
+
Schema
+
Statistics
+
Physical\ Design
\]

数据库回答：

\[
\boxed{
What\ is\ the\ cheapest\ way
to\ execute\ the\ current\ query?
}
\]

特点是：

\[
Future\ Visibility = None
\]

因此系统主要是 reactive：

\[
Query\ arrives
\rightarrow
Optimize
\rightarrow
Execute
\]

---

## 3.2 Known-Future Optimization：Future Query 可直接观察

MQO、Query-Sequence Optimization、procedural SQL optimization 等属于这一范式。

系统已经能够观察：

\[
q_{t+1},q_{t+2},\ldots
\]

因此回答：

\[
\boxed{
Given\ the\ upcoming\ workload,
how\ should\ execution\ be\ shared?
}
\]

这里 future information 是：

\[
Explicit + Deterministic
\]

因此可以称为：

\[
\boxed{
Known\text{-}Future\ Optimization
}
\]

---

## 3.3 Inferred-Future Optimization：从历史行为推断未来

EDA、ForeCache、HAWC、SparkCruise、PreView 等更接近：

\[
W_{past}
\rightarrow
P(W_{future}|W_{past})
\]

系统不知道 future query，但根据：

- historical workload；
- current session；
- past user interactions；
- recent query templates；

预测未来。

因此其 future information 是：

\[
Implicit + Probabilistic
\]

可以统一称为：

\[
\boxed{
Inferred\text{-}Future\ Optimization
}
\]

或者：

\[
Behavior\text{-}Driven\ Future\ Optimization
\]

---

## 3.4 Exposed-Future Optimization：未来 Query 未知，但 Intent 可见

Agent workload 引入了一种不同的信息状态。

未来 SQL：

\[
q_{t+1}
\]

仍然未知。

但是生成这些 SQL 的 workload generator 不再完全是黑盒。

Agent 可以潜在地暴露：

\[
Goal
\]

\[
Plan
\]

\[
Stage
\]

\[
Hypothesis
\]

\[
CandidateActions
\]

甚至：

\[
CandidateFutureDataAccess
\]

因此出现一种新的信息条件：

\[
\boxed{
Query\ Unknown,\ Intent\ Visible
}
\]

数据库可以从：

\[
P(W_{future}|W_{past})
\]

升级到：

\[
P(
W_{future}
|
W_{past},
R_{past},
AgentIntent
)
\]

这一范式可以称为：

\[
\boxed{
Exposed\text{-}Future\ Optimization
}
\]

更强调系统协同时，也可以称为：

\[
\boxed{
Agent\text{-}DB\ Cooperative\ Optimization
}
\]

这里最重要的变化不是简单地增加了一个 predictor，而是：

> **future workload information 第一次可以由 workload generator 主动提供，而不必完全由数据库根据过去行为反向猜测。**

---

# 4. 从数据库优化范式演进来看：Reactive → Predictive → Cooperative

上述四种范式还可以进一步抽象成数据库优化能力的一条演进路径。

### 第一阶段：Reactive

\[
Current\ Query
\rightarrow
Optimize
\]

数据库知道：

> **What am I querying now?**

对应传统 Query Optimization。

---

### 第二阶段：Predictive

\[
Past\ Behavior
\rightarrow
Predict\ Future
\rightarrow
Prepare
\]

数据库开始回答：

> **Based on what happened before, what may happen next?**

对应：

- History-Aware Optimization；
- EDA；
- ForeCache；
- SparkCruise；
- PreView。

---

### 第三阶段：Cooperative

\[
Agent\ Intent
+
Observed\ Trajectory
\rightarrow
Future\ Workload\ Belief
\rightarrow
DB\ Physical\ Preparation
\]

数据库开始回答：

> **Given what the workload generator intends to do next, what should I prepare now?**

因此整个研究演进可以概括为：

\[
\boxed{
Reactive
\rightarrow
Predictive
\rightarrow
Cooperative
}
\]

同时也是：

\[
\boxed{
Current
\rightarrow
History
\rightarrow
Intent
}
\]

本研究希望探索的正是第三种状态。

---

# 5. 综合对比：本研究在相关工作中的位置

下面的表不再简单比较“有没有多个 query”，而是围绕决定研究本质的几个维度进行区分。

| 比较维度 | Traditional Query Optimization | MQO / Known Query Sequence | History-Aware Reuse | Interactive / Predictive Exploration | Agentic Query / Workflow Systems | **本研究：Agent-Aware Trajectory Optimization** |
|---|---|---|---|---|---|---|
| **主要优化单元** | 单条 Query | Query batch / 已知 sequence | Query history + current query | Interactive session / future access | Agentic plan / workflow | **Evolving Agent query trajectory** |
| **未来具体 Query 是否可见** | ✗ | **✓** | ✗ | ✗ | △，取决于 workflow | **✗** |
| **未来访问是否可预测** | ✗ | 不需要预测 | △，从历史 reuse pattern 推断 | **✓，从历史/交互行为预测** | △ | **✓** |
| **Future intent 是否直接可见** | ✗ | Query 本身已知，因此通常不需要 intent | ✗ | **✗，用户 intent 通常是黑盒** | △ / ✓ | **✓，作为核心输入** |
| **Workload generator 是否参与优化** | ✗ | ✗ | ✗ | 通常 ✗ | ✓，Agent 属于执行系统 | **✓，Agent 与 DB 显式协同** |
| **Future query 是否受当前结果影响** | 不考虑 | 通常已固定 | △ | **✓** | **✓** | **✓，核心 workload 特征** |
| **Future uncertainty 是否显式建模** | ✗ | ✗ | △ | ✓ | △ | **✓，作为优化问题的一部分** |
| **跨 Query 共享计算/结果** | ✗ | **✓** | **✓** | mechanism-specific | 通常不是核心 | **✓** |
| **主动创建 Future-Oriented Physical State** | ✗ | ✓ | △ / ✓ | ✓，通常针对特定机制 | △ | **✓，核心能力** |
| **物化结果 / Intermediate Reuse** | 当前 Query 内 | ✓ | **✓** | 部分 | △ | **✓** |
| **Prefetch** | execution-level | 部分 | 部分 | **✓** | 部分 | **✓** |
| **Ephemeral Physical Design / Index** | 现有 index selection | 部分，如 procedural SQL | 较少 | 较少 | 非核心 | **✓，潜在统一 action** |
| **多类 Physical State 的统一决策** | ✗ | △ | △ | 通常单机制 | ✗ | **目标：✓** |
| **核心 Future 信息来源** | 无 | **未来 Query 本身** | **Past Queries** | **Past Queries / User Behavior** | Agent workflow state | **Agent Intent + Trajectory Observation** |
| **信息状态** | No Future | **Known Future** | **Inferred Future** | **Inferred Future** | Agent-Aware | **Exposed but Uncertain Future** |
| **核心优化目标** | Current-query cost | Batch / sequence cost | Future query reuse benefit | Interactive latency | Quality / workflow cost | **Expected trajectory-level DB cost** |

这张表中最关键的并不是“我们这一列 ✓ 最多”，而是前三个关于未来信息的维度：

\[
\text{Future Query Visibility}
\]

\[
\text{Future Predictability}
\]

以及：

\[
\boxed{\text{Future Intent Visibility}}
\]

它们定义了本研究与已有工作的根本信息条件差异。

---

# 6. 一个更凝练的二维定位

从两个维度可以进一步定位这些工作。

第一维：

\[
\textbf{Future Query Visibility}
\]

即未来查询是：

\[
Unknown
\rightarrow
Known
\]

第二维：

\[
\textbf{Workload Generator Visibility}
\]

即产生 workload 的主体是：

\[
Black\text{-}Box
\rightarrow
Intent\ Visible
\]

那么不同方向大致处于：

```text
                     Future Query
                 Unknown ←────────→ Known

 Black-box       EDA / PreView       MQO
 workload        SparkCruise         Query Sequence
 generator       HAWC                Procedural SQL


 Intent          ★ Our Work          Agent plan with
 visible         Agent intent +      fully exposed workflow
 generator       uncertain query
```

这里本研究对应的是一个比较特殊的信息条件：

\[
\boxed{
Future\ Query\ Unknown
+
Future\ Intent\ Partially\ Visible
}
\]

也可以进一步凝练为：

\[
\boxed{
Query\ Unknown,\ Intent\ Visible
}
\]

这可能是整个研究最重要的 conceptual distinction。

---

# 7. 本研究真正应该强调的三个差异

综合前述工作后，本研究不宜再简单声称：

> “我们第一次从 query-level 扩展到了 trajectory-level。”

因为 MQO、session optimization、EDA 和 query-sequence optimization 已经不同程度突破了单 query scope。

更准确的研究差异可以概括为三个方面。

### 7.1 Future Intent Is Exposed Rather Than Only Inferred

已有 predictive systems 主要通过：

\[
Past\ Queries
\rightarrow
Predict\ Future
\]

本研究希望进一步利用：

\[
Agent\ Goal
+
Agent\ Plan
+
Candidate\ Actions
\]

即 future workload producer 自身提供的 foresight。

核心变化为：

\[
\boxed{
Behavior\text{-}Driven
\rightarrow
Intent\text{-}Augmented
}
\]

---

### 7.2 Future Queries Remain Uncertain and Result-Dependent

本研究又不同于 MQO 与 Query-Sequence Optimization。

虽然 Agent 可以暴露未来 intent，但它并不能保证真正产生某条具体 SQL。

因为：

\[
q_{t+1}
=
Agent(
r_t,
State_t
)
\]

执行结果可能导致 Agent 改变方向。

因此：

\[
Agent\ Hint
\neq
Future\ Query
\]

数据库面对的是：

\[
\boxed{
Probabilistic\ Future\ Workload
}
\]

而不是 deterministic future workload。

---

### 7.3 DBMS Proactively Manages Cross-Query Physical State

本研究的最终贡献不应只是：

> “预测 Agent 下一条 SQL。”

而应该是：

> 将 Agent-side foresight 转换成 DBMS 内部可执行的 physical optimization decision。

即：

\[
Agent\ Intent
\]

\[
\downarrow
\]

\[
Future\ Access\ Belief
\]

\[
\downarrow
\]

\[
Trajectory\ Optimizer
\]

\[
\downarrow
\]

\[
\{
Retain,
Materialize,
Prefetch,
Index,
Evict
\}
\]

真正新的系统 abstraction 是：

\[
\boxed{
Agent\text{-}Aware\ Cross\text{-}Query
Physical\ State\ Management
}
\]

---

# 8. 推荐的 Related Work 总体组织方式

正式论文中，可以将 Related Work 收敛为三个 subsection。

## 8.1 Cross-Query and Workload-Level Optimization

包含：

- Multi-Query Optimization；
- shared sub-expression；
- intermediate result reuse；
- HAWC；
- HashStash；
- query sequence；
- procedural SQL optimization；
- physical design。

核心评价：

> 已有工作证明跨查询信息可以显著改善 query processing，但其 future information 通常来自已知 query workload 或已经发生的 workload。

---

## 8.2 Interactive and Predictive Query Processing

包含：

- Exploratory Data Analysis；
- interactive analytics；
- ForeCache；
- SparkCruise；
- PreView。

核心评价：

> 已有工作已经能够在 future query unknown 的条件下进行预测性优化，但通常需要通过历史 query 或用户交互行为推断未来访问意图。

---

## 8.3 Agentic Data Systems

包含：

- AgenticData；
- Lumilake；
- Cost-Aware Agentic Query Execution；
- 其他 Agentic Analytics / Agentic DB systems。

核心评价：

> 已有 Agentic Data Systems 已认识到 Agent workload 需要突破传统单-query execution abstraction，但目前主要关注 Agent workflow、semantic operator 和 LLM execution，而不是利用 Agent 暴露的 future intent 主动管理连续 SQL 之间的 DB physical state。

因此本研究位于三者交叉位置：

\[
\boxed{
Cross\text{-}Query\ Optimization
}
\]

\[
+
\]

\[
\boxed{
Predictive\ Query\ Processing
}
\]

\[
+
\]

\[
\boxed{
Agentic\ Data\ Systems
}
\]

最终形成：

\[
\boxed{
Agent\text{-}Aware\
Trajectory\text{-}Level\
Query\ Processing
}
\]

---

# 9. 推荐的研究定位表述

经过上述 related work 对比后，不建议把本研究简单表述为：

> “Existing databases optimize individual queries, while we optimize trajectories.”

这一表述过强，也容易被 MQO、EDA、SparkCruise 和 Query-Sequence Optimization 反驳。

更准确的英文定位可以表述为：

> Existing database systems exploit cross-query information either when future queries are already available or by inferring likely future accesses from historical workload behavior. Agentic workloads introduce a distinct information regime: while concrete future queries remain unknown and depend on intermediate results, the workload generator itself can expose machine-readable task context, evolving intent, and candidate future data actions before those queries are issued. We study how a DBMS can exploit such agent-side foresight, together with observed trajectory feedback, to proactively manage cross-query physical state and minimize expected trajectory-level execution cost.

对应中文为：

> **现有数据库跨查询优化方法主要存在两种未来信息来源：一类直接利用已经可见的后续查询，另一类根据历史查询或用户交互行为推断未来访问。Agent 工作负载带来了第三种不同的信息条件：具体的未来查询仍然未知，并受到中间查询结果的动态影响，但作为工作负载生成者的 Agent 可以在这些查询真正产生之前暴露机器可读的任务上下文、当前意图和候选数据访问行为。本研究关注数据库如何联合利用这种 Agent 侧前瞻信息与已经观测到的查询轨迹，主动管理跨查询物理状态，从而最小化整个 Agent 查询轨迹的期望执行成本。**

---

# 10. 最核心的概念总结

如果将整个 Related Work 的区别最后浓缩成一句话，可以表述为：

\[
\boxed{
\textbf{Existing systems either know the future or infer the future;
Agentic workloads allow the future intent to be exposed.}
}
\]

进一步对应三个优化范式：

\[
Known\ Future
\quad\rightarrow\quad
Inferred\ Future
\quad\rightarrow\quad
Exposed\ Future
\]

以及数据库系统能力的演进：

\[
Reactive
\quad\rightarrow\quad
Predictive
\quad\rightarrow\quad
Cooperative
\]

本研究真正希望探索的并不是“Agent 产生了更多相关 SQL”，而是一个新的数据库优化信息条件：

\[
\boxed{
Query\ Unknown,\ Intent\ Visible
}
\]

以及由此带来的新问题：

> **当未来具体查询仍然未知，但数据库能够提前观察 workload generator 的未来意图时，应当如何进行面向整个 Agent trajectory 的 proactive query processing and physical-state optimization？**