## BUG-001: Không sinh được file báo cáo chất lượng
- **Mã và mức độ:** BUG-001 | Minor
- **Phát hiện bởi:** Chạy thử file pipeline.py
- **Triệu chứng:** Terminal chạy xong nhưng thư mục reports/ trống trơn.
- **Cách tái lập:** Chạy lệnh `python -m src.pipeline`
- **Nguyên nhân:** Khối lệnh ghi file bằng `os.makedirs` nằm ngoài hàm `run_pipeline()`, không truy cập được biến cục bộ `df` và `ket_qua` nên báo lỗi NameError ngầm.
- **Cách sửa:** Thụt lề đưa đoạn code ghi file vào bên trong hàm `run_pipeline()`.
- **Commit và xác nhận:** Test chạy lại sinh file .txt thành công.