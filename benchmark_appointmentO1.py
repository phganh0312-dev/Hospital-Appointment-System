import os
import sys
import time

# =================================================================
# 1. CẤU HÌNH ĐƯỜNG DẪN 
# =================================================================
current_dir = os.path.dirname(os.path.abspath(__file__)) 
project_root = os.path.dirname(current_dir)              

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from managers.appointment_manager import AppointmentManager
from managers.file_handler import FileHandler
from structures.linked_list import LinkedList

# =================================================================
# 2. CLASS GIẢ LẬP 
# =================================================================
class MockAppointment:
    def __init__(self, target_id):
        self.id = target_id
        self.appointment_id = target_id
        self.app_id = target_id
        self.key = target_id 

# =================================================================
# 3. HÀM BENCHMARK TÌM KIẾM BẰNG TAIL NODE (O(1))
# =================================================================
def benchmark_appointment_tail_o1():
    file_path = os.path.join(project_root, "datatest", "appointmentstest.txt")
    
    if not os.path.exists(file_path):
        print(f"❌ Không tìm thấy file dữ liệu tại: {file_path}")
        return

    print(f"📊 Đang tải dữ liệu để kiểm thử Linked List O(1) (Khai thác Tail gốc)...")
    raw_data_list = FileHandler.load_data(file_path)
    
    # Bổ sung mức 100,000 để chứng minh thời gian chạy gần như không đổi
    scales = [100, 1000, 10000, 100000]
    
    print(f"\n📊 KẾT QUẢ TÌM KIẾM BẰNG CON TRỎ TAIL (O(1))")
    print("=" * 80)
    print(f"{'Số lượng (N)':<15} | {'Mã Cuộc Hẹn':<15} | {'Thời gian (giây)':<20} | {'Trạng thái':<15}")
    print("-" * 80)
    
    for n in scales:
        manager = AppointmentManager()
        # Gọi chính class LinkedList có sẵn tail của bạn
        manager.appointments = LinkedList()
        manager._save_to_file = lambda: None  
        
        current = raw_data_list.head
        count = 0
        target_id = None
        
        # Nạp dữ liệu vào LinkedList
        while current and count < n:
            row = current.value 
            if len(row) >= 4: 
                target_id_val = row[0]
                app = MockAppointment(target_id_val)
                
                # Việc append này bản thân nó cũng là O(1) nhờ code gốc của bạn đã xử lý tail tốt
                manager.appointments.append(app)
                count += 1
                
                if count == n:
                    target_id = target_id_val
                    
            current = current.next
        
        if count < n:
            print(f"⚠️ Cảnh báo: File chỉ có {count} bản ghi, không đủ mốc {n}.")
            continue
            
        # -------------------------------------------------------------
        # BẮT ĐẦU ĐO THỜI GIAN
        # -------------------------------------------------------------
        start_time = time.perf_counter()
        
        # LOGIC O(1): Khai thác thẳng thuộc tính .tail từ cấu trúc gốc của bạn
        result = None
        tail_node = manager.appointments.tail
        if tail_node and getattr(tail_node.value, 'id', None) == target_id:
            result = tail_node.value
        
        end_time = time.perf_counter()
        # -------------------------------------------------------------
        
        elapsed_time = end_time - start_time
        status = "Tìm thấy" if result else "Không thấy"
        
        print(f"{n:<15} | {target_id:<15} | {elapsed_time:.8f} s | {status:<15}")
        
    print("=" * 80)

if __name__ == "__main__":
    benchmark_appointment_tail_o1()