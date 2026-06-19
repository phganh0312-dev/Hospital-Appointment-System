from managers.user_manager import UserManager
from managers.patient_manager import PatientManager
from managers.doctor_manager import DoctorManager
from managers.schedule_manager import ScheduleManager
from managers.medical_record_manager import MedicalRecordManager
from managers.appointment_manager import AppointmentManager
from managers.file_handler import FileHandler
from ui.main_menu import main_menu

from entities.user import User
from entities.doctor import Doctor
from entities.patient import Patient
from entities.doctor_schedule import Schedule
from entities.appointment import Appointment
from entities.medical_record import MedicalRecord


def load_all_data(user_manager, patient_manager, doctor_manager, schedule_manager, appointment_manager, medical_record_manager):
    users_nodes = FileHandler.load_data("data/user_credentials.txt")
    current = users_nodes.head
    while current:
        u = current.value
        if len(u) >= 6:
            user_manager.users.set(u[1], User(u[0], u[1], u[2], u[3], u[4], u[5]))
        current = current.next

    doctors_nodes = FileHandler.load_data("data/doctors.txt")
    current = doctors_nodes.head
    while current:
        d = current.value
        if len(d) >= 6:
            doctor_manager.doctors.append(Doctor(d[0], d[1], d[2], d[3], d[4], d[5]))
        current = current.next

    patients_nodes = FileHandler.load_data("data/patients.txt")
    current = patients_nodes.head
    while current:
        p = current.value
        if len(p) >= 8:
            bhyt_code = p[8] if len(p) >= 9 else None
            bhyt_expiry = p[9] if len(p) >= 10 else None
            patient_manager.patients.set(
                p[3],
                Patient(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], bhyt_code, bhyt_expiry)
            )
        current = current.next

    schedules_nodes = FileHandler.load_data("data/schedules.txt")
    current = schedules_nodes.head
    while current:
        s = current.value
        if len(s) >= 5:
            is_booked = (s[4] == 'True')
            day_of_week = int(s[5]) if len(s) >= 6 and s[5] else None
            slot_num = int(s[6]) if len(s) >= 7 and s[6] else None
            schedule_manager.schedules.append(Schedule(s[0], s[1], s[2], s[3], is_booked, day_of_week, slot_num))
        current = current.next

    appts_nodes = FileHandler.load_data("data/appointments.txt")
    current = appts_nodes.head
    while current:
        a = current.value
        if len(a) >= 4:
            payment_status = a[4] if len(a) >= 5 else "Chua thanh toan"
            appointment_manager.appointments.append(Appointment(a[0], a[1], a[2], a[3], payment_status))
        current = current.next

    records_nodes = FileHandler.load_data("data/records.txt")
    current = records_nodes.head
    while current:
        r = current.value
        if len(r) >= 5:
            medical_record_manager.medical_records.append(MedicalRecord(r[0], r[1], r[2], r[3], r[4]))
        current = current.next


def main():
    user_manager = UserManager()
    patient_manager = PatientManager()
    doctor_manager = DoctorManager()
    schedule_manager = ScheduleManager()
    appointment_manager = AppointmentManager()
    medical_record_manager = MedicalRecordManager()

    user_manager.patient_manager = patient_manager
    user_manager.doctor_manager = doctor_manager
    user_manager.schedule_manager = schedule_manager
    user_manager.appointment_manager = appointment_manager

    patient_manager.user_manager = user_manager
    patient_manager.appointment_manager = appointment_manager

    doctor_manager.user_manager = user_manager
    doctor_manager.schedule_manager = schedule_manager
    doctor_manager.appointment_manager = appointment_manager

    medical_record_manager.appointment_manager = appointment_manager
    medical_record_manager.schedule_manager = schedule_manager

    appointment_manager.schedule_manager = schedule_manager
    appointment_manager.patient_manager = patient_manager
    appointment_manager.doctor_manager = doctor_manager
    appointment_manager.user_manager = user_manager

    try:
        load_all_data(user_manager, patient_manager, doctor_manager, schedule_manager, appointment_manager, medical_record_manager)
    except Exception as e:
        print(f"[ERROR] Failed to load data: {type(e).__name__}: {e}")

    managers = {
        "user": user_manager,
        "patient": patient_manager,
        "doctor": doctor_manager,
        "schedule": schedule_manager,
        "appointment": appointment_manager,
        "record": medical_record_manager
    }

    main_menu(managers)


if __name__ == "__main__":
    main()
