# Mapping: `m_fact_sales`

**Purpose:** Load one row per validated order item into `fact_sales`.

**Flow:** Valid `stg_order_items` joined/looked up to staged orders, `dim_customer`, `dim_product`, and `dim_date` → Expression (net sales) → Lookup existing fact key / Router → target insert or governed update path.

**Grain:** One row per source order-item identifier. Store surrogate keys for date, customer, and product plus order identifiers and measures.

**Measures:** Quantity, unit price, discount percentage, gross amount, and net sales amount. Exclude cancelled orders according to the business rule; make the treatment of processing orders explicit. Use the source line business key for duplicate prevention on reruns.
