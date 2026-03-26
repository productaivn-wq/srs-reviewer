# US-35: Cơ chế đảm bảo không có quảng cáo hoặc gợi ý thương mại

## 1. Thông tin chung
- **Epic / Feature**: [SPRIN-2307: An toàn, quyền riêng tư & phạm vi tư vấn của AI](https://vin3s.atlassian.net/browse/SPRIN-2307)
- **User Story**: [SPRIN-2547: Không quảng cáo trong AI tra cứu SKYT chuyên sâu](https://vin3s.atlassian.net/browse/SPRIN-2547)
- **Module / Domain**: AI Agent - AI Health
- **Priority**: High
- **Document Status**: Approved
- **Document owner**: BA Team AI Agent
- **Reference Document**: PRD - AI for healthcare - v2.2.docx
- **Design**: [Figma Link](https://www.figma.com/design/fOkcQUDzMNlN5vR7PiQxaF/-Handoff--V-AI-Chat---Health-agent?node-id=0-1&p=f&t=n3Rr0QOg5HE20pnG-0)

## 2. Objective
- **I want**: Là người dùng, tôi muốn các phản hồi từ AI Health không có quảng cáo hoặc gợi ý thương mại.
- **So that**: Để tôi có thể tin tưởng vào tính khách quan và an toàn của các thông tin y tế được cung cấp.

## 3. Trace Requirement
| ID | Tên tính năng | Mô tả chung | PIC |
| --- | --- | --- | --- |
| US-35-01 | Cơ chế Tách biệt Nội dung Y khoa và Thương mại | Hệ thống AI Agent và các thành phần liên quan phải đảm bảo toàn bộ tính năng Health không chứa quảng cáo, gợi ý thương mại trực tiếp (product placement) hoặc các yếu tố khuyến nghị mua hàng từ bên thứ ba. | AI Agent |
| US-35-02 | Không sử dụng dữ liệu từ AI Health để phục vụ mục đích quảng cáo | Hệ thống V-App đảm bảo không sử dụng dữ liệu sức khỏe (bao gồm lịch sử chat và dữ liệu đồng bộ từ thiết bị) cho mục đích marketing hoặc quảng cáo cá nhân hóa bên ngoài phạm vi y tế của ứng dụng. | Super App |

## 4. Mô tả chi tiết

### 1. Mô tả nghiệp vụ (Dựa trên US-32: Cơ chế đảm bảo không có quảng cáo hoặc gợi ý thương mại)

#### 1.1 Quy tắc kiểm soát nội dung thương mại

- **(a) Nội dung bị cấm tuyệt đối**:
  - Phản hồi của hệ thống AI Agent không được bao gồm thông điệp marketing hoặc CTA thương mại (ví dụ: "Đặt ngay", "Đăng ký gói", "Dùng thử miễn phí").
  - Không chủ động gợi ý tên thương hiệu, giá dịch vụ, hoặc thông tin khuyến mãi/ưu đãi.
  - AI không được lợi dụng ngữ cảnh tư vấn sức khỏe để chèn nội dung có tính chất quảng bá thương mại một cách gián tiếp.
- **(b) Nội dung được phép có điều kiện**:
  - Hệ thống được phép đề cập đến thông tin dịch vụ y tế của cơ sở y tế cụ thể (gói khám, bảo hiểm, xét nghiệm) khi và chỉ khi người dùng chủ động hỏi.
  - Khi được phép đề cập, nội dung phải tuân thủ: chỉ mang tính cung cấp thông tin khách quan, không so sánh thiên hướng và không sử dụng ngôn ngữ tạo urgency thương mại (ví dụ: "ưu đãi có hạn").
- **(c) Quy tắc ngôn ngữ**:
  - Toàn bộ phản hồi phải sử dụng ngôn ngữ trung lập.
  - Gợi ý chuyên khoa (nếu có) chỉ nêu tên chuyên khoa phù hợp và lý do y khoa, không kèm tên cơ sở y tế cụ thể trong cùng phản hồi.

#### 1.2. Trách nhiệm hệ thống

| Thành phần | Trách nhiệm |
| --- | --- |
| **AI Agent** | - Không sinh nội dung quảng cáo trong mọi phản hồi health.<br>- Không đề xuất sản phẩm thương mại.<br>- Không dùng dữ liệu health để cá nhân hóa nội dung thương mại.<br>- Chỉ đưa khuyến nghị y khoa trung lập khi có trigger hợp lệ. |
| **V-App** | - Không hiển thị quảng cáo trong giao diện Health.<br>- Không chèn banner thương mại. |

### 2. Tiêu chí chấp nhận (Acceptance Criteria)

- **AC-01**: AI Health không chủ động đề xuất gói khám hoặc bảo hiểm cụ thể trong phản hồi tư vấn sức khỏe. Chỉ hiển thị thông tin gói khám/bảo hiểm khi người dùng chủ động yêu cầu bằng câu hỏi có ý định rõ ràng (ví dụ: "có gói khám nào phù hợp không?").
- **AC-02**: Khi AI Health khuyến nghị người dùng khám chuyên khoa, phản hồi chỉ chứa thông tin y tế (lý do cần khám, chuyên khoa phù hợp). Không được kèm tên cơ sở y tế cụ thể (trừ khi người dùng chủ động yêu cầu thông tin về cơ sở y tế), giá dịch vụ, hoặc link đặt lịch trong cùng phản hồi khuyến nghị.
- **AC-03**: Phản hồi của AI Health không được chứa các yếu tố sau: lời kêu gọi mua/đăng ký dịch vụ (CTA thương mại), so sánh giá hoặc khuyến mãi, ngôn ngữ tạo urgency thương mại (ví dụ: "ưu đãi có hạn", "chỉ còn X suất"), tên thương hiệu sản phẩm/dịch vụ trả phí.
