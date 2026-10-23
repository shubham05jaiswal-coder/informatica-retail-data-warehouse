# Mapping: `m_load_stg_order_items`

**Purpose:** Stage sales order-line records with validation and reference checks.

**Flow:** `FF_ORDER_ITEMS` → Source Qualifier → Expression (type conversion and net amount calculation) → Lookup order/product → Router → staging/reject targets.

**Rules:** Require a unique numeric `order_item_id`; order and product must resolve; quantity must be greater than zero; unit price must be non-negative; discount must be between 0 and 100. Calculate net line amount as `quantity * unit_price * (1 - discount_pct / 100)`. Route any failed checks to `etl_reject` with a reason.
