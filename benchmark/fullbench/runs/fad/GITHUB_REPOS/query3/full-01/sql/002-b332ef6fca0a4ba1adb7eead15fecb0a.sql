SELECT COUNT(*) AS n_repos FROM languages l JOIN licenses c ON l.repo_name = c.repo_name WHERE c.license = 'apache-2.0' AND l.language_description LIKE '%Shell (%'
