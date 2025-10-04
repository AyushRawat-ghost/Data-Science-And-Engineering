Drop Table silver.crm_prd_info;
go

CREATE Table silver.crm_prd_info(
    prd_id INT,
    cat_id nvarchar(50),
    prd_key nvarchar(50),
    prd_rm nvarchar(50),
    prd_cost INT,
    prd_line nvarchar(50),
    prd_start_dt Date,
    prd_end_dt date,
    dwh_create_date DateTime2 DEFAULT getdate()
);
go


insert into silver.crm_prd_info(
    prd_id,cat_id,prd_key,prd_rm,prd_cost,prd_line,prd_start_dt,prd_end_dt
)
SELECT
prd_id,
REPLACE(substring(prd_key,1,5),'-','_') as cat_id,
substring(prd_key,7,len(prd_key)) as prd_key,
prd_rm,
isnull(prd_cost,0) as prd_cost,

CASE upper(trim(prd_line))
    WHEN 'M' THEN 'Mountain'
    WHEN 'R' THEN 'Road'
    WHEN 'S' THEN 'other sales'
    WHEN 'T' THEN 'Touring'
    ELSE 'n/a'
END as prd_line,

cast (prd_start_dt as Date ) as prd_start_dt,
cast (lead(prd_start_dt) OVER (PARTITION BY prd_key ORDER BY prd_start_dt)-1 as date) as prd_end_dt
FROM bronze.crm_prd_info;
