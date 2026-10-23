# Informatica PowerCenter — Retail Data Warehouse ETL

An end-to-end retail data warehouse ETL portfolio project designed around Informatica PowerCenter and PostgreSQL. It includes sample CSV source data, source-to-target mappings, mapping specifications, workflow design, DDL, data-quality scenarios, and analytical SQL.

> **Scope note:** This repository is a PowerCenter implementation blueprint, not an exported/importable Informatica workflow package. Build the mappings and sessions in your licensed PowerCenter environment using the included specifications. PostgreSQL is the reference target database.

## Architecture

```text
CSV sources (customers, products, orders, order_items)
       |
       v
Informatica PowerCenter mappings
(Source Qualifier -> Expression / Lookup / Router / Aggregator)
       |
       v
PostgreSQL staging tables -> dimensions -> fact_sales
       |
       +-- reject and batch-control tracking
       +-- SQL analytics for retail sales
```

## Project explanation guide

- [Download the project explanation PDF](docs/project-explanation.pdf)
- [Read the Markdown explanation](docs/project-explanation.md)
- The PDF is generated from the Markdown guide by [GitHub Actions](.github/workflows/generate-project-pdf.yml).

## Repository structure

- `config/` — runtime parameter-file example
- `data/source/` — sample CSV extracts, including quality edge cases
- `docs/` — data dictionary, source-to-target mapping, build checklist
- `informatica/mapping_specs/` — mapping design specifications
- `informatica/workflow_specs/` — daily workflow/session orchestration design
- `sql/` — PostgreSQL schema, date dimension, analytics

## Data and quality scenarios

The sample inputs cover customers, products, orders, and order items. They intentionally include records that help demonstrate duplicate handling, invalid dates, unknown product references, and invalid quantities. Use the reject-handling rules described in the mapping specs rather than silently dropping source rows.

## Build outline

1. Create a PostgreSQL database and run `sql/01_create_schema.sql`.
2. Load the date dimension using `sql/03_load_date_dimension.sql`.
3. Import the CSV files as flat-file sources in the PowerCenter Designer/Repository tools.
4. Create the staging mappings and then the customer/product dimensions and sales fact mapping, following `informatica/mapping_specs/` and `docs/source_to_target_mapping.csv`.
5. Configure connections and file paths for your own environment; treat `config/retail_dw_dev.par` as a template.
6. Build the workflow from `informatica/workflow_specs/wf_retail_dw_daily.md`, run it, and review reject/batch-control records.
7. Run `sql/02_analytics_queries.sql` to explore the loaded warehouse.

## Tools and concepts

- Informatica PowerCenter ETL design
- PostgreSQL and SQL
- Staging, dimensional modeling, and sales fact design
- Source-to-target mapping
- Data validation and reject handling
- SCD Type 1 customer dimension strategy
- Workflow orchestration and batch monitoring


