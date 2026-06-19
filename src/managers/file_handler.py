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
    def save_data(file_path, data_collection, to_string_func):
        with open(file_path, "w", encoding="utf-8") as f:
            if hasattr(data_collection, 'head'):
                current = data_collection.head
                while current:
                    f.write(to_string_func(current.value) + "\n")
                    current = current.next

    @staticmethod
    def load_data(file_path, split_char='|'):
        data_list = LinkedList()
        if not os.path.exists(file_path):
            return data_list

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    data_list.append(tuple(line.split(split_char)))
        return data_list

    @staticmethod
    def save_all_to_files(manager):
        FileHandler.save_data(
            "data/doctors.txt",
            manager.doctors,
            lambda d: f"{d.id}|{d.name}|{d.gender}|{d.specialty}|{getattr(d, 'base_price', 0)}|{d.phone}"
        )
        FileHandler.save_data(
            "data/patients.txt",
            manager.patients.values(),
            lambda p: f"{p.id}|{p.cccd}|{p.full_name}|{p.phone}|{p.email}|{p.province}|{p.ward}|{p.detailed_address}|{getattr(p, 'bhyt_code', '')}|{getattr(p, 'bhyt_expiry', '')}"
        )
        FileHandler.save_data(
            "data/schedules.txt",
            manager.schedules,
            lambda s: f"{s.id}|{s.doctor_id}|{s.date}|{s.time_slot}|{s.is_booked}|{getattr(s, 'day_of_week', '')}|{getattr(s, 'slot_num', '')}"
        )
        FileHandler.save_data(
            "data/appointments.txt",
            manager.appointments,
            lambda a: f"{a.id}|{a.patient_id}|{a.schedule_id}|{a.status}|{getattr(a, 'payment_status', '')}"
        )
        FileHandler.save_data(
            "data/records.txt",
            manager.medical_records,
            lambda m: f"{m.id}|{m.appointment_id}|{m.symptoms}|{m.diagnosis}|{m.prescription}"
        )
        FileHandler.save_data(
            "data/user_credentials.txt",
            manager.users.values(),
            lambda u: f"{u.user_id}|{u.phone}|{u.email}|{u.password}|{u.role}|{u.linked_id}"
        )

    @staticmethod
    def load_all_from_files(manager):
        current = FileHandler.load_data("data/doctors.txt").head
        while current:
            d = current.value
            if len(d) >= 6:
                manager.doctors.append(Doctor(d[0], d[1], d[2], d[3], d[4], d[5]))
            current = current.next

        current = FileHandler.load_data("data/patients.txt").head
        while current:
            p = current.value
            if len(p) >= 8:
                bhyt_code = p[8] if len(p) >= 9 else None
                bhyt_expiry = p[9] if len(p) >= 10 else None
                manager.patients.set(p[3], Patient(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], bhyt_code, bhyt_expiry))
            current = current.next

        current = FileHandler.load_data("data/schedules.txt").head
        while current:
            s = current.value
            if len(s) >= 5:
                is_booked = (s[4] == 'True')
                day_of_week = int(s[5]) if len(s) >= 6 and s[5] else None
                slot_num = int(s[6]) if len(s) >= 7 and s[6] else None
                manager.schedules.append(Schedule(s[0], s[1], s[2], s[3], is_booked, day_of_week, slot_num))
            current = current.next

        current = FileHandler.load_data("data/appointments.txt").head
        while current:
            a = current.value
            if len(a) >= 4:
                payment_status = a[4] if len(a) >= 5 else ""
                manager.appointments.append(Appointment(a[0], a[1], a[2], a[3], payment_status))
            current = current.next

        current = FileHandler.load_data("data/records.txt").head
        while current:
            r = current.value
            if len(r) >= 5:
                manager.medical_records.append(MedicalRecord(r[0], r[1], r[2], r[3], r[4]))
            current = current.next

        current = FileHandler.load_data("data/user_credentials.txt").head
        while current:
            u = current.value
            if len(u) >= 6:
                manager.users.set(u[1], User(u[0], u[1], u[2], u[3], u[4], u[5]))
            current = current.next
