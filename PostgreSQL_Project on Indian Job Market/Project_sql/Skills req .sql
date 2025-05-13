-- what are top skills require for top paying Data Analyst?

-- method1

with top_paying_jobs as(
    select 
        job_id,job_title,job_location,job_schedule_type,salary_year_avg,job_posted_date 
    FROM 
        job_postings_fact 
    left join company_dim on job_postings_fact.company_id = company_dim.company_id 
    where
        job_title_short='Data Analyst' 
    and
        job_location='Anywhere' 
    and 
        salary_year_avg is not null 
    ORDER BY 
        salary_year_avg DESC LIMIT 10 
)
SELECT
    top_paying_jobs.*,skills 
from
    top_paying_jobs 
    inner join skills_job_dim on top_paying_jobs.job_id=skills_job_dim.job_id 
    INNER JOIN skills_dim on skills_job_dim.skill_id=skills_dim.skill_id 
    ORDER BY 
        salary_year_avg DESC,skills DESC;


-- method2

with top_paying_jobs as (
    select
        job_id,job_title,job_location,job_schedule_type,salary_year_avg,job_posted_date
    FROM
        job_postings_fact
    left join company_dim on job_postings_fact.company_id = company_dim.company_id
    where
            job_title_short='Data Analyst'
        and
            job_location='Anywhere'
        and
            salary_year_avg is not null
    ORDER BY
        salary_year_avg DESC
    LIMIT 10
)
SELECT 
    skills_dim.skills,count(*) as skill_count 
from 
    top_paying_jobs
inner join skills_job_dim on top_paying_jobs.job_id=skills_job_dim.job_id
INNER JOIN skills_dim on skills_job_dim.skill_id=skills_dim.skill_id
GROUP BY
    skills_dim.skills
ORDER BY
    skill_count DESC;

