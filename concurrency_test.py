import os
import sys
import threading

# =================================================================
# 1. CẤU HÌNH ĐƯỜNG DẪN 
# =================================================================
current_dir = os.path.dirname(os.path.abspath(__file__)) 
project_root = os.path.dirname(current_dir)              

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from managers.appointment_manager import AppointmentManager
from structures.linked_list import LinkedList

# =================================================================
# 2. KHỞI TẠO BIẾN CHO BÀI TEST
# =================================================================
# Khởi tạo Manager của bạn
appointment_manager = AppointmentManager()
appointment_manager.appointments = LinkedList()

# Chặn tạm hàm ghi file để tránh lỗi khi nhiều luồng cùng gọi đến
appointment_manager._save_to_file = lambda: None 

# Tạo một cuộc hẹn giả lập để 100 luồng cùng tranh nhau nạp vào
class DummyAppointment:
    def __init__(self):
        self.id = "A_TEST_RACE_001"
        self.schedule_id = "S_TEST_001"
        self.status = "PENDING"

appointment = DummyAppointment()

# =================================================================
# 3. ĐOẠN CODE KIỂM THỬ ĐỒNG THỜI (100 LUỒNG CÙNG BOOK CUỘC HẸN)
# =================================================================
success = 0

def booking():
    global success

    try:
        appointment_manager.add_appointment(appointment)
        success += 1
    except:
        pass

threads = []

for i in range(100):
    t = threading.Thread(target=booking)
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Success:", success)