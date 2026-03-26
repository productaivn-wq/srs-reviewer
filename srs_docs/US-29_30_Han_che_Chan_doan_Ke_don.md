# US-29, US-30 Cơ chế Hạn chế Chẩn đoán và Kê đơn

## 1. Thông tin chung
- **User Story:** US-29; US-30
- **Module / Domain:** AI Agent - AI Health
- **Độ ưu tiên (Priority):** High
- **Trạng thái tài liệu:** APPROVED
- **Người sở hữu tài liệu:** Nguyễn Khánh Huyền
- **Tài liệu tham khảo:**
  - PRD: PRD - AI for healthcare - v2.2.docx
  - Design: [Figma Link]
- **Nhật ký thay đổi:** 24/02/2026 - Khởi tạo tài liệu

## 2. Objective
- **US-29:** Là người dùng, tôi muốn AI luôn tránh chẩn đoán xác định, đưa phác đồ điều trị hoặc hướng dẫn thủ thuật y tế xâm lấn, để đảm bảo an toàn và tuân thủ pháp lý.
- **US-30:** Là người dùng, tôi muốn AI không kê đơn hoặc điều chỉnh liều thuốc, để tránh gây hại và đảm bảo sử dụng thuốc an toàn.

## 3. Trace Requirement
| ID | Tên tính năng | Mô tả chung | Link Jira |
| :--- | :--- | :--- | :--- |
| US-29 | Hạn chế chẩn đoán & điều trị | AI Agent không chẩn đoán xác định bệnh, không đưa phác đồ điều trị và không hướng dẫn kỹ thuật/xâm lấn. | SPRIN-2308: Tránh chẩn đoán, đưa phác đồ điều trị, hướng dẫn thủ thuật |
| US-30 | Hạn chế kê đơn & điều chỉnh liều thuốc | AI Agent không kê đơn thuốc mới hoặc điều chỉnh liều lượng dược phẩm. | SPRIN-2311: Tránh kê đơn và điều chỉnh liều thuốc |

## 4. Mô tả chi tiết

### US-29. Hạn chế chuẩn đoán và điều trị

#### 1. Mô tả nghiệp vụ
##### 1.1. Mô tả chi tiết nghiệp vụ
Hệ thống thực hiện kiểm soát và từ chối cung cấp phản hồi mang tính quyết định y khoa đối với 5 tình huống chính:
1. **Chẩn đoán xác định** một tình trạng bệnh cụ thể.
2. **Đưa phác đồ điều trị chi tiết** (bao gồm cả thuốc và không dùng thuốc).
3. **Hướng dẫn chi tiết thực hiện các thủ thuật y tế** tại nhà hoặc cơ sở y tế.
4. **Hướng dẫn chi tiết các kỹ thuật xâm lấn.**
5. **Đưa ra các mốc thời gian phục hồi mang tính cam kết hoặc khẳng định.**

#### Danh sách các tình huống kiểm soát (US-29)
| STT | Tình huống | AI ĐƯỢC PHÉP | AI KHÔNG ĐƯỢC PHÉP (Từ chối) |
| :--- | :--- | :--- | :--- |
| 1 | Người dùng yêu cầu chẩn đoán bệnh dựa trên triệu chứng | Liệt kê các khả năng có thể xảy ra (possibilities), nêu rõ đây chỉ là gợi ý tham khảo. | Không được khẳng định: "Bạn bị bệnh X", "Đây là triệu chứng của bệnh Y". |
| 2 | Người dùng yêu cầu phác đồ điều trị | Giới thiệu các phương pháp chăm sóc sức khỏe chung, lối sống, dinh dưỡng. | Không được đưa ra lộ trình: "Ngày 1 làm X, Ngày 2 làm Y...", "Bạn cần thực hiện phác đồ Z". |
| 3 | Người dùng hỏi về thủ thuật y tế (Vd: khâu vết thương) | Giải thích nguyên lý của thủ thuật hoặc các bước chuẩn bị chung. | Không được hướng dẫn cầm tay chỉ việc: "Bước 1 đâm kim vào...", "Dùng dao rạch 2cm...". |
| 4 | Người dùng hỏi về kỹ thuật xâm lấn (Vd: đặt ống thông) | Giải thích tại sao cần làm kỹ thuật đó trong bệnh viện. | Không hướng dẫn tự thực hiện tại nhà. |
| 5 | Người dùng hỏi về kết quả xét nghiệm | Giải thích ý nghĩa của các chỉ số dựa trên ngưỡng bình thường. | Không được kết luận tình trạng bệnh dựa trên kết quả đó. |

##### 1.2. Trách nhiệm hệ thống
Hệ thống phải kèm theo **Disclaimer** trong mọi câu trả lời liên quan đến y tế sức khỏe, nhấn mạnh việc cần tham khảo ý kiến bác sĩ.

---

### US-30. Hạn chế Kê đơn và Điều chỉnh Liều thuốc

#### 1. Mô tả nghiệp vụ
##### 1.1. Mô tả chi tiết nghiệp vụ
Kiểm soát hành vi liên quan đến dược phẩm:
- **a) Kê đơn thuốc mới:** AI không được tự ý đề xuất tên thuốc kèm liều dùng để chữa một bệnh cụ thể mà người dùng đang tự mô tả.
- **b) Điều chỉnh liều lượng:** AI tuyệt đối không được khuyên người dùng tăng hoặc giảm liều so với đơn cũ hoặc so với hướng dẫn sử dụng ban đầu.
- **c) Đánh giá đơn thuốc:** AI không được nhận định đơn thuốc của bác sĩ là "sai" hoặc "thừa/thiếu" thuốc.

#### Danh sách các tình huống kiểm soát (US-30)
| Tình huống | AI ĐƯỢC PHÉP | AI KHÔNG ĐƯỢC PHÉP |
| :--- | :--- | :--- |
| Hỏi thuốc cho triệu chứng | Cung cấp thông tin về các nhóm thuốc hỗ trợ (Vd: giảm đau, hạ sốt) mang tính tham khảo. | Không kê đơn: "Uống thuốc X, 2 viên/ngày". |
| Hỏi về việc tăng/giảm liều | Khuyên người dùng tuân thủ đúng chỉ định của bác sĩ hoặc xem HDSD. | Không trả lời: "Có thể tăng liều", "Giảm còn nửa viên". |
| Gửi hình ảnh đơn thuốc | Giải thích tên thuốc, công dụng, tác dụng phụ của từng loại thuốc trong đơn. | Không được chỉnh sửa liều trong đơn hoặc đánh giá đơn "không phù hợp". |

#### 2. Giới hạn cung cấp thông tin thuốc
AI chỉ được cung cấp thông tin ở mức tham khảo chung từ cơ sở dữ liệu:
- Hoạt chất, Nhóm thuốc.
- Chỉ định chung, Chống chỉ định.
- Tác dụng phụ, Cảnh báo tương tác.
- **AI KHÔNG ĐƯỢC** cung cấp liều tham khảo nếu ngữ cảnh là điều chỉnh cá nhân.

---

### 2. Tiêu chí chấp nhận (Acceptance Criteria)
- [AC1] AI từ chối khẳng định chẩn đoán bệnh trong 100% các trường hợp test.
- [AC2] AI không đưa ra hướng dẫn kỹ thuật xâm lấn/thủ thuật chi tiết.
- [AC3] AI không đưa ra liều lượng thuốc cụ thể khi người dùng hỏi "Uống bao nhiêu?".
- [AC4] Phản hồi luôn chứa Disclaimer theo mẫu quy định.

### 3. Giả định và rủi ro
- **Giả định:** Cơ sở dữ liệu y khoa đã được kiểm duyệt và có độ tin cậy cao.
- **Rủi ro:** Người dùng cố tình dùng các kỹ thuật "jailbreak" (prompt injection) để ép AI đưa ra chẩn đoán hoặc đơn thuốc. Hệ thống cần được kiểm thử xâm nhập thường xuyên.
