# TÀI LIỆU YÊU CẦU PHẦN MỀM (SRS RÚT GỌN) - LUỒNG L8: KHẢO SÁT HÀI LÒNG CSAT / NPS

## Mục 1. Giới thiệu & Bảng thuật ngữ
* **Mục đích:** Hệ thống thu thập, tổng hợp và phân tích dữ liệu phản hồi khảo sát mức độ hài lòng của khách hàng (CSAT) và chỉ số đo lường mức độ quảng bá (NPS) sau khi hoàn tất dịch vụ bảo hành/sửa chữa tại chuỗi cửa hàng Mekong Mobile.
* **Bảng thuật ngữ nhất quán:**
  * **CSAT (Customer Satisfaction Score):** Chỉ số đo lường mức độ hài lòng về dịch vụ sửa chữa (thang điểm 1 đến 5).
  * **NPS (Net Promoter Score):** Chỉ số đo lường mức độ khách hàng sẵn sàng giới thiệu dịch vụ cho người khác (thang điểm 0 đến 10, phân loại thành Detractor, Passive, Promoter).
  * **Phiếu khảo sát (Survey Response):** Bản ghi phản hồi đánh giá kèm ý kiến đóng góp của khách hàng sau khi nhận lại thiết bị.

---

## Mục 2. Danh sách User Story (Chuẩn INVEST & MoSCoW)
* **US1 (MUST):** Là Quản lý chất lượng dịch vụ (QA Manager), tôi muốn trích xuất dữ liệu điểm đánh giá CSAT và NPS theo từng chi nhánh cửa hàng để giám sát chất lượng phục vụ của kỹ thuật viên.
  * *Tiêu chí chấp nhận 1 (Given-When-Then):* Given hệ thống đã có phản hồi khảo sát hợp lệ, When tôi chọn mã cửa hàng và khoảng thời gian, Then hệ thống trả về bảng danh sách điểm CSAT trung bình, phân bố điểm NPS và tỷ lệ phản hồi của chi nhánh đó.
  * *Tiêu chí chấp nhận 2 (Ngoại lệ):* Given chi nhánh mới khai trương chưa có dữ liệu phản hồi, When tôi yêu cầu trích xuất dữ liệu, Then hệ thống hiển thị thông báo "Cửa hàng chưa có dữ liệu khảo sát trong kỳ" và không xuất file rỗng.
* **US2 (MUST):** Là Nhà phân tích dữ liệu (Data Analyst), tôi muốn tính toán chỉ số NPS ròng (% Promoter - % Detractor) theo từng tháng để đánh giá xu hướng mức độ trung thành của khách hàng đối với thương hiệu Mekong Mobile.
  * *Tiêu chí chấp nhận 1:* Given tập dữ liệu khảo sát của tháng có tối thiểu 30 phản hồi, When tôi chọn báo cáo xu hướng NPS, Then hệ thống tính toán chỉ số NPS theo công thức chuẩn và vẽ biểu đồ đường (Line chart) biến thiên qua các tháng.
  * *Tiêu chí chấp nhận 2 (Ngoại lệ):* Given số lượng phản hồi trong tháng nhỏ hơn 10 (mẫu quá nhỏ), When hệ thống chạy phân tích, Then hệ thống hiển thị nhãn cảnh báo "Cỡ mẫu nhỏ (<10 phản hồi), chỉ số NPS mang tính tham khảo" kèm số lượng mẫu thực tế.
* **US3 (MUST):** Là Giám đốc dịch vụ khách hàng, tôi muốn xem bảng điều khiển (Dashboard) so sánh chỉ số CSAT giữa các cửa hàng trên toàn quốc để khen thưởng các đơn vị xuất sắc và hỗ trợ cải thiện các cửa hàng điểm thấp.
  * *Tiêu chí chấp nhận 1:* Given có ít nhất 2 cửa hàng có dữ liệu phản hồi, When tôi mở màn hình đối sánh chi nhánh, Then hệ thống hiển thị biểu đồ cột so sánh điểm CSAT và xếp hạng các cửa hàng từ cao xuống thấp.
  * *Tiêu chí chấp nhận 2 (Ngoại lệ):* Given một cửa hàng bị lỗi mất kết nối đồng bộ dữ liệu khảo sát, When hệ thống dựng biểu đồ, Then hệ thống hiển thị biểu tượng cảnh báo "Dữ liệu đang đồng bộ dở dang" tại cột của cửa hàng đó.
* **US4 (SHOULD):** Là Nhà phân tích dữ liệu, tôi muốn phân tích ma trận tương quan giữa thời gian chờ sửa chữa và điểm hài lòng CSAT để tìm điểm nghẽn trong quy trình kỹ thuật.
* **US5 (SHOULD):** Là Quản lý cửa hàng, tôi muốn nhận thông báo cảnh báo tức thì khi có phản hồi đánh giá cực thấp (CSAT = 1 sao hoặc NPS <= 3) để kịp thời liên hệ xử lý khiếu nại cho khách hàng.
* **US6 (SHOULD):** Là Kỹ sư dữ liệu, tôi muốn thiết lập tiến trình ETL tự động tổng hợp bảng Fact khảo sát từ cơ sở dữ liệu phiếu bảo hành sang Data Warehouse vào lúc 23:00 hàng ngày.
* **US7 (COULD):** Là Quản lý chất lượng, tôi muốn xuất toàn bộ ý kiến đóng góp dạng văn bản tự do của khách hàng ra tệp Excel để phân tích từ khóa khiếu nại.
* **US8 (WON'T):** Là Hệ thống, tự động phân tích cảm xúc (Sentiment Analysis) trên văn bản đánh giá bằng mô hình ngôn ngữ lớn (hoãn lại phiên bản sau).

---

## Mục 3. Yêu cầu chức năng (FR)
* **FR1:** Hệ thống trích xuất và lưu trữ dữ liệu khảo sát CSAT và NPS gắn liền với mã phiếu bảo hành và mã cửa hàng.
* **FR2:** Hệ thống tự động tính toán tỷ lệ % Promoter, % Passive, % Detractor và chỉ số NPS tổng thể theo công thức chuẩn.
* **FR3:** Hệ thống hiển thị bảng điều khiển so sánh chỉ số CSAT/NPS đa chiều (theo thời gian, theo chi nhánh cửa hàng, theo nhóm lỗi thiết bị).
* **FR4:** Hệ thống cung cấp báo cáo phân tích độ trễ sửa chữa ảnh hưởng tới điểm hài lòng của khách hàng.
* **FR5:** Hệ thống hỗ trợ bộ lọc dữ liệu theo khoảng ngày, dòng sản phẩm bảo hành và phân loại điểm số.

---

## Mục 4. Yêu cầu phi chức năng có ngưỡng số (NFR)
* **NFR1 (Thời gian phản hồi):** Thời gian tải và vẽ lại toàn bộ biểu đồ trên Dashboard CSAT/NPS không vượt quá **3 giây** với tập dữ liệu 50,000 lượt phản hồi.
* **NFR2 (Độ chính xác dữ liệu):** Tỷ lệ ghép nối thành công giữa phiếu khảo sát và phiếu bảo hành (Foreign Key Integrity) đạt **100%** trong luồng ETL.
* **NFR3 (Độ trễ đồng bộ):** Dữ liệu phản hồi khảo sát từ máy tính bảng tại cửa hàng được đồng bộ về kho dữ liệu trong vòng tối đa **10 phút**.

---

## Mục 5. Use Case & Đặc tả chi tiết Use Case chính

### 5.1. Danh sách Use Case
* **Actor:** Quản lý chất lượng dịch vụ (QA Manager), Giám đốc dịch vụ khách hàng, Hệ thống lập lịch (Scheduler).
* **Danh sách Use Case:**
  1. `Trích xuất dữ liệu khảo sát CSAT và NPS`
  2. `Phân tích chỉ số NPS ròng và xu hướng`
  3. `Xem bảng điều khiển so sánh điểm chi nhánh`
  4. `Phân tích tương quan thời gian sửa và mức hài lòng`
  5. `Đồng bộ dữ liệu khảo sát định kỳ (ETL)`
  6. `Xuất báo cáo chất lượng dịch vụ`

### 5.2. Đặc tả chi tiết Use Case: "Phân tích chỉ số NPS ròng và xu hướng"
* **Mã UC:** UC2
* **Tên UC:** Phân tích chỉ số NPS ròng và xu hướng
* **Actor chính:** Quản lý chất lượng dịch vụ
* **Điều kiện tiên quyết:** Đã có dữ liệu khảo sát được ghi nhận trong khoảng thời gian được chọn.
* **Điều kiện sau:** Biểu đồ xu hướng và bảng phân loại NPS được tính toán và hiển thị.
* **Luồng chính:**
  1. Người dùng chọn mục "Phân tích chỉ số NPS" trên thanh điều hướng.
  2. Hệ thống hiển thị bộ lọc thời gian; Người dùng chọn khoảng thời gian (theo tháng hoặc theo quý) và nhấn "Phân tích".
  3. Hệ thống tải toàn bộ dữ liệu phản hồi khảo sát hợp lệ trong kỳ.
  4. Hệ thống phân loại điểm số: 9-10 điểm là Promoter, 7-8 điểm là Passive, 0-6 điểm là Detractor.
  5. Hệ thống tính toán chỉ số NPS = % Promoter - % Detractor.
  6. Hệ thống hiển thị biểu đồ xu hướng đường và bảng cơ cấu tỷ lệ phần trăm các nhóm khách hàng.
* **Luồng ngoại lệ:**
  * **3a. Không có dữ liệu phản hồi trong khoảng thời gian đã chọn:**
    * 3a1. Khoảng thời gian người dùng chọn không có bất kỳ lượt đánh giá nào.
    * 3a2. Hệ thống thông báo: *"Không tìm thấy dữ liệu khảo sát trong giai đoạn này"* và giữ nguyên màn hình lọc.
  * **4a. Dữ liệu điểm khảo sát bị sai định dạng ngoài dải 0-10:**
    * 4a1. Tồn tại bản ghi có điểm đánh giá < 0 hoặc > 10 hoặc bị NULL do lỗi đường truyền.
    * 4a2. Hệ thống tự động cô lập bản ghi lỗi vào bảng theo dõi chất lượng dữ liệu, chỉ tính toán trên các bản ghi hợp lệ và hiển thị thông báo: *"Đã loại trừ X bản ghi không hợp lệ khỏi tập phân tích"*.

---

## Mục 6. Bảng truy vết yêu cầu (Traceability Matrix)

| Mã FR | Tên yêu cầu chức năng | Mã User Story | Mã Use Case | Mức MoSCoW |
| :--- | :--- | :--- | :--- | :--- |
| **FR1** | Trích xuất và lưu trữ dữ liệu khảo sát | US1 | UC1 | MUST |
| **FR2** | Tính toán chỉ số NPS và cơ cấu khách hàng | US2 | UC2 | MUST |
| **FR3** | Bảng điều khiển so sánh đối sánh chi nhánh | US3 | UC3 | MUST |
| **FR4** | Phân tích tương quan thời gian và mức hài lòng | US4 | UC4 | SHOULD |
| **FR5** | Đồng bộ dữ liệu định kỳ (ETL) | US6 | UC5 | SHOULD |