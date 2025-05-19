-- Identifies unique values or categories in each dimension
-- Recognizing how data might be grouped or segmented which is useful for later analysis
-- Use distinct keywords for it

-- Explore all countries, customer cones
SELECT DISTINCT COUNTRY FROM GOLD.dim_customer;
go

-- explore categories and its related 
select distinct category,subcategory,product_name from gold.dim_products 
order by 1,2,3;
go

