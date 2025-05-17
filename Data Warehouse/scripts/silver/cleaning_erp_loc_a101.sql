insert into silver.erp_loc_a101(cid,cntry)
SELECT
REPLACE(cid,'-','') as cid,

CASE
    WHEN upper(trim(cntry)) ='DE' THEN 'Germany'
    WHEN upper(trim(cntry)) IN ('USA','US') THEN 'United States'
    WHEN trim(cntry) ='' or cntry is NULL THEN 'n/a'
    ELSE trim(cntry)
END as cntry

from bronze.erp_loc_a101;