import os
import pandas as pd
import psycopg2
import pytest

from src.transform.gia_danh import gia_danh
from src.quality.three_dimensions import do_day_du, do_chinh_xac, do_nhat_quan
from src.pipeline import run_pipeline


def _ket_noi():
    return psycopg2.connect(os.environ["DWH_URL"])


# 1. Test Gia danh hoa HMAC-SHA256 (Bao mat & Track DA)
def test_TC08_gia_danh_hmac_nhat_quan():
    ma_1 = gia_danh("1024")
    ma_2 = gia_danh("1024")
    assert ma_1 is not None
    assert len(ma_1) == 64
    assert ma_1 == ma_2
    assert ma_1 != "1024"


# 2. Test Do 3 chieu chat luong du lieu (Day du, Chinh xac, Nhat quan)
def test_TC09_do_ba_chieu_chat_luong_du_lieu_sach():
    df = pd.read_csv("data/sample/survey_sample.csv")
    df["score_chuan"] = df["score"]
    df["nps_chuan"] = df["nps_score"]
    df["ngay_chuan"] = pd.to_datetime(df["responded_at"])

    kq_3d = do_day_du(df) + do_chinh_xac(df) + do_nhat_quan(df)
    assert len(kq_3d) == 12
    assert all(m.dat for m in kq_3d), f"Co phep do khong dat: {[m for m in kq_3d if not m.dat]}"


# 3. Test Tich hop: Du lieu ban day vao bang reject_survey, khong lam sap pipeline
def test_TC10_du_lieu_ban_day_vao_reject_survey():
    conn = _ket_noi()
    with conn, conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE fact_survey, reject_survey RESTART IDENTITY;")
    conn.close()

    ma_thoat = run_pipeline("data/sample/survey_dirty_sample.csv")
    assert ma_thoat == 0

    conn = _ket_noi()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM fact_survey;")
        so_sach = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM reject_survey;")
        so_ban = cur.fetchone()[0]
    conn.close()

    assert so_sach == 3
    assert so_ban == 4


# 4. Test Tinh tai lap (Idempotency - C8): Chay pipeline 2 lan lien tiep khong nhan doi du lieu
def test_TC11_chay_lai_pipeline_khong_nhan_doi():
    conn = _ket_noi()
    with conn, conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE fact_survey, reject_survey RESTART IDENTITY;")
    conn.close()

    # Lan chay 1
    assert run_pipeline("data/sample/survey_sample.csv") == 0
    # Lan chay 2 (cung tap du lieu)
    assert run_pipeline("data/sample/survey_sample.csv") == 0

    conn = _ket_noi()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM fact_survey;")
        tong_dong = cur.fetchone()[0]
    conn.close()

    assert tong_dong == 10


# 5. Test Bao mat phan quyen (D4): Vai tro nha_phan_tich bi tu choi khi doc bang goc dim_customer
def test_TC12_phan_quyen_nha_phan_tich_bi_chan_bang_goc():
    dwh_name = os.environ.get("DWH_NAME", "mekong_crm")
    conn_analyst = psycopg2.connect(
        host="warehouse",
        port=5432,
        dbname=dwh_name,
        user="nha_phan_tich",
        password="analyst_readonly_2026",
    )
    with pytest.raises(psycopg2.errors.InsufficientPrivilege):
        with conn_analyst.cursor() as cur:
            cur.execute("SELECT * FROM dim_customer;")
    conn_analyst.close()