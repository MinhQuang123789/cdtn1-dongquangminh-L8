-- 1. Bang Chieu Ngay (dim_date)
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day_of_week VARCHAR(15) NOT NULL,
    month_num INT NOT NULL,
    year_num INT NOT NULL
);

-- 2. Bang Chieu Cua hang / Trung tam (dim_store)
CREATE TABLE IF NOT EXISTS dim_store (
    store_key SERIAL PRIMARY KEY,
    store_id INT NOT NULL UNIQUE,
    store_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL
);

-- 3. Bang Chieu Khach hang (dim_customer - luu ma gia danh HMAC-SHA256)
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INT NOT NULL UNIQUE,
    customer_pseudo_id VARCHAR(64) NOT NULL,
    customer_segment VARCHAR(20) DEFAULT 'MOI'
);

-- 4. Bang Chieu Ky thuat vien (dim_technician)
CREATE TABLE IF NOT EXISTS dim_technician (
    technician_key SERIAL PRIMARY KEY,
    technician_id INT NOT NULL UNIQUE,
    skill_level VARCHAR(20) NOT NULL
);

-- 5. Bang Fact Khao sat Hai long (fact_survey - co response_id UNIQUE de ON CONFLICT khong nhan doi)
CREATE TABLE IF NOT EXISTS fact_survey (
    survey_fact_key BIGSERIAL PRIMARY KEY,
    response_id INT NOT NULL UNIQUE,
    date_key INT NOT NULL REFERENCES dim_date(date_key),
    store_key INT NOT NULL REFERENCES dim_store(store_key),
    customer_key INT NOT NULL REFERENCES dim_customer(customer_key),
    technician_key INT NOT NULL REFERENCES dim_technician(technician_key),
    ticket_id INT NOT NULL,
    csat_score INT NOT NULL CHECK (csat_score BETWEEN 1 AND 5),
    nps_score INT NOT NULL CHECK (nps_score BETWEEN 0 AND 10),
    is_promoter SMALLINT NOT NULL CHECK (is_promoter IN (0, 1)),
    is_detractor SMALLINT NOT NULL CHECK (is_detractor IN (0, 1)),
    is_passive SMALLINT NOT NULL CHECK (is_passive IN (0, 1)),
    comment TEXT,
    batch_id VARCHAR(50) NOT NULL,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Bang luu du lieu bi tu choi (reject_survey)
CREATE TABLE IF NOT EXISTS reject_survey (
    reject_id BIGSERIAL PRIMARY KEY,
    batch_id VARCHAR(50) NOT NULL,
    raw_response_id VARCHAR(100),
    raw_ticket_id VARCHAR(100),
    raw_score VARCHAR(50),
    raw_nps_score VARCHAR(50),
    raw_responded_at VARCHAR(100),
    reject_rule VARCHAR(20) NOT NULL,
    reject_reason TEXT NOT NULL,
    rejected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_fact_survey_date ON fact_survey(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_survey_store ON fact_survey(store_key);