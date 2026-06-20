from ui.menu_utils import print_header, print_divider, get_input
from entities.appointment import Appointment
from structures.hash_table import HashTable
from managers.base_manager import ValidationError, DataConsistencyError, AppointmentStatus


def patient_menu(managers, current_user):
    user_manager = managers["user"]
    patient_manager = managers["patient"]
    appointment_manager = managers["appointment"]
    medical_record_manager = managers["record"]
    doctor_manager = managers["doctor"]

    patient_id = getattr(current_user, 'linked_id', '')

    while True:
        print_header("MENU BENH NHAN")
        print("1. Xem ho so ca nhan")
        print("2. Cap nhat ho so")
        print("3. Tim bac si dat lich")
        print("4. Xem lich kham con trong")
        print("5. Dat lich kham")
        print("6. Cap nhat BHYT")
        print("7. Huy lich kham")
        print("8. Xem lich su cuoc hen")
        print("9. Xem ho so benh an")
        print("10. Doi mat khau")
        print("0. Dang xuat")
        print_divider()

        choice = get_input("Nhap lua chon: ")

        try:
            if choice == "1":
                print_header("HO SO CA NHAN")
                p = patient_manager.find_patient_by_id(patient_id)
                if p:
                    print(f"ID: {p.id}")
                    print(f"Ho ten: {p.full_name}")
                    print(f"CCCD: {p.cccd}")
                    print(f"Email: {p.email}")
                    print(f"SDT: {p.phone}")
                    print(f"Dia chi: {p.province}, {p.ward}, {p.detailed_address}")
                    print(f"BHYT: {getattr(p, 'bhyt_code', '')} | Han dung: {getattr(p, 'bhyt_expiry', '')}")
                else:
                    print("Khong tim thay thong tin ca nhan hop le.")

            elif choice == "2":
                print_header("CAP NHAT HO SO")
                updates = HashTable()
                name = get_input("Nhap ten moi (Bo qua nhan Enter): ")
                if name:
                    updates.set("full_name", name)
                email = get_input("Nhap email moi (Bo qua nhan Enter): ")
                if email:
                    updates.set("email", email)
                phone = get_input("Nhap phone moi (Bo qua nhan Enter): ")
                if phone:
                    updates.set("phone", phone)
                addr = get_input("Nhap dia chi chi tiet moi (Bo qua nhan Enter): ")
                if addr:
                    updates.set("detailed_address", addr)
                bhyt = get_input("Nhap ma BHYT moi (Bo qua nhan Enter): ")
                if bhyt:
                    updates.set("bhyt_code", bhyt)

                patient_manager.update_patient(patient_id, updates)
                print("Da cap nhat ho so ca nhan thanh cong.")

            elif choice == "3":
                print_header("TIM KIEM BAC SI DAT LICH")
                print("1. Tim theo ten bac si")
                print("2. Tim theo chuyen khoa")
                sub_choice = get_input("Nhap lua chon cua ban (1-2): ")
                keyword = get_input("Nhap tu khoa can tim: ")

                if sub_choice == "1":
                    results = doctor_manager.search_doctors(keyword=keyword)
                else:
                    results = doctor_manager.search_doctors(specialty=keyword)

                print_divider()
                print(f"{'Ma BS':<8} | {'Ho ten bac si':<24} | {'Chuyen khoa':<18} | {'Gia kham':<10}")
                print_divider()

                current = results.head
                if not current:
                    print("Khong tim thay bac si nao phu hop voi yeu cau.")
                while current:
                    doc = current.value
                    print(f"{doc.id:<8} | {doc.name:<24} | {doc.specialty:<18} | {doc.base_price} VND")
                    current = current.next

            elif choice == "4":
                print_header("XEM LICH KHAM CON TRONG CUA BAC SI")
                doc_id = get_input("Nhap Ma bac si ban muon dat lich: ")
                schedules = appointment_manager.get_schedules_by_doctor_flow(doc_id)

                current = schedules.head
                if not current:
                    print("Bac si nay hien tai da het ca truc trong hoac nhap sai Ma BS.")
                while current:
                    sch = current.value
                    print(f"Ma lich: {sch.id} | Ngay: {sch.date} | Gio: {sch.time_slot}")
                    current = current.next

            elif choice == "5":
                print_header("DAT LICH KHAM")

                schedule_id = get_input("Nhap ma lich kham: ")

                schedule = appointment_manager.schedule_manager.find_schedule_by_id(schedule_id)

                if not schedule:
                    print("Khong tim thay lich kham.")
                    continue

                if getattr(schedule, "is_booked", False):
                    print("Lich nay da duoc dat.")
                    continue

                patient = patient_manager.find_patient_by_id(patient_id)

                has_bhyt = get_input("Ban co BHYT khong? (Y/N): ").upper()

                if has_bhyt == "Y":
                    bhyt_code = get_input("Nhap ma BHYT: ")
                    bhyt_expiry = get_input("Nhap han BHYT: ")

                    patient.bhyt_code = bhyt_code
                    patient.bhyt_expiry = bhyt_expiry
                    patient_manager._save_to_file()

                current = appointment_manager.appointments.head
                max_id = 0

                while current:
                    try:
                        num = int(current.value.id[1:])
                        if num > max_id:
                            max_id = num
                    except:
                        pass
                    current = current.next

                appointment_id = "A" + str(max_id + 1).zfill(8)

                new_apt = Appointment(
                    appointment_id,
                    patient_id,
                    schedule_id,
                    "PENDING"
                )

                appointment_manager.add_appointment(new_apt)

                print("--------------------------------")
                print("DAT LICH THANH CONG")
                print("Ma cuoc hen:", appointment_id)
                print("--------------------------------")

            
            elif choice == "6":

                print_header("CAP NHAT BHYT")

                patient = patient_manager.find_patient_by_id(patient_id)

                if not patient:
                    print("Khong tim thay benh nhan.")
                    continue

                bhyt_code = get_input("Nhap ma BHYT: ")
                bhyt_expiry = get_input("Nhap han BHYT: ")

                patient.bhyt_code = bhyt_code
                patient.bhyt_expiry = bhyt_expiry

                patient_manager._save_to_file()

                print("Cap nhat BHYT thanh cong.")
                
            elif choice == "7":
                print_header("HUY LICH KHAM")
                apt_id = get_input("Nhap ID cuoc hen muon huy: ")
                apt = appointment_manager.find_appointment_by_id(apt_id)

                if apt and getattr(apt, 'patient_id', '') == patient_id:
                    status_norm = AppointmentStatus.normalize(getattr(apt, 'status', ''))
                    if status_norm in (AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED):
                        appointment_manager.cancel_appointment(apt_id)
                        print("Da huy cuoc hen va giai phong slot ca truc thanh cong!")
                    else:
                        print(f"Cuoc hen dang o trang thai '{apt.status}', khong the huy.")
                else:
                    print("Ma cuoc hen khong hop le hoac khong thuoc quyen so huu cua ban.")

            elif choice == "8":
                print_header("LICH SU CUOC HEN CA NHAN")
                current = appointment_manager.appointments.head
                has_history = False
                while current:
                    apt = current.value
                    if apt.patient_id == patient_id:
                        print(f"Ma hen: {apt.id} | Schedule ID: {apt.schedule_id} | Trang thai: {apt.status}")
                        has_history = True
                    current = current.next
                if not has_history:
                    print("Ban chua tung dat cuoc hen nao.")

            elif choice == "9":
                print_header("XEM BENH AN CUA BAN")
                results = medical_record_manager.find_medical_records_by_patient_id(patient_id)
                current = results.head
                if not current:
                    print("Ban chua co ho so benh an nao tren he thong.")
                while current:
                    mr = current.value
                    print(f"Trieu chung: {mr.symptoms} | Chan doan: {mr.diagnosis} | Don thuoc: {mr.prescription}")
                    current = current.next

            elif choice == "10":
                print_header("DOI MAT KHAU")
                username = getattr(current_user, 'phone', '') or getattr(current_user, 'email', '')
                old_pwd = get_input("Nhap mat khau cu: ")
                new_pwd = get_input("Nhap mat khau moi: ")
                status, message = user_manager.change_password(username, old_pwd, new_pwd)
                print(message)

            elif choice == "0":
                print("Dang xuat khoi quyen Benh nhan.")
                break
            else:
                print("Lua chon khong hop le.")
        except Exception as e:
            print(f"Loi thuc thi chuc nang: {str(e)}")
