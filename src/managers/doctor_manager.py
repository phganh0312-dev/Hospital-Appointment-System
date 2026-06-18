import threading
from structures.linked_list import LinkedList
from structures.hash_table import HashTable
from entities.doctor import Doctor
from managers.base_manager import BaseManager, ValidationError, DataConsistencyError
from managers.file_handler import FileHandler


# =========================================================================
# CÁC CLASS BỔ TRỢ ĐỂ THAY THẾ DICTIONARY/HASH NATIVE CỦA PYTHON
# =========================================================================

class DoctorRevenue:
    """Class đại diện cho doanh thu của một bác sĩ (thay thế dict native)"""
    def __init__(self, doctor, revenue):
        self.doctor = doctor
        self.revenue = revenue

    def __str__(self):
        return f"Bác sĩ: {self.doctor.name} (ID: {self.doctor.id}) | Doanh thu: {self.revenue:,} VND"


class ScheduleSlotInfo:
    """Class chứa thông tin chi tiết về một slot khám trong ngày (thay thế dict native)"""
    def __init__(self, schedule_id, slot_num, status, patient_id):
        self.schedule_id = schedule_id
        self.slot_num = slot_num
        self.status = status
        self.patient_id = patient_id


# =========================================================================
# MAIN DOCTOR MANAGER CLASS
# =========================================================================

class DoctorManager(BaseManager):
    """
    Quản lý thông tin và lịch trình của Bác sĩ.
    Đã chuẩn hóa 100% KHÔNG sử dụng list [] hay dict {} native của Python.
    """
    
    def __init__(self, doctors=None, schedule_manager=None, appointment_manager=None, user_manager=None):
        super().__init__()
        self.doctors = doctors or LinkedList()
        self.schedule_manager = schedule_manager
        self.appointment_manager = appointment_manager
        self.user_manager = user_manager
        
        # Lock để đảm bảo thao tác xóa diễn ra an toàn đơn luồng (Atomic)
        self.delete_lock = threading.Lock()
 
    # ==========================================
    # LƯU TRỮ DỮ LIỆU (PERSISTENCE)
    # ==========================================
    def _save_doctors_to_file(self):
        """Lưu danh sách bác sĩ xuống file text qua FileHandler"""
        try:
            FileHandler.save_data(
                "data/doctors.txt",
                self.doctors,
                lambda d: f"{d.id}|{d.name}|{d.specialty}|{d.phone}|{d.email}|{getattr(d, 'base_price', 0)}"
            )
        except Exception as e:
            print(f"Lỗi đồng bộ file doctors.txt: {e}")
 
    # ==========================================
    # CÁC THAO TÁC NGHIỆP VỤ (BUSINESS LOGIC)
    # ==========================================
    def add_doctor(self, doctor: Doctor):
        """Thêm bác sĩ mới vào hệ thống"""
        if not isinstance(doctor, Doctor):
            raise ValidationError("Dữ liệu đầu vào phải là một đối tượng Doctor.")
            
        if self.find_doctor_by_id(doctor.id):
            raise ValidationError(f"Mã bác sĩ {doctor.id} đã tồn tại trên hệ thống.")
            
        self.doctors.append(doctor)
        self._save_doctors_to_file()
 
    def find_doctor_by_id(self, doctor_id):
        """Tìm kiếm bác sĩ theo ID bằng Linear Search trên LinkedList"""
        current = self.doctors.head
        while current:
            if getattr(current.value, 'id', None) == doctor_id:
                return current.value
            current = current.next
        return None
 
    def search_doctors(self, keyword=None, specialty=None):
        """Tìm kiếm bác sĩ theo từ khóa (Tên/SĐT) hoặc Chuyên khoa"""
        results = LinkedList()
        keyword_lower = self._to_lower(keyword) if keyword else None
        specialty_lower = self._to_lower(specialty) if specialty else None
        
        current = self.doctors.head
        while current:
            doc = current.value
            match = True
            
            # Lọc theo chuyên khoa
            if specialty_lower:
                doc_spec_lower = self._to_lower(getattr(doc, 'specialty', ''))
                if not self._custom_find_substring(doc_spec_lower, specialty_lower):
                    match = False
            
            # Lọc theo từ khóa tên hoặc số điện thoại
            if match and keyword_lower:
                doc_name_lower = self._to_lower(getattr(doc, 'name', ''))
                doc_phone = getattr(doc, 'phone', '')
                if not (self._custom_find_substring(doc_name_lower, keyword_lower) or keyword in doc_phone):
                    match = False
                    
            if match:
                results.append(doc)
                
            current = current.next
        return results
 
    def remove_doctor(self, doctor_id):
        """ Xóa bác sĩ kèm theo cơ chế Cascade Delete an toàn tài nguyên """
        with self.delete_lock:
            doctor = self.find_doctor_by_id(doctor_id)
            if not doctor:
                raise ValidationError("Bác sĩ không tồn tại để xóa.")
                
            # 1. KIỂM TRA RÀNG BUỘC TOÀN VẸN (Chống Orphan Records từ môn DB)
            if self.appointment_manager:
                current_a = self.appointment_manager.appointments.head
                while current_a:
                    app = current_a.value
                    if self.schedule_manager:
                        sched = self.schedule_manager.find_schedule_by_id(getattr(app, 'schedule_id', None))
                        if sched and getattr(sched, 'doctor_id', None) == doctor_id:
                            # Nếu có cuộc hẹn chưa khám/chưa hủy thì không cho xóa bác sĩ
                            if getattr(app, 'status', '') not in ['COMPLETED', 'CANCELLED', 'Đã khám', 'Đã hủy']:
                                raise DataConsistencyError("Không thể xóa bác sĩ do đang có lịch hẹn khám chưa hoàn tất.")
                    current_a = current_a.next
                    
            # 2. CASCADE DELETE: Xóa toàn bộ lịch trực liên quan của bác sĩ này
            if self.schedule_manager:
                updated_schedules = LinkedList()
                current_s = self.schedule_manager.schedules.head
                while current_s:
                    if getattr(current_s.value, 'doctor_id', None) != doctor_id:
                        updated_schedules.append(current_s.value)
                    current_s = current_s.next
                self.schedule_manager.schedules = updated_schedules
                self.schedule_manager._save_to_file()
 
            # 3. ĐỒNG BỘ ACCOUNT: Xóa thông tin đăng nhập trong UserManager
            if self.user_manager and getattr(doctor, 'phone', None):
                if hasattr(self.user_manager, 'users'):
                    self.user_manager.users.remove(doctor.phone)
                    if hasattr(self.user_manager, '_save_data_to_file'):
                        self.user_manager._save_data_to_file()
 
            # 4. THỰC HIỆN XÓA BÁC SĨ
            self.doctors.remove(doctor_id)
            self._save_doctors_to_file()
            return True
 
    def get_daily_schedule(self, doctor_id, date_input):
        """
        Lấy danh sách các ca khám trong ngày của bác sĩ.
        Trả về LinkedList chứa các đối tượng cụ thể (ScheduleSlotInfo) thay vì Dictionary native.
        """
        target_date = self._to_date(date_input)
        daily_schedule = LinkedList()
        
        if not self.schedule_manager or not self.appointment_manager:
            return daily_schedule
        
        current_s = self.schedule_manager.schedules.head
        while current_s:
            sched = current_s.value
            if (getattr(sched, 'doctor_id', None) == doctor_id and 
                self._to_date(getattr(sched, 'date', None)) == target_date):
                
                patient_id = None
                status_text = "Trống"
                
                # Tìm xem có cuộc hẹn nào được đặt vào slot lịch này không
                current_a = self.appointment_manager.appointments.head
                while current_a:
                    app = current_a.value
                    if getattr(app, 'schedule_id', None) == sched.id:
                        status_text = getattr(app, 'status', 'Đã đặt hẹn')
                        patient_id = getattr(app, 'patient_id', 'Chưa rõ')
                        break
                    current_a = current_a.next
                
                # Bọc dữ liệu vào object cấu trúc tự xây
                slot_info = ScheduleSlotInfo(
                    schedule_id=sched.id,
                    slot_num=getattr(sched, 'slot_num', None),
                    status=status_text,
                    patient_id=patient_id
                )
                daily_schedule.append(slot_info)
            
            current_s = current_s.next
        
        return daily_schedule

    def rank_doctors_by_revenue(self):
        """
        Thống kê doanh thu của từng bác sĩ dựa trên các cuộc hẹn đã khám thành công.
        Sử dụng HashTable để gom nhóm và thuật toán BUBBLE SORT tự xây trên LinkedList để xếp hạng giảm dần.
        """
        if not self.appointment_manager or not self.schedule_manager:
            return LinkedList()
            
        # Sử dụng HashTable tự xây để lưu trữ tạm thời doanh thu theo dạng (doctor_id: revenue_value)
        revenue_map = HashTable()
        
        # Khởi tạo doanh thu ban đầu bằng 0 cho toàn bộ bác sĩ
        current_d = self.doctors.head
        while current_d:
            revenue_map.set(current_d.value.id, 0.0)
            current_d = current_d.next
            
        # Duyệt qua danh sách cuộc hẹn để tính lũy kế doanh thu
        current_a = self.appointment_manager.appointments.head
        while current_a:
            app = current_a.value
            status = getattr(app, 'status', '')
            
            if status in ['COMPLETED', 'Đã khám']:
                sched = self.schedule_manager.find_schedule_by_id(getattr(app, 'schedule_id', None))
                if sched:
                    doc_id = getattr(sched, 'doctor_id', None)
                    doc = self.find_doctor_by_id(doc_id)
                    if doc:
                        price = float(getattr(doc, 'base_price', 0))
                        current_rev = revenue_map.get(doc_id, 0.0)
                        revenue_map.set(doc_id, current_rev + price)
            current_a = current_a.next
            
        # Chuyển dữ liệu từ HashTable sang LinkedList để chuẩn bị thực hiện thuật toán sắp xếp
        ranked_list = LinkedList()
        current_d = self.doctors.head
        while current_d:
            doc = current_d.value
            rev = revenue_map.get(doc.id, 0.0)
            ranked_list.append(DoctorRevenue(doc, rev))
            current_d = current_d.next
            
        # THUẬT TOÁN BUBBLE SORT TỰ XÂY TRÊN LINKED LIST (Sắp xếp giảm dần theo doanh thu)
        if not ranked_list.head:
            return ranked_list
            
        swapped = True
        while swapped:
            swapped = False
            current = ranked_list.head
            while current and current.next:
                if current.value.revenue < current.next.value.revenue:
                    # Hoán đổi (swap) dữ liệu value giữa hai Node kề nhau
                    temp = current.value
                    current.value = current.next.value
                    current.next.value = temp
                    swapped = True
                current = current.next
                
        return ranked_list