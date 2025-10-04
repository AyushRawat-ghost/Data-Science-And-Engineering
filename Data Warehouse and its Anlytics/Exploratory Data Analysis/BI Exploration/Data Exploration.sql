-- understand the scope of date and boundaries of it
-- find the date of first and last date (order date,shipping date, due date)
SELECT
MIN(order_date) as first_order_date,
MAX(order_date) as last_order_date,
datediff(month,min(order_date),max(order_date)) as order_range_months
from gold.fact_sales;


SELECT
MIN(shipping_date) as first_shipping_date,
MAX(shipping_date) as last_shipping_date,
datediff(month,min(shipping_date),max(shipping_date)) as shipping_range_months
from gold.fact_sales;


SELECT
MIN(due_date) as first_due_date,
MAX(due_date) as last_due_date,
datediff(month,min(due_date),max(due_date)) as due_range_months
from gold.fact_sales;


-- Find the youngest and oldest customer
SELECT
MIN(birthdate) as oldest,
datediff(year,min(birthdate),getdate()) as oldest_age,
MAX(birthdate) as youngest,
datediff(year,max(birthdate),getdate()) as youngest_age
FROM gold.dim_customer;
