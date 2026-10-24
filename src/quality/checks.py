import pandas as pd
from dataclasses import dataclass

@dataclass
class KetQuaKiem:
    ma: str
    ten: str
    so_dong_kiem: int
    so_dong_loi: int
    nguong_cho_phep: float

    @property
    def ti_le_loi(self):
        return self.so_dong_loi / self.so_dong_kiem if self.so_dong_kiem else 0.0

    @property
    def dat(self):
        return self.ti_le_loi <= self.nguong_cho_phep

def cl1_csat_hop_le(df, nguong=0.05):
    loi = df['score_chuan'].isna()
    return KetQuaKiem('CL1', 'Điểm CSAT hợp lệ (1-5)', len(df), int(loi.sum()), nguong)

def cl2_nps_hop_le(df, nguong=0.05):
    loi = df['nps_chuan'].isna() & df['nps_score'].notna()
    return KetQuaKiem('CL2', 'Điểm NPS hợp lệ (0-10)', len(df), int(loi.sum()), nguong)

def cl3_ngay_hop_le(df, nguong=0.01):
    loi = df['ngay_chuan'].isna()
    return KetQuaKiem('CL3', 'Ngày phản hồi đúng định dạng', len(df), int(loi.sum()), nguong)

def cl4_khoa_khong_trung(df, nguong=0.0):
    loi = df.duplicated(subset=['response_id'], keep=False)
    return KetQuaKiem('CL4', 'ID phản hồi là duy nhất', len(df), int(loi.sum()), nguong)

def cl5_co_ticket_id(df, nguong=0.0):
    loi = df['ticket_id'].isna() | (df['ticket_id'] == '')
    return KetQuaKiem('CL5', 'Bắt buộc có Ticket ID', len(df), int(loi.sum()), nguong)