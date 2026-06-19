import threading
from entities.user import User
from entities.patient import Patient
from structures.hash_table import HashTable
from structures.linked_list import LinkedList
from managers.file_handler import FileHandler
from managers.base_manager import BaseManager


class UserManager(BaseManager):
    def __init__(self, users=None, patient_manager=None, doctor_manager=None, schedule_manager=None, appointment_manager=None):
        super().__init__()
        self.users = users or HashTable()
        self.patient_manager = patient_manager
        self.doctor_manager = doctor_manager
        self.schedule_manager = schedule_manager
        self.appointment_manager = appointment_manager
        self.id_lock = threading.Lock()
        self.failed_attempts = HashTable()
        self.locked_accounts = HashTable()

    def _validate_password(self, password):
        if not password:
            return False, "Mat khau khong duoc de trong"

        length = 0
        has_alpha = False
        has_digit = False

        for char in password:
            length += 1
            if ('a' <= char <= 'z') or ('A' <= char <= 'Z'):
                has_alpha = True
            elif '0' <= char <= '9':
                has_digit = True

        if length < 8:
            return False, "Mat khau phai dai tu 8 ky tu tro len"
        if not has_alpha or not has_digit:
            return False, "Mat khau phai co it nhat 1 chu cai va 1 chu so"

        return True, "Hop le"

    def _pad_number(self, number, width):
        num_str = str(number)
        while len(num_str) < width:
            num_str = "0" + num_str
        return num_str

    def _generate_patient_id(self):
        with self.id_lock:
            max_id = 0
            if self.patient_manager:
                current = self.patient_manager.patients.values().head
                while current:
                    p_id = getattr(current.value, 'id', 'B00000000')
                    try:
                        num = int(p_id[1:])
                        if num > max_id:
                            max_id = num
                    except Exception:
                        pass
                    current = current.next
            return "B" + self._pad_number(max_id + 1, 8)

    def _generate_user_id(self):
        max_id = 0
        current = self.users.values().head
        while current:
            user_id = getattr(current.value, 'user_id', 'U00000000')
            try:
                num = int(user_id[1:])
                if num > max_id:
                    max_id = num
            except Exception:
                pass
            current = current.next
        return "U" + self._pad_number(max_id + 1, 8)

    def add_user(self, user):
        if user is None:
            return False
        if self.users.get(user.phone):
            return False
        self.users.set(user.phone, user)
        return True

    def _save_data_to_file(self):
        FileHandler.save_data(
            "data/user_credentials.txt",
            self.users.values(),
            lambda u: f"{u.user_id}|{u.phone}|{u.email}|{u.password}|{u.role}|{u.linked_id}"
        )

    def find_user_by_linked_id(self, linked_id, role=None):
        current = self.users.values().head
        while current:
            user = current.value
            if getattr(user, 'linked_id', '') == linked_id:
                if role is None or getattr(user, 'role', '') == role:
                    return user
            current = current.next
        return None

    def register_patient(self, phone, email, cccd, full_name, province, ward, detailed_address, password, confirm_password):
        current = self.users.values().head
        while current:
            user = current.value
            if getattr(user, 'phone', '') == phone:
                return False, "So dien thoai da ton tai tren he thong"
            if getattr(user, 'email', '') == email:
                return False, "Email da ton tai tren he thong"
            current = current.next

        if self.patient_manager:
            current = self.patient_manager.patients.values().head
            while current:
                if getattr(current.value, 'cccd', '') == cccd:
                    return False, "CCCD da duoc dang ky"
                current = current.next

        if password != confirm_password:
            return False, "Mat khau xac nhan khong khop"

        is_pw_valid, pw_msg = self._validate_password(password)
        if not is_pw_valid:
            return False, pw_msg

        new_patient_id = self._generate_patient_id()
        new_user_id = self._generate_user_id()
        new_patient = Patient(new_patient_id, cccd, full_name, phone, email, province, ward, detailed_address, None, None)
        new_user = User(new_user_id, phone, email, password, "patient", new_patient_id)

        if self.patient_manager:
            self.patient_manager.add_patient(new_patient)
        self.users.set(phone, new_user)
        self._save_data_to_file()

        return True, "Dang ky thanh cong"

    def authenticate(self, identifier, password):
        found_user = None
        current = self.users.values().head
        while current:
            user = current.value
            if getattr(user, 'phone', '') == identifier or getattr(user, 'email', '') == identifier:
                found_user = user
                break
            current = current.next

        if not found_user:
            return False, "Khong tim thay tai khoan trong he thong"

        user_id = getattr(found_user, 'user_id', '')
        if self.locked_accounts.get(user_id, False):
            return False, "Tai khoan da bi khoa do nhap sai mat khau qua 5 lan."

        if getattr(found_user, 'password', '') == password:
            self.locked_accounts.set(user_id, False)
            self.failed_attempts.remove(user_id)
            return True, found_user

        attempts = self.failed_attempts.get(user_id, 0) or 0
        attempts += 1
        self.failed_attempts.set(user_id, attempts)

        if attempts >= 5:
            self.locked_accounts.set(user_id, True)
            return False, "Tai khoan da bi khoa do nhap sai mat khau 5 lan."

        return False, f"Sai mat khau. Ban con {5 - attempts} lan thu."

    def change_password(self, identifier, old_password, new_password):
        from entities.user import User

        status, result = self.authenticate(identifier, old_password)

        if not status:
            return False, "Mat khau cu khong chinh xac"

        if not isinstance(result, User):
            return False, "Loi du lieu"

        result.password = new_password
        self._save_data_to_file()
        return True, "Doi mat khau thanh cong"

    def admin_search_users(self, keyword, role_filter=None):
        results = LinkedList()
        keyword_lower = self._to_lower(keyword)

        current = self.users.values().head
        while current:
            user = current.value
            next_node = current.next

            if role_filter and getattr(user, 'role', '') != role_filter:
                current = next_node
                continue

            match = False
            phone = getattr(user, 'phone', '')
            email = getattr(user, 'email', '')

            if phone == keyword or email == keyword:
                match = True

            if not match and getattr(user, 'role', '') == 'patient' and self.patient_manager:
                patient = self.patient_manager.find_patient_by_id(getattr(user, 'linked_id', ''))
                if patient:
                    p_name_lower = self._to_lower(getattr(patient, 'full_name', ''))
                    p_cccd = getattr(patient, 'cccd', '')
                    if p_cccd == keyword or self._custom_find_substring(p_name_lower, keyword_lower):
                        match = True

            if not match and getattr(user, 'role', '') == 'doctor' and self.doctor_manager:
                doctor = self.doctor_manager.find_doctor_by_id(getattr(user, 'linked_id', ''))
                if doctor:
                    d_name_lower = self._to_lower(getattr(doctor, 'name', ''))
                    if self._custom_find_substring(d_name_lower, keyword_lower):
                        match = True

            if match:
                results.append(user)

            current = next_node

        return results
