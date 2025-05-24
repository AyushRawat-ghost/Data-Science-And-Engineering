with yearly_product_sales as(
select
year(f.order_date) as order_year,
p.product_name,
SUM(f.sales_amount) as current_sales

FROM gold.fact_sales f
LEFT JOIN gold.dim_products p
on f.product_key = p.product_key

WHERE f.order_date IS NOT NULL
GROUP BY
year(f.order_date),
p.product_name
)
select
order_year,
product_name,
current_sales,

AVG(current_sales) OVER (PARTITION BY product_name) as avg_sales,
current_sales - AVG(current_sales) OVER (PARTITION BY product_name) as diff_avg,
CASE
    WHEN current_sales - AVG(current_sales) OVER (PARTITION BY product_name) > 0 THEN 'Above Avg'
    WHEN current_sales - AVG(current_sales) OVER (PARTITION BY product_name) < 0 THEN 'Below Avg'
    ELSE 'Avg'
END avg_change,

lag(current_sales)OVER (PARTITION BY product_name ORDER BY order_year) as prev_sales,
current_sales-lag(current_sales)OVER (PARTITION BY product_name ORDER BY order_year) as diff_prev_sales,
CASE
    WHEN current_sales - lag(current_sales)OVER (PARTITION BY product_name ORDER BY order_year) > 0 THEN 'Increasing'
    WHEN current_sales - lag(current_sales)OVER (PARTITION BY product_name ORDER BY order_year) < 0 THEN 'Decreasing'
    ELSE 'Neutral'
END prev_year_change

FROM yearly_product_sales
ORDER BY product_name,order_year;