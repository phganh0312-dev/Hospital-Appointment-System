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
        
        # Lock để đảm bảo tính an toàn cho luồng (Thread-safe) khi sinh mã bệnh nhân
        self.id_lock = threading.Lock()
        
        # Quản lý trạng thái khóa và số lần nhập sai trong RAM (tránh sửa entity quá nhiều)
        self.failed_attempts = HashTable() 
        self.locked_accounts = HashTable()

    def _validate_password(self, password):
        """Tự xây logic kiểm tra mật khẩu: >=8 ký tự, có số, có chữ"""
        if not password:
            return False, "Mật khẩu không được để trống"
        
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
            return False, "Mật khẩu phải dài từ 8 ký tự trở lên"
        if not has_alpha or not has_digit:
            return False, "Mật khẩu phải chứa ít nhất 1 chữ cái và 1 chữ số"
            
        return True, "Hợp lệ"

    def _generate_patient_id(self):
        """Sinh mã BN tự động, bọc Lock để tránh đụng độ (Race Condition)"""
        with self.id_lock:
            max_id = 0
            if self.patient_manager:
                current = self.patient_manager.patients.head
                while current:
                    p_id = getattr(current.value, 'id', 'B00000001')
                    try:
                        num = int(p_id[1:])
                        if num > max_id:
                            max_id = num
                    except:
                        pass
                    current = current.next
            return f"B{str(max_id + 1).zfill(8)}"

    # ==========================
    # LUỒNG ĐĂNG KÝ (REGISTRATION)
    # ==========================
    def register_patient(self, phone, email, cccd, full_name, province, ward, detailed_address, password, confirm_password):
        """
        Luồng xác thực tuần tự: Trả về (Status: bool, Message: str)
        """
        # 1. Kiểm tra tồn tại SĐT hoặc Email (Linear Search trên HashTable)
        for user in self.users.values():
            if getattr(user, 'phone', '') == phone:
                return False, "Số điện thoại đã tồn tại trên hệ thống"
            if getattr(user, 'email', '') == email:
                return False, "Email đã tồn tại trên hệ thống"

        # 2. Kiểm tra tồn tại CCCD bên Patient Manager
        if self.patient_manager:
            current = self.patient_manager.patients.head
            while current:
                if getattr(current.value, 'cccd', '') == cccd:
                    return False, "Căn cước công dân đã được đăng ký"
                current = current.next

        # 3. Kiểm tra Mật khẩu
        if password != confirm_password:
            return False, "Mật khẩu xác nhận không khớp"
        
        is_pw_valid, pw_msg = self._validate_password(password)
        if not is_pw_valid:
            return False, pw_msg

        # 4. Sinh mã và tạo Entity
        new_patient_id = self._generate_patient_id()
        new_user_id = "U" + new_patient_id[1:] 

        new_patient = Patient(new_patient_id, cccd, full_name, phone, email, province, ward, detailed_address, None, None)
        new_user = User(new_user_id, phone, email, password, "patient", new_patient_id)

        # 5. Lưu vào bộ nhớ
        if self.patient_manager:
            self.patient_manager.add_patient(new_patient)
        self.users.set(phone, new_user) # Dùng SĐT làm key trên HashTable

        # 6. Ghi xuống File (Lưu dữ liệu cứng)
        self._save_data_to_file()

        return True, "Đăng ký thành công"

    def _save_data_to_file(self):
        """Gọi FileHandler để cập nhật file txt"""
        FileHandler.save_data("data/user_credentials.txt", self.users.values(),
            lambda u: f"{u.user_id}|{u.phone}|{u.email}|{u.password}|{u.role}|{u.linked_id}")
        if self.patient_manager:
            FileHandler.save_data("data/patients.txt", self.patient_manager.patients,
                lambda p: f"{p.id}|{p.cccd}|{p.full_name}|{p.phone}|{p.email}|{p.province}|{p.ward}|{p.detailed_address}|{p.bhyt_code}|{p.bhyt_expiry}")

    # ==========================
    # LUỒNG ĐĂNG NHẬP (LOGIN)
    # ==========================
    def authenticate(self, identifier, password):
        """ identifier có thể là Phone hoặc Email. Trả về (Status: bool, User object / Lỗi: str) """
        found_user = None
        for user in self.users.values():
            if getattr(user, 'phone', '') == identifier or getattr(user, 'email', '') == identifier:
                found_user = user
                break
                
        if not found_user:
            return False, "Không tìm thấy tài khoản trong hệ thống"

        user_id = found_user.user_id
        
        # Check tài khoản có đang bị khóa không
        if self.locked_accounts.get(user_id) == True:
            return False, "Tài khoản của bạn đã bị khóa do nhập sai MK quá 5 lần hoặc vi phạm nội quy."

        # So khớp mật khẩu
        if getattr(found_user, 'password', '') == password:
            self.failed_attempts.remove(user_id) # Reset số lần sai
            return True, found_user
        else:
            # Ghi nhận nhập sai
            # Lấy giá trị ra trước, nếu là None thì mặc định là 0
            current_attempts = self.failed_attempts.get(user_id, 0)
            attempts = (current_attempts if current_attempts is not None else 0) + 1
            self.failed_attempts.set(user_id, attempts)
            
            if attempts >= 5:
                self.locked_accounts.set(user_id, True)
                return False, "Tài khoản của bạn đã bị khóa do nhập sai mật khẩu 5 lần."
            
            return False, f"Sai mật khẩu. Bạn còn {5 - attempts} lần thử."

    # ==========================
    # QUẢN LÝ MẬT KHẨU
    # ==========================
    def change_password(self, identifier, old_password, new_password):
        """Đổi mật khẩu nếu nhập đúng mật khẩu cũ"""
        status, result = self.authenticate(identifier, old_password)
        if not status:
            return False, "Mật khẩu cũ không chính xác"
            
        is_pw_valid, pw_msg = self._validate_password(new_password)
        if not is_pw_valid:
            return False, pw_msg
            
        user = result
        if isinstance(user, User):
            user.password = new_password
        self._save_data_to_file()
        return True, "Đổi mật khẩu thành công"

    # ==========================
    # QUẢN TRỊ VIÊN (ADMIN)
    # ==========================
    def admin_search_users(self, keyword, role_filter=None):
        """Admin tìm kiếm bằng tên, sđt, email, cccd (Bằng vòng lặp tự xây)"""
        results = LinkedList()
        keyword_lower = self._to_lower(keyword)

        for user in self.users.values():
            if role_filter and getattr(user, 'role', '') != role_filter:
                continue
                
            match = False
            phone = getattr(user, 'phone', '')
            email = getattr(user, 'email', '')
            
            # Khớp định danh trực tiếp
            if phone == keyword or email == keyword:
                match = True
                
            # Duyệt thông tin BN
            if not match and getattr(user, 'role', '') == 'patient' and self.patient_manager:
                patient = self.patient_manager.find_patient_by_id(getattr(user, 'linked_id', ''))
                if patient:
                    p_name_lower = self._to_lower(getattr(patient, 'full_name', ''))
                    p_cccd = getattr(patient, 'cccd', '')
                    if p_cccd == keyword or self._custom_find_substring(p_name_lower, keyword_lower):
                        match = True
                        
            # Duyệt thông tin BS
            if not match and getattr(user, 'role', '') == 'doctor' and self.doctor_manager:
                doctor = self.doctor_manager.find_doctor_by_id(getattr(user, 'linked_id', ''))
                if doctor:
                    d_name_lower = self._to_lower(getattr(doctor, 'name', ''))
                    if self._custom_find_substring(d_name_lower, keyword_lower):
                        match = True
            
            if match:
                results.append(user)
                
        return results

    def get_list_by_role(self, role):
        """Lấy danh sách chuyên biệt (Bác sĩ hoặc Bệnh nhân)"""
        return self.admin_search_users("", role_filter=role)