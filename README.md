# Smart CRM - Mekong Mobile: Phân hệ Khảo sát CSAT / NPS (Luồng L8)

- **Sinh viên:** Đồng Quang Minh
- **MSSV:** 2374802010308
- **Chuyên ngành (Track):** Data Analytics (DA)
- **Học phần:** Chuyên đề Tốt nghiệp 1 (HK1 2026-2027)

## 1. Mục tiêu
Xây dựng pipeline dữ liệu và kho dữ liệu phân tích (Star Schema) phục vụ đo lường, giám sát chỉ số hài lòng CSAT và chỉ số khuyến nghị NPS từ phản hồi của khách hàng sau khi đóng phiếu bảo hành tại Mekong Mobile.

## 2. Yêu cầu môi trường
- Python 3.11+
- PostgreSQL 16
- Thư viện: pandas, sqlalchemy, python-dotenv

## 3. Cấu trúc thư mục tài liệu thiết kế (BT1)
- `docs/srs.md`: Bản đặc tả yêu cầu rút gọn 6 mục
- `docs/usecase.drawio`: Sơ đồ Use Case Diagram (file gốc draw.io)
- `docs/architecture.drawio`: Sơ đồ kiến trúc luồng dữ liệu (Data Architecture)
- `docs/dwh.drawio`: Lược đồ hình sao (Star Schema cho Kho dữ liệu)
- `docs/wireframe.drawio`: Thiết kế 3 khung Dashboard phân tích BI
- `docs/data-requirements.md`: Đặc tả yêu cầu dữ liệu (Data Spec theo Track DA)
- `docs/ai-disclosure.md`: Bảng khai báo sử dụng công cụ AI
- `db/schema.sql`: Kịch bản DDL khởi tạo bảng kho dữ liệu

## 4. Trạng thái hiện tại
- [x] Khởi tạo dự án và smoke test (Buổi 2)
- [x] Hoàn thiện hồ sơ Phân tích & Thiết kế BT1 (Buổi 6)
- [ ] Xây dựng Pipeline trích xuất và làm sạch dữ liệu (Buổi 7-9)
- [ ] Nạp kho dữ liệu và Dashboard phân tích (Buổi 10-12)