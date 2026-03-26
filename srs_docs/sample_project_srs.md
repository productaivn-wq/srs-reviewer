# Software Requirements Specification (SRS)
## Hệ thống Quản lý Thư viện Trực tuyến — LibraryX

**Phiên bản**: 1.0  
**Ngày**: 2025-01-15  
**Tác giả**: Nguyễn Văn An, Trần Thị Bình  

---

# 1. Introduction

## 1.1 Purpose
Tài liệu này mô tả đặc tả yêu cầu phần mềm (SRS) cho Hệ thống Quản lý Thư viện Trực tuyến LibraryX. Hệ thống cho phép người dùng tìm kiếm, mượn, trả sách và quản lý tài khoản thông qua giao diện web.

## 1.2 Scope
LibraryX phục vụ 3 nhóm người dùng chính: Độc giả, Thủ thư, và Quản trị viên. Hệ thống hỗ trợ quản lý kho sách lên đến 100.000 đầu sách với khả năng phục vụ 5.000 người dùng đồng thời.

## 1.3 Definitions and Abbreviations
| Thuật ngữ | Định nghĩa |
|---|---|
| SRS | Software Requirements Specification |
| API | Application Programming Interface |
| ISBN | International Standard Book Number |
| OPAC | Online Public Access Catalog |

## 1.4 References
- IEEE 830-1998: Recommended Practice for SRS
- ISO/IEC 29148:2018: Systems and software engineering

---

# 2. Overall Description

## 2.1 Product Perspective
LibraryX là hệ thống web-based, kế thừa và thay thế hệ thống quản lý thư viện legacy hiện tại. Hệ thống tích hợp với:
- Cổng thanh toán VNPay cho phí phạt trả muộn
- Hệ thống email SMTP cho thông báo
- Google OAuth 2.0 cho đăng nhập

## 2.2 Product Functions
- **Quản lý sách**: CRUD đầu sách, quản lý kho, theo dõi vị trí
- **Mượn/Trả**: Đặt trước, mượn, gia hạn, trả sách
- **Tìm kiếm**: Full-text search, lọc theo thể loại/tác giả/ISBN
- **Quản lý người dùng**: Đăng ký, danh sách đen, lịch sử mượn
- **Báo cáo**: Thống kê mượn trả, sách phổ biến, doanh thu phí phạt

## 2.3 User Characteristics
| Nhóm | Đặc điểm | Kỹ năng IT |
|---|---|---|
| Độc giả | Sinh viên, giảng viên, 18-60 tuổi | Cơ bản |
| Thủ thư | Nhân viên thư viện | Trung bình |
| Quản trị viên | IT staff | Cao |

## 2.4 Constraints
- Ngân sách phát triển: 500 triệu VND
- Timeline: 6 tháng
- Phải tương thích với hệ thống quản lý sinh viên hiện tại
- Tuân thủ PDPA về bảo mật thông tin cá nhân

## 2.5 Assumptions and Dependencies
- Internet ổn định tại thư viện (>= 100 Mbps)
- Server hosting tại data center trường đại học
- Hệ thống email trường đại học hoạt động ổn định

---

# 3. Specific Requirements

## 3.1 Functional Requirements

### FR-001: Đăng ký tài khoản
- Hệ thống cho phép người dùng đăng ký bằng email hoặc Google OAuth
- Yêu cầu xác thực email trước khi kích hoạt tài khoản
- Thời gian xử lý đăng ký: < 3 giây

### FR-002: Tìm kiếm sách
- Hỗ trợ tìm kiếm theo tiêu đề, tác giả, ISBN, thể loại
- Kết quả trả về trong < 500ms cho 95% truy vấn
- Hỗ trợ gợi ý tìm kiếm (autocomplete)

### FR-003: Mượn sách
- Giới hạn mượn: tối đa 5 cuốn/lần, 14 ngày/cuốn
- Phát thông báo email 3 ngày trước hạn trả
- Tự động tính phí phạt: 5.000 VND/ngày trễ

### FR-004: Trả sách
- Hỗ trợ trả sách tại quầy (scan barcode) và online (drop box)
- Cập nhật trạng thái kho tức thì
- Gửi biên nhận trả sách qua email

### FR-005: Quản lý kho sách
- Thêm/sửa/xóa đầu sách với thông tin ISBN, vị trí kệ, số bản sao
- Import hàng loạt từ file CSV/Excel
- Cảnh báo khi số bản sao xuống dưới ngưỡng tối thiểu

### FR-006: Báo cáo thống kê
- Dashboard thời gian thực hiển thị: số lượt mượn, sách phổ biến, tỷ lệ trả đúng hạn
- Xuất báo cáo PDF/Excel theo khoảng thời gian

## 3.2 Non-Functional Requirements

### NFR-001: Performance
- Thời gian phản hồi API: P95 < 500ms
- Thông lượng: >= 200 requests/second
- Thời gian khởi động hệ thống: < 30 giây

### NFR-002: Availability
- Uptime SLA: 99.5%
- Planned maintenance window: Chủ nhật 2:00-4:00 AM
- Recovery Time Objective (RTO): < 4 giờ

### NFR-003: Security
- Mã hóa dữ liệu: TLS 1.3 cho truyền tải, AES-256 cho lưu trữ
- Authentication: OAuth 2.0 + JWT (access token TTL: 15 phút)
- Authorization: RBAC (3 roles: reader, librarian, admin)
- Rate limiting: 100 requests/phút/user

### NFR-004: Scalability
- Hỗ trợ horizontal scaling qua container orchestration
- Database sharding khi vượt 1 triệu records

### NFR-005: Usability
- WCAG 2.1 AA compliance
- Responsive design: desktop, tablet, mobile
- Hỗ trợ đa ngôn ngữ: Tiếng Việt (mặc định), English

---

# 4. System Architecture & Interfaces

## 4.1 System Architecture
- **Frontend**: React 18 + TypeScript, deployed on Cloudflare Pages
- **Backend API**: Node.js + Express, containerized with Docker
- **Database**: PostgreSQL 16 (primary), Redis (cache)
- **Search**: Elasticsearch 8 for full-text search
- **Message Queue**: RabbitMQ for async tasks

## 4.2 External Interfaces
| Interface | Protocol | Purpose |
|---|---|---|
| VNPay Gateway | REST API | Xử lý thanh toán phí phạt |
| Google OAuth | OAuth 2.0 | Đăng nhập xã hội |
| SMTP Server | SMTP/TLS | Gửi email thông báo |
| Student System | REST API | Đồng bộ thông tin sinh viên |

## 4.3 Hardware Interfaces
- Barcode scanner (USB HID) tại quầy thủ thư
- Receipt printer (ESC/POS) cho biên nhận

---

# 5. Data Requirements

## 5.1 Data Model
- **Books**: id, isbn, title, author, publisher, year, category, shelf_location, copies_total, copies_available
- **Users**: id, email, name, role, status, created_at
- **Loans**: id, user_id, book_id, borrow_date, due_date, return_date, status, fine_amount
- **Reservations**: id, user_id, book_id, reserved_at, expires_at, status

## 5.2 Data Retention
- Lịch sử mượn trả: lưu trữ vĩnh viễn
- Logs: giữ 90 ngày, sau đó archive sang cold storage
- Dữ liệu cá nhân: xóa sau 3 năm nếu tài khoản bị hủy (theo PDPA)

---

# 6. Use Cases & Scenarios

## UC-001: Mượn sách
**Actor**: Độc giả  
**Precondition**: Tài khoản đã kích hoạt, không bị khóa, chưa đạt giới hạn mượn  
**Main Flow**:
1. Độc giả tìm kiếm và chọn sách
2. Hệ thống kiểm tra số bản sao khả dụng
3. Độc giả xác nhận mượn
4. Hệ thống tạo phiếu mượn, cập nhật kho, gửi email xác nhận
**Alternative Flow**:
- 2a. Không còn bản sao → Chuyển sang luồng Đặt trước
**Exception Flow**:
- 3a. Tài khoản bị khóa → Hiển thị thông báo lỗi, redirect liên hệ thủ thư

## UC-002: Trả sách
**Actor**: Thủ thư  
**Precondition**: Sách đã được mượn  
**Main Flow**:
1. Thủ thư scan barcode sách
2. Hệ thống tra cứu phiếu mượn
3. Hệ thống tính phí phạt (nếu trả muộn)
4. Thủ thư xác nhận trả
5. Hệ thống cập nhật kho, gửi biên nhận qua email

---

# 7. Acceptance Criteria & Testing

## 7.1 Acceptance Criteria
- AC-001: Tìm kiếm trả kết quả trong < 500ms cho 95% truy vấn
- AC-002: Mượn sách hoàn tất trong < 3 click
- AC-003: Phí phạt tính chính xác đến VND
- AC-004: Email thông báo gửi trong < 5 phút sau sự kiện

## 7.2 Testing Strategy
| Loại test | Phạm vi | Công cụ |
|---|---|---|
| Unit Test | Core business logic | Jest, pytest |
| Integration | API endpoints | Supertest |
| E2E | User flows | Playwright |
| Performance | Load testing | k6 |
| Security | OWASP Top 10 | OWASP ZAP |

---

# 8. Traceability Matrix

| Requirement | Use Case | Test Case | Priority |
|---|---|---|---|
| FR-001 | — | TC-001 | P0 |
| FR-002 | UC-001 | TC-002 | P0 |
| FR-003 | UC-001 | TC-003 | P0 |
| FR-004 | UC-002 | TC-004 | P0 |
| FR-005 | — | TC-005 | P1 |
| FR-006 | — | TC-006 | P2 |
| NFR-001 | — | TC-PERF-001 | P0 |
| NFR-002 | — | TC-AVAIL-001 | P1 |
| NFR-003 | — | TC-SEC-001 | P0 |

---

# 9. Appendices

## 9.1 Glossary
Xem mục 1.3.

## 9.2 Change Log
| Version | Date | Author | Description |
|---|---|---|---|
| 1.0 | 2025-01-15 | Nguyễn Văn An | Initial draft |
