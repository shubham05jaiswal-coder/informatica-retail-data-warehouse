-- Reference DDL for PostgreSQL. Validate against your PostgreSQL version and target naming standards.
CREATE SCHEMA IF NOT EXISTS stg;
CREATE SCHEMA IF NOT EXISTS dw;
CREATE SCHEMA IF NOT EXISTS etl;

CREATE TABLE IF NOT EXISTS etl.batch_control (
    batch_id BIGSERIAL PRIMARY KEY,
    workflow_name TEXT NOT NULL,
    run_id TEXT NOT NULL UNIQUE,
    start_ts TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_ts TIMESTAMPTZ,
    status TEXT NOT NULL DEFAULT 'RUNNING',
    source_rows BIGINT DEFAULT 0,
    loaded_rows BIGINT DEFAULT 0,
    rejected_rows BIGINT DEFAULT 0,
    message TEXT
);

CREATE TABLE IF NOT EXISTS etl.reject (
    reject_id BIGSERIAL PRIMARY KEY,
    run_id TEXT NOT NULL,
    source_name TEXT NOT NULL,
    business_key TEXT,
    source_row JSONB,
    reason_code TEXT NOT NULL,
    reason_detail TEXT,
    created_ts TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stg.customers (
    customer_id TEXT, first_name TEXT, last_name TEXT, email TEXT,
    city TEXT, state TEXT, signup_date DATE, run_id TEXT NOT NULL,
    source_file TEXT, ingest_ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS stg.products (
    product_id TEXT, product_name TEXT, category TEXT, unit_price NUMERIC(12,2),
    run_id TEXT NOT NULL, source_file TEXT, ingest_ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS stg.orders (
    order_id TEXT, customer_id TEXT, order_date DATE, order_status TEXT,
    payment_method TEXT, run_id TEXT NOT NULL, source_file TEXT,
    ingest_ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS stg.order_items (
    order_item_id BIGINT, order_id TEXT, product_id TEXT, quantity INTEGER,
    unit_price NUMERIC(12,2), discount_pct NUMERIC(5,2), run_id TEXT NOT NULL,
    source_file TEXT, ingest_ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dw.dim_customer (
    customer_key BIGSERIAL PRIMARY KEY,
    customer_id TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT,
    city TEXT, state TEXT, signup_date DATE,
    updated_ts TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS dw.dim_product (
    product_key BIGSERIAL PRIMARY KEY,
    product_id TEXT NOT NULL UNIQUE,
    product_name TEXT NOT NULL, category TEXT, unit_price NUMERIC(12,2) NOT NULL,
    updated_ts TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS dw.dim_date (
    date_key INTEGER PRIMARY KEY, calendar_date DATE NOT NULL UNIQUE,
    year_num INTEGER NOT NULL, quarter_num INTEGER NOT NULL, month_num INTEGER NOT NULL,
    month_name TEXT NOT NULL, day_num INTEGER NOT NULL, day_of_week_num INTEGER NOT NULL,
    day_name TEXT NOT NULL, is_weekend BOOLEAN NOT NULL
);
CREATE TABLE IF NOT EXISTS dw.fact_sales (
    sales_key BIGSERIAL PRIMARY KEY,
    order_item_id BIGINT NOT NULL UNIQUE,
    order_id TEXT NOT NULL,
    order_date_key INTEGER NOT NULL REFERENCES dw.dim_date(date_key),
    customer_key BIGINT NOT NULL REFERENCES dw.dim_customer(customer_key),
    product_key BIGINT NOT NULL REFERENCES dw.dim_product(product_key),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    discount_pct NUMERIC(5,2) NOT NULL CHECK (discount_pct >= 0 AND discount_pct <= 100),
    gross_amount NUMERIC(14,2) NOT NULL,
    net_sales_amount NUMERIC(14,2) NOT NULL,
    loaded_ts TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_fact_sales_date ON dw.fact_sales(order_date_key);
CREATE INDEX IF NOT EXISTS ix_fact_sales_customer ON dw.fact_sales(customer_key);
CREATE INDEX IF NOT EXISTS ix_fact_sales_product ON dw.fact_sales(product_key);
