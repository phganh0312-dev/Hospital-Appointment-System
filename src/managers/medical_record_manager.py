from structures.linked_list import LinkedList
from entities.medical_record import MedicalRecord
from managers.file_handler import FileHandler

class MedicalRecordManager:
    def __init__(self, medical_records=None, appointment_manager=None, schedule_manager=None):
        self.medical_records = medical_records or LinkedList()
        self.appointment_manager = appointment_manager
        self.schedule_manager = schedule_manager # Cần để check bác sĩ phụ trách

    def _save_to_file(self):
        """Lưu bệnh án xuống file để đồng bộ"""
        FileHandler.save_data("data/records.txt", self.medical_records,
            lambda r: f"{r.id}|{r.appointment_id}|{r.symptoms}|{r.diagnosis}|{r.prescription}")

    def add_medical_record(self, record: MedicalRecord, doctor_id):
        """Chỉ bác sĩ phụ trách mới được thêm bệnh án"""
        if not isinstance(record, MedicalRecord):
            raise TypeError('Phải nhập một hồ sơ bệnh án')
        
        # 1. Kiểm tra cuộc hẹn tồn tại và trạng thái
        appointment = self.appointment_manager.find_appointment_by_id(record.appointment_id)
        if not appointment:
            raise ValueError('Cuộc hẹn không tồn tại')
        
        # 2. Phân quyền: Kiểm tra bác sĩ có đúng là người phụ trách lịch khám này không
        schedule = self.schedule_manager.find_schedule_by_id(appointment.schedule_id)
        if not schedule or schedule.doctor_id != doctor_id:
            raise PermissionError("Bác sĩ không có quyền tạo bệnh án cho cuộc khám này.")
            
        if appointment.status != "Đã khám":
            raise ValueError("Chỉ tạo bệnh án sau khi hoàn thành khám.")
            
        if self.find_by_appointment_id(record.appointment_id):
            raise ValueError("Appointment đã có bệnh án, hãy sử dụng tính năng sửa.")

        self.medical_records.append(record)
        self._save_to_file()
        return True

    def update_medical_record(self, record_id, symptoms, diagnosis, prescription, doctor_id):
        """Chỉ bác sĩ phụ trách mới được sửa bệnh án"""
        record = self.find_medical_record_by_id(record_id)
        if not record:
            return False
            
        # Kiểm tra quyền: lấy appointment -> lấy schedule -> check doctor_id
        appointment = self.appointment_manager.find_appointment_by_id(record.appointment_id)
        schedule = self.schedule_manager.find_schedule_by_id(appointment.schedule_id)
        
        if schedule.doctor_id != doctor_id:
            raise PermissionError("Bác sĩ không có quyền chỉnh sửa bệnh án này.")

        record.symptoms = symptoms
        record.diagnosis = diagnosis
        record.prescription = prescription
        
        self._save_to_file()
        return True

    def remove_medical_record_by_id(self, record_id, doctor_id):
        """Quyền xóa chỉ dành cho Admin (hoặc bác sĩ chủ quản nếu cần)"""
        # Logic hiện tại: Chỉ cho phép xóa nếu đúng bác sĩ chủ quản
        record = self.find_medical_record_by_id(record_id)
        if not record:
            return False
            
        appointment = self.appointment_manager.find_appointment_by_id(record.appointment_id)
        schedule = self.schedule_manager.find_schedule_by_id(appointment.schedule_id)
        
        if schedule.doctor_id != doctor_id:
            raise PermissionError("Không có quyền xóa bệnh án này.")
            
        self.medical_records.remove(record_id)
        self._save_to_file()
        return True

    def find_medical_record_by_id(self, record_id):
        return self.medical_records.find_by_attribute('id', record_id)

    def find_by_appointment_id(self, appointment_id):
        return self.medical_records.find_by_attribute('appointment_id', appointment_id)

    def find_medical_records_by_patient_id(self, patient_id):
        results = LinkedList()
        for r in self.medical_records:
            appointment_id = getattr(r, 'appointment_id', None)
            if appointment_id:
                appointment = self.appointment_manager.find_appointment_by_id(appointment_id)
                if appointment and getattr(appointment, 'patient_id', None) == patient_id:
                    results.append(r)
        return results

    def auto_generate_record(self, appointment_id):
        """Tự động sinh bệnh án trống cho một lịch hẹn nếu chưa tồn tại"""
        # 1. Kiểm tra chống trùng lặp
        if self.find_by_appointment_id(appointment_id):
            return False
            
        # 2. Sinh ID tự động (Lấy max ID hiện tại + 1, định dạng R + 8 chữ số)
        max_id = 0
        for r in self.medical_records:
            try:
                num = int(getattr(r, 'id', 'R00000000')[1:])
                max_id = max(max_id, num)
            except (ValueError, TypeError):
                continue
                
        new_record_id = f"R{str(max_id + 1).zfill(8)}"
        
        # 3. Khởi tạo đối tượng MedicalRecord với các trường trống
        new_record = MedicalRecord(
            record_id=new_record_id, 
            appointment_id=appointment_id, 
            symptoms="", 
            diagnosis="", 
            prescription=""
        )
        
        # 4. Thêm vào LinkedList và lưu đồng bộ xuống file
        self.medical_records.append(new_record)
        self._save_to_file()
        
        return new_record