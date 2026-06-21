import threading
from structures.linked_list import LinkedList
from structures.hash_table import HashTable
from managers.file_handler import FileHandler
from managers.base_manager import (
    BaseManager, ValidationError, DataConsistencyError, AppointmentStatus
)

class Transaction:
    def __init__(self, operation_type, target_manager, details):
        self.id = f"TXN_{int(__import__('datetime').datetime.now().timestamp() * 1000)}"
        self.operation_type = operation_type  
        self.target_manager = target_manager
        self.details = details
        self.status = "PENDING"  
        self.created_at = __import__('datetime').datetime.now()
        
        self.snapshots = HashTable() 
    
class AppointmentManager(BaseManager):
    def __init__(self, appointments=None, schedule_manager=None, doctor_manager=None, user_manager=None):
        super().__init__()
        self.appointments = appointments or LinkedList()
        self.schedule_manager = schedule_manager
        self.doctor_manager = doctor_manager
        self.user_manager = user_manager
        self.patient_manager = user_manager.patient_manager if user_manager else None
        
        self.transactions = LinkedList()
        
        self.lock = threading.Lock()
 
    def _save_to_file(self):
        try:
            FileHandler.save_data(
                "data/appointments.txt",
                self.appointments,
                lambda a: f"{a.id}|{a.patient_id}|{a.schedule_id}|{a.status}|{getattr(a, 'payment_status', '')}"
            )
        except Exception as e:
            print(f"Lỗi đồng bộ file appointments.txt: {e}")
 
    def find_appointment_by_id(self, app_id):
        current = self.appointments.head
        while current:
            if getattr(current.value, 'id', None) == app_id:
                return current.value
            current = current.next
        return None
 
    def add_appointment(self, appointment):
        with self.lock:
            if self.find_appointment_by_id(appointment.id):
                raise ValidationError("Mã cuộc hẹn đã tồn tại trên hệ thống.")
            
            if self.schedule_manager:
                sched = self.schedule_manager.find_schedule_by_id(appointment.schedule_id)
                if not sched:
                    raise ValidationError("Lịch khám của bác sĩ không tồn tại.")
                if getattr(sched, 'is_booked', False):
                    raise ValidationError("Lịch khám này đã có bệnh nhân khác đặt trước.")
                
                txn = Transaction("CREATE_APPOINTMENT", self, appointment.id)
                txn.snapshots.set("schedule_booked_status", getattr(sched, 'is_booked', False))
                self.transactions.append(txn)
                
                try:
                    setattr(sched, 'is_booked', True)
                    self.schedule_manager._save_to_file()
                    
                    appointment.status = AppointmentStatus.PENDING
                    self.appointments.append(appointment)
                    self._save_to_file()
                    
                    txn.status = "COMMITTED"
                except Exception as e:
                    txn.status = "FAILED"
                    status_backup = txn.snapshots.get("schedule_booked_status", False)
                    setattr(sched, 'is_booked', status_backup)
                    self.schedule_manager._save_to_file()
                    raise DataConsistencyError(f"Gặp sự cố hệ thống khi lưu lịch hẹn. Đã rollback dữ liệu gốc: {e}")
            else:
                self.appointments.append(appointment)
                self._save_to_file()
 
    def cancel_appointment(self, app_id):
        with self.lock:
            app = self.find_appointment_by_id(app_id)
            if not app:
                raise ValidationError("Cuộc hẹn không tồn tại để hủy.")
            
            current_status = AppointmentStatus.normalize(getattr(app, 'status', ''))
            if current_status == AppointmentStatus.CANCELLED:
                raise ValidationError("Cuộc hẹn này đã được thực hiện hủy từ trước.")
            if current_status == AppointmentStatus.COMPLETED:
                raise ValidationError("Không thể hủy lịch đã khám xong")
            
            txn = Transaction("CANCEL_APPOINTMENT", self, app_id)
            txn.snapshots.set("appointment_old_status", getattr(app, 'status', ''))
            
            sched = None
            if self.schedule_manager:
                sched = self.schedule_manager.find_schedule_by_id(app.schedule_id)
                if sched:
                    txn.snapshots.set("schedule_booked_status", getattr(sched, 'is_booked', True))
            
            self.transactions.append(txn)
            
            try:
                app.status = AppointmentStatus.CANCELLED
                if self.schedule_manager and sched:
                    setattr(sched, 'is_booked', False)
                    self.schedule_manager._save_to_file()
                
                self._save_to_file()
                txn.status = "COMMITTED"
                return True
            except Exception as e:
                txn.status = "FAILED"
                app.status = txn.snapshots.get("appointment_old_status")
                if self.schedule_manager and sched:
                    status_backup = txn.snapshots.get("schedule_booked_status", True)
                    setattr(sched, 'is_booked', status_backup)
                    self.schedule_manager._save_to_file()
                self._save_to_file()
                raise DataConsistencyError(f"Không thể hủy cuộc hẹn do lỗi đồng bộ file. Đã hồi phục trạng thái: {e}")
 
    def get_available_schedules_by_date(self, date_input):
        results = LinkedList()
        if not self.schedule_manager:
            return results
        
        target_date = self.schedule_manager._to_date(date_input)
        current = self.schedule_manager.schedules.head
        while current:
            s = current.value
            if (self.schedule_manager._to_date(getattr(s, 'date', None)) == target_date 
                and not getattr(s, 'is_booked', False)):
                results.append(s)
            current = current.next
        return results
 
    def search_doctors_for_booking(self, name=None, specialty=None, gender=None):
        results = LinkedList()
        if not self.doctor_manager:
            return results
 
        base_results = self.doctor_manager.search_doctors(specialty=specialty)
        
        current = base_results.head
        while current:
            doc = current.value
            match = True
          
            if name:
                name_lower = self._to_lower(name)
                doc_name_lower = self._to_lower(getattr(doc, 'name', ''))
                if not self._custom_find_substring(doc_name_lower, name_lower):
                    match = False
                    
            if match and gender:
                gender_param = self._to_lower(str(gender).strip())
                doc_gender = self._to_lower(str(getattr(doc, 'gender', '')).strip())
                if gender_param != doc_gender:
                    match = False
                    
            if match:
                results.append(doc)
                
            current = current.next
        return results
 
    def get_schedules_by_doctor_flow(self, doctor_id):
        results = LinkedList()
        if not self.schedule_manager:
            return results
 
        current = self.schedule_manager.schedules.head
        while current:
            s = current.value
            if getattr(s, 'doctor_id', None) == doctor_id and not getattr(s, 'is_booked', False):
                results.append(s)
            current = current.next
        return results
