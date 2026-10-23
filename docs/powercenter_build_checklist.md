# PowerCenter Build Checklist

## Prerequisites

- Informatica PowerCenter client/repository and Integration Service available.
- PostgreSQL database plus supported PostgreSQL ODBC/JDBC/native connector configured for the PowerCenter version.
- Database connection object and flat-file source directory configured for the environment.

## Repository objects

- [ ] Import/create flat-file source definitions for customers, products, orders, and order items.
- [ ] Create PostgreSQL target definitions from the reference DDL.
- [ ] Create source and target connection objects; keep credentials outside source control.
- [ ] Review datatypes, precision/scale, nullability, and date formats against the installed versions.

## Mappings and sessions

- [ ] Build the four source-to-staging mappings.
- [ ] Add required-field and parse/validation checks.
- [ ] Implement duplicate handling using a deterministic business-key rule.
- [ ] Lookup product/customer/order keys before fact loading.
- [ ] Route rejected or unmatched rows to `etl_reject`.
- [ ] Load `dim_customer` using the Type 1 overwrite approach.
- [ ] Load `dim_product` and then `fact_sales`.
- [ ] Configure session commit interval, reject file settings, and recovery strategy.

## Workflow and verification

- [ ] Build `wf_retail_dw_daily` with dependency links and failure paths.
- [ ] Record batch start/end state and source/target/reject counts.
- [ ] Test valid rows and each intentional quality issue in sample data.
- [ ] Re-run a completed batch and verify idempotency strategy.
- [ ] Run the SQL analytics queries and reconcile totals to source rows.

This checklist is a design aid; specific object names and options must be adapted and validated in the actual PowerCenter environment.
