-- Monthly net sales and order counts
SELECT d.year_num, d.month_num, d.month_name,
       SUM(f.net_sales_amount) AS net_sales,
       COUNT(DISTINCT f.order_id) AS orders,
       SUM(f.quantity) AS units_sold
FROM dw.fact_sales f
JOIN dw.dim_date d ON d.date_key = f.order_date_key
GROUP BY d.year_num, d.month_num, d.month_name
ORDER BY d.year_num, d.month_num;

-- Best-selling products by net sales
SELECT p.product_id, p.product_name, p.category,
       SUM(f.quantity) AS units_sold,
       SUM(f.net_sales_amount) AS net_sales
FROM dw.fact_sales f
JOIN dw.dim_product p ON p.product_key = f.product_key
GROUP BY p.product_id, p.product_name, p.category
ORDER BY net_sales DESC
LIMIT 10;

-- Customer lifetime value proxy (all-time net sales in this sample)
SELECT c.customer_id, c.first_name, c.last_name,
       COUNT(DISTINCT f.order_id) AS order_count,
       SUM(f.net_sales_amount) AS lifetime_net_sales
FROM dw.fact_sales f
JOIN dw.dim_customer c ON c.customer_key = f.customer_key
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY lifetime_net_sales DESC;

-- Reject monitoring
SELECT run_id, source_name, reason_code, COUNT(*) AS rejected_rows
FROM etl.reject
GROUP BY run_id, source_name, reason_code
ORDER BY run_id, source_name, reason_code;

-- Batch status monitoring
SELECT run_id, workflow_name, status, start_ts, end_ts,
       source_rows, loaded_rows, rejected_rows, message
FROM etl.batch_control
ORDER BY start_ts DESC;
