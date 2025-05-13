-- most demanding skills for Data Analyst
select
    skills,COUNT(skills_job_dim.job_id) as demand_count
from
    job_postings_fact
inner join skills_job_dim on job_postings_fact.job_id=skills_job_dim.job_id 
INNER JOIN skills_dim on skills_job_dim.skill_id=skills_dim.skill_id 
WHERE
    job_title_short='Data Analyst'
    AND
    job_country='India'
group BY
    skills
order BY
    demand_count DESC
LIMIT 10;