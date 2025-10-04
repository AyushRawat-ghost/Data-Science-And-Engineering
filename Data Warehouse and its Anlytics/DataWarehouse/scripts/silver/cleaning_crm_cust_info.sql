/*
This script cleans up the customer Info table of bronze layer and insert data in silver layer customer info table
*/
INSERT INTO silver.crm_cust_info(
    cst_id,
    cst_key,
    cst_firstname,
    cst_lastname,
    cst_marital_status,
    cst_gender,
    cst_create_date)

select
    cst_id,
    cst_key,

-- removes whitespace from first and last name
    Trim(cst_firstname) AS cst_firstname,
    TRim(cst_lastname) AS cst_lastname,

-- converts Small abrevation to meaningful data and null to 'n/a'
    CASE
        WHEN upper(trim(cst_marital_status)) = 'S' THEN  'Single'
        WHEN upper(trim(cst_marital_status)) = 'M' THEN  'Married'
        ELSE 'n/a'
    END as cst_marital_status,
    CASE
        WHEN upper(trim(cst_gender)) = 'F' THEN  'Female'
        WHEN upper(trim(cst_gender)) = 'M' THEN  'Male'
        ELSE 'n/a'
    END as cst_gndr,
    cst_create_date
	FROM(
-- Removing duplicates and null from primary key : cst_id
        SELECT *, row_number() over (PARTITION BY cst_id ORDER BY cst_create_date DESC) as flag_last
        FROM bronze.crm_cust_info
        WHERE cst_id is NOT NULL
    )t WHERE flag_last=1;
go

SELECT * from silver.crm_cust_info;
