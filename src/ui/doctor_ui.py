import datetime
from ui.menu_utils import print_header, print_divider, get_input
from entities.medical_record import MedicalRecord

def doctor_menu(managers, current_user):
    doctor_manager = managers["doctor"]
    appointment_manager = managers["appointment"]
    medical_record_manager = managers["record"]
    schedule_manager = managers["schedule"]
    
    doctor_id = getattr(current_user, 'linked_id', '')

    while True:
        print_header("MENU BAC SI PHONG KHAM")
        print("1. Xem thong tin ca nhan")
        print("2. Xem lich lam viec hom nay")
        print("3. Xem toan bo lich kham")
        print("4. Danh sach benh nhan hom nay")
        print("5. Kham benh")
        print("6. Tra cuu benh an")
        print("7. Xem doanh thu")
        print("0. Dang xuat")
        print("0. Dang xuat")
        print_divider()
        
        choice = get_input("Nhap lua chon: ")
        
        try:
            if choice == "1":
                print_header("THONG TIN CA NHAN BAC SI")
                d = doctor_manager.find_doctor_by_id(doctor_id)
                if d:
                    email = doctor_manager.get_doctor_email(doctor_id)
                    print(f"ID: {d.id} | Ho ten: {d.name} | Chuyen khoa: {d.specialty}")
                    print(f"Gioi tinh: {d.gender} | SDT: {d.phone} | Email: {email} | Gia: {d.base_price}")
                else:
                    print("Khong tim thay thong tin bac si tren he thong.")

            elif choice == "2":
                today_str = str(datetime.date.today())
                print_header(f"LICH LAM VIEC HOM NAY ({today_str})")
                if hasattr(doctor_manager, "get_daily_schedule"):
                    results = doctor_manager.get_daily_schedule(doctor_id, today_str)
                    current = results.head
                    if not current: print("Hom nay ban khong co ca truc.")
                    while current:
                        s = current.value
                        print(f"Schedule ID: {s.schedule_id} | Khung gio: {s.time_slot} | Dat cho: {s.is_booked} | Trang thai: {s.status} | Patient ID: {s.patient_id}")
                        current = current.next
                else:
                    current = schedule_manager.schedules.head
                    found = False
                    while current:
                        s = current.value
                        if s.doctor_id == doctor_id and str(s.date) == today_str:
                            print(f"Schedule ID: {s.id} | Khung gio: {s.time_slot} | Trang thai dat: {s.is_booked}")
                            found = True
                        current = current.next
                    if not found: print("Hom nay ban khong co ca truc nao.")

            elif choice == "3":
                print_header("TOAN BO LICH KHAM")
                current = schedule_manager.schedules.head
                found = False
                while current:
                    s = current.value
                    if s.doctor_id == doctor_id:
                        print(f"ID: {s.id} | Ngay: {s.date} | Gio: {s.time_slot} | Dat cho: {s.is_booked}")
                        found = True
                    current = current.next
                if not found: print("Ban chua co bat ky lich kham nao.")

            elif choice == "4":
                today_str = str(datetime.date.today())
                print_header(f"BENH NHAN HEN LICH HOM NAY ({today_str})")
                current = appointment_manager.appointments.head
                found = False
                while current:
                    apt = current.value
                    sched = schedule_manager.find_schedule_by_id(apt.schedule_id)
                    if sched and sched.doctor_id == doctor_id and str(sched.date) == today_str:
                        print(f"Appointment ID: {apt.id} | Patient ID: {apt.patient_id} | Gio: {sched.time_slot} | Trang thai: {apt.status}")
                        found = True
                    current = current.next
                if not found: print("Khong co benh nhan nao dat lich cho ban hom nay.")

            elif choice == "5":

                print_header("KHAM BENH")

                apt_id = get_input("Nhap Appointment ID: ")

                apt = appointment_manager.find_appointment_by_id(apt_id)

                if not apt:
                    print("Khong tim thay cuoc hen.")
                    continue

                sch = schedule_manager.find_schedule_by_id(
                    apt.schedule_id
                )

                if not sch:
                    print("Khong tim thay lich kham.")
                    continue

                if sch.doctor_id != doctor_id:
                    print("Ban khong co quyen xu ly cuoc hen nay.")
                    continue

                symptoms = get_input("Trieu chung: ")
                diagnosis = get_input("Chan doan: ")
                prescription = get_input("Don thuoc: ")

                record = medical_record_manager.find_by_appointment_id(
                    apt_id
                )

                if record:

                    record.symptoms = symptoms
                    record.diagnosis = diagnosis
                    record.prescription = prescription

                    medical_record_manager._save_to_file()

                paid = get_input(
                    "Benh nhan da thanh toan? (Y/N): "
                ).upper()

                if paid == "Y":
                    apt.payment_status = "PAID"
                else:
                    apt.payment_status = "UNPAID"

                apt.status = "COMPLETED"

                appointment_manager._save_to_file()

                print("Kham benh va hoan tat thanh cong.")
            
            elif choice == "6":
                print_header("TRA CUU BENH AN")
                patient_id = get_input("Nhap Patient ID can tim: ")
                results = medical_record_manager.find_medical_records_by_patient_id(patient_id)
                current = results.head
                if not current: print("Benh nhan nay chua co lich su benh an.")
                while current:
                    mr = current.value
                    print(f"Record ID: {mr.id} | Trieu chung: {mr.symptoms} | Chuan doan: {mr.diagnosis} | Ke don: {mr.prescription}")
                    current = current.next

            elif choice == "7":
                print_header("XEM DOANH THU CA NHAN")
                ranked = doctor_manager.rank_doctors_by_revenue()
                current = ranked.head
                found = False
                while current:
                    dr_rev = current.value
                    if dr_rev.doctor.id == doctor_id:
                        print(f"Tong doanh thu hien tai cua ban: {dr_rev.revenue:,} VND")
                        found = True
                        break
                    current = current.next
                if not found: print("Doanh thu hien tai: 0 VND")

            elif choice == "0":
                print("Dang xuat quyen Bac si.")
                break
            else:
                print("Lua chon khong hop le.")
        except Exception as e:
            print(f"Loi he thong: {str(e)}")
