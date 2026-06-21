# HỆ THỐNG QUẢN LÝ LỊCH KHÁM BỆNH VIỆN

## Mô tả dự án

Đây là chương trình mô phỏng hệ thống quản lý lịch khám bệnh được xây dựng bằng Python theo mô hình hướng đối tượng (OOP). Hệ thống hỗ trợ ba vai trò người dùng gồm **Admin**, **Doctor** và **Patient**, cho phép quản lý tài khoản, lịch khám, cuộc hẹn và hồ sơ bệnh án.

Mục tiêu của đề tài là vận dụng các kiến thức về:

* Lập trình hướng đối tượng.
* Cấu trúc dữ liệu và giải thuật.
* Tổ chức mã nguồn theo kiến trúc nhiều tầng.
* Quản lý dữ liệu bằng tệp văn bản.

---

# Mô tả mã nguồn

## Điểm bắt đầu chương trình

Toàn bộ chương trình được khởi động từ:

```text
app.py
```

Hàm `main()` thực hiện:

1. Khởi tạo các Manager.
2. Liên kết các Manager với nhau (Dependency Injection).
3. Nạp dữ liệu từ các tệp lưu trữ.
4. Chuyển điều khiển đến giao diện chính.

Luồng tổng quát:

```text
app.py
│
├── Khởi tạo Managers
├── Load dữ liệu
├── Main Menu
│
├── Admin UI
├── Doctor UI
└── Patient UI
```

---

# Kiến trúc mã nguồn

```text
Hospital-Appointment-System/
│
├── app.py
│
├── data/
│
└── src/
    ├── structures/
    ├── entities/
    ├── managers/
    └── ui/
```

Hệ thống được chia thành 4 tầng độc lập.

---

## 1. structures/

Cài đặt các cấu trúc dữ liệu nền tảng.

```text
structures/
├── node.py
├── linked_list.py
└── hash_table.py
```

### linked_list.py

Tự xây dựng danh sách liên kết đơn dùng để:

* Lưu danh sách bác sĩ.
* Lưu lịch khám.
* Lưu cuộc hẹn.
* Lưu bệnh án.

Các thao tác chính:

* append()
* remove()
* find()
* iteration()

### hash_table.py

Tự cài đặt Hash Table theo phương pháp Separate Chaining.

Được sử dụng cho:

* Tra cứu bệnh nhân theo số điện thoại.
* Tra cứu tài khoản người dùng.
* Theo dõi trạng thái đăng nhập.
* Theo dõi số lần đăng nhập sai.

Mục tiêu là giảm thời gian tìm kiếm từ O(n) xuống trung bình O(1).

---

## 2. entities/

Định nghĩa các đối tượng dữ liệu nghiệp vụ.

```text
entities/
├── user.py
├── doctor.py
├── patient.py
├── appointment.py
├── doctor_schedule.py
└── medical_record.py
```

Mỗi lớp chỉ chịu trách nhiệm lưu trữ dữ liệu và biểu diễn một thực thể trong hệ thống.

Ví dụ:

### User

Lưu thông tin đăng nhập:

```text
user_id
phone
email
password
role
linked_id
```

### Doctor

Lưu thông tin bác sĩ:

```text
id
name
specialty
base_price
phone
```

### Appointment

Biểu diễn một cuộc hẹn khám giữa bệnh nhân và bác sĩ.

---

## 3. managers/

Đây là tầng xử lý nghiệp vụ chính của hệ thống.

```text
managers/
├── base_manager.py
├── file_handler.py
├── user_manager.py
├── doctor_manager.py
├── patient_manager.py
├── appointment_manager.py
├── schedule_manager.py
└── hospital_manager.py
```

### BaseManager

Lớp cơ sở dùng chung cho các Manager.

Cung cấp:

* Nạp dữ liệu.
* Lưu dữ liệu.
* Các thao tác quản lý cơ bản.

### UserManager

Xử lý:

* Đăng ký tài khoản.
* Đăng nhập.
* Đổi mật khẩu.
* Khóa tài khoản sau 5 lần đăng nhập sai.

### DoctorManager

Xử lý:

* Quản lý bác sĩ.
* Tìm kiếm bác sĩ.
* Thống kê doanh thu.

### PatientManager

Xử lý:

* Hồ sơ bệnh nhân.
* Thông tin BHYT.

### ScheduleManager

Xử lý:

* Tạo lịch khám.
* Chỉnh sửa lịch khám.
* Kiểm tra lịch còn trống.

### AppointmentManager

Xử lý nghiệp vụ quan trọng nhất:

* Đặt lịch khám.
* Hủy lịch khám.
* Kiểm tra trùng lịch.
* Đồng bộ trạng thái lịch khám.

---

## 4. ui/

Tầng giao diện Console.

```text
ui/
├── main_menu.py
├── admin_ui.py
├── doctor_ui.py
├── patient_ui.py
└── menu_utils.py
```

Tầng này chỉ:

* Nhận dữ liệu từ người dùng.
* Hiển thị kết quả.
* Gọi các hàm nghiệp vụ trong Manager.

Không chứa logic xử lý dữ liệu.

---

# Dữ liệu lưu trữ

Dữ liệu được lưu dưới dạng văn bản trong thư mục:

```text
data/
```

Gồm:

```text
user_credentials.txt
doctors.txt
patients.txt
schedules.txt
appointments.txt
records.txt
```

Khi khởi động:

```text
File -> Entity -> Manager
```

Khi cập nhật dữ liệu:

```text
Manager -> File
```

Mọi thay đổi đều được ghi xuống tệp ngay sau khi thao tác thành công nhằm hạn chế mất dữ liệu khi chương trình dừng đột ngột.

---

# Các nghiệp vụ chính cần xem trong mã nguồn

Nếu muốn đánh giá nhanh chương trình, có thể xem các chức năng sau:

### Đăng nhập và phân quyền

```text
UserManager.authenticate()
```

* Đăng nhập bằng email hoặc số điện thoại.
* Theo dõi số lần nhập sai.
* Khóa tài khoản sau 5 lần thất bại.

### Đặt lịch khám

```text
AppointmentManager.book_appointment()
```

* Kiểm tra lịch tồn tại.
* Kiểm tra lịch đã được đặt hay chưa.
* Tạo cuộc hẹn.
* Cập nhật trạng thái lịch.

### Quản lý hồ sơ bệnh án

```text
MedicalRecordManager.add_record()
```

* Kiểm tra quyền của bác sĩ.
* Kiểm tra cuộc hẹn đã hoàn thành.
* Ngăn tạo trùng hồ sơ bệnh án.

### Tìm kiếm bệnh nhân

```text
PatientManager.find_by_phone()
```

Sử dụng Hash Table để tối ưu tốc độ tra cứu.

---

# Yêu cầu chạy chương trình

```bash
python app.py
```

Yêu cầu:

* Python 3.x
* Không sử dụng thư viện ngoài chuẩn Python

---

# Ghi chú

Trong dự án này nhóm tập trung vào việc xây dựng cấu trúc dữ liệu, thiết kế hướng đối tượng và mô hình xử lý nghiệp vụ trên môi trường Console. Hệ thống được tổ chức theo hướng dễ mở rộng để có thể phát triển thành ứng dụng GUI hoặc Web trong tương lai.
