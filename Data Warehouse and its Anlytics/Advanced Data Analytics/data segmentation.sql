-- product segmentation
with product_segments as(
    SELECT
        product_key,
        product_name,
        cost,
        CASE
            WHEN cost<100 THEN 'Below 100'
            WHEN cost BETWEEN 100 and 500 THEN '100-500' 
            WHEN cost BETWEEN 500 and 1000 THEN '500-1000' 
            ELSE 'above 1000'
        END as cost_range
    FROM gold.dim_products
)
SELECT
    cost_range,
    COUNT(product_key) as total_products
FROM product_segments
GROUP BY cost_range
ORDER BY total_products DESC;
go




-- customer segmentation
with customer_spending as(
    SELECT 
        c.customer_key,
        SUM(f.sales_amount) as total_spending,
        MIN(order_date) as first_order,
        max(order_date) as last_order,
        datediff(month,MIN(order_date),MAX(order_date)) as lifespan

    from gold.fact_sales f
    LEFT JOIN gold.dim_customer c
        ON f.customer_key = c.customer_key
    GROUP BY c.customer_key
)
SELECT
    customer_segment,
    COUNT(customer_key) as total_customers
FROM (
    SELECT
        customer_key,
        CASE
            WHEN lifespan>=12 and total_spending>5000 THEN 'VIP' 
            WHEN lifespan>=12 and total_spending<=5000 THEN 'Regular' 
            ELSE  'New'
        END as customer_segment
        from customer_spending
) as segmented_customers
GROUP BY customer_segment
ORDER BY total_customers DESC;