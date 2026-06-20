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
# 2. CLASS GIẢ LẬP SIÊU CẤP (Bao trọn mọi tên ID)
# =================================================================
class MockAppointment:
    def __init__(self, target_id):
        # Gán tất cả các trường hợp tên gọi ID phổ biến để chắc chắn vượt qua 
        # được vòng kiểm tra của hàm find_appointment_by_id
        self.id = target_id
        self.appointment_id = target_id
        self.app_id = target_id
        self.key = target_id 

# =================================================================
# 3. HÀM BENCHMARK TÌM KIẾM BẰNG LINKED LIST (O(N))
# =================================================================
def benchmark_appointment_linked_list():
    file_path = os.path.join(project_root, "datatest", "appointmentstest.txt")
    
    if not os.path.exists(file_path):
        print(f"❌ Không tìm thấy file dữ liệu tại: {file_path}")
        return

    print(f"📊 Đang tải dữ liệu từ file để kiểm thử Linked List O(N)...")
    raw_data_list = FileHandler.load_data(file_path)
    
    scales = [100, 1000, 10000]
    
    print(f"\n📊 KẾT QUẢ TÌM KIẾM BẰNG LINKED LIST (O(N))")
    print("=" * 80)
    print(f"{'Số lượng (N)':<15} | {'Mã Cuộc Hẹn':<15} | {'Thời gian chạy (giây)':<25} | {'Trạng thái':<15}")
    print("-" * 80)
    
    for n in scales:
        # Khởi tạo manager an toàn (Không truyền argument trực tiếp vào __init__)
        manager = AppointmentManager()
        # Ghi đè LinkedList rỗng vào sau khi khởi tạo
        manager.appointments = LinkedList()
        manager._save_to_file = lambda: None  
        
        current = raw_data_list.head
        count = 0
        target_id = None
        
        # Nạp dữ liệu vào Linked List
        while current and count < n:
            row = current.value 
            if len(row) >= 4: 
                target_id_val = row[0]
                # Truyền ID vào class giả lập
                app = MockAppointment(target_id_val)
                
                # Thêm vào LinkedList
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
        
        # Gọi hàm tìm kiếm
        result = manager.find_appointment_by_id(target_id)
        
        end_time = time.perf_counter()
        # -------------------------------------------------------------
        
        elapsed_time = end_time - start_time
        status = "Tìm thấy" if result else "Không thấy"
        
        print(f"{n:<15} | {target_id:<15} | {elapsed_time:.8f} s | {status:<15}")
        
    print("=" * 80)

if __name__ == "__main__":
    benchmark_appointment_linked_list()