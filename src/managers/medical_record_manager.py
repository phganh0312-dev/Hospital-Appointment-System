from structures.linked_list import LinkedList
from entities.medical_record import MedicalRecord
from managers.file_handler import FileHandler


class MedicalRecordManager:
    # Ham quan ly benh an: them, sua, xoa benh an cua benh nhan sau khi kham xong
    def __init__(self, medical_records=None, appointment_manager=None, schedule_manager=None):
        self.medical_records = medical_records or LinkedList()
        self.appointment_manager = appointment_manager
        self.schedule_manager = schedule_manager

    def _save_to_file(self):
        FileHandler.save_data(
            "data/records.txt",
            self.medical_records,
            lambda r: f"{r.id}|{r.appointment_id}|{r.symptoms}|{r.diagnosis}|{r.prescription}"
        )

    def _doctor_owns_record(self, record, doctor_id):
        if not self.appointment_manager or not self.schedule_manager:
            return False
        appointment = self.appointment_manager.find_appointment_by_id(getattr(record, 'appointment_id', ''))
        if not appointment:
            return False
        schedule = self.schedule_manager.find_schedule_by_id(getattr(appointment, 'schedule_id', ''))
        return bool(schedule and getattr(schedule, 'doctor_id', '') == doctor_id)

    def add_medical_record(self, record: MedicalRecord, doctor_id):
        if not isinstance(record, MedicalRecord):
            raise TypeError('Phai nhap mot ho so benh an')
        if not self.appointment_manager or not self.schedule_manager:
            raise ValueError('He thong thieu lien ket lich hen/lich kham')

        appointment = self.appointment_manager.find_appointment_by_id(record.appointment_id)
        if not appointment:
            raise ValueError('Cuoc hen khong ton tai')

        schedule = self.schedule_manager.find_schedule_by_id(getattr(appointment, 'schedule_id', ''))
        if not schedule or getattr(schedule, 'doctor_id', '') != doctor_id:
            raise PermissionError("Bac si khong co quyen tao benh an cho cuoc kham nay")

        if getattr(appointment, 'status', '') not in ("COMPLETED", "Da kham", "Da hoan thanh"):
            raise ValueError("Chi tao benh an sau khi hoan thanh kham")

        if self.find_by_appointment_id(record.appointment_id):
            raise ValueError("Cuoc hen da co benh an")

        self.medical_records.append(record)
        self._save_to_file()
        return True

    def update_medical_record(self, record_id, symptoms, diagnosis, prescription, doctor_id):
        record = self.find_medical_record_by_id(record_id)
        if not record:
            return False
        if not self._doctor_owns_record(record, doctor_id):
            raise PermissionError("Bac si khong co quyen chinh sua benh an nay")

        if symptoms is not None:
            record.symptoms = symptoms
        if diagnosis is not None:
            record.diagnosis = diagnosis
        if prescription is not None:
            record.prescription = prescription

        self._save_to_file()
        return True

    def remove_medical_record_by_id(self, record_id, doctor_id):
        record = self.find_medical_record_by_id(record_id)
        if not record:
            return False
        if not self._doctor_owns_record(record, doctor_id):
            raise PermissionError("Khong co quyen xoa benh an nay")

        self.medical_records.remove(record_id)
        self._save_to_file()
        return True

    def find_medical_record_by_id(self, record_id):
        return self.medical_records.find_by_attribute('id', record_id)

    def find_by_appointment_id(self, appointment_id):
        return self.medical_records.find_by_attribute('appointment_id', appointment_id)

    def find_medical_records_by_patient_id(self, patient_id):
        results = LinkedList()
        if not self.appointment_manager:
            return results

        current = self.medical_records.head
        while current:
            record = current.value
            appointment = self.appointment_manager.find_appointment_by_id(getattr(record, 'appointment_id', ''))
            if appointment and getattr(appointment, 'patient_id', None) == patient_id:
                results.append(record)
            current = current.next
        return results

    def auto_generate_record(self, appointment_id):
        if self.find_by_appointment_id(appointment_id):
            return False

        max_id = 0
        current = self.medical_records.head
        while current:
            try:
                num = int(getattr(current.value, 'id', 'R00000000')[1:])
                if num > max_id:
                    max_id = num
            except Exception:
                pass
            current = current.next

        num_str = str(max_id + 1)
        while len(num_str) < 8:
            num_str = "0" + num_str

        new_record = MedicalRecord("R" + num_str, appointment_id, "", "", "")
        self.medical_records.append(new_record)
        self._save_to_file()
        return new_record
