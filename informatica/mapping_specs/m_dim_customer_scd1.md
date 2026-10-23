# Mapping: `m_dim_customer_scd1`

**Purpose:** Maintain one current dimension row per customer using Slowly Changing Dimension Type 1 semantics.

**Flow:** Valid staged customers → lookup `dim_customer` by `customer_id` → Router (new/changed/unchanged) → insert new rows / update changed rows / skip unchanged rows.

**Rules:** Type 1 overwrites current attributes; no historical customer versions are retained. Use stable surrogate keys and maintain business key uniqueness. For reruns, ensure the update strategy and session properties make the load repeatable.
