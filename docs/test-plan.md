# Kế hoạch Kiểm thử (Test Plan) — Luồng L8: Khảo sát CSAT/NPS (Track DA)

## 1. Phạm vi kiểm thử và phần chủ ý không kiểm
- **Phạm vi kiểm thử:** Quy tắc chuẩn hóa và kiểm tra dữ liệu (`CL1`–`CL5`: CSAT `[1, 5]`, NPS `[0, 10]`, định dạng ngày, tính duy nhất `response_id`, bắt buộc `ticket_id`); giả danh hóa HMAC-SHA256; đo 3 chiều chất lượng dữ liệu (Đầy đủ, Chính xác, Nhất quán); nạp kho PostgreSQL (`ON CONFLICT` không nhân đôi, tách dòng lỗi vào `reject_survey`) và phân quyền `nha_phan_tich`.
- **Phần chủ ý không kiểm và lý do:** Kiểm thử tải hàng triệu bản ghi (thuộc phạm vi Chuyên đề tốt nghiệp 2) và kiểm thử giao diện tự động bằng Selenium (Dashboard chỉ hiển thị biểu đồ từ View, logic đã kiểm ở tầng dữ liệu).

## 2. Loại test và số lượng mỗi tầng
Tổng cộng **12 nhóm test case** (**16 test runs** tham số hóa):
- **Unit Test (7 test cases — `TC-01` đến `TC-07`):** Kiểm tra hàm thuần chuẩn hóa điểm, giá trị biên, định dạng ngày và dữ liệu rác (`tests/test_rules.py`).
- **Integration Test & Quality/Security (4 test cases — `TC-08` đến `TC-10`, `TC-12`):** Kiểm tra giả danh hóa HMAC-SHA256, đo 3 chiều chất lượng, tách dòng bẩn vào `reject_survey` và chặn quyền đọc bảng gốc của `nha_phan_tich` (`tests/test_bt3_integration.py`).
- **System / Idempotency Test (1 test case — `TC-11`):** Kiểm tra chạy lại pipeline 2 lần liên tiếp không nhân đôi dữ liệu trong `fact_survey`.

## 3. Tiêu chí thành công đo được
- **100% (12/12)** test case (16/16 test runs) chạy thực tế đạt `PASS` bằng lệnh `pytest -v`.
- Mọi quy tắc nghiệp vụ đã hiện thực đều có test bao phủ; không còn bug mức `Critical` hoặc `Major` chưa sửa.

## 4. Môi trường và dữ liệu thử
- **Môi trường:** Docker (`python:3.12-slim` và `postgres:16-alpine`) điều phối qua `docker-compose.yml`.
- **Dữ liệu thử:** `data/sample/survey_sample.csv` (10 bản ghi sạch) và `data/sample/survey_dirty_sample.csv` (7 bản ghi: 3 sạch, 4 lỗi `CL1, CL2, CL3, CL5`). Dọn sạch bảng trước mỗi test bằng `TRUNCATE TABLE fact_survey, reject_survey RESTART IDENTITY`.
