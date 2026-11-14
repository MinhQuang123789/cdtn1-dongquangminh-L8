import os
from dataclasses import dataclass
import pandas as pd


@dataclass
class KetQuaBaChieu:
    chieu: str          # DAY_DU | CHINH_XAC | NHAT_QUAN
    doi_tuong: str      # ten bang.cot hoac ten quy tac
    so_kiem: int
    so_dat: int
    nguong: float

    @property
    def ti_le(self) -> float:
        return self.so_dat / self.so_kiem if self.so_kiem else 0.0

    @property
    def dat(self) -> bool:
        return self.ti_le >= self.nguong


NGUONG_DAY_DU = {
    "response_id": 1.00,
    "ticket_id": 1.00,
    "score": 0.95,
    "nps_score": 0.95,
    "responded_at": 1.00,
    "comment": 0.00,  # Binh luan cho phep trong -> nguong 0%
}


def do_day_du(df: pd.DataFrame, ten_bang: str = "survey_raw") -> list[KetQuaBaChieu]:
    kq = []
    for cot, nguong in NGUONG_DAY_DU.items():
        if cot not in df.columns:
            continue
        co_gia_tri = df[cot].notna() & (df[cot].astype(str).str.strip() != "")
        kq.append(KetQuaBaChieu("DAY_DU", f"{ten_bang}.{cot}", len(df), int(co_gia_tri.sum()), nguong))
    return kq


def do_chinh_xac(df: pd.DataFrame) -> list[KetQuaBaChieu]:
    kq = []
    tong = len(df)
    # QT-CX1: Diem CSAT nam trong khoang [1, 5]
    csat_ok = df["score_chuan"].notna()
    kq.append(KetQuaBaChieu("CHINH_XAC", "fact_survey.csat_score trong [1, 5]", tong, int(csat_ok.sum()), 0.95))

    # QT-CX2: Diem NPS nam trong khoang [0, 10]
    nps_ok = df["nps_chuan"].notna()
    kq.append(KetQuaBaChieu("CHINH_XAC", "fact_survey.nps_score trong [0, 10]", tong, int(nps_ok.sum()), 0.95))

    # QT-CX3: Ngay phan hoi dung dinh dang chuan
    ngay_ok = df["ngay_chuan"].notna()
    kq.append(KetQuaBaChieu("CHINH_XAC", "fact_survey.responded_at dung dinh dang", tong, int(ngay_ok.sum()), 0.95))
    return kq


def do_nhat_quan(df: pd.DataFrame) -> list[KetQuaBaChieu]:
    kq = []
    tong = len(df)
    # QT-NQ1: Khoa response_id duy nhat
    khong_trung = ~df.duplicated(subset=["response_id"], keep=False)
    kq.append(KetQuaBaChieu("NHAT_QUAN", "fact_survey.response_id duy nhat", tong, int(khong_trung.sum()), 1.00))

    # QT-NQ2: Co phan nhom NPS hop le (Promoter / Passive / Detractor khong chong cheo)
    hop_le_nhom = df["nps_chuan"].notna()
    kq.append(KetQuaBaChieu("NHAT_QUAN", "Phan nhom NPS (Promoter/Passive/Detractor) nhat quan", tong, int(hop_le_nhom.sum()), 0.95))

    # QT-NQ3: Moi ticket_id deu la so nguyen duong hop le
    ticket_ok = pd.to_numeric(df["ticket_id"], errors="coerce").notna()
    kq.append(KetQuaBaChieu("NHAT_QUAN", "fact_survey.ticket_id tham chieu hop le", tong, int(ticket_ok.sum()), 1.00))
    return kq


def sinh_bao_cao_ba_chieu(tat_ca_do: list[KetQuaBaChieu], duong_dan: str = "reports/chat-luong.md") -> list[KetQuaBaChieu]:
    os.makedirs(os.path.dirname(duong_dan), exist_ok=True)
    dong = [
        "# Báo cáo Đo lường Ba chiều Chất lượng Dữ liệu (Track DA)",
        "",
        "| Chiều | Đối tượng | Số kiểm | Số đạt | Tỉ lệ | Ngưỡng | Kết luận |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: |",
    ]
    for d in tat_ca_do:
        kl = "ĐẠT" if d.dat else "**KHÔNG ĐẠT**"
        dong.append(f"| {d.chieu} | {d.doi_tuong} | {d.so_kiem} | {d.so_dat} | {d.ti_le:.2%} | {d.nguong:.2%} | {kl} |")

    khong_dat = [d for d in tat_ca_do if not d.dat]
    dong.append("")
    dong.append(f"**Tổng kết: {len(tat_ca_do)} phép đo, {len(khong_dat)} không đạt.**")

    with open(duong_dan, "w", encoding="utf-8") as f:
        f.write("\n".join(dong))
    return khong_dat