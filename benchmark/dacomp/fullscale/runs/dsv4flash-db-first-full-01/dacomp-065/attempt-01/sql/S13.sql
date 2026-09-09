SELECT MIN(technical_score) AS min_t, MAX(technical_score) AS max_t, AVG(technical_score) AS avg_t,
       MIN(problem_solving_score) AS min_p, MAX(problem_solving_score) AS max_p, AVG(problem_solving_score) AS avg_p,
       MIN(communication_score) AS min_c, MAX(communication_score) AS max_c, AVG(communication_score) AS avg_c,
       MIN(culture_fit_score) AS min_cf, MAX(culture_fit_score) AS max_cf, AVG(culture_fit_score) AS avg_cf,
       MIN(leadership_score) AS min_l, MAX(leadership_score) AS max_l, AVG(leadership_score) AS avg_l
FROM greenhouse__interview_enhanced