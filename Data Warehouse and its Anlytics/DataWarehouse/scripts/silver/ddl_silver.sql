/*
DDl Scripts : Create silver schemas Tables

Purpose :
    Creates all necessary Tables in silver Schema
    If tables already exist drop it

*/


-- Customer Info table from CRM folder
CREATE Table silver.crm_cust_info(
    cst_id INT,
    cst_key nvarchar(50),
    cst_firstname nvarchar(50),
    cst_lastname nvarchar(50),
    cst_marital_status nvarchar(50),
    cst_gender nvarchar(50),
    cst_create_date DATE,
    dwh_create_date DateTime2 DEFAULT getdate()
);
go

-- Customers Product Info from CRM folder
CREATE Table silver.crm_prd_info(
    prd_id INT,
    prd_key nvarchar(50),
    prd_rm nvarchar(50),
    prd_cost INT,
    prd_line nvarchar(50),
    prd_start_dt Datetime,
    prd_end_dt datetime,
    dwh_create_date DateTime2 DEFAULT getdate()
);
go

-- Customer Sales Details from CRM Folder
CREATE Table silver.crm_sales_details(
    sls_ord_num nvarchar(50),
    sls_prd_key nvarchar(50),
    sls_cust_id INT,
    sls_order_dt INT,
    sls_ship_dt INT,
    sls_due_dt INT,
    sls_sales INT,
    sls_quantity INT,
    sls_price INT,
    dwh_create_date DateTime2 DEFAULT getdate()
);
go


-- Location detail table from ERP folder
CREATE Table silver.erp_loc_a101(
    cid nvarchar(50),
    cntry nvarchar(50),
    dwh_create_date DateTime2 DEFAULT getdate()
);
go

-- Customer age info table from ERP folder
CREATE Table silver.erp_cust_az12(
    cid nvarchar(50),
    bdate DATE,
    gen nvarchar(50),
    dwh_create_date DateTime2 DEFAULT getdate()
);
go

-- Catalog table from ERP folder
CREATE Table silver.erp_px_cat_g1v2(
    id nvarchar(50),
    cat nvarchar(50),
    subcat nvarchar(50),
    maintenance nvarchar(50),
    dwh_create_date DateTime2 DEFAULT getdate()
);
go
