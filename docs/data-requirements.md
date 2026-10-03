# ĐẶC TẢ YÊU CẦU DỮ LIỆU (DATA REQUIREMENT SPECIFICATION) - LUỒNG L8

## 1. Phát biểu mức độ chi tiết (GRAIN - 1 câu)
Mỗi bản ghi trong bảng dữ liệu đại diện cho một phiếu phản hồi khảo sát mức độ hài lòng của một khách hàng sau khi hoàn tất một phiếu bảo hành tại một cửa hàng Mekong Mobile.

---

## 2. Bảng nguồn dữ liệu (Data Source Table)

| Tên nguồn dữ liệu | Hệ thống nguồn | Định dạng | Tần suất cập nhật | Khối lượng ước tính |
| :--- | :--- | :--- | :--- | :--- |
| `raw_survey_feedback` | Máy tính bảng quầy dịch vụ (App khảo sát) | Table (SQL Server) | Real-time theo lượt khách đánh giá | ~25,000 bản ghi/tháng |
| `raw_warranty_tickets` | Hệ thống Service Desk (Smart CRM L2) | Table (SQL Server) | Real-time khi đóng phiếu bảo hành | ~28,000 bản ghi/tháng |
| `master_stores` | Hệ thống quản lý chi nhánh | Table (SQL Server) | Hàng tháng khi mở chi nhánh mới | ~50 cửa hàng |

---

## 3. Từ điển dữ liệu nguồn (Data Dictionary)

| Tên cột | Kiểu dữ liệu | Ý nghĩa nghiệp vụ | Giá trị hợp lệ | Tỉ lệ thiếu (Đo mẫu) |
| :--- | :--- | :--- | :--- | :--- |
| `feedback_id` | VARCHAR(36) | Định danh duy nhất của lượt phản hồi | Chuỗi UUID | 0.0% |
| `ticket_id` | VARCHAR(36) | Mã phiếu bảo hành tương ứng | UUID tham chiếu raw_warranty_tickets | 0.0% |
| `store_id` | VARCHAR(20) | Mã chi nhánh cửa hàng Mekong Mobile | Tham chiếu master_stores | 0.0% |
| `csat_score` | INT | Điểm hài lòng về chất lượng sửa chữa | Số nguyên từ 1 đến 5 | 0.0% |
| `nps_score` | INT | Điểm đánh giá mức độ sẵn sàng giới thiệu | Số nguyên từ 0 đến 10 | 1.2% (Khách bỏ qua câu này) |
| `repair_duration_hours`| DECIMAL(5,2)| Tổng thời gian từ lúc nhận máy đến lúc trả máy (giờ) | > 0 | 0.1% |
| `feedback_comment` | NVARCHAR(500)| Ý kiến góp ý dạng văn bản của khách hàng | Chuỗi ký tự tự do | 65.0% (Khách không ghi chú) |
| `created_at` | DATETIME | Thời gian khách hàng gửi phản hồi | Ngày giờ hợp lệ | 0.0% |

---

## 4. Quy tắc chất lượng dữ liệu phải đạt (Data Quality Rules)
* **Tính đầy đủ (Completeness):** Các trường khóa `feedback_id`, `ticket_id`, `store_id` và trường đo lường `csat_score` phải đạt độ đầy đủ >= 99.8%.
* **Tính duy nhất (Uniqueness):** Mỗi phiếu bảo hành `ticket_id` chỉ được tồn tại tối đa một phản hồi khảo sát `feedback_id` tương ứng (tỷ lệ trùng lặp = 0%).
* **Tính hợp lệ (Validity):** 100% giá trị `csat_score` nằm trong khoảng [1, 5]; 100% giá trị `nps_score` hợp lệ phải nằm trong khoảng [0, 10].

---

## 5. Danh sách câu hỏi phân tích (Analytical Questions)

| Mã câu hỏi | Câu hỏi phân tích cần trả lời | Mức chi tiết báo cáo (Granularity) | Truy vết User Story |
| :--- | :--- | :--- | :--- |
| **AQ1** | Điểm CSAT trung bình và cơ cấu NPS (Promoter/Detractor) của từng chi nhánh cửa hàng trong tháng qua như thế nào? | Theo từng Cửa hàng - từng Tháng | US1, US3 |
| **AQ2** | Xu hướng chỉ số NPS ròng của toàn hệ thống Mekong Mobile có sự cải thiện qua các quý không? | Theo toàn hệ thống - từng Quý | US2 |
| **AQ3** | Các ca bảo hành có thời gian sửa kéo dài trên 48 giờ có làm giảm điểm CSAT xuống dưới mức 3 sao không? | Theo khoảng thời gian sửa chữa (Time bucket) | US4 |