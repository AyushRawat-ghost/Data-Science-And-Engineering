CREATE VIEW gold.dim_customer AS
    SELECT
        row_number() over (order by cst_id) as customer_key,
        ci.cst_id as customer_id,
        ci.cst_firstname as first_name,
        ci.cst_lastname as last_name,
        la.cntry as country,
        
        ci.cst_marital_status as marital_status,
        CASE 
            WHEN ci.cst_gender!='n/a' THEN ci.cst_gender 
            ELSE  coalesce(ca.gen,'n/a')
        END as gender,
        
        ca.bdate as birthdate,
        ci.cst_create_date as create_date
    from silver.crm_cust_info ci
    
    LEFT JOIN silver.erp_cust_az12 ca
            ON ci.cst_key=ca.cid
    
    LEFT JOIN silver.erp_loc_a101 la
            ON ci.cst_key=la.cid;