import os
from entities.doctor import Doctor
from entities.patient import Patient
from entities.doctor_schedule import Schedule
from entities.appointment import Appointment
from entities.medical_record import MedicalRecord

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
    def load_data(file_path, constructor, split_char='|'):
        """
        Đọc dữ liệu từ file và trả về một danh sách (list) các dữ liệu thô.
        """
        data_list = []
        if not os.path.exists(file_path):
            return data_list
            
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(split_char)
                    data_list.append(parts)
        return data_list

    # --- Các hàm Helper cụ thể cho từng loại dữ liệu ---
    
    @staticmethod
    def save_all_to_files(manager):
        # Lưu Doctors
        FileHandler.save_data("data/doctors.txt", manager.doctors, 
            lambda d: f"{d.id}|{d.name}|{d.gender}|{d.specialty}|{d.base_price}|{d.phone}")
        
        # Lưu Patients
        FileHandler.save_data("data/patients.txt", manager.patients,
            lambda p: f"{p.id}|{p.cccd}|{p.full_name}|{p.phone}|{p.province}|{p.ward}|{p.detailed_address}")
            
        # Lưu Schedules
        FileHandler.save_data("data/schedules.txt", manager.schedules,
            lambda s: f"{s.id}|{s.doctor_id}|{s.date}|{s.time_slot}|{s.is_booked}")

        # Lưu Appointments
        FileHandler.save_data("data/appointments.txt", manager.appointments,
            lambda a: f"{a.id}|{a.patient_id}|{a.schedule_id}|{a.status}")

    @staticmethod
    def load_all_from_files(manager):
        # Nạp Doctors
        for d in FileHandler.load_data("data/doctors.txt", Doctor):
            manager.add_doctor(Doctor(*d))
            
        # Nạp Patients
        for p in FileHandler.load_data("data/patients.txt", Patient):
            manager.add_patient(Patient(*p))
            
        # Nạp Schedules
        for s in FileHandler.load_data("data/schedules.txt", Schedule):
            # Cần convert is_booked từ string 'True' sang bool
            s[4] = (s[4] == 'True')
            manager.add_schedule(Schedule(*s))
            
        # Nạp Appointments
        for a in FileHandler.load_data("data/appointments.txt", Appointment):
            manager.add_appointment(Appointment(*a))
