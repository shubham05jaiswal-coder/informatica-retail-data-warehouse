# Mapping: `m_load_stg_orders`

**Purpose:** Stage order header records.

**Flow:** `FF_ORDERS` → Source Qualifier → Expression (trim and standardize fields, parse order date) → Lookup customer key/business key → Router → staging/reject targets.

**Rules:** Require `order_id`, valid `customer_id`, parseable `order_date`, and a supported status. A missing customer is a reject or an explicitly modeled unknown member; do not silently discard the row. Normalize status and payment-method values to uppercase.
