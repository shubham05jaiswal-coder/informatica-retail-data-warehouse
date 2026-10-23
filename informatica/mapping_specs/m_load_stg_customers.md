# Mapping: `m_load_stg_customers`

**Purpose:** Land customer rows from `customers.csv` into `stg_customers` while capturing source lineage and invalid records.

**Flow:** `FF_CUSTOMERS` → Source Qualifier → Expression (`TRIM`, email normalization, date parse/validation) → Router (valid/reject) → `T_STG_CUSTOMERS` / `T_ETL_REJECT`.

**Rules:** Require customer ID, first name, and last name; normalize email to lowercase; parse `signup_date` as ISO `YYYY-MM-DD`; define a deterministic duplicate policy for `customer_id` (for example, latest valid record wins). Preserve rejected source values and a reason code.

**Session notes:** Set source path through a parameter, enable reject logging, and record source/target/reject counts in batch control. Verify target column types against the PostgreSQL DDL.
