
SELECT DISTINCT i.application_id, i.interview_id, i.interviewer_user_id,
       i.technical_score, i.problem_solving_score, i.communication_score,
       i.culture_fit_score, i.leadership_score, i.overall_recommendation,
       i.candidate_gender, i.candidate_race, i.candidate_disability_status, i.candidate_veteran_status,
       i.interviewer_gender, i.interviewer_level, i.interviewer_experience_years,
       i.interview_time_of_day, i.interview_day_of_week, i.interview_season,
       i.interview_duration_minutes, i.interviewer_is_hiring_manager,
       i.follow_up_questions_count, i.interviewer_satisfaction
FROM greenhouse__interview_enhanced i
WHERE i.technical_score IS NOT NULL
