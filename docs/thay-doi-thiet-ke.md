# Nhật ký thay đổi thiết kế
## Sau phản hồi Bài tập 1 (buổi 8)

### TD-01 Bổ sung chú thích ký hiệu cho các sơ đồ
- Phản hồi của GV: Use Case Diagram, sơ đồ data flow và star schema chưa có chú thích ký hiệu.
- Quyết định: SỬA
- Lý do: Cần giải thích rõ các ký hiệu mũi tên, quan hệ để bản thiết kế dễ đọc và tuân thủ chuẩn.
- Ảnh hưởng: Bổ sung hộp chú thích vào sơ đồ Use Case, Data Flow và Star Schema.

### TD-02 Điều chỉnh Lập luận kiến trúc số 2
- Phản hồi của GV: Lập luận 2 (SCD loại 2) chưa gắn mã NFR và ngưỡng cụ thể.
- Quyết định: SỬA
- Lý do: Cần tuân thủ chuẩn cấu trúc câu lập luận (Vì [NFR/Ràng buộc có ngưỡng cụ thể] -> Tôi chọn [Giải pháp] -> Đánh đổi là [Chi phí/Hậu quả]).
- Ảnh hưởng: Viết lại nội dung Lập luận 2 ở Mục 3.2, gắn thêm Ràng buộc nghiệp vụ cần lưu vết lịch sử trọn đời.

### TD-03 Bổ sung từ điển dữ liệu cho các bảng trong DWH
- Phản hồi của GV: Các cột của fact_survey và dim mới có kiểu dữ liệu, chưa có mô tả; từ điển ở 4.3 là cho cột nguồn CSV.
- Quyết định: SỬA
- Lý do: Bảng từ điển dữ liệu nguồn chưa đủ để phục vụ phát triển hệ thống; cần có từ điển giải thích ý nghĩa các cột của các bảng lưu trong kho dữ liệu (DWH).
- Ảnh hưởng: Bổ sung thêm bảng "Từ điển dữ liệu DWH" cho các bảng trong Star Schema vào Mục 4.3.

### TD-04 Đánh số thứ tự cho Luồng chính UC2
- Phản hồi của GV: Luồng chính UC2 chưa đánh số bước nên 2a, 4a, 6a không biết rẽ từ bước nào.
- Quyết định: SỬA
- Lý do: Thiếu số thứ tự ở luồng chính (Happy Path) khiến các bước của luồng ngoại lệ (2a, 4a, 6a) bị mất tính tham chiếu.
- Ảnh hưởng: Đánh số thứ tự từ 1 đến 6 cho 6 gạch đầu dòng tại phần "Luồng chính (Happy Path)" của UC2.

### TD-05 Bổ sung trường nhận xét (feedback_comment) vào kho dữ liệu
- Phản hồi của GV: Khung 3 hiển thị feedback_comment nhưng kho dữ liệu không có cột nhận xét.
- Quyết định: SỬA
- Lý do: Dữ liệu trên Dashboard Khung 3 yêu cầu hiển thị "Ý kiến đóng góp của khách hàng" nhưng bảng `fact_survey` chưa lưu thông tin này.
- Ảnh hưởng: Bổ sung cột `feedback_comment` vào bảng `fact_survey` trong Lược đồ Star Schema và cập nhật lại tập lệnh SQL DDL.