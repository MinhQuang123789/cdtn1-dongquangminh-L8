-- Nap du lieu danh muc cho cac ngay trong survey_sample.csv
INSERT INTO dim_date (date_key, full_date, day_of_week, month_num, year_num) VALUES
(20260801, '2026-08-01', 'Saturday', 8, 2026),
(20260802, '2026-08-02', 'Sunday', 8, 2026),
(20260803, '2026-08-03', 'Monday', 8, 2026),
(20260804, '2026-08-04', 'Tuesday', 8, 2026),
(20260805, '2026-08-05', 'Wednesday', 8, 2026)
ON CONFLICT (date_key) DO NOTHING;

INSERT INTO dim_store (store_id, store_name, city) VALUES
(1, 'Trung tam Quan 1', 'Ho Chi Minh'),
(2, 'Trung tam Thu Duc', 'Ho Chi Minh')
ON CONFLICT (store_id) DO NOTHING;

INSERT INTO dim_customer (customer_id, customer_pseudo_id, customer_segment) VALUES
(100, '8f9a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a', 'THAN_THIET'),
(101, '1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b', 'MOI')
ON CONFLICT (customer_id) DO NOTHING;

INSERT INTO dim_technician (technician_id, skill_level) VALUES
(501, 'SENIOR'),
(502, 'JUNIOR')
ON CONFLICT (technician_id) DO NOTHING;

-- Tao View phan tich cho Dashboard (an danh hoa, khong chua thong tin dinh danh goc)
CREATE OR REPLACE VIEW v_survey_analytics AS
SELECT
    f.response_id,
    d.full_date AS responded_date,
    s.store_name,
    s.city,
    c.customer_pseudo_id,
    c.customer_segment,
    f.csat_score,
    f.nps_score,
    f.is_promoter,
    f.is_detractor,
    f.is_passive,
    f.comment
FROM fact_survey f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_store s ON f.store_key = s.store_key
JOIN dim_customer c ON f.customer_key = c.customer_key;

-- View tong hop theo cua hang (ap dung nguong nhom toi thieu >= 3 khao sat)
CREATE OR REPLACE VIEW v_store_summary AS
SELECT
    s.store_name,
    s.city,
    COUNT(f.response_id) AS total_responses,
    ROUND(AVG(f.csat_score)::NUMERIC, 2) AS avg_csat,
    ROUND(((SUM(f.is_promoter) - SUM(f.is_detractor))::NUMERIC / COUNT(f.response_id)) * 100, 1) AS nps_index
FROM fact_survey f
JOIN dim_store s ON f.store_key = s.store_key
GROUP BY s.store_name, s.city
HAVING COUNT(f.response_id) >= 3;

-- Tao tai khoan & vai tro han che cho Dashboard (Chi doc View, cam doc bang goc dim_customer)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'nha_phan_tich') THEN
        CREATE ROLE nha_phan_tich LOGIN PASSWORD 'analyst_readonly_2026';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE mekong_crm TO nha_phan_tich;
GRANT USAGE ON SCHEMA public TO nha_phan_tich;
GRANT SELECT ON v_survey_analytics, v_store_summary TO nha_phan_tich;
REVOKE ALL ON dim_customer, fact_survey, reject_survey FROM nha_phan_tich;