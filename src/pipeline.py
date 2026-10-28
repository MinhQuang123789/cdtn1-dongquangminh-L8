import pandas as pd
import os
import datetime
from src.log_config import cau_hinh_log
import logging

from src.transform.rules import chuan_hoa_diem, doc_ngay
from src.quality.checks import (
    cl1_csat_hop_le, cl2_nps_hop_le, cl3_ngay_hop_le, 
    cl4_khoa_khong_trung, cl5_co_ticket_id
)

# Cấu hình log một lần ở điểm vào chương trình
cau_hinh_log()
log = logging.getLogger('pipeline')

def run_pipeline():
    file_path = 'data/sample/survey_sample.csv'
    log.info(f"--- Đang đọc dữ liệu từ: {file_path} ---")
    
    if not os.path.exists(file_path):
        log.error("Không tìm thấy file dữ liệu!")
        return

    # 1. EXTRACT
    df = pd.read_csv(file_path)
    log.info(f"Số dòng nguồn: {len(df)}")

    # 2. TRANSFORM
    df['score_chuan'] = df['score'].apply(lambda x: chuan_hoa_diem(x, 1, 5))
    df['nps_chuan'] = df['nps_score'].apply(lambda x: chuan_hoa_diem(x, 0, 10))
    df['ngay_chuan'] = df['responded_at'].apply(doc_ngay)
    
    # 3. QUALITY
    ket_qua = [
        cl1_csat_hop_le(df), cl2_nps_hop_le(df), cl3_ngay_hop_le(df),
        cl4_khoa_khong_trung(df), cl5_co_ticket_id(df)
    ]
    
    log.info(f"\n{'MÃ':<5} | {'TÊN QUY TẮC':<32} | {'DÒNG LỖI':<10} | {'KẾT LUẬN'}")
    log.info("-" * 65)
    for kq in ket_qua:
        trang_thai = "ĐẠT" if kq.dat else "KHÔNG ĐẠT"
        log.info(f"{kq.ma:<5} | {kq.ten:<32} | {kq.so_dong_loi:<10} | {trang_thai}")

    # Ghi báo cáo chất lượng
    os.makedirs('reports', exist_ok=True)
    report_path = f"reports/quality_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"Số dòng nguồn: {len(df)}\n")
        f.write(f"{'MÃ':<5} | {'TÊN QUY TẮC':<32} | {'DÒNG LỖI':<10} | {'KẾT LUẬN'}\n")
        f.write("-" * 65 + "\n")
        for kq in ket_qua:
            trang_thai = "ĐẠT" if kq.dat else "KHÔNG ĐẠT"
            f.write(f"{kq.ma:<5} | {kq.ten:<32} | {kq.so_dong_loi:<10} | {trang_thai}\n")
    
    log.info(f"Đã lưu báo cáo chất lượng tại: {report_path}")

if __name__ == "__main__":
    run_pipeline()