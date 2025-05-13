-- What are top paying  jobs for Data Analyst

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
LIMIT 10;
