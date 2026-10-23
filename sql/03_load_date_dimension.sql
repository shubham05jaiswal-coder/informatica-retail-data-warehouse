-- Example date dimension load for the sample order period; extend the range as needed.
INSERT INTO dw.dim_date
(date_key, calendar_date, year_num, quarter_num, month_num, month_name,
 day_num, day_of_week_num, day_name, is_weekend)
SELECT TO_CHAR(d::date, 'YYYYMMDD')::INTEGER,
       d::date,
       EXTRACT(YEAR FROM d)::INTEGER,
       EXTRACT(QUARTER FROM d)::INTEGER,
       EXTRACT(MONTH FROM d)::INTEGER,
       TO_CHAR(d::date, 'FMMonth'),
       EXTRACT(DAY FROM d)::INTEGER,
       EXTRACT(ISODOW FROM d)::INTEGER,
       TO_CHAR(d::date, 'FMDay'),
       EXTRACT(ISODOW FROM d)::INTEGER IN (6, 7)
FROM GENERATE_SERIES(DATE '2024-01-01', DATE '2026-12-31', INTERVAL '1 day') AS g(d)
ON CONFLICT (date_key) DO NOTHING;
