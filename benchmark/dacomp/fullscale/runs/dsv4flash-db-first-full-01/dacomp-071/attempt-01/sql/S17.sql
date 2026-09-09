WITH stage_order AS (
    SELECT DISTINCT stage_id, stage,
           CAST(SUBSTR(stage_id, 8) AS INTEGER) AS stage_num
    FROM lever__opportunity_stage_history
),
stage_entries AS (
    SELECT stage_id, stage, opportunity_id, archive_reason, days_in_stage
    FROM lever__opportunity_stage_history
),
-- For each opportunity, find the max stage_num they reached
opp_max_stage AS (
    SELECT opportunity_id, MAX(CAST(SUBSTR(stage_id, 8) AS INTEGER)) AS max_stage_num
    FROM lever__opportunity_stage_history
    GROUP BY opportunity_id
),
-- Per stage: count entries, advanced, attrited, proceeding
stage_stats AS (
    SELECT 
        e.stage_id,
        e.stage,
        CAST(SUBSTR(e.stage_id, 8) AS INTEGER) AS stage_num,
        COUNT(DISTINCT e.opportunity_id) AS total_entries,
        ROUND(AVG(e.days_in_stage), 1) AS avg_days,
        -- Count candidates who advanced (have a later stage)
        COUNT(DISTINCT CASE WHEN o.max_stage_num > CAST(SUBSTR(e.stage_id, 8) AS INTEGER) THEN e.opportunity_id END) AS advanced,
        -- Count candidates who are at their terminal stage with a negative reason (attrition)
        COUNT(DISTINCT CASE WHEN o.max_stage_num = CAST(SUBSTR(e.stage_id, 8) AS INTEGER) 
                             AND e.archive_reason NOT IN ('Advanced to next stage','Qualified','Proceeding','Hired')
                        THEN e.opportunity_id END) AS attrited,
        -- Count candidates still proceeding
        COUNT(DISTINCT CASE WHEN o.max_stage_num = CAST(SUBSTR(e.stage_id, 8) AS INTEGER) 
                             AND e.archive_reason = 'Proceeding'
                        THEN e.opportunity_id END) AS proceeding,
        -- Count candidates hired at this stage
        COUNT(DISTINCT CASE WHEN o.max_stage_num = CAST(SUBSTR(e.stage_id, 8) AS INTEGER) 
                             AND e.archive_reason = 'Hired'
                        THEN e.opportunity_id END) AS hired
    FROM stage_entries e
    LEFT JOIN opp_max_stage o ON e.opportunity_id = o.opportunity_id
    GROUP BY e.stage_id, e.stage
)
SELECT 
    stage_id,
    stage,
    total_entries,
    avg_days,
    advanced,
    attrited,
    proceeding,
    hired,
    ROUND(CAST(advanced AS REAL) / total_entries * 100, 1) AS pass_rate_pct,
    ROUND(CAST(attrited AS REAL) / total_entries * 100, 1) AS attrition_rate_pct,
    ROUND(CAST(advanced AS REAL) / NULLIF(total_entries - proceeding, 0) * 100, 1) AS resolved_pass_rate_pct,
    ROUND(CAST(attrited AS REAL) / NULLIF(total_entries - proceeding, 0) * 100, 1) AS resolved_attrition_rate_pct
FROM stage_stats
ORDER BY stage_num