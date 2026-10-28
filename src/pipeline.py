import pandas as pd
import os
import sys
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
    ma_lo = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    log.info(f"Bắt đầu lô {ma_lo}")
    
    bao_cao = {'ma_lo': ma_lo, 'cac_pha': []}
    
    try:
        file_path = 'data/sample/survey_sample.csv'
        log.info(f"--- Đang đọc dữ liệu từ: {file_path} ---")
        
        if not os.path.exists(file_path):
            log.error("Không tìm thấy file dữ liệu!")
            bao_cao['ket_luan'] = 'LOI_KHONG_CO_FILE'
            return 1

        # 1. EXTRACT
        df = pd.read_csv(file_path)
        log.info(f"Số dòng nguồn: {len(df)}")
        bao_cao['cac_pha'].append('extract: OK')

        # 2. TRANSFORM
        df['score_chuan'] = df['score'].apply(lambda x: chuan_hoa_diem(x, 1, 5))
        df['nps_chuan'] = df['nps_score'].apply(lambda x: chuan_hoa_diem(x, 0, 10))
        df['ngay_chuan'] = df['responded_at'].apply(doc_ngay)
        bao_cao['cac_pha'].append('transform: OK')
        
        # 3. QUALITY
        ket_qua = [
            cl1_csat_hop_le(df), cl2_nps_hop_le(df), cl3_ngay_hop_le(df),
            cl4_khoa_khong_trung(df), cl5_co_ticket_id(df)
        ]
        
        log.info(f"\n{'MÃ':<5} | {'TÊN QUY TẮC':<32} | {'DÒNG LỖI':<10} | {'KẾT LUẬN'}")
        log.info("-" * 65)
        
        khong_dat = []
        bao_cao['quality'] = []
        
        for kq in ket_qua:
            trang_thai = "ĐẠT" if kq.dat else "KHÔNG ĐẠT"
            log.info(f"{kq.ma:<5} | {kq.ten:<32} | {kq.so_dong_loi:<10} | {trang_thai}")
            bao_cao['quality'].append({'ma': kq.ma, 'dat': kq.dat})
            if not kq.dat:
                khong_dat.append(kq)

        # Dừng lại nếu có quy tắc KHÔNG ĐẠT (Yêu cầu Buổi 11)
        if khong_dat:
            log.error("DỪNG LẠI. Nạp dữ liệu rác sẽ làm hỏng kho dữ liệu!")
            bao_cao['ket_luan'] = 'DUNG_VI_CHAT_LUONG'
            return 2

        # 4. LOAD (Giả lập)
        bao_cao['cac_pha'].append('load: OK')
        bao_cao['ket_luan'] = 'THANH_CONG'
        return 0

    except Exception as e:
        log.exception(f"Lô {ma_lo} thất bại ở pha đang chạy")
        bao_cao['ket_luan'] = 'LOI_KY_THUAT'
        bao_cao['loi'] = str(e)
        return 1

    finally:
        # BÁO CÁO LUÔN ĐƯỢC GHI, kể cả khi thất bại (Yêu cầu Buổi 11)
        os.makedirs('reports', exist_ok=True)
        report_path = f"reports/run_{ma_lo}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"Mã lô: {bao_cao['ma_lo']}\n")
            f.write(f"Kết luận: {bao_cao.get('ket_luan', 'CHUA_RO')}\n")
            f.write(f"Các pha hoàn thành: {bao_cao['cac_pha']}\n")
            if 'loi' in bao_cao:
                f.write(f"Lỗi: {bao_cao['loi']}\n")
        log.info(f"Đã lưu báo cáo chạy tại: {report_path}")

if __name__ == "__main__":
    ma_thoat = run_pipeline()
    sys.exit(ma_thoat)