-- Explore all  objects in the data base
select * from information_schema.TABLES;
go


-- Explore all columns in the Data Base
SELECT * from information_schema.columns
where TABLE_name='dim_customer';
go

SELECT * from information_schema.columns
where TABLE_name='dim_products';
go

SELECT * from information_schema.columns
where TABLE_name='fact_sales';
go

