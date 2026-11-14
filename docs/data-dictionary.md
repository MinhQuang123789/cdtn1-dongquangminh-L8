# Data Dictionary — Customer Satisfaction Data Warehouse (Flow L8)

## Table 1: `fact_survey`
| Column | Type | Meaning | Valid Values | Nullable | Classification | Security Handling |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| `survey_fact_key` | `BIGSERIAL` | Surrogate primary key | Integers >= 1 | No | Internal | Exposed via views; direct table access revoked from `nha_phan_tich`. |
| `response_id` | `INT` | Business key of survey response | Integers >= 1 (`UNIQUE`) | No | Internal | Exposed in `v_survey_analytics` for row audit. |
| `date_key` | `INT` | FK to `dim_date` | `YYYYMMDD` | No | Public | Joined to expose `responded_date`. |
| `store_key` | `INT` | FK to `dim_store` | Valid `store_key` | No | Internal | Joined to expose `store_name`, `city`. |
| `customer_key` | `INT` | FK to `dim_customer` | Valid `customer_key` | No | Internal | Joined internally for `customer_pseudo_id`. |
| `technician_key` | `INT` | FK to `dim_technician` | Valid `technician_key` | No | Internal | Restricted to internal warehouse roles. |
| `ticket_id` | `INT` | Repair service ticket ID | Integers >= 1 | No | Personally Identifying | Omitted from all analytical views. |
| `csat_score` | `INT` | CSAT rating | `1` to `5` | No | Internal | Exposed in views for SLA (`>= 4.0`) tracking. |
| `nps_score` | `INT` | NPS rating | `0` to `10` | No | Internal | Exposed in views for NPS analysis. |
| `is_promoter` | `SMALLINT` | Promoter flag (`nps >= 9`) | `0` or `1` | No | Internal | Used for NPS index calculation. |
| `is_detractor` | `SMALLINT` | Detractor flag (`nps <= 6`) | `0` or `1` | No | Internal | Used for NPS index calculation. |
| `is_passive` | `SMALLINT` | Passive flag (`nps` in `7, 8`) | `0` or `1` | No | Internal | Used for NPS index calculation. |
| `comment` | `TEXT` | Optional customer comment | UTF-8 text | Yes | Internal | Exposed in `v_survey_analytics`; omitted from `v_store_summary`. |
| `batch_id` | `VARCHAR(50)` | ETL batch timestamp ID | `YYYYMMDD_HHMMSS` | No | Internal | Audit metadata; hidden from views. |
| `loaded_at` | `TIMESTAMP` | Load/update timestamp | Valid timestamp | No | Internal | Audit metadata; hidden from views. |

## Table 2: `dim_customer`
| Column | Type | Meaning | Valid Values | Nullable | Classification | Security Handling |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| `customer_key` | `SERIAL` | Surrogate primary key | Integers >= 1 | No | Internal | Base table revoked from `nha_phan_tich`. |
| `customer_id` | `INT` | Operational customer ID | Integers >= 1 (`UNIQUE`) | No | Personally Identifying | Hidden from views; `nha_phan_tich` gets `permission denied`. |
| `customer_pseudo_id` | `VARCHAR(64)` | HMAC-SHA256 customer hash | 64-char hex string | No | Internal (Pseudonymized) | Computed in pipeline using `PSEUDO_KEY` from `.env`. |
| `customer_segment` | `VARCHAR(20)` | Customer tier | `'MOI'`, `'THAN_THIET'`, `'VIP'` | Yes | Internal | Exposed in `v_survey_analytics`. |

## Table 3: `reject_survey`
| Column | Type | Meaning | Valid Values | Nullable | Classification | Security Handling |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| `reject_id` | `BIGSERIAL` | Surrogate primary key | Integers >= 1 | No | Internal | Restricted to `app_user`; revoked from `nha_phan_tich`. |
| `batch_id` | `VARCHAR(50)` | Rejecting batch ID | `YYYYMMDD_HHMMSS` | No | Internal | Used for pipeline audit. |
| `raw_response_id` | `VARCHAR(100)` | Raw `response_id` value | Raw text | Yes | Internal | Preserved unmodified for debugging. |
| `raw_ticket_id` | `VARCHAR(100)` | Raw `ticket_id` value | Raw text | Yes | Personally Identifying | Quarantined in base table; hidden from views. |
| `raw_score` | `VARCHAR(50)` | Raw `score` value | Raw text | Yes | Internal | Preserved unmodified. |
| `raw_nps_score` | `VARCHAR(50)` | Raw `nps_score` value | Raw text | Yes | Internal | Preserved unmodified. |
| `raw_responded_at` | `VARCHAR(100)` | Raw timestamp string | Raw text | Yes | Internal | Preserved unmodified. |
| `reject_rule` | `VARCHAR(20)` | Violated rule codes | `CL1`..`CL5` | No | Internal | Used for quality reporting. |
| `reject_reason` | `TEXT` | Rejection explanation | Non-empty text | No | Internal | Used by engineers to diagnose source errors. |
| `rejected_at` | `TIMESTAMP` | Quarantine timestamp | Valid timestamp | No | Internal | Audit metadata. |

> **Minimum Group Size Policy:** `v_store_summary` enforces `HAVING COUNT(f.response_id) >= 3` so individual ratings in small groups cannot be inferred.
