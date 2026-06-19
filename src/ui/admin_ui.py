from ui.menu_utils import print_header, print_divider, get_input, get_int, get_float
from entities.doctor import Doctor
from entities.user import User
from entities.doctor_schedule import Schedule
from structures.hash_table import HashTable
from managers.base_manager import ValidationError, DataConsistencyError

def admin_menu(managers, current_user):
    user_manager = managers["user"]
    patient_manager = managers["patient"]
    doctor_manager = managers["doctor"]
    schedule_manager = managers["schedule"]
    appointment_manager = managers["appointment"]
    medical_record_manager = managers["record"]

    while True:
        print_header("MENU QUAN TRI VIEN (ADMIN)")
        print("1. Quan ly nguoi dung (Tim kiem user)")
        print("2. Danh sach benh nhan")
        print("3. Them bac si")
        print("4. Tim kiem bac si")
        print("5. Xoa bac si")
        print("6. Tao lich kham")
        print("7. Sua lich kham")
        print("8. Xoa lich kham")
        print("9. Xem lich theo bac si")
        print("10. Thong ke doanh thu bac si")
        print("11. Danh sach cuoc hen")
        print("12. Danh sach benh an")
        print("0. Dang xuat")
        print_divider()
        
        choice = get_input("Nhap lua chon cua ban: ")
        
        try:
            if choice == "1":
                print_header("TIM KIEM NGUOI DUNG")
                keyword = get_input("Nhap tu khoa (Ten/CCCD/Email/SDT): ")
                if hasattr(user_manager, "admin_search_users"):
                    results = user_manager.admin_search_users(keyword)
                else:
                    results = user_manager.search_users(keyword)
                
                current = results.head
                if not current:
                    print("Khong tim thay nguoi dung.")
                while current:
                    u = current.value
                    print(f"User ID: {u.user_id} | Email: {u.email} | SDT: {u.phone} | Role: {u.role} | Linked ID: {u.linked_id}")
                    current = current.next

            elif choice == "2":
                print_header("DANH SACH TOAN BO BENH NHAN")
                patients_list = patient_manager.patients.values()
                current = patients_list.head
                if not current:
                    print("He thong chua co benh nhan.")
                while current:
                    p = current.value
                    print(f"ID: {p.id} | Ho ten: {p.full_name} | CCCD: {p.cccd} | SDT: {p.phone} | Email: {p.email}")
                    current = current.next

            elif choice == "3":
                print_header("THEM BAC SI MOI")
                doc_id = get_input("Nhap ID bac si: ")
                name = get_input("Nhap ho ten: ")
                gender = get_input("Nhap gioi tinh: ")
                specialty = get_input("Nhap chuyen khoa: ")
                phone = get_input("Nhap so dien thoai: ")
                email = get_input("Nhap email: ")
                password = get_input("Nhap mat khau dang nhap cho bac si: ")
                base_price = get_float("Nhap gia kham co ban: ")
                
                new_doc = Doctor(doc_id, name, gender, specialty, base_price, phone)
                doctor_manager.add_doctor(new_doc)
                user_id = user_manager._generate_user_id()
                user_manager.add_user(User(user_id, phone, email, password, "doctor", doc_id))
                user_manager._save_data_to_file()
                print("Da them bac si moi thanh cong.")

            elif choice == "4":
                print_header("TIM KIEM BAC SI")
                keyword = get_input("Nhap tu khoa can tim: ")
                results = doctor_manager.search_doctors(keyword)
                current = results.head
                if not current:
                    print("Khong tim thay bac si phu hop.")
                while current:
                    d = current.value
                    email = doctor_manager.get_doctor_email(d.id)
                    print(f"ID: {d.id} | Ten: {d.name} | Chuyen khoa: {d.specialty} | SDT: {d.phone} | Email: {email} | Gia: {d.base_price}")
                    current = current.next

            elif choice == "5":
                print_header("XOA BAC SI")
                doc_id = get_input("Nhap ID bac si can xoa: ")
                try:
                    doctor_manager.remove_doctor(doc_id)
                    print("Da xoa bac si va dong bo du lieu thanh cong.")
                except (ValidationError, DataConsistencyError) as e:
                    print(f"Loi dong bo du lieu: {str(e)}")

            elif choice == "6":
                print_header("TAO LICH KHAM")
                sch_id = get_input("Nhap ID lich kham: ")
                doc_id = get_input("Nhap ID bac si: ")
                if not doctor_manager.find_doctor_by_id(doc_id):
                    print("Khong tim thay bac si, khong the tao lich.")
                    continue
                date = get_input("Nhap ngay (DD/MM/YYYY): ")
                time_slot = get_input("Nhap khung gio (vi du: 08:00-09:00): ")
                
                # SỬA LỖI: Sử dụng get_int() thay vì get_input() để khớp kiểu dữ liệu int ở backend
                day_of_week = get_int("Nhap thu trong tuan (2-8): ")
                slot_num = get_int("Nhap so thu tu ca kham (1-4): ")
                
                new_sch = Schedule(sch_id, doc_id, date, time_slot, False, day_of_week, slot_num)
                schedule_manager.add_schedule(new_sch)
                print("Tao lich kham moi cho bac si thanh cong!")

            elif choice == "7":
                print_header("SUA LICH KHAM")
                schedule_id = get_input("Nhap Schedule ID can sua: ")
                updates = HashTable()
                new_date = get_input("Nhap ngay moi (De trong de bo qua): ")
                if new_date: updates.set("date", new_date)
                new_slot = get_input("Nhap ca moi (De trong de bo qua): ")
                if new_slot: updates.set("time_slot", new_slot)
                
                schedule_manager.update_schedule(schedule_id, updates)
                print("Cap nhat lich kham thanh cong.")

            elif choice == "8":
                print_header("XOA LICH KHAM")
                schedule_id = get_input("Nhap Schedule ID can xoa: ")
                schedule_manager.remove_schedule_by_id(schedule_id)
                print("Da xoa lich kham.")

            elif choice == "9":
                print_header("XEM LICH THEO BAC SI")
                doctor_id = get_input("Nhap Doctor ID: ")
                results = schedule_manager.search_available_schedules(doctor_id)
                current = results.head
                if not current:
                    print("Khong co lich lam viec hop le.")
                while current:
                    s = current.value
                    print(f"Schedule ID: {s.id} | Ngay: {s.date} | Ca: {s.time_slot} | Da dat: {s.is_booked}")
                    current = current.next

            elif choice == "10":
                print_header("THONG KE DOANH THU BAC SI")
                ranked = doctor_manager.rank_doctors_by_revenue()
                current = ranked.head
                rank = 1
                if not current:
                    print("Chua co du lieu thong ke.")
                while current:
                    print(f"Hang {rank} | {str(current.value)}")
                    rank += 1
                    current = current.next

            elif choice == "11":
                print_header("DANH SACH CUOC HEN")
                current = appointment_manager.appointments.head
                if not current:
                    print("Chua co cuoc hen nao.")
                while current:
                    apt = current.value
                    print(f"ID: {apt.id} | Patient ID: {apt.patient_id} | Schedule ID: {apt.schedule_id} | Trang thai: {apt.status}")
                    current = current.next

            elif choice == "12":
                print_header("DANH SACH BENH AN")
                current = medical_record_manager.medical_records.head
                if not current:
                    print("Chua co ho so benh an nao.")
                while current:
                    mr = current.value
                    print(f"Record ID: {mr.id} | Appointment ID: {mr.appointment_id} | Trieu chung: {mr.symptoms} | Chuan doan: {mr.diagnosis}")
                    current = current.next

            elif choice == "0":
                print("Dang xuat khoi quyen Admin.")
                break
            else:
                print("Lua chon khong hop le.")
        except Exception as e:
            print(f"Loi xu ly chuc nang: {str(e)}")
