# Data Dictionary

## Source files

| File | Grain | Key fields |
|---|---|---|
| `customers.csv` | One source customer record | `customer_id` |
| `products.csv` | One source product record | `product_id` |
| `orders.csv` | One order header | `order_id` |
| `order_items.csv` | One row per order line | `order_item_id`, `order_id`, `product_id` |

## Warehouse tables

- `stg_customers`, `stg_products`, `stg_orders`, `stg_order_items`: landed source records and ingestion metadata.
- `dim_customer`: one current customer record per business key; Type 1 overwrite strategy in this blueprint.
- `dim_product`: one current product record per product business key.
- `dim_date`: calendar attributes used for date-based reporting.
- `fact_sales`: order-line grain, with quantity, price, discount and net sales amount.
- `etl_reject`: invalid or unresolvable records with source, reason and run ID.
- `etl_batch_control`: batch status and row-count summary.

## Data-quality rules

Validate business keys, required values, parseable dates, positive quantity, non-negative price/discount, valid discount range, and referential integrity to products/orders/customers. Send failed rows to reject tracking with a clear reason.
