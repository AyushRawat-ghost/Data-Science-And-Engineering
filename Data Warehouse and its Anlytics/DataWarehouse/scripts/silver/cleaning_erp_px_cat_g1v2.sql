insert into silver.erp_px_cat_g1v2 (id,cat,subcat,maintenance
)
select
id,
cat,
subcat,
maintenance
from bronze.erp_px_cat_g1v2;