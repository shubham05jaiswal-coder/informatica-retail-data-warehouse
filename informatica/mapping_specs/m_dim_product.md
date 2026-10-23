# Mapping: `m_dim_product`

**Purpose:** Load and maintain product attributes in `dim_product`.

**Flow:** Valid `stg_products` → Lookup target by product business key → Router (new/changed/unchanged) → insert or update.

**Rules:** Keep one product row per `product_id`; validate decimal precision/scale and use deterministic update rules. Ensure all product dimension rows are loaded before fact rows reference them.
