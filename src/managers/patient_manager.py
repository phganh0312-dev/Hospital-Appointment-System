from structures.hash_table import HashTable
from structures.linked_list import LinkedList
from entities.patient import Patient
from managers.base_manager import BaseManager
from managers.file_handler import FileHandler

class PatientManager(BaseManager):
    def __init__(self, patients=None, appointment_manager=None, user_manager=None):
        self.patients = patients or HashTable()
        self.appointment_manager = appointment_manager
        self.user_manager = user_manager  # Bổ sung User Manager để đồng bộ tài khoản

    def _save_to_file(self):
        """Tự động đồng bộ HashTable xuống file qua FileHandler"""
        FileHandler.save_data(
            "data/patients.txt", 
            self.patients.values(), 
            lambda p: f"{p.id}|{p.cccd}|{p.full_name}|{p.phone}|{p.email}|{p.province}|{p.ward}|{p.detailed_address}|{getattr(p, 'bhyt_code', '')}|{getattr(p, 'bhyt_expiry', '')}"
        )

    def add_patient(self, patient: Patient):
        if not isinstance(patient, Patient):
            raise TypeError('Phải nhập một bệnh nhân')
            
        if self.find_patient_by_id(patient.id):
            raise ValueError('Mã bệnh nhân đã tồn tại')

        # Kiểm tra trùng CCCD
        for p in self.patients.values():
            if getattr(p, 'cccd', None) == patient.cccd:
                raise ValueError('CCCD đã tồn tại')

        self.patients.set(patient.phone, patient)
        self._save_to_file()

    def find_patient_by_id(self, patient_id):
        for p in self.patients.values():
            if getattr(p, 'id', None) == patient_id:
                return p
        return None

    def update_patient(self, phone, updates):
        """
        Cập nhật thông tin bệnh nhân.
        ĐÃ CHUYỂN allowed_fields SANG TUPLE ĐỂ TRÁNH DÙNG SET {}
        """
        patient = self.patients.get(phone)
        if not patient:
            raise ValueError('Không tìm thấy bệnh nhân')

        new_phone = updates.get('phone')
        new_email = updates.get('email')
        old_phone = getattr(patient, 'phone', '')

        # 2. Cập nhật dữ liệu cho Patient (Sử dụng Tuple thay cho Set)
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

        for key, value in updates.items():
            if key in allowed_fields:
                setattr(patient, key, value)

        self._save_to_file()

        # 3. Transaction đồng bộ chéo: Bắn tín hiệu sang UserManager
        if self.user_manager and (new_phone or new_email):
            user = self.user_manager.users.get(old_phone)
            if user:
                if new_email:
                    user.email = new_email
                
                # Đặc biệt: Nếu đổi SĐT, phải thay cả Key trong Hash Table của UserManager
                if new_phone and new_phone != old_phone:
                    user.phone = new_phone
                    self.user_manager.users.remove(old_phone)
                    self.user_manager.users.set(new_phone, user)
                
                # Gọi lệnh lưu cứng xuống user_credentials.txt
                if hasattr(self.user_manager, '_save_data_to_file'):
                    self.user_manager._save_data_to_file()

        return True