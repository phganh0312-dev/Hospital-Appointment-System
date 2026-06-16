import datetime
from structures.linked_list import LinkedList
from entities.doctor import Doctor
from entities.doctor_schedule import Schedule
from entities.medical_record import MedicalRecord
from entities.patient import Patient
from entities.appointment import Appointment

class HospitalManager:
    def __init__(self):
        self.doctors = LinkedList()
        self.schedules = LinkedList()
        self.medical_records = LinkedList()
        self.patients = LinkedList()
        self.appointments = LinkedList()

    # Chức năng quản lý bác sĩ
    def add_doctor(self, doctor: Doctor):
        if not isinstance(doctor, Doctor):
            raise TypeError('Phải nhập một bác sĩ')
        if self.find_doctor_by_id(doctor.id):
            raise ValueError('Mã bác sĩ đã tồn tại')
        self.doctors.append(doctor)

    def remove_doctor_by_id(self, doctor_id):
        self.doctors.remove(doctor_id)

    def find_doctor_by_id(self, doctor_id):
        return self.doctors.find_by_attribute('id', doctor_id)

    def find_doctor_by_name(self, name):
        return self.doctors.find_by_attribute('name', name)

    # Chức năng quản lý lịch khám
    def add_schedule(self, schedule: Schedule):
        if not isinstance(schedule, Schedule):
            raise TypeError('Phải nhập một lịch khám')
        if self.find_schedule_by_id(schedule.id):
            raise ValueError('Mã lịch đã tồn tại')
        if self.is_conflict(schedule):
            raise ValueError('Trùng lịch với ca đã có')
        self.schedules.append(schedule)

    def remove_schedule_by_id(self, schedule_id):
        self.schedules.remove(schedule_id)

    def find_schedule_by_id(self, schedule_id):
        return self.schedules.find_by_attribute('id', schedule_id)

    def is_conflict(self, new_schedule: Schedule): # Kiểm tra nếu new_schedule có trùng lịch với bất kỳ ca nào đã tồn tại của cùng bác sĩ (cùng doctor_id, date và time_slot)
        for s in self.schedules:
            if getattr(s, 'doctor_id', None) == new_schedule.doctor_id:
                if s.date == new_schedule.date and s.time_slot == new_schedule.time_slot:
                    return True
        return False

    # Chức năng quản lý bệnh nhân
    def add_patient(self, patient: Patient):
        if not isinstance(patient, Patient):
            raise TypeError('Phải nhập một bệnh nhân')
        if self.find_patient_by_id(patient.id):
            raise ValueError('Mã bệnh nhân đã tồn tại')
        self.patients.append(patient)

    def find_patient_by_id(self, patient_id):
        return self.patients.find_by_attribute('id', patient_id)
    
    def remove_patient_by_id(self, patient_id):
        self.patients.remove(patient_id)

    # Chưc năng quản lý cuộc hẹn
    def add_appointment(self, appointment: Appointment):
        if not isinstance(appointment, Appointment):
            raise TypeError('Phải nhập một cuộc hẹn')
        if self.find_appointment_by_id(appointment.id):
            raise ValueError('Mã cuộc hẹn đã tồn tại')
        # Kiểm tra nếu schedule_id của appointment có tồn tại trong schedules
        schedule = self.find_schedule_by_id(getattr(appointment, 'schedule_id', None))
        if not schedule:
            raise ValueError('Cuộc hẹn không tồn tại')
        self.appointments.append(appointment)
    
    def find_appointment_by_id(self, appointment_id):
        return self.appointments.find_by_attribute('id', appointment_id)
    
    def remove_appointment_by_id(self, appointment_id):
        self.appointments.remove(appointment_id)

    # Chức năng quản lý hồ sơ bệnh án
    def add_medical_record(self, record: MedicalRecord):
        if not isinstance(record, MedicalRecord):
            raise TypeError('Phải nhập một hồ sơ bệnh án')
        if self.find_medical_record_by_id(record.id):
            raise ValueError('Mã hồ sơ đã tồn tại')
        # Kiểm tra nếu appointment_id của record có tồn tại trong appointments
        appointment = self.find_appointment_by_id(getattr(record, 'appointment_id', None))
        if not appointment:
            raise ValueError('Hồ sơ bệnh án không tồn tại')
        self.medical_records.append(record)

    def find_medical_record_by_id(self, record_id):
        return self.medical_records.find_by_attribute('id', record_id)       
    
    def find_medical_records_by_patient_id(self, patient_id):
        results = LinkedList()
        for r in self.medical_records:
            appointment_id = getattr(r, 'appointment_id', None)
            if appointment_id is not None:
                appointment = self.find_appointment_by_id(appointment_id)
                if appointment and getattr(appointment, 'patient_id', None) == patient_id:
                    results.append(r)
        return results

    # Chức năng tìm kiếm bác sĩ theo chuyên khoa, ngày cụ thể, hoặc lịch cố định theo tuần (weekday)
    def search_doctors(self, specialty=None, date=None, weekday=None):
        results = LinkedList()
        for d in self.doctors:
            ok = True # Biến cờ để kiểm tra 
            if specialty:
                if (d.specialty or '').strip().lower() != str(specialty).strip().lower():
                    ok = False
            if ok and date:
                date_obj = self._to_date(date)
                # doctor phải có ít nhất một schedule tại date_obj
                has = any((s for s in self.schedules if getattr(s, 'doctor_id', None) == d.id and s.date == date_obj))
                if not has:
                    ok = False
            if ok and weekday is not None:
                wd = self._weekday_to_int(weekday)
                has = any((s for s in self.schedules if getattr(s, 'doctor_id', None) == d.id and s.date.weekday() == wd))
                if not has:
                    ok = False
            if ok:
                results.append(d)
        return results
    
    # Chức năng tìm kiếm lịch khám trống của bác sĩ theo ngày cụ thể hoặc lịch cố định theo tuần (weekday)
    def search_available_schedules(self, doctor_id, date=None, weekday=None):
        results = LinkedList()
        
        for s in self.schedules:
            # Lọc theo mã bác sĩ
            if getattr(s, 'doctor_id', None) != doctor_id:
                continue
                
            # Lọc theo ngày cụ thể (nếu có)
            if date:
                date_obj = self._to_date(date)
                if s.date != date_obj:
                    continue
                    
            # Lọc theo thứ trong tuần (nếu có)
            if weekday is not None:
                wd = self._weekday_to_int(weekday)
                if s.date.weekday() != wd:
                    continue
            # Kiểm tra xem lịch này đã bị đặt hay chưa
            if not s.is_booked:
                results.append(s)
                
        return results

    # Chức năng tính giá khám bệnh dựa trên bác sĩ và có áp dụng BHYT hay không
    def calculate_price(self, doctor: Doctor, has_bhyt=False, coverage=0.8):
        price = getattr(doctor, 'base_price', 0) or 0
        if has_bhyt:
            covered = int(price * coverage)
            return max(0, price - covered)
        return price

    # Chức năng tính doanh thu của bác sĩ dựa trên các cuộc hẹn đã đặt, đã khám hoặc đã hoàn thành
    def calculate_doctor_revenue(self, doctor: Doctor): 
        if not isinstance(doctor, Doctor):
            raise TypeError('Phải nhập một bác sĩ')

        revenue = 0
        for appointment in self.appointments:
            schedule_id = getattr(appointment, 'schedule_id', None)
            if schedule_id is None:
                continue

            schedule = self.find_schedule_by_id(schedule_id)
            if not schedule:
                continue

            if getattr(schedule, 'doctor_id', None) != doctor.id:
                continue

            status = getattr(appointment, 'status', '').strip().lower()
            if status == 'đã đặt' or status == 'đã khám' or status == 'đã hoàn thành':
                revenue += getattr(doctor, 'base_price', 0) or 0

        return revenue

    # Chức năng sắp xếp doanh thu bác sĩ bằng bubble sort trực tiếp trên LinkedList
    def sort_doctors_by_revenue_bubble_sort(self, ascending=True):
        # Đếm số lượng nút trong LinkedList
        n = 0
        current = self.doctors.head
        while current:
            n += 1
            current = current.next
        
        # Bubble sort algorithm áp dụng trực tiếp trên LinkedList
        for i in range(n):
            swapped = False  # Cờ để kiểm tra nếu có hoán đổi trong vòng lặp
            current = self.doctors.head
            
            # Duyệt qua các nút liền kề và so sánh
            for j in range(n - i - 1):
                if not current or not current.next:
                    break
                
                # Lấy doanh thu của hai bác sĩ trong hai nút liền kề
                revenue_current = self.calculate_doctor_revenue(current.value)
                revenue_next = self.calculate_doctor_revenue(current.next.value)
                
                # So sánh và hoán đổi giá trị nếu cần
                should_swap = False
                if ascending:
                    # Sắp xếp tăng dần: nếu nút hiện tại có doanh thu lớn hơn nút tiếp theo
                    should_swap = revenue_current > revenue_next
                else:
                    # Sắp xếp giảm dần: nếu nút hiện tại có doanh thu nhỏ hơn nút tiếp theo
                    should_swap = revenue_current < revenue_next
                
                if should_swap:
                    # Hoán đổi giá trị giữa hai nút
                    current.value, current.next.value = current.next.value, current.value
                    swapped = True
                
                current = current.next
            
            # Nếu không có hoán đổi nào, danh sách đã được sắp xếp
            if not swapped:
                break
        
        return self.doctors
    
    # Chức năng sắp xếp số ca hẹn của bác sĩ bằng bubble sort trực tiếp trên LinkedList
    def sort_doctors_by_appointments_bubble_sort(self, ascending=True):
        # Đếm số lượng nút trong LinkedList
        n = 0
        current = self.doctors.head
        while current:
            n += 1
            current = current.next
        
        # Bubble sort algorithm áp dụng trực tiếp trên LinkedList
        for i in range(n):
            swapped = False  # Cờ để kiểm tra nếu có hoán đổi trong vòng lặp
            current = self.doctors.head
            
            # Duyệt qua các nút liền kề và so sánh
            for j in range(n - i - 1):
                if not current or not current.next:
                    break
                
                # Lấy số lượng cuộc hẹn của hai bác sĩ trong hai nút liền kề
                count_current = self.count_appointments_by_doctor(current.value)
                count_next = self.count_appointments_by_doctor(current.next.value)
                
                # So sánh và hoán đổi giá trị nếu cần
                should_swap = False
                if ascending:
                    # Sắp xếp tăng dần: nếu nút hiện tại có số lượng cuộc hẹn lớn hơn nút tiếp theo
                    should_swap = count_current > count_next
                else:
                    # Sắp xếp giảm dần: nếu nút hiện tại có số lượng cuộc hẹn nhỏ hơn nút tiếp theo
                    should_swap = count_current < count_next
                
                if should_swap:
                    # Hoán đổi giá trị giữa hai nút
                    current.value, current.next.value = current.next.value, current.value
                    swapped = True
                
                current = current.next
            
            # Nếu không có hoán đổi nào, danh sách đã được sắp xếp
            if not swapped:
                break
        
        return self.doctors

    # Chức năng thống kê số lượng cuộc hẹn theo ngày cụ thể
    def count_appointments_by_date(self, date):
        date_obj = self._to_date(date)
        count = 0
        for appointment in self.appointments:
            schedule_id = getattr(appointment, 'schedule_id', None)
            if schedule_id is None:
                continue
            schedule = self.find_schedule_by_id(schedule_id)
            if schedule and getattr(schedule, 'date', None) == date_obj:
                count += 1
        return count
    
    # Chức năng thống kê số lượng cuộc hẹn theo bác sĩ cụ thể
    def count_appointments_by_doctor(self, doctor: Doctor):
        if not isinstance(doctor, Doctor):
            raise TypeError('Phải nhập một bác sĩ')
        count = 0
        for appointment in self.appointments:
            schedule_id = getattr(appointment, 'schedule_id', None)
            if schedule_id is None:
                continue
            schedule = self.find_schedule_by_id(schedule_id)
            if schedule and getattr(schedule, 'doctor_id', None) == doctor.id:
                count += 1
        return count

    # Hàm phụ trợ để chuyển đổi ngày và weekday
    def _to_date(self, date_input):
        if isinstance(date_input, datetime.datetime): # Nếu là datetime, chỉ lấy phần date
            return date_input.date()
        if isinstance(date_input, datetime.date): # Nếu đã là date, trả về trực tiếp
            return date_input
        if isinstance(date_input, str): # Nếu là chuỗi, cố gắng chuyển đổi từ định dạng ISO (YYYY-MM-DD)
            return datetime.date.fromisoformat(date_input)
        raise ValueError('Invalid date')

    def _weekday_to_int(self, weekday):
        if isinstance(weekday, int): # Nếu đã là số nguyên, trả về trực tiếp (0-6)
            return weekday
        w = str(weekday).strip().lower() # Chuyển sang chữ thường và loại bỏ khoảng trắng
        mapping_vi = {'thứ hai': 0, 'thứ ba': 1, 'thứ tư': 2, 'thứ năm': 3, 'thứ sáu': 4, 'thứ bảy': 5, 'chủ nhật': 6} 
        if w in mapping_vi: # Nếu là tên ngày trong tuần bằng tiếng Việt, trả về số nguyên tương ứng
            return mapping_vi[w]
        try:
            return int(w) # Nếu là số nguyên, trả về trực tiếp (0-6)
        except Exception:
            raise ValueError('Ngày không hợp lệ.') 
