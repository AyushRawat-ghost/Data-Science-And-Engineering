INSERT INTO silver.erp_cust_az12 (cid,bdate,gen)
SELECT
case when cid like 'NAS%' THEN substring(cid,4,len(cid))
    ELSE cid
end cid,

CASE
    WHEN bdate > getdate() THEN NULL
    ELSE bdate
end bdate,

CASE
    WHEN upper(trim(gen)) IN ('F','FEMALE') THEN 'Female'
    WHEN upper(trim(gen)) IN ('M','MALE') THEN 'Male'
    ELSE  'n/a'
END gen
from bronze.erp_cust_az12;