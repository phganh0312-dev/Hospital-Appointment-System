import os
from structures.linked_list import LinkedList
from entities.doctor import Doctor
from entities.patient import Patient
from entities.doctor_schedule import Schedule
from entities.appointment import Appointment
from entities.medical_record import MedicalRecord
from entities.user import User

class FileHandler:
    @staticmethod
    def save_data(file_path, linked_list, to_string_func):
        """
        Lưu danh sách bất kỳ xuống file. 
        to_string_func là hàm format object thành chuỗi lưu file.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            for item in linked_list:
                f.write(to_string_func(item) + "\n")

    @staticmethod
    def load_data(file_path, split_char='|'):
        """
        Đọc dữ liệu từ file và trả về LinkedList chứa các Tuple (không dùng List).
        """
        data_list = LinkedList()
        if not os.path.exists(file_path):
            return data_list
            
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    # Ép kiểu về tuple để tránh sử dụng kiểu list []
                    parts = tuple(line.strip().split(split_char))
                    data_list.append(parts)
        return data_list

    # --- Các hàm Helper cụ thể cho từng loại dữ liệu ---
    
    @staticmethod
    def save_all_to_files(manager):
        FileHandler.save_data("data/doctors.txt", manager.doctors, 
            lambda d: f"{d.id}|{d.name}|{d.gender}|{d.specialty}|{d.base_price}|{d.phone}")
        FileHandler.save_data("data/patients.txt", manager.patients,
            lambda p: f"{p.id}|{p.cccd}|{p.full_name}|{p.phone}|{p.email}|{p.province}|{p.ward}|{p.detailed_address}|{p.bhyt_code}|{p.bhyt_expiry}")
        FileHandler.save_data("data/schedules.txt", manager.schedules,
            lambda s: f"{s.id}|{s.doctor_id}|{s.date}|{s.time_slot}|{s.is_booked}|{getattr(s, 'day_of_week', '')}|{getattr(s, 'slot_num', '')}")
        FileHandler.save_data("data/appointments.txt", manager.appointments,
            lambda a: f"{a.id}|{a.patient_id}|{a.schedule_id}|{a.status}|{getattr(a, 'payment_status', '')}")
        FileHandler.save_data("data/records.txt", manager.medical_records,
            lambda m: f"{m.id}|{m.appointment_id}|{m.symptoms}|{m.diagnosis}|{m.prescription}")
        FileHandler.save_data("data/user_credentials.txt", manager.users,
            lambda u: f"{u.user_id}|{u.phone}|{u.email}|{u.password}|{u.role}|{u.linked_id}")

    @staticmethod
    def load_all_from_files(manager):
        for d in FileHandler.load_data("data/doctors.txt"):
            manager.add_doctor(Doctor(*d))
            
        for p in FileHandler.load_data("data/patients.txt"):
            manager.add_patient(Patient(*p))
            
        for s in FileHandler.load_data("data/schedules.txt"):
            is_booked = (s[4] == 'True')
            day_of_week = int(s[5]) if len(s) >= 6 and s[5] else None
            slot_num = int(s[6]) if len(s) >= 7 and s[6] else None
            manager.add_schedule(Schedule(s[0], s[1], s[2], s[3], is_booked, day_of_week, slot_num))
            
        for a in FileHandler.load_data("data/appointments.txt"):
            manager.add_appointment(Appointment(*a))

        for m in FileHandler.load_data("data/records.txt"):
            manager.add_medical_record(MedicalRecord(*m))

        for u in FileHandler.load_data("data/user_credentials.txt"):
            manager.add_user(User(*u))