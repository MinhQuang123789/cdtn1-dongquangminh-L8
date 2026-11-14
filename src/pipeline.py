import argparse
import datetime
import logging
import os
import sys
import pandas as pd

from src.log_config import cau_hinh_log
from src.transform.rules import chuan_hoa_diem, doc_ngay
from src.transform.gia_danh import gia_danh
from src.quality.checks import (
    cl1_csat_hop_le, cl2_nps_hop_le, cl3_ngay_hop_le,
    cl4_khoa_khong_trung, cl5_co_ticket_id,
)
from src.quality.three_dimensions import (
    do_day_du, do_chinh_xac, do_nhat_quan, sinh_bao_cao_ba_chieu,
)
from src.load.warehouse_loader import nap_du_lieu_kho

cau_hinh_log()
log = logging.getLogger("pipeline")


def phan_loai_dong_loi(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Tach du lieu thanh 2 luong: sach (nap Fact) va ban (day vao Reject)."""
    trung_id = df.duplicated(subset=["response_id"], keep="first")
    danh_sach_loi = []
    chi_so_loi = []

    for idx, row in df.iterrows():
        ly_do = []
        ma_quy_tac = []

        if pd.isna(row["score_chuan"]):
            ma_quy_tac.append("CL1")
            ly_do.append("Diem CSAT ngoai khoang hop le [1, 5]")
        if pd.isna(row["nps_chuan"]):
            ma_quy_tac.append("CL2")
            ly_do.append("Diem NPS ngoai khoang hop le [0, 10]")
        if pd.isna(row["ngay_chuan"]):
            ma_quy_tac.append("CL3")
            ly_do.append("Ngay phan hoi sai dinh dang chuan")
        if trung_id.loc[idx]:
            ma_quy_tac.append("CL4")
            ly_do.append("Trung lap response_id trong lo du lieu")
        if pd.isna(row["ticket_id"]) or str(row["ticket_id"]).strip() == "":
            ma_quy_tac.append("CL5")
            ly_do.append("Thieu ma phieu ticket_id bat buoc")

        if ma_quy_tac:
            ban_ghi = row.to_dict()
            ban_ghi["reject_rule"] = ",".join(ma_quy_tac)
            ban_ghi["reject_reason"] = "; ".join(ly_do)
            danh_sach_loi.append(ban_ghi)
            chi_so_loi.append(idx)

    df_loi = pd.DataFrame(danh_sach_loi)
    df_sach = df.drop(index=chi_so_loi).copy()
    return df_sach, df_loi


def run_pipeline(file_path: str = "data/sample/survey_sample.csv") -> int:
    ma_lo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log.info(f"Bat dau lo {ma_lo}")
    bao_cao = {"ma_lo": ma_lo, "cac_pha": []}

    try:
        log.info(f"--- Doc du lieu tu: {file_path} ---")
        if not os.path.exists(file_path):
            log.error("Khong tim thay file du lieu nguon!")
            bao_cao["ket_luan"] = "LOI_KHONG_CO_FILE"
            return 1

        # 1. EXTRACT
        df = pd.read_csv(file_path)
        if df.empty:
            log.warning("File du lieu rong, khong co ban ghi nao de xu ly.")
            bao_cao["ket_luan"] = "FILE_RONG"
            return 0
        log.info(f"So dong nguon: {len(df)}")
        bao_cao["cac_pha"].append("extract: OK")

        # 2. TRANSFORM + GIA DANH HOA
        df["score_chuan"] = df["score"].apply(lambda x: chuan_hoa_diem(x, 1, 5))
        df["nps_chuan"] = df["nps_score"].apply(lambda x: chuan_hoa_diem(x, 0, 10))
        df["ngay_chuan"] = df["responded_at"].apply(doc_ngay)
        df["ticket_pseudo"] = df["ticket_id"].apply(gia_danh)
        bao_cao["cac_pha"].append("transform: OK")

        # 3. QUALITY (5 quy tac + Do 3 chieu chat luong)
        ket_qua_5qt = [
            cl1_csat_hop_le(df), cl2_nps_hop_le(df), cl3_ngay_hop_le(df),
            cl4_khoa_khong_trung(df), cl5_co_ticket_id(df),
        ]
        for kq in ket_qua_5qt:
            tt = "DAT" if kq.dat else "CANH_BAO"
            log.info(f"{kq.ma:<5} | {kq.ten:<32} | Loi: {kq.so_dong_loi:<5} | {tt}")

        tat_ca_do = do_day_du(df) + do_chinh_xac(df) + do_nhat_quan(df)
        sinh_bao_cao_ba_chieu(tat_ca_do, "reports/chat-luong.md")
        bao_cao["cac_pha"].append("quality_3d: OK")

        # 4. TACH DONG SACH / BAN & LOAD VAO KHO DU LIEU
        df_sach, df_loi = phan_loai_dong_loi(df)
        ket_qua_nap = nap_du_lieu_kho(df_sach, df_loi, ma_lo)
        log.info(
            f"Hoan tat nap kho: {ket_qua_nap['so_nap']} dong vao fact_survey, "
            f"{ket_qua_nap['so_reject']} dong vao reject_survey."
        )
        bao_cao["cac_pha"].append("load: OK")
        bao_cao["ket_luan"] = "THANH_CONG"
        return 0

    except Exception as e:
        log.exception(f"Lo {ma_lo} that bai do loi ky thuat")
        bao_cao["ket_luan"] = "LOI_KY_THUAT"
        bao_cao["loi"] = str(e)
        return 1

    finally:
        os.makedirs("reports", exist_ok=True)
        report_path = f"reports/run_{ma_lo}.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"Ma lo: {bao_cao['ma_lo']}\n")
            f.write(f"Ket luan: {bao_cao.get('ket_luan', 'CHUA_RO')}\n")
            f.write(f"Cac pha hoan thanh: {bao_cao['cac_pha']}\n")
        log.info(f"Da luu bao cao chay tai: {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chay Pipeline ETL Khao sat CSAT/NPS")
    parser.add_argument("--input", default="data/sample/survey_sample.csv", help="Duong dan file CSV nguon")
    args = parser.parse_args()
    sys.exit(run_pipeline(args.input))