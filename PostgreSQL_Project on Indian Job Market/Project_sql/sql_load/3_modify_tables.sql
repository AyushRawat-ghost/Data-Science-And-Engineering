




-- pgadmin commands
\copy company_dim FROM 'C:\Users\Ayush\OneDrive\Work Directory\computing\Data Science\Data_analyst\PostgreSQL_Project\all_folders\csv_files\company_dim.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');


\copy skills_dim FROM 'C:\Users\Ayush\OneDrive\Work Directory\computing\Data Science\Data_analyst\PostgreSQL_Project\all_folders\csv_files\skills_dim.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');


\copy job_postings_fact FROM 'C:\Users\Ayush\OneDrive\Work Directory\computing\Data Science\Data_analyst\PostgreSQL_Project\all_folders\csv_files\job_postings_fact.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');


\copy skills_job_dim FROM 'C:\Users\Ayush\OneDrive\Work Directory\computing\Data Science\Data_analyst\PostgreSQL_Project\all_folders\csv_files\skills_job_dim.csv' 
WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');