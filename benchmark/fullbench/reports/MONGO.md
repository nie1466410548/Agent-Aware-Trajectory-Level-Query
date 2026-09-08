# MongoDB 原生查询

**进度：108/108 次运行已结束。全量运行已结束。**

Mongo 请求独立记录，不计入 SQL 表。集合重访按同任务同库此前成功原生数据请求去重；集合名相同不代表计算可复用。

| 任务 | 组 | 成功数据请求 | 失败数据请求 | 集合元数据请求 | 重访集合的后续请求 | 原始日志 |
|---|---|---:|---:|---:|---:|---|
| agnews/query1 | fad | 5 | 1 | 1 | 4 | [日志](../runs/fad/agnews/query1/full-01/tool_calls.jsonl) |
| agnews/query2 | fad | 7 | 0 | 1 | 6 | [日志](../runs/fad/agnews/query2/full-01/tool_calls.jsonl) |
| agnews/query3 | fad | 3 | 0 | 1 | 2 | [日志](../runs/fad/agnews/query3/full-01/tool_calls.jsonl) |
| agnews/query4 | fad | 5 | 0 | 1 | 4 | [日志](../runs/fad/agnews/query4/full-01/tool_calls.jsonl) |
| yelp/query1 | fad | 2 | 0 | 1 | 1 | [日志](../runs/fad/yelp/query1/full-01/tool_calls.jsonl) |
| yelp/query2 | fad | 2 | 0 | 1 | 1 | [日志](../runs/fad/yelp/query2/full-01/tool_calls.jsonl) |
| yelp/query3 | fad | 4 | 0 | 1 | 3 | [日志](../runs/fad/yelp/query3/full-01/tool_calls.jsonl) |
| yelp/query4 | fad | 2 | 0 | 1 | 1 | [日志](../runs/fad/yelp/query4/full-01/tool_calls.jsonl) |
| yelp/query5 | fad | 3 | 0 | 1 | 2 | [日志](../runs/fad/yelp/query5/full-01/tool_calls.jsonl) |
| yelp/query6 | fad | 3 | 0 | 0 | 2 | [日志](../runs/fad/yelp/query6/full-01/tool_calls.jsonl) |
| yelp/query7 | fad | 2 | 0 | 1 | 1 | [日志](../runs/fad/yelp/query7/full-01/tool_calls.jsonl) |
| agnews/query1 | natural | 9 | 0 | 1 | 8 | [日志](../runs/natural/agnews/query1/full-01/tool_calls.jsonl) |
| agnews/query2 | natural | 4 | 0 | 1 | 3 | [日志](../runs/natural/agnews/query2/full-01/tool_calls.jsonl) |
| agnews/query3 | natural | 5 | 0 | 1 | 4 | [日志](../runs/natural/agnews/query3/full-01/tool_calls.jsonl) |
| agnews/query4 | natural | 5 | 0 | 1 | 4 | [日志](../runs/natural/agnews/query4/full-01/tool_calls.jsonl) |
| yelp/query1 | natural | 2 | 0 | 1 | 1 | [日志](../runs/natural/yelp/query1/full-01/tool_calls.jsonl) |
| yelp/query2 | natural | 2 | 0 | 1 | 1 | [日志](../runs/natural/yelp/query2/full-01/tool_calls.jsonl) |
| yelp/query3 | natural | 2 | 0 | 1 | 1 | [日志](../runs/natural/yelp/query3/full-01/tool_calls.jsonl) |
| yelp/query4 | natural | 4 | 0 | 1 | 3 | [日志](../runs/natural/yelp/query4/full-01/tool_calls.jsonl) |
| yelp/query5 | natural | 3 | 0 | 0 | 2 | [日志](../runs/natural/yelp/query5/full-01/tool_calls.jsonl) |
| yelp/query6 | natural | 3 | 0 | 0 | 2 | [日志](../runs/natural/yelp/query6/full-01/tool_calls.jsonl) |
| yelp/query7 | natural | 3 | 0 | 1 | 2 | [日志](../runs/natural/yelp/query7/full-01/tool_calls.jsonl) |
