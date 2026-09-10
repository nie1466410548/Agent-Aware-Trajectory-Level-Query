Use db_query for every database query, including SQL for schema exploration.
Submit exactly one read-only SQLite statement and the latest future_access together.

Describe accesses that may occur AFTER the current SQL returns and before the task
ends, based only on the task, results already observed, and your existing plan.
Do not copy the current query as a prediction unless you actually anticipate
revisiting that access. Do not invent results that have not been returned yet.

Multiple candidates may all happen. Their order is neither a rank nor a schedule.
priority (high/medium/low) means importance to completing the task, not likelihood
or urgency. Optional likelihood (high/medium/low) means the chance of at least one
such access during the remaining task, taking trigger conditions into account.
Omit likelihood if uncertain; the levels are not calibrated numeric probabilities.

Each candidate needs known table names and priority. Supply columns, AND-connected
simple filters, equality joins, group_by and aggregations only when known. Use
actual table and column names, including spaces, not query aliases. Columns use
table.column form. Omission means unspecified, not absence or SELECT *.
Put result-dependent or unsupported details in short condition/unresolved fields;
never put a guessed placeholder into a concrete filter value.

Use status=provided with coverage=partial_plan (or remaining_task if your existing
plan covers the remainder) and at least one candidate. Each call REPLACES the old
set. Use status=unknown with candidates=[] when unable to predict. Use
status=no_further_access with candidates=[] when you currently expect no further
database calls; this does not end the task or prevent a later query. Omit coverage
for these two empty statuses. The horizon is the remaining task, not the next query.

At most {max_candidates} candidates, at most 200 characters per condition or
unresolved item, and at most 8 unresolved items per candidate. Do not fill a quota
or generate a separate long planning narrative. Do not add queries or change the
analysis to support a hint. Predictions are revisable descriptions, not commitments.
Continue solving the original task according to actual results.
