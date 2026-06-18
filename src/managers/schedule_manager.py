from structures.linked_list import LinkedList
from entities.doctor_schedule import Schedule
from managers.base_manager import BaseManager
from managers.file_handler import FileHandler  # Thêm import FileHandler

class ScheduleManager(BaseManager):
    def __init__(self, schedules=None):
        self.schedules = schedules or LinkedList()

    # ==========================================
    # LƯU TRỮ DỮ LIỆU (PERSISTENCE)
    # ==========================================
    def _save_to_file(self):
        """Tự động lưu thay đổi xuống file để đồng bộ toàn hệ thống"""
        FileHandler.save_data("data/schedules.txt", self.schedules,
            lambda s: f"{s.id}|{s.doctor_id}|{s.date}|{s.time_slot}|{s.is_booked}|{getattr(s, 'day_of_week', '')}|{getattr(s, 'slot_num', '')}")

    # ==========================================
    # CÁC HÀM CRUD CƠ BẢN
    # ==========================================
    def add_schedule(self, schedule: Schedule):
        if not isinstance(schedule, Schedule):
            raise TypeError('Phải nhập một lịch khám')
        if self.find_schedule_by_id(schedule.id):
            raise ValueError('Mã lịch đã tồn tại')
        
        # Đảm bảo kiểm tra trùng lặp thời gian tuyệt đối dựa trên doctor_id, date và time_slot
        if self.is_conflict(schedule):
            raise ValueError('Trùng lịch với ca đã có')
        
        self.schedules.append(schedule)
        self._save_to_file()

    def remove_schedule_by_id(self, schedule_id):
        schedule = self.find_schedule_by_id(schedule_id)
        if not schedule:
            return False

        if schedule.is_booked:
            raise ValueError("Không thể xóa lịch đã có người đặt")

        self.schedules.remove(schedule_id)
        self._save_to_file()
        return True

    def update_schedule(self, schedule_id, **updates):
        schedule = self.find_schedule_by_id(schedule_id)
        if not schedule or not self.can_update_schedule(schedule_id):
            return False
            
        # Cơ chế 'Locking': Khi một khung giờ có is_booked = True, không được phép sửa bất kỳ thuộc tính nào của nó
        if getattr(schedule, 'is_booked', False):
            raise ValueError("Không thể sửa lịch đã được đặt")
            
        for key, value in updates.items():
            if hasattr(schedule, key):
                setattr(schedule, key, value)
                
        self._save_to_file()
        return True

    def find_schedule_by_id(self, schedule_id):
        return self.schedules.find_by_attribute('id', schedule_id)

    # ==========================================
    # QUẢN LÝ TRẠNG THÁI (BOOK / RELEASE)
    # ==========================================
    def book_schedule(self, schedule_id):
        schedule = self.find_schedule_by_id(schedule_id)
        if not schedule or schedule.is_booked:
            return False

        schedule.is_booked = True
        self._save_to_file()
        return True
    
    def book_slot(self, schedule_id):
        """
        Kiểm tra biến is_booked, nếu là False thì mới được gán True và lưu file.
        Nếu là True thì ném ra lỗi ValueError('Lịch này đã có người đặt').
        """
        schedule = self.find_schedule_by_id(schedule_id)
        if not schedule:
            raise ValueError('Không tìm thấy lịch khám tương ứng')

        if getattr(schedule, 'is_booked', False):
            raise ValueError('Lịch này đã có người đặt')

        schedule.is_booked = True
        self._save_to_file()
        return True

    def release_schedule(self, schedule_id):
        schedule = self.find_schedule_by_id(schedule_id)
        if not schedule:
            return False

        schedule.is_booked = False
        self._save_to_file()
        return True

    # ==========================================
    # KIỂM TRA ĐIỀU KIỆN & RÀNG BUỘC
    # ==========================================
    def is_conflict(self, new_schedule: Schedule):
        """Kiểm tra trùng lặp thời gian tuyệt đối dựa trên doctor_id, date và time_slot"""
        for s in self.schedules:
            if (getattr(s, 'doctor_id', None) == getattr(new_schedule, 'doctor_id', None) and
                getattr(s, 'date', None) == getattr(new_schedule, 'date', None) and
                getattr(s, 'time_slot', None) == getattr(new_schedule, 'time_slot', None)):
                return True
        return False

    def can_update_schedule(self, schedule_id):
        schedule = self.find_schedule_by_id(schedule_id)
        if not schedule:
            return False
        from datetime import datetime
        today = datetime.now().date()
        if schedule.date <= today:
            return False
        return True

    # ==========================================
    # CÁC HÀM TÌM KIẾM HỖ TRỢ
    # ==========================================
    def search_available_schedules(self, doctor_id, date=None, weekday=None):
        results = LinkedList()
        for s in self.schedules:
            if getattr(s, 'doctor_id', None) != doctor_id:
                continue
            if date:
                date_obj = self._to_date(date)
                if s.date != date_obj:
                    continue
            if weekday is not None:
                wd = self._weekday_to_int(weekday)
                if s.date.weekday() != wd:
                    continue
            if not s.is_booked:
                results.append(s)
        return results

    def get_schedules_by_day_of_week(self, doctor_id, day_of_week):
        results = LinkedList()
        for s in self.schedules:
            if getattr(s, 'doctor_id', None) == doctor_id and getattr(s, 'day_of_week', None) == day_of_week:
                results.append(s)
        return results

    def get_schedules_by_day_of_week_and_slot(self, doctor_id, day_of_week, slot_num):
        results = LinkedList()
        for s in self.schedules:
            if (getattr(s, 'doctor_id', None) == doctor_id 
                and getattr(s, 'day_of_week', None) == day_of_week 
                and getattr(s, 'slot_num', None) == slot_num):
                results.append(s)
        return results

    def get_schedules_by_slot_number(self, slot_num):
        results = LinkedList()
        for s in self.schedules:
            if getattr(s, 'slot_num', None) == slot_num:
                results.append(s)
        return results

    def get_schedules_within_days(self, days=30):
        """Đã tối ưu lại logic datetime siêu gọn gàng bằng BaseManager"""
        from datetime import datetime, timedelta
        results = LinkedList()
        today = datetime.now().date()
        end_date = today + timedelta(days=days)
        
        for s in self.schedules:
            schedule_date = self._to_date(getattr(s, 'date', None))
            if today <= schedule_date <= end_date:
                results.append(s)
        return results