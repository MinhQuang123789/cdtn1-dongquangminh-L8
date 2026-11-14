# Technical Pipeline Documentation — Customer Satisfaction Survey ETL (Flow L8)

## 1. Phase Diagram
1. **EXTRACT (`src/pipeline.py`):** Reads raw survey batches from `data/sample/*.csv`.
2. **TRANSFORM & PSEUDONYMIZE (`src/transform/rules.py`, `src/transform/gia_danh.py`):** Normalizes CSAT `[1, 5]`, NPS `[0, 10]`, timestamps, and hashes identifiers via HMAC-SHA256.
3. **QUALITY GATE & 3D MEASUREMENT (`src/quality/checks.py`, `src/quality/three_dimensions.py`):** Evaluates Completeness, Accuracy, and Consistency, generating `reports/chat-luong.md`.
4. **LOAD & QUARANTINE (`src/load/warehouse_loader.py`):** Upserts clean records into `fact_survey` (`ON CONFLICT (response_id) DO UPDATE`) and quarantines invalid rows into `reject_survey`.

## 2. Data Sources
- **Source:** Customer Post-Repair CSAT/NPS Survey CSV (`UTF-8`), updated daily at 23:00, owned by Customer Service & QA Department (Mekong Mobile), mounted at `/data/sample/survey_sample.csv`.

## 3. Targets and Grain
- **`fact_survey`:** Grain = 1 valid survey response per repair ticket; Business Key = `response_id` (`UNIQUE`); Surrogate Key = `survey_fact_key` (`BIGSERIAL`).
- **`reject_survey`:** Grain = 1 rejected source row per ETL batch; Business Key = (`batch_id`, `raw_response_id`); Surrogate Key = `reject_id` (`BIGSERIAL`).

## 4. Cleaning and Quality Rules
| Rule Code | Dimension | Description | Threshold | Rejected Rows (Sample Run) |
| :--- | :--- | :--- | :---: | :---: |
| `CL1` | Accuracy | `csat_score` integer in `[1, 5]` | >= 95% | `0` (Clean) / `1` (Dirty) |
| `CL2` | Accuracy | `nps_score` integer in `[0, 10]` | >= 95% | `0` (Clean) / `1` (Dirty) |
| `CL3` | Accuracy | `responded_at` matches `%Y-%m-%d %H:%M:%S` or `%d/%m/%Y %H:%M` | >= 95% | `0` (Clean) / `1` (Dirty) |
| `CL4` | Consistency | `response_id` unique in batch | 100% | `0` (Clean) / `0` (Dirty) |
| `CL5` | Completeness | `ticket_id` non-null and non-empty | 100% | `0` (Clean) / `1` (Dirty) |

## 5. Schedule and Backfill
- **Schedule:** Daily at 23:15 UTC+7.
- **Backfill:** `docker compose run --rm pipeline python -m src.pipeline --input /data/sample/survey_sample.csv`. Re-running updates existing rows via `ON CONFLICT` without duplicating records.

## 6. Known Limitations and Data Latency
- Free-text `comment` is optional (`0%` completeness threshold) and excluded from public aggregate views (`v_store_summary`).
- Quarantined rows in `reject_survey` are excluded from `fact_survey`; if source rejection exceeds 5%, dashboard averages may under-represent dissatisfied customers until upstream POS validation is fixed.
- Batch latency is up to 24 hours in production; Streamlit caches view queries for `30` seconds.
