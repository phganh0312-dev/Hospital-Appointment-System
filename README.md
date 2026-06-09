# 🏥 Hospital Appointment Management System

Hệ thống Quản lý Lịch khám Bệnh viện được xây dựng bằng **Python OOP** nhằm hỗ trợ quản lý bác sĩ, bệnh nhân, lịch khám và bệnh án. Dự án được phát triển theo kiến trúc phân tầng (Layered Architecture), sử dụng cấu trúc dữ liệu tự cài đặt và lưu trữ dữ liệu bằng tệp văn bản.

---

## 📌 Mục tiêu

* Quản lý thông tin bác sĩ theo chuyên khoa.
* Quản lý hồ sơ bệnh nhân.
* Đăng ký và quản lý lịch khám.
* Kiểm tra trùng lịch hẹn.
* Quản lý bệnh án sau khám.
* Thống kê và báo cáo dữ liệu.

---

## ✨ Chức năng chính

### 👨‍⚕️ Quản lý bác sĩ

* Thêm, sửa, xóa thông tin bác sĩ.
* Quản lý chuyên khoa.
* Quản lý lịch làm việc và khung giờ khám.

### 👤 Quản lý bệnh nhân

* Lưu trữ thông tin cá nhân.
* Quản lý hồ sơ khám bệnh.

### 📅 Quản lý lịch khám

* Đặt lịch theo chuyên khoa.
* Chọn bác sĩ.
* Chọn khung giờ phù hợp.
* Kiểm tra và xử lý trùng lịch.
* Hủy hoặc cập nhật lịch khám.

### 📋 Quản lý bệnh án

* Ghi nhận triệu chứng.
* Kết luận chẩn đoán.
* Lưu đơn thuốc sau mỗi lần khám.

### 📊 Báo cáo thống kê

* Số cuộc hẹn trong ngày.
* Bác sĩ được đăng ký nhiều nhất.
* Số lần khám.
* Doanh thu khám bệnh.

---

## 🏗️ Kiến trúc hệ thống

```text
Presentation Layer (UI)
        │
        ▼
Manager / Controller Layer
        │
        ▼
Entities Layer
        │
        ▼
Data Storage (.txt)
```

---

## 📂 Cấu trúc thư mục

```text
hospital-appointment-system/
│
├── src/
│   ├── entities/
│   ├── managers/
│   ├── structures/
│   ├── ui/
│   └── app.py
│
├── data/
│   ├── doctors.txt
│   ├── patients.txt
│   ├── schedules.txt
│   ├── appointments.txt
│   └── records.txt
│
├── docs/
├── README.md
└── .gitignore
```

---

## 💻 Công nghệ sử dụng

* Python 3
* Object-Oriented Programming (OOP)
* Linked List tự cài đặt
* File Text (.txt)
* Git & GitHub

---

## 🚀 Cách chạy chương trình

Clone repository:

```bash
git clone <repository-url>
```

Di chuyển vào thư mục dự án:

```bash
cd hospital-appointment-system
```

Chạy chương trình:

```bash
python src/app.py
```

---

## 👥 Thành viên

| Thành viên | Vai trò                                                                   |
| ---------- | ------------------------------------------------------------------------- |
| TV1        | Core Logic, LinkedList, Doctor, DoctorSchedule, HospitalManager, Thống kê |
| TV2        | Appointment, FileHandler, Đọc/Ghi dữ liệu, Kiểm tra trùng lịch            |
| TV3        | Patient, MedicalRecord, Giao diện người dùng, Kiểm thử                    |

---

## 📄 Báo cáo

Dự án được thực hiện cho học phần **Kỹ thuật lập trình**, áp dụng các nguyên tắc:

* Object-Oriented Programming (OOP)
* Layered Architecture
* Custom Data Structure
* File-based Data Management

---

## 📜 License

Dự án được phát triển phục vụ mục đích học tập và nghiên cứu.
