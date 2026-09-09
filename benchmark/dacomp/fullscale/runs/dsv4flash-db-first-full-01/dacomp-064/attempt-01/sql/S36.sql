-- Get all target stakeholders with their metrics
SELECT s.stakeholder_id, s.user_display_name, s.engagement_depth_score, s.engagement_breadth_score,
       s.engagement_quality_score, s.engagement_impact_score, s.total_engagement_score,
       s.issues_reported, s.issues_assigned, s.total_comments_authored,
       s.total_projects_involved, s.direct_network_connections,
       s.total_outbound_influence, s.total_inbound_influence,
       s.cross_functional_projects, s.strategic_value_score,
       s.response_pattern_type, s.stakeholder_archetype, s.influence_level,
       s.engagement_risk_status, s.recommended_engagement_strategy,
       s.development_opportunity,
       CASE WHEN s.issues_reported > 0 THEN s.issues_assigned * 1.0 / s.issues_reported ELSE NULL END AS assign_report_ratio,
       s.total_outbound_influence - s.total_inbound_influence AS influence_imbalance
FROM jira__stakeholder_engagement_insights s
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
ORDER BY s.total_engagement_score DESC