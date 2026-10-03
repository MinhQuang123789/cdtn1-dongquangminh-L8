# ĐẶC TẢ YÊU CẦU DỮ LIỆU (DATA REQUIREMENT SPECIFICATION) - TRACK DA

## 1. Phát biểu mức độ chi tiết (GRAIN - 1 câu)
Mỗi bản ghi trong bảng dữ liệu phân tích đại diện cho một câu trả lời của một sinh viên trong một lượt làm bài thi trắc nghiệm cụ thể.

---

## 2. Bảng nguồn dữ liệu (Data Source Table)

| Tên nguồn dữ liệu | Hệ thống nguồn | Định dạng | Tần suất cập nhật | Khối lượng ước tính |
| :--- | :--- | :--- | :--- | :--- |
| `raw_exam_submissions` | SQL Database (Làm bài trực tuyến) | Table (Relational) | Real-time theo lượt nộp | ~15,000 bản ghi/học kỳ |
| `raw_student_answers` | MongoDB (Log chi tiết bài làm) | JSON / NoSQL | Real-time theo từng câu | ~450,000 bản ghi/học kỳ |
| `master_questions` | SQL Database (Ngân hàng câu hỏi) | Table (Relational) | Khi giảng viên cập nhật | ~5,000 câu hỏi |

---

## 3. Từ điển dữ liệu nguồn (Data Dictionary)

| Tên cột | Kiểu dữ liệu | Ý nghĩa nghiệp vụ | Giá trị hợp lệ | Tỉ lệ thiếu (Đo mẫu) |
| :--- | :--- | :--- | :--- | :--- |
| `submission_id` | VARCHAR(36) | Định danh duy nhất của lượt thi | Chuỗi UUID | 0.0% |
| `student_id` | VARCHAR(20) | Mã số sinh viên làm bài | Định dạng chuỗi số chuẩn | 0.0% |
| `exam_id` | VARCHAR(36) | Mã đề thi | UUID tham chiếu master_exams | 0.0% |
| `total_score` | DECIMAL(4,2) | Điểm tổng kết của lượt thi | Từ 0.00 đến 10.00 | 0.0% |
| `time_spent_seconds` | INT | Thời gian sinh viên làm bài (giây) | > 0 và <= thời gian tối đa của đề | 0.2% |
| `question_id` | VARCHAR(36) | Mã câu hỏi | UUID tham chiếu ngân hàng câu | 0.0% |
| `selected_option` | CHAR(1) | Phương án sinh viên chọn | 'A', 'B', 'C', 'D' hoặc NULL | 3.5% (Do SV bỏ trống) |
| `is_correct` | BOOLEAN | Trạng thái đúng/sai | TRUE / FALSE | 0.0% |

---

## 4. Quy tắc chất lượng dữ liệu phải đạt (Data Quality Rules)
* **Tính đầy đủ (Completeness):** Trường `total_score`, `submission_id`, `exam_id` phải đạt độ đầy đủ $\ge 99.8\%$.
* **Tính duy nhất (Uniqueness):** Không tồn tại cặp trùng lặp `(student_id, exam_id)` đối với các bài thi chỉ cho phép thi một lần (độ trùng lặp = 0%).
* **Tính hợp lệ (Validity):** 100% giá trị trường `total_score` phải nằm trong đoạn $[0.00, 10.00]$; trường `selected_option` chỉ nhận các giá trị `{A, B, C, D, NULL}`.

---

## 5. Danh sách câu hỏi phân tích (Analytical Questions)

| Mã câu hỏi | Câu hỏi phân tích cần trả lời | Mức chi tiết báo cáo (Granularity) | Truy vết User Story |
| :--- | :--- | :--- | :--- |
| **AQ1** | Phổ điểm của từng lớp học phần có tuân theo phân phối chuẩn không? Có hiện tượng điểm dị biệt (outlier) bất thường không? | Theo từng Đề thi - từng Lớp học phần | US1, US3 |
| **AQ2** | Những câu hỏi nào có độ phân biệt thấp (D < 0.2) cần được loại bỏ hoặc biên tập lại nội dung? | Theo từng Câu hỏi trắc nghiệm | US2 |
| **AQ3** | Phương án nhiễu nào trong câu hỏi trắc nghiệm không có sinh viên nào lựa chọn? | Theo từng Phương án lựa chọn (A, B, C, D) | US4 |