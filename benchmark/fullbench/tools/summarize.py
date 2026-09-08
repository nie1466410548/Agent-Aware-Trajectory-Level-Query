"""Final findings; refuses to label a partial cohort complete."""
import collections,json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 tasks=json.loads((ROOT/'tasks.json').read_text())['tasks'];expected=2*sum(map(len,tasks.values()))
 a=json.loads((ROOT/'reports/analysis.json').read_text());raw=json.loads((ROOT/'reports/overlap-detail.json').read_text());op=json.loads((ROOT/'reports/opportunities.json').read_text())
 assert len(a['runs'])==len(raw['runs'])==expected,'Cohort is not complete'
 assert {(r['task_id'],r['group']) for r in a['runs']}=={(f'{d}/query{i}',g) for d,ids in tasks.items() for i in ids for g in ['natural','fad']}
 lines=['# 全量 DAB 轨迹实验：结论','',f'正式清单的 {sum(map(len,tasks.values()))} 个任务、自然/FAD 两组，共 {expected} 次运行均已结束。结束不等于解题成功，超时和验证失败均保留。原 9 题试跑不混入本组。','',
 '| 指标 | 自然组 | FAD 组 |','|---|---:|---:|']
 groups={g:[r for r in a['runs'] if r['group']==g] for g in ['natural','fad']}
 def metric(label,fn):lines.append('| '+label+' | '+' | '.join(str(fn(groups[g])) for g in groups)+' |')
 metric('原始验证器通过',lambda rs:sum(r['validator_passed'] for r in rs))
 metric('超时结束',lambda rs:sum(r['timed_out'] for r in rs))
 metric('成功数据 SQL 调用',lambda rs:sum(r['successful_data_queries'] for r in rs))
 metric('失败数据 SQL 尝试',lambda rs:sum(r['failed_data_queries'] for r in rs))
 metric('Mongo 数据请求（含失败）',lambda rs:sum(r['mongo_queries'] for r in rs))
 metric('assistant 消息轮数中位数',lambda rs:statistics.median(r['assistant_turns'] for r in rs))
 metric('运行时长中位秒数',lambda rs:round(statistics.median(r['duration_s'] for r in rs),1))
 lines+=['','## 如何使用分析结果','',
 '先看 [OVERLAP.md](OVERLAP.md) 的逐任务查询表，列定义已附上：这些是实际访问、结构或输出重复，不是可省掉的查询数量。Mongo 请求另表统计，不混成 SQL。','',
 '再看公共准备候选表与 [逐对象证据](OPPORTUNITY_CASES.md)。筛选要求同一基表同一条件；Join 要求相同输入、类型和键；聚合状态要求 FROM、WHERE、GROUP BY 全部相同。派生计算还需保留求值范围、NULL 和异常语义。不同对象可能是同一优化的替代方案，不能把类型计数直接相加当成独立收益。','',
 '自然组 CRM query7 的首次尝试发生目录/记录错位，已归档排除并单独恢复。v2 适配器绑定任务目录；版本与恢复过程见 README 和 ERRORS。', '',
 '所有机会来自完整轨迹的事后静态识别，未实施物化/索引，未验证改写结果等价或净加速。包含未通过任务中的探索调用，不能证明正确解题路径必然需要这些工作。未支持的复杂作用域也不等于不存在机会。','',
 'FAD 是显式协作干预，会改变查询选择并增加模型/工具开销。下一步描述与后续选择一致不能证明自然 Agent 的被动可预测性，也不能将 FAD 到请求提交的时间间隔当作免费的准备窗口。[FAD 分项统计](FAD.md) 单列 SQL/Mongo 并保留预测分母。','',
 '## 完整材料','',
 '- [逐任务统计、定义与候选覆盖](OVERLAP.md)',
 '- [SQL/请求级候选及原文链接](OPPORTUNITY_CASES.md)',
 '- [运行结果、轮数、时间、超时](RUNS.md)',
 '- [MongoDB 原生请求](MONGO.md)',
 '- [数据库位置、行数和字段](DATA.md)',
 '- [失败、解析覆盖与协议偏离](ERRORS.md)',
 '- [结果文件及导出完整性校验](artifact-audit.json)',
 '- [机器可读逐查询/配对](overlap-detail.json)、[候选](opportunities.json)、[逐任务 CSV](task-overlap.csv)',
 '- [运行配置及复算说明](../README.md)',
 '', '实际 SQL、完整工具响应、逐语句结果、Python 源码、可见 Kimi 消息和最终答案位于 runs/GROUP/DATASET/queryN/full-01。绕过 Python 适配器但可见于 Bash 消息的代码在审核后单独提取，并明确标为协议偏离。']
 (ROOT/'reports/FINDINGS.md').write_text('\n'.join(lines)+'\n')
 print('Final findings rendered')
if __name__=='__main__':main()
