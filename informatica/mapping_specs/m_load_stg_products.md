# Mapping: `m_load_stg_products`

**Purpose:** Load product master data into `stg_products`.

**Flow:** `FF_PRODUCTS` → Source Qualifier → Expression (trim text; convert `unit_price` to decimal) → Router (valid/reject) → staging/reject targets.

**Rules:** Require `product_id` and `product_name`; normalize category text; price must be numeric and non-negative. Identify duplicate `product_id` values and apply a documented survivorship rule. Store rejects with the source file, business key, run ID, and reason.
