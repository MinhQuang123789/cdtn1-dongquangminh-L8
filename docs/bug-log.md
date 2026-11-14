# Nhật ký Sửa lỗi (Bug Log) — Luồng L8 (Track DA)

## BUG-01: Pipeline chưa kết nối được PostgreSQL và thiếu cơ chế khởi tạo bảng tự động
1. **Mã bug và mức độ:** BUG-01 — **CRITICAL** (Hệ thống không nạp được dữ liệu vào kho PostgreSQL khi chạy trong Docker và thiếu bảng `reject_survey`).
2. **Phát hiện bởi:** Kiểm thử tích hợp khi chuyển từ mô phỏng BT2 sang kho dữ liệu thật ở BT3 (`TC-10`, `TC-11`).
3. **Triệu chứng:** Container `pipeline` không ghi được bản ghi vào PostgreSQL; volume mới khởi tạo không có bảng `fact_survey`, `reject_survey` và chưa có role hạn chế cho Dashboard.
4. **Cách tái lập:** Chạy `docker compose down -v && docker compose up -d` và chạy `python -m src.pipeline`; kiểm tra PostgreSQL thấy chưa tồn tại bảng dữ liệu.
5. **Nguyên nhân:** `requirements.txt` thiếu thư viện `psycopg2-binary`; `docker-compose.yml` chưa mount thư mục `./db/init` vào `/docker-entrypoint-initdb.d`; `src/pipeline.py` mới chỉ dừng ở pha Load giả lập.
6. **Cách sửa:** Bổ sung `psycopg2-binary==2.9.10` vào `requirements.txt`; tạo `db/init/001_schema.sql` và `002_seed_and_security.sql`; viết `src/load/warehouse_loader.py` hỗ trợ `ON CONFLICT` và tách `reject_survey`; cập nhật `docker-compose.yml`.
7. **Link commit và xác nhận:** https://github.com/MinhQuang123789/cdtn1-dongquangminh-L8/commit/e6f7bb57c3941105eb694864595acae1b64dbde2 — Đã chạy lại `docker compose up -d --build`, bảng tự động khởi tạo và nạp dữ liệu thành công (`TC-10`, `TC-11` -> **PASS**).

---

## BUG-02: Lệnh `pytest -v` trong container lỗi `ModuleNotFoundError: No module named 'src'` và quét nhầm tệp mẫu cũ
1. **Mã bug và mức độ:** BUG-02 — **MAJOR** (Bộ kiểm thử tự động không thể chạy bằng lệnh tiêu chuẩn `pytest -v` trong môi trường sạch).
2. **Phát hiện bởi:** Chạy lệnh `docker compose run --rm pipeline pytest -v` tại buổi 14.
3. **Triệu chứng:** Pytest dừng ngay ở bước thu thập test với 3 lỗi: `ModuleNotFoundError: No module named 'src'` và `FileNotFoundError: 'data/sample/warranty_sample.csv'` tại `src/smoke_test.py`.
4. **Cách tái lập:** Khởi động container `pipeline` và gõ trực tiếp `pytest -v` tại thư mục `/app`.
5. **Nguyên nhân:** Chưa có tệp `pytest.ini` khai báo `pythonpath = .` và `testpaths = tests`, khiến pytest không nhận diện package `src` đồng thời quét nhầm tệp `src/smoke_test.py` còn giữ đường dẫn tệp mẫu cũ.
6. **Cách sửa:** Tạo tệp `pytest.ini` ở thư mục gốc với `pythonpath = .` và `testpaths = tests`; cập nhật đường dẫn dữ liệu trong `src/smoke_test.py` sang `data/sample/survey_sample.csv`.
7. **Link commit và xác nhận:** https://github.com/MinhQuang123789/cdtn1-dongquangminh-L8/commit/26253f49b189624a1c658086301645f46a027dfd — Đã build lại image và chạy `docker compose run --rm pipeline pytest -v`, toàn bộ 16 test đều được thu thập và chạy ổn định (**PASS**).

---

## BUG-03: Tệp dữ liệu mẫu sạch `survey_sample.csv` bị lẫn bản ghi sai định dạng ngày
1. **Mã bug và mức độ:** BUG-03 — **MAJOR** (Dữ liệu đầu vào chuẩn bị sai làm phép đo 3 chiều chất lượng dữ liệu thất bại).
2. **Phát hiện bởi:** `TC-09` (`test_TC09_do_ba_chieu_chat_luong_du_lieu_sach`) và `TC-11`.
3. **Triệu chứng:** `TC-09` báo lỗi `ValueError: time data "khong-phai-ngay" doesn't match format "%Y-%m-%d %H:%M:%S"` và `TC-11` chỉ nạp được 3 dòng thay vì 10 dòng.
4. **Cách tái lập:** Chạy `pytest -v` khi `data/sample/survey_sample.csv` chứa 7 dòng dữ liệu kiểm thử lỗi.
5. **Nguyên nhân:** Tệp dữ liệu mẫu sạch `survey_sample.csv` bị ghi đè bởi dữ liệu kiểm thử bẩn trong quá trình thử nghiệm thủ công trước đó, đồng thời tệp `survey_dirty_sample.csv` chưa được tách riêng.
6. **Cách sửa:** Khôi phục đúng 10 bản ghi sạch trong `data/sample/survey_sample.csv` và tạo tệp riêng `data/sample/survey_dirty_sample.csv` (7 dòng) phục vụ riêng cho `TC-10`.
7. **Link commit và xác nhận:** https://github.com/MinhQuang123789/cdtn1-dongquangminh-L8/commit/6d4aebbc5cfacf80705fea1353aa5b77b6d2e394 — Đã chạy lại toàn bộ bộ kiểm thử `docker compose run --rm pipeline pytest -v`: **16 passed in 0.88s** (**PASS**).