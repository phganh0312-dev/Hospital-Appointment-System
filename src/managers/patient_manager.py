from structures.hash_table import HashTable
from entities.patient import Patient
from managers.base_manager import BaseManager
from managers.file_handler import FileHandler


class PatientManager(BaseManager):
    # Ham quan ly thong tin benh nhan: them, sua, xoa, tim kiem benh nhan
    def __init__(self, patients=None, appointment_manager=None, user_manager=None):
        self.patients = patients or HashTable()
        self.appointment_manager = appointment_manager
        self.user_manager = user_manager

    def _save_to_file(self):
        FileHandler.save_data(
            "data/patients.txt",
            self.patients.values(),
            lambda p: f"{p.id}|{p.cccd}|{p.full_name}|{p.phone}|{p.email}|{p.province}|{p.ward}|{p.detailed_address}|{getattr(p, 'bhyt_code', '')}|{getattr(p, 'bhyt_expiry', '')}"
        )

    def add_patient(self, patient: Patient):
        if not isinstance(patient, Patient):
            raise TypeError('Phai nhap mot benh nhan')

        if self.find_patient_by_id(patient.id):
            raise ValueError('Ma benh nhan da ton tai')

        current = self.patients.values().head
        while current:
            if getattr(current.value, 'cccd', None) == patient.cccd:
                raise ValueError('CCCD da ton tai')
            current = current.next

        self.patients.set(patient.phone, patient)
        self._save_to_file()

    def find_patient_by_id(self, patient_id):
        current = self.patients.values().head
        while current:
            if getattr(current.value, 'id', None) == patient_id:
                return current.value
            current = current.next
        return None

    # Cap nhat thong tin benh nhan (ten, dia chi, email, etc)
    def update_patient(self, identifier, updates):
        patient = self.patients.get(identifier)
        if not patient:
            patient = self.find_patient_by_id(identifier)
        if not patient:
            raise ValueError('Khong tim thay benh nhan')

        old_phone = getattr(patient, 'phone', '')
        new_phone = None
        new_email = None
        
        # Kiem tra updates co phai HashTable khong de lay .items()
        if hasattr(updates, 'items'):
            items_iter = updates.items()
            if hasattr(items_iter, 'head'):
                current = items_iter.head
            else:
                current = None
        else:
            current = None

        allowed_fields = (
            "full_name",
            "phone",
            "email",
            "province",
            "ward",
            "detailed_address",
            "bhyt_code",
            "bhyt_expiry"
        )

        while current:
            key = current.value.key
            value = current.value.value
            if key in allowed_fields:
                if key == 'phone':
                    new_phone = value
                elif key == 'email':
                    new_email = value
                setattr(patient, key, value)
            current = current.next

        if new_phone and new_phone != old_phone:
            self.patients.remove(old_phone)
            self.patients.set(new_phone, patient)

        self._save_to_file()

        if self.user_manager and (new_phone or new_email):
            user = self.user_manager.users.get(old_phone)
            if user:
                if new_email:
                    user.email = new_email
                if new_phone and new_phone != old_phone:
                    user.phone = new_phone
                    self.user_manager.users.remove(old_phone)
                    self.user_manager.users.set(new_phone, user)
                self.user_manager._save_data_to_file()

        return True
