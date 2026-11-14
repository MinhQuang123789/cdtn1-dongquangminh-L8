import os
import psycopg2
from psycopg2.extras import execute_values


def ket_noi_db():
    dwh_url = os.environ.get("DWH_URL")
    if not dwh_url:
        raise RuntimeError("Thieu bien moi truong DWH_URL")
    return psycopg2.connect(dwh_url)


def nap_du_lieu_kho(df_sach, df_loi, ma_lo: str) -> dict:
    """Nap dong sach vao fact_survey (Upsert) va dong loi vao reject_survey."""
    conn = ket_noi_db()
    so_nap = 0
    so_reject = 0

    try:
        with conn:
            with conn.cursor() as cur:
                # 1. Dam bao dim_date luon co ngay tuong ung de tranh loi khoa ngoai
                for ngay in df_sach["ngay_chuan"].dropna().unique():
                    date_key = int(ngay.strftime("%Y%m%d"))
                    cur.execute(
                        """
                        INSERT INTO dim_date (date_key, full_date, day_of_week, month_num, year_num)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (date_key) DO NOTHING;
                        """,
                        (date_key, ngay.date(), ngay.strftime("%A"), ngay.month, ngay.year),
                    )

                # 2. Upsert vao fact_survey (chay lai khong nhan doi)
                for _, row in df_sach.iterrows():
                    resp_id = int(row["response_id"])
                    t_id = int(row["ticket_id"])
                    csat = int(row["score_chuan"])
                    nps = int(row["nps_chuan"])
                    date_key = int(row["ngay_chuan"].strftime("%Y%m%d"))

                    is_promoter = 1 if nps >= 9 else 0
                    is_detractor = 1 if nps <= 6 else 0
                    is_passive = 1 if 7 <= nps <= 8 else 0

                    # Anh xa khoa thay the danh muc da seed (1 hoac 2)
                    store_key = (t_id % 2) + 1
                    customer_key = (resp_id % 2) + 1
                    tech_key = (t_id % 2) + 1

                    cur.execute(
                        """
                        INSERT INTO fact_survey (
                            response_id, date_key, store_key, customer_key, technician_key,
                            ticket_id, csat_score, nps_score, is_promoter, is_detractor, is_passive,
                            comment, batch_id
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (response_id) DO UPDATE SET
                            date_key = EXCLUDED.date_key,
                            store_key = EXCLUDED.store_key,
                            customer_key = EXCLUDED.customer_key,
                            technician_key = EXCLUDED.technician_key,
                            ticket_id = EXCLUDED.ticket_id,
                            csat_score = EXCLUDED.csat_score,
                            nps_score = EXCLUDED.nps_score,
                            is_promoter = EXCLUDED.is_promoter,
                            is_detractor = EXCLUDED.is_detractor,
                            is_passive = EXCLUDED.is_passive,
                            comment = EXCLUDED.comment,
                            batch_id = EXCLUDED.batch_id,
                            loaded_at = CURRENT_TIMESTAMP;
                        """,
                        (
                            resp_id, date_key, store_key, customer_key, tech_key,
                            t_id, csat, nps, is_promoter, is_detractor, is_passive,
                            str(row.get("comment", "")) if row.get("comment") is not None else "",
                            ma_lo,
                        ),
                    )
                    so_nap += 1

                # 3. Ghi cac dong vi pham vao reject_survey
                if not df_loi.empty:
                    ban_ghi_loi = [
                        (
                            ma_lo,
                            str(r.get("response_id", "")),
                            str(r.get("ticket_id", "")),
                            str(r.get("score", "")),
                            str(r.get("nps_score", "")),
                            str(r.get("responded_at", "")),
                            r["reject_rule"],
                            r["reject_reason"],
                        )
                        for _, r in df_loi.iterrows()
                    ]
                    execute_values(
                        cur,
                        """
                        INSERT INTO reject_survey (
                            batch_id, raw_response_id, raw_ticket_id, raw_score,
                            raw_nps_score, raw_responded_at, reject_rule, reject_reason
                        ) VALUES %s;
                        """,
                        ban_ghi_loi,
                    )
                    so_reject = len(ban_ghi_loi)
    finally:
        conn.close()

    return {"so_nap": so_nap, "so_reject": so_reject}