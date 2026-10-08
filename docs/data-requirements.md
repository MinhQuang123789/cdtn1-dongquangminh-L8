# ĐẶC TẢ YÊU CẦU DỮ LIỆU (DATA REQUIREMENT SPECIFICATION)
Chuyên ngành: Công nghệ Dữ liệu (Track DA)
Luồng nghiệp vụ: L8 - Khảo sát hài lòng CSAT / NPS (Smart CRM Mekong Mobile)

---

## 1. CÂU HỎI PHÂN TÍCH NGHIỆP VỤ (BUSINESS ANALYTICAL QUESTIONS)
Mỗi câu hỏi phân tích đều truy vết trực tiếp về một User Story đã đặc tả:
- **CH1:** Điểm CSAT trung bình và tỷ lệ % NPS của từng cửa hàng/trung tâm theo từng tháng là bao nhiêu? (Phục vụ: US2, US5)
- **CH2:** Những chi nhánh nào có chỉ số CSAT sụt giảm liên tiếp trong 2 tháng gần nhất? (Phục vụ: US5)
- **CH3:** Nhóm khách hàng chỉ trích (Detractors) chiếm tỷ lệ cao nhất ở các loại sự cố/thiết bị nào? (Phục vụ: US3)
- **CH4:** Thời gian sửa chữa hoàn tất phiếu bảo hành (turnaround_hours) có tương quan như thế nào với mức độ hài lòng của khách hàng? (Phục vụ: US2)

---

## 2. NGUỒN DỮ LIỆU VÀ KHỐI LƯỢNG (DATA SOURCES)
1. **survey_responses.csv:**
   - Định dạng: CSV, UTF-8.
   - Tần suất nạp: Hàng ngày / Batch.
   - Khối lượng: ~2.600 dòng.
   - Vấn đề chất lượng: Cột comment bị khuyết ~51.4%; định dạng thời gian lẫn lộn.
2. **tickets_history.csv:**
   - Định dạng: CSV, UTF-8.
   - Khối lượng: ~7.800 dòng.
   - Vai trò: Cung cấp thông tin store_id, technician_id và thời gian xử lý phiếu bảo hành liên kết với khảo sát.
3. **stores.csv & service_centers.csv:**
   - Định dạng: CSV, UTF-8.
   - Khối lượng: 24 dòng cửa hàng, 6 dòng trung tâm.
   - Vai trò: Bảng danh mục chiều (Dimension) phân tích theo địa bàn và người quản lý.

---

## 3. TỪ ĐIỂN DỮ LIỆU NGUỒN (DATA DICTIONARY - BẢNG SURVEY_RESPONSES)
Tỷ lệ thiếu được đo trực tiếp trên tập dữ liệu mẫu:
- `response_id`: Kiểu Int | Mã định danh phản hồi | Tỷ lệ thiếu: 0.0%
- `ticket_id`: Kiểu Int | Mã phiếu bảo hành liên kết | Tỷ lệ thiếu: 0.0%
- `score`: Kiểu Int | Điểm CSAT đánh giá từ 1 đến 5 sao | Tỷ lệ thiếu: 0.0%
- `nps_score`: Kiểu Int | Điểm NPS đánh giá từ 0 đến 10 | Tỷ lệ thiếu: 0.0%
- `comment`: Kiểu Text | Ý kiến đóng góp của khách hàng | Tỷ lệ thiếu: 51.4% (trường tùy chọn)
- `responded_at`: Kiểu Text | Thời điểm khách gửi phản hồi | Tỷ lệ thiếu: 0.0%

---

## 4. QUY TẮC CHẤT LƯỢNG DỮ LIỆU (DATA QUALITY RULES - CÓ NGƯỠNG ĐO ĐƯỢC)
- **CL1 (Completeness):** Sau khi làm sạch và nạp vào Fact, tỷ lệ khuyết thiếu của các trường khóa (ticket_id, date_key, store_key) và điểm số (csat_score, nps_score) phải đạt chính xác 0%.
- **CL2 (Validity):** 100% bản ghi nạp vào fact_survey phải thỏa mãn: 1 <= csat_score <= 5 và 0 <= nps_score <= 10. Dòng dữ liệu vi phạm bị đẩy vào bảng reject_surveys kèm lý do.
- **CL3 (Uniqueness):** Mỗi phiếu bảo hành (ticket_id) chỉ xuất hiện duy nhất 1 lần trong bảng dữ liệu khảo sát (tính duy nhất đạt 100% theo quy tắc QT-10).
- **CL4 (Consistency):** 100% mã chi nhánh trong dữ liệu khảo sát phải ánh xạ thành công tới dim_store. Bản ghi không khớp được gán vào store_key = -1 (Unknown).

---

## 5. PHÁT BIỂU MỨC CHI TIẾT (GRAIN) VÀ QUY TẮC BIẾN ĐỔI
- **Phát biểu GRAIN:** "Một dòng trong bảng fact_survey đại diện cho MỘT LƯỢT PHẢN HỒI ĐÁNH GIÁ KHẢO SÁT HÀI LÒNG của một khách hàng gắn liền với MỘT PHIẾU BẢO HÀNH ĐÃ ĐÓNG tại MỘT CỬA HÀNG/TRUNG TÂM vào MỘT NGÀY CỤ THỂ."
- **Quy tắc phân loại NPS:**
  - nps_score thuộc [9, 10]: Gán is_promoter = 1, is_detractor = 0, is_passive = 0.
  - nps_score thuộc [7, 8]: Gán is_promoter = 0, is_detractor = 0, is_passive = 1.
  - nps_score thuộc [0, 6]: Gán is_promoter = 0, is_detractor = 1, is_passive = 0.
- **Công thức tính chỉ số:**
  - Điểm CSAT trung bình = SUM(csat_score) / COUNT(*).
  - Chỉ số % NPS = [(SUM(is_promoter) - SUM(is_detractor)) / COUNT(*)] * 100%.