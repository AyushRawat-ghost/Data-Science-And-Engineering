drop Table silver.crm_sales_details;
go

CREATE Table silver.crm_sales_details(
    sls_ord_num nvarchar(50),
    sls_prd_key nvarchar(50),
    sls_cust_id INT,
    sls_order_dt DATE,
    sls_ship_dt DATE,
    sls_due_dt DATE,
    sls_sales INT,
    sls_quantity INT,
    sls_price INT,
    dwh_create_date datetime2 DEFAULT getdate()
);
go

INSERT into silver.crm_sales_details (
    sls_ord_num,sls_prd_key,sls_cust_id,sls_order_dt,sls_ship_dt,sls_due_dt,sls_sales,sls_quantity,sls_price
)
select
sls_ord_num,
sls_prd_key,
sls_cust_id,

case WHEN sls_order_dt = 0 OR len(sls_order_dt)!=8 then NULL
    ELSE cast(cast(sls_order_dt as varchar) as date)
end as sls_order_dt,

case WHEN sls_ship_dt = 0 OR len(sls_ship_dt)!=8 then NULL
    ELSE cast(cast(sls_ship_dt as varchar) as date)
end as sls_ship_dt,

case WHEN sls_due_dt = 0 OR len(sls_due_dt)!=8 then NULL
    ELSE cast(cast(sls_due_dt as varchar) as date)
end as sls_due_dt,

case when sls_sales is null or sls_sales <=0 or sls_sales != sls_quantity * abs(sls_price)
        then sls_quantity * abs(sls_price)
    else sls_sales
end as sls_sales,
sls_quantity,
case when sls_price is null or sls_price <=0 or sls_sales != sls_quantity * abs(sls_price)
        then sls_sales / nullif(sls_quantity,0)
    else sls_price
end as sls_price
FROM bronze.crm_sales_details;