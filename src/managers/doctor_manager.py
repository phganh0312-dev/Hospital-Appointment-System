import threading
from structures.linked_list import LinkedList
from structures.hash_table import HashTable
from entities.doctor import Doctor
from managers.base_manager import BaseManager, ValidationError, DataConsistencyError
from managers.file_handler import FileHandler


class DoctorRevenue:
    def __init__(self, doctor: Doctor, revenue: float):
        self.doctor = doctor
        self.revenue = revenue

    def __str__(self):
        return f"Bac si: {self.doctor.name} (ID: {self.doctor.id}) | Doanh thu: {self.revenue:,.0f} VND"


class ScheduleSlotInfo:
    def __init__(self, schedule_id, time_slot, is_booked, status, patient_id):
        self.schedule_id = schedule_id
        self.time_slot = time_slot
        self.is_booked = is_booked
        self.status = status
        self.patient_id = patient_id


class DoctorManager(BaseManager):
    # Ham quan ly thong tin bac si: them, sua, xoa, tim kiem, xem lich khac bac si
    def __init__(self, doctors=None, schedule_manager=None, appointment_manager=None, user_manager=None):
        super().__init__()
        self.doctors = doctors or LinkedList()
        self.schedule_manager = schedule_manager
        self.appointment_manager = appointment_manager
        self.user_manager = user_manager
        self.delete_lock = threading.Lock()

    def _save_doctors_to_file(self):
        FileHandler.save_data(
            "data/doctors.txt",
            self.doctors,
            lambda d: f"{d.id}|{d.name}|{d.gender}|{d.specialty}|{getattr(d, 'base_price', 0)}|{d.phone}"
        )

    def add_doctor(self, doctor: Doctor):
        if not isinstance(doctor, Doctor):
            raise ValidationError("Du lieu dau vao phai la bac si")
        if self.find_doctor_by_id(doctor.id):
            raise ValidationError(f"Ma bac si {doctor.id} da ton tai")
        self.doctors.append(doctor)
        self._save_doctors_to_file()

    def find_doctor_by_id(self, doctor_id):
        current = self.doctors.head
        while current:
            if getattr(current.value, 'id', None) == doctor_id:
                return current.value
            current = current.next
        return None

    def get_doctor_email(self, doctor_id):
        if not self.user_manager:
            return ""
        user = self.user_manager.find_user_by_linked_id(doctor_id, "doctor")
        return getattr(user, 'email', '') if user else ""

    def search_doctors(self, keyword=None, specialty=None):
        results = LinkedList()
        keyword_lower = self._to_lower(keyword) if keyword else None
        specialty_lower = self._to_lower(specialty) if specialty else None

        current = self.doctors.head
        while current:
            doc = current.value
            match = True

            if specialty_lower:
                doc_spec_lower = self._to_lower(getattr(doc, 'specialty', ''))
                if not self._custom_find_substring(doc_spec_lower, specialty_lower):
                    match = False

            if match and keyword_lower:
                doc_name_lower = self._to_lower(getattr(doc, 'name', ''))
                doc_phone = str(getattr(doc, 'phone', ''))
                if not (
                    self._custom_find_substring(doc_name_lower, keyword_lower)
                    or self._custom_find_substring(doc_phone, str(keyword))
                ):
                    match = False

            if match:
                results.append(doc)
            current = current.next

        return results

    def remove_doctor(self, doctor_id):
        with self.delete_lock:
            doctor = self.find_doctor_by_id(doctor_id)
            if not doctor:
                raise ValidationError("Bac si khong ton tai")

            if self.appointment_manager and self.schedule_manager:
                current_a = self.appointment_manager.appointments.head
                while current_a:
                    app = current_a.value
                    sched = self.schedule_manager.find_schedule_by_id(getattr(app, 'schedule_id', None))
                    if sched and getattr(sched, 'doctor_id', None) == doctor_id:
                        status = getattr(app, 'status', '')
                        if status not in ('COMPLETED', 'CANCELLED', 'Đã khám', 'Đã hủy'):
                            raise DataConsistencyError("Bac si dang co lich hen chua hoan tat")
                    current_a = current_a.next

            if self.schedule_manager:
                updated_schedules = LinkedList()
                current_s = self.schedule_manager.schedules.head
                while current_s:
                    if getattr(current_s.value, 'doctor_id', None) != doctor_id:
                        updated_schedules.append(current_s.value)
                    current_s = current_s.next
                self.schedule_manager.schedules = updated_schedules
                self.schedule_manager._save_to_file()

            if self.user_manager and getattr(doctor, 'phone', None):
                self.user_manager.users.remove(doctor.phone)
                self.user_manager._save_data_to_file()

            self.doctors.remove(doctor_id)
            self._save_doctors_to_file()
            return True

    def get_daily_schedule(self, doctor_id, date_input):
        target_date = self._to_date(date_input)
        daily_schedule = LinkedList()

        if not self.schedule_manager or not self.appointment_manager:
            return daily_schedule

        current_s = self.schedule_manager.schedules.head
        while current_s:
            sched = current_s.value
            if getattr(sched, 'doctor_id', None) == doctor_id and self._to_date(getattr(sched, 'date', None)) == target_date:
                patient_id = ""
                status_text = "Trong"

                current_a = self.appointment_manager.appointments.head
                while current_a:
                    app = current_a.value
                    if getattr(app, 'schedule_id', None) == sched.id:
                        status_text = getattr(app, 'status', 'Da dat')
                        patient_id = getattr(app, 'patient_id', '')
                        break
                    current_a = current_a.next

                daily_schedule.append(ScheduleSlotInfo(
                    sched.id,
                    getattr(sched, 'time_slot', ''),
                    getattr(sched, 'is_booked', False),
                    status_text,
                    patient_id
                ))
            current_s = current_s.next

        return daily_schedule

    def rank_doctors_by_revenue(self):
        if not self.appointment_manager or not self.schedule_manager:
            return LinkedList()

        revenue_map = HashTable()
        current_d = self.doctors.head
        while current_d:
            revenue_map.set(current_d.value.id, 0.0)
            current_d = current_d.next

        current_a = self.appointment_manager.appointments.head
        while current_a:
            app = current_a.value
            if getattr(app, 'status', '') in ('COMPLETED', 'Đã khám', 'Đã hoàn thành'):
                sched = self.schedule_manager.find_schedule_by_id(getattr(app, 'schedule_id', None))
                if sched:
                    doc = self.find_doctor_by_id(getattr(sched, 'doctor_id', None))
                    if doc:
                        current_rev = revenue_map.get(doc.id, 0.0) or 0.0
                        revenue_map.set(doc.id, float(current_rev) + float(getattr(doc, 'base_price', 0)))
            current_a = current_a.next

        ranked_list = LinkedList()
        current_d = self.doctors.head
        while current_d:
            doc = current_d.value
            ranked_list.append(DoctorRevenue(doc, float(revenue_map.get(doc.id, 0.0) or 0.0)))
            current_d = current_d.next

        swapped = True
        while swapped:
            swapped = False
            current = ranked_list.head
            while current and current.next:
                if current.value.revenue < current.next.value.revenue:
                    temp = current.value
                    current.value = current.next.value
                    current.next.value = temp
                    swapped = True
                current = current.next

        return ranked_list
