# Checklist Tự Đánh Giá Bảo Mật (OWASP Top 10:2025 & Track DA)

1. **Không có secret nào trong repo (`A02:2025`):** **ĐÃ LÀM** — `.env` nằm trong `.gitignore`; `git log --all --oneline -- .env` trả về rỗng; mật khẩu và `PSEUDO_KEY` tách ra `.env.example`.
2. **Dữ liệu vào được kiểm tra ở tầng ứng dụng (`A05:2025`):** **ĐÃ LÀM** — Quy tắc `CL1`–`CL5` kiểm tra miền giá trị, kiểu số và định dạng ngày; truy vấn SQL tham số hóa (`%s`) chống SQL Injection (`TC-03`, `TC-04`, `TC-06`, `TC-10` **PASS**).
3. **Kiểm soát truy cập theo vai trò (`A01:2025`):** **ĐÃ LÀM** — Dashboard kết nối bằng user `nha_phan_tich` chỉ có quyền `SELECT` trên View; `SELECT * FROM dim_customer` bị chặn với lỗi `permission denied` (`TC-12` **PASS**).
4. **Mật khẩu và dữ liệu nhạy cảm được băm hoặc giả danh hóa (`A04:2025`):** **ĐÃ LÀM** — Định danh khách hàng (`customer_pseudo_id`) được băm bằng `HMAC-SHA256` với `PSEUDO_KEY` từ `.env` (`TC-08` **PASS**); `v_store_summary` áp dụng ngưỡng nhóm tối thiểu (`HAVING COUNT >= 3`).
5. **Thông báo lỗi không để lộ cấu trúc bên trong (`A10:2025`, `A02:2025`):** **ĐÃ LÀM** — Cấu hình `showErrorDetails = false` trong `.streamlit/config.toml` và bắt ngoại lệ trong `src/dashboard/app.py` để ẩn `DWH_URL`.
6. **Nhật ký hệ thống không ghi secret hay dữ liệu cá nhân (`A09:2025`):** **ĐÃ LÀM** — `src/log_config.py` và `src/pipeline.py` chỉ ghi mã lô, số lượng dòng và mã quy tắc vi phạm dưới dạng JSON.
7. **Phụ thuộc bên ngoài được ghim phiên bản cứng (`A03:2025`):** **ĐÃ LÀM** — Tất cả 6 thư viện trong `requirements.txt` đều khóa cứng phiên bản bằng `==`.
