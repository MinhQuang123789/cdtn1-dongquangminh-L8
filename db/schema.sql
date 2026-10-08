-- ==============================================================================
-- MỤC 4.2: SQL DDL SKELETON CHO KHO DỮ LIỆU (TRACK DA - LUỒNG L8)
-- ==============================================================================

-- 1. Bảng Chiều Thời gian (dim_date)
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    week_of_year INT NOT NULL,
    is_weekend BOOLEAN NOT NULL
);

-- 2. Bảng Chiều Cửa hàng / Trung tâm (dim_store - SCD Loại 2)
CREATE TABLE dim_store (
    store_key SERIAL PRIMARY KEY,
    store_id INT NOT NULL,
    store_name VARCHAR(100) NOT NULL,
    manager_name VARCHAR(100),
    city VARCHAR(50) NOT NULL,
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP,
    is_current BOOLEAN DEFAULT TRUE NOT NULL
);

-- 3. Bảng Chiều Khách hàng (dim_customer - SCD Loại 1)
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    phone_masked VARCHAR(20) NOT NULL,
    customer_segment VARCHAR(20) DEFAULT 'MOI'
);

-- 4. Bảng Chiều Kỹ thuật viên (dim_technician)
CREATE TABLE dim_technician (
    technician_key SERIAL PRIMARY KEY,
    technician_id INT NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    skill_level VARCHAR(20) NOT NULL
);

-- 5. Bảng Fact Khảo sát Hài lòng (fact_survey)
CREATE TABLE fact_survey (
    survey_fact_key BIGSERIAL PRIMARY KEY,
    date_key INT NOT NULL REFERENCES dim_date(date_key),
    store_key INT NOT NULL REFERENCES dim_store(store_key),
    customer_key INT NOT NULL REFERENCES dim_customer(customer_key),
    technician_key INT NOT NULL REFERENCES dim_technician(technician_key),
    ticket_code VARCHAR(30) NOT NULL,
    
    csat_score INT NOT NULL CHECK (csat_score BETWEEN 1 AND 5),
    nps_score INT NOT NULL CHECK (nps_score BETWEEN 0 AND 10),
    is_promoter SMALLINT NOT NULL CHECK (is_promoter IN (0, 1)),
    is_detractor SMALLINT NOT NULL CHECK (is_detractor IN (0, 1)),
    is_passive SMALLINT NOT NULL CHECK (is_passive IN (0, 1)),
    turnaround_hours NUMERIC(6, 2),
    
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Tạo chỉ mục tối ưu hiệu năng lọc Dashboard (Phục vụ NFR1)
CREATE INDEX idx_fact_survey_date ON fact_survey(date_key);
CREATE INDEX idx_fact_survey_store ON fact_survey(store_key);
CREATE INDEX idx_fact_survey_composite ON fact_survey(store_key, date_key);