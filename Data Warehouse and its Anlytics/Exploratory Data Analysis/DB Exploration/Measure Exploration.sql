-- find the total sales
select sum(sales_amount) as total_sales from gold.fact_sales;
go

-- find how many items are sold
select SUM(quantity) as total_quantity from gold.fact_sales;
go

-- find avg selling price
SELECT AVG(price) as avg_price from gold.fact_sales;
go

-- Total num of orders
SELECT count(order_number) as total_order from gold.fact_sales;
go
SELECT COUNT(DISTINCT order_number) as total_order from gold.fact_sales;
go

-- Total num of products
SELECT COUNT(product_name) as total_products from gold.dim_products
go
SELECT COUNT(Distinct product_name) as total_products from gold.dim_products
go
-- Total num of customers

select count(customer_key) as total_customers from gold.dim_customer;-- Total num of customer that placed orders
go
select count(distinct customer_key) as total_customers from gold.fact_sales;
go


-- Generate a Report that shows all key metrics of the business
SELECT 'Total Sales' AS measure_name, SUM(sales_amount) AS measure_value FROM gold.fact_sales
UNION ALL
SELECT 'Total Quantity', SUM(quantity) FROM gold.fact_sales
UNION ALL
SELECT 'Average Price', AVG(price) FROM gold.fact_sales
UNION ALL
SELECT 'Total Orders', COUNT(DISTINCT order_number) FROM gold.fact_sales
UNION ALL
SELECT 'Total Products', COUNT(DISTINCT product_name) FROM gold.dim_products
UNION ALL
SELECT 'Total Customers', COUNT(customer_key) FROM gold.dim_customer;