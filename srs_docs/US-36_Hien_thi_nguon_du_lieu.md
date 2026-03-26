# US-36: Hiển thị nguồn dữ liệu y khoa

**Tác giả:** Lê Quỳnh Mai
**Ngày cập nhật:** 14/03/2026
**Lượt xem:** 13

---

## 1. Thông tin chung

- **Epic / Feature:** [SPRIN-2307: An toàn, quyền riêng tư & phạm vi tư vấn của AI](https://vin3s.atlassian.net/browse/SPRIN-2307) (New)
- **User Story:** [SPRIN-2314: Minh bạch nguồn dữ liệu y khoa](https://vin3s.atlassian.net/browse/SPRIN-2314) (In Review)
- **Module / Domain:** AI Agent - AI Health
- **Ghi chú:** Mô tả dưới đây chỉ tập trung mô tả năng lực của team AI Agent để đáp ứng cho tính năng Hiển thị nguồn y khoa uy tín AI Health. Không đại diện cho mô tả US của Super App.
- **Độ ưu tiên:** High
- **Trạng thái tài liệu:** Approved
- **Chủ sở hữu tài liệu:** BA Team AI Agent
- **Tài liệu tham khảo:**
  - PRD: PRD - AI for healthcare - v2.2.docx
  - Design: [Figma Link](https://www.figma.com/design/fOkcQUDzMNlN5vR7PiQxaF/-Handoff--V-AI-Chat---Health-agent?node-id=0-1&p=f&t=n3Rr0QOg5HE20pnG-0)

---

## 2. Objective

- Minh bạch hóa nguồn thông tin y khoa mà AI Agent sử dụng để trả lời câu hỏi của người dùng, giúp tăng độ tin cậy.
- Hiển thị trạng thái suy luận của Agent trong quá trình xử lý để người dùng hiểu được các bước Agent đang thực hiện (Tìm kiếm, Phân tích, Tổng hợp).

---

## 3. Trace Requirement

| Req ID | Title |
| :--- | :--- |
| **US-36** | Cung cấp nguồn tài liệu của câu trả lời |
| **US-Thinking-01** | Hiện thị quá trình suy luận của Agent |

---

## 4. Mô tả chi tiết tính năng: Cung cấp nguồn tài liệu của câu trả lời (US-36)

### 4.1. Mô tả nghiệp vụ (User Flow)

1. Người dùng đặt câu hỏi cho AI Health.
2. Hệ thống AI Agent kiểm tra điều kiện cần hiển thị nguồn (Dựa trên cấu hình Enable/Disable trên Console).
3. AI Agent truy vấn dữ liệu từ **Internal KB** (Cơ sở dữ liệu y khoa nội bộ) và/hoặc **Internet Search**.
4. **Phía Agent:** Trả về nội dung câu trả lời (message content) có gắn index trích dẫn ở dạng `[1]`, `[2]`,... kèm theo danh sách `citations[]` tương ứng trong metadata.
5. **Phía Frontend (Super App):** Map các index `[n]` trong văn bản với danh sách `citations[]` nhận được và hiển thị khối thông tin nguồn ở cuối câu trả lời.

### 4.2. Trách nhiệm hệ thống

| Hệ thống | Trách nhiệm |
| :--- | :--- |
| **AI Agent** | - Thực hiện RAG (Retrieval-Augmented Generation) từ KB và Internet.<br>- Gắn index trích dẫn vào text trả về.<br>- Cung cấp metadata chi tiết cho từng citation. |
| **Frontend (Super App)** | - Nhận data stream từ Agent.<br>- Hiển thị text theo thời gian thực.<br>- Render danh sách nguồn (Source List) dưới dạng các thẻ click được để mở URL hoặc xem chi tiết. |

### 4.3. Bảng Data Dictionary (Metadata Citations)

#### Trường hợp Nguồn Nội bộ (Internal KB)
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Yes | Mapping index (vị trí [n] trong text). |
| `title` | String | Yes | Tiêu đề: "Tài liệu y khoa chính thức". |
| `source` | String | Yes | Fixed value: `internal`. |

#### Trường hợp Nguồn Internet (External)
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Yes | Mapping index (vị trí [n] trong text). |
| `title` | String | Yes | Tiêu đề bài viết từ trang web. |
| `sourceName` | String | Yes | Tên website/domain (e.g., vnexpress.net). |
| `url` | String | Yes | Đường dẫn URL để truy cập nguồn. |
| `favicon_image`| String | No | Link icon của website (nếu có). |
| `source` | String | Yes | Fixed value: `external`. |

### 4.4. Cơ chế Streaming Citation (KB + Internet)

Trong quá trình stream, Agent trả về các tag số thứ tự đơn giản:
> "Theo nghiên cứu, triệu chứng này có thể do virus [1]. Bạn nên nghỉ ngơi và uống nhiều nước [2]."

**Mẫu dữ liệu trả về cho Internet Search:**
```json
{
  "title": "Bảng giá xe ô tô điện VinFast mới nhất 2026",
  "url": "https://vinfastotominhdao.vn/bang-gia-xe-o-to-dien-vinfast/",
  "source": "external"
}
```

---

## 5. Mô tả chi tiết tính năng: Trạng thái suy luận của Agent (US-Thinking-01)

### 5.1. Kịch bản trạng thái (Reasoning States)

| Trạng thái | Nội dung hiển thị trên UI | Mô tả hành động |
| :--- | :--- | :--- |
| **Searching KB** | "Đang tìm kiếm trong cơ sở dữ liệu y khoa..." | Agent đang truy vấn dữ liệu từ bộ não nội bộ. |
| **Searching Internet**| "Đang tìm kiếm thông tin trên Internet..." | Agent đang sử dụng công cụ tìm kiếm bên ngoài. |
| **Analyzing** | "Đang tổng hợp và phân tích thông tin..." | Agent đang xử lý các dữ liệu thô thu thập được. |
| **Thinking** | "Đang chuẩn bị câu trả lời..." | Agent đang bắt đầu quá trình sinh văn bản. |

### 5.2. Quy trình hiển thị

1. Khi bắt đầu quá trình suy luận, Agent gửi message có `type: "thinking"` hoặc `type: "searching"`.
2. Frontend hiển thị icon loading kèm text trạng thái tương ứng.
3. Các trạng thái có thể thay đổi liên tục (Searching -> Analyzing -> Thinking).
4. Khi gói tin đầu tiên của câu trả lời thực sự (`type: "message"`) được gửi về, trạng thái suy luận sẽ tự động ẩn đi và thay thế bằng text stream.

### 5.3. Mapping Metadata cho Trạng thái Thinking

Khi Agent thực hiện internet search, object `thinking` sẽ chứa danh sách các website đang được tham khảo:
```json
{
  "type": "thinking",
  "value": {
    "content": "Đang tìm kiếm liệu trên internet từ",
    "websites": [
      {
        "site_name": "vnexpress.net",
        "title": "Bảng giá xe ôtô điện VinFast 2025...",
        "url": "https://vnexpress.net/oto-xe-may/..."
      }
    ]
  }
}
```
