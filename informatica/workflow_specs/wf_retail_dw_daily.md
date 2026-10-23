# Workflow: `wf_retail_dw_daily`

**Purpose:** Orchestrate the daily load from flat-file extracts to the retail warehouse.

## Suggested task sequence

1. `s_start_batch` — create batch-control row and record run ID.
2. `s_load_stg_customers` and `s_load_stg_products` — stage master data (parallel where appropriate).
3. `s_load_stg_orders` — stage order headers after customers are staged.
4. `s_load_stg_order_items` — stage order lines after orders/products are available.
5. `s_load_dim_customer_scd1` — load customer dimension.
6. `s_load_dim_product` — load product dimension.
7. `s_load_dim_date` — ensure required dates exist in date dimension.
8. `s_load_fact_sales` — load validated, non-cancelled order lines.
9. `s_reconcile_batch` — compare input, staged, loaded, and rejected row counts.
10. `s_finish_batch` — mark batch succeeded; failure links should mark batch failed and preserve session logs.

## Operational controls

- Use parameterized source paths and connection objects; do not commit credentials.
- Configure dependency links, failure workflow, recovery strategy, and notifications appropriate to the environment.
- Record start/end timestamps, source counts, target counts, rejects and status for each run.
- Plan duplicate prevention and rerun behavior explicitly before production deployment.

Task names are recommendations; create and validate actual sessions/tasks in PowerCenter Workflow Manager.
