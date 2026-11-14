# Deployment Guide — Customer Satisfaction Survey ETL Pipeline (Flow L8, Track DA)

## 1. Requirements
- **Operating System:** Windows 10/11 (WSL2 enabled), macOS, or Linux (Ubuntu 22.04+).
- **Container Runtime:** Docker Engine 24.0+ and Docker Compose v2.20+ (verify via `docker compose version`). No local Python or PostgreSQL installation is required.
- **Version Control:** Git 2.30+.
- **System Resources:** At least 2 GB free disk space and port `8501` available on host (`5432` stays isolated inside Docker network).

## 2. Setup Steps
1. **Clone the repository at tag `v1.0`:**
   `git clone --branch v1.0 https://github.com/MinhQuang123789/cdtn1-dongquangminh-L8.git && cd cdtn1-dongquangminh-L8`
2. **Create environment file from template (Command 1 of 2):**
   `cp .env.example .env`
3. **Build images, initialize database, run ETL pipeline, and start dashboard (Command 2 of 2):**
   `docker compose up -d --build`

## 3. Environment Variables
| Variable Name | Description | Sample Value (`.env.example`) | Required |
| :--- | :--- | :--- | :---: |
| `DWH_NAME` | Target PostgreSQL database name | `mekong_crm` | Yes |
| `DWH_USER` | Admin DB user for schema init and ETL load | `app_user` | Yes |
| `DWH_PASSWORD` | Password for `DWH_USER` (rotate in production) | `mat_khau_kho_du_lieu_cua_ban` | Yes |
| `DWH_PORT` | PostgreSQL port reference | `5433` | No |
| `DASHBOARD_PORT` | Host port for Streamlit dashboard | `8501` | No |
| `PSEUDO_KEY` | Secret HMAC-SHA256 key (>= 32 chars) for pseudonymization | `khoa-bi-mat-gia-danh-hoa-it-nhat-32-ky-tu-2026` | Yes |

## 4. Sample Data
- **DB Seed (`db/init/001_schema.sql`, `002_seed_and_security.sql`):** Auto-runs on empty volume; seeds 5 dates, 2 stores, 2 pseudonymized customers, 2 technicians, analytical views (`v_survey_analytics`, `v_store_summary`), and restricted role `nha_phan_tich`.
- **CSV Files:** `data/sample/survey_sample.csv` (10 valid records loaded into `fact_survey`) and `data/sample/survey_dirty_sample.csv` (7 records: 3 valid, 4 invalid for `reject_survey` integration test).

## 5. Verify It Works
1. **Container health:** `docker compose ps` -> `warehouse` shows `Up ... (healthy)` and `dashboard` shows `Up ...` on port `8501`.
2. **Automated tests:** `docker compose run --rm pipeline pytest -v` -> `16 passed` with exit code `0`.
3. **Idempotent reload:** `docker compose run --rm pipeline` -> outputs `Hoan tat nap kho: 10 dong vao fact_survey, 0 dong vao reject_survey.`.
4. **Dashboard UI:** Open `http://localhost:8501` -> displays CSAT and NPS Plotly charts queried via role `nha_phan_tich`.

### Troubleshooting
- **Port 8501 in use:** Change `DASHBOARD_PORT=8502` in `.env` and run `docker compose up -d`.
- **Stale DB volume:** Reset with `docker compose down -v && docker compose up -d --build`.
