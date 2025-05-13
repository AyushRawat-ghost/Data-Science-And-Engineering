SELECT
    skills,round(AVG(salary_year_avg),0) as avg_salary
FROM
    job_postings_fact
inner JOIN skills_job_dim on job_postings_fact.job_id = skills_job_dim.job_id
INNER JOIN skills_dim on skills_job_dim.skill_id=skills_dim.skill_id
WHERE
        job_title_short='Data Analyst'
    AND
        salary_year_avg is not NULL
    AND
        job_country='India'
GROUP BY
    skills
ORDER BY
    avg_salary DESC
limit 20;