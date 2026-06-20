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

from entities.patient import Patient
from managers.patient_manager import PatientManager
from managers.file_handler import FileHandler
from structures.hash_table import HashTable


# =================================================================
# 2. HÀM BENCHMARK TÌM KIẾM BẰNG HASH TABLE
# =================================================================
def benchmark_searchpatient():
    file_path = os.path.join(project_root, "datatest", "patientstest.txt")
    
    if not os.path.exists(file_path):
        print(f"❌ Không tìm thấy file dữ liệu tại: {file_path}")
        return

    print(f"📊 Đang tải dữ liệu từ file để kiểm thử Hash Table...")
    raw_data_list = FileHandler.load_data(file_path)
    
    scales = [100, 1000, 10000]
    
    print(f"\n📊 KẾT QUẢ TÌM KIẾM BẰNG BẢNG BĂM (HASH TABLE - O(1))")
    print("=" * 80)
    print(f"{'Số lượng (N)':<15} | {'SĐT tìm kiếm':<15} | {'Thời gian chạy (giây)':<25} | {'Trạng thái':<15}")
    print("-" * 80)
    
    for n in scales:
        manager = PatientManager(patients=HashTable())
        manager._save_to_file = lambda: None  
        
        current = raw_data_list.head
        count = 0
        target_phone = None
        
        # Nạp dữ liệu vào Hash Table
        while current and count < n:
            row = current.value 
            if len(row) >= 8: 
                p = Patient(
                    patient_id=row[0],
                    cccd=row[1],
                    full_name=row[2],
                    phone=row[3],
                    email=row[4],
                    province=row[5],
                    ward=row[6],
                    detailed_address=row[7],
                    bhyt_code=row[8] if len(row) > 8 else None,
                    bhyt_expiry=row[9] if len(row) > 9 else None
                )
                
                # Hàm set của Hash Table
                manager.patients.set(p.phone, p)
                count += 1
                
                # Lưu lại số điện thoại của người cuối cùng để mang đi test
                if count == n:
                    target_phone = p.phone
                    
            current = current.next
        
        if count < n:
            print(f"⚠️ Cảnh báo: File chỉ có {count} bản ghi, không đủ mốc {n}.")
            continue
            
        # -------------------------------------------------------------
        # BẮT ĐẦU ĐO THỜI GIAN TÌM KIẾM BẰNG HASH TABLE
        # -------------------------------------------------------------
        start_time = time.perf_counter()
        
        # Sử dụng hàm get() của Hash Table với key là số điện thoại
        result = manager.patients.get(target_phone)
        
        end_time = time.perf_counter()
        # -------------------------------------------------------------
        
        elapsed_time = end_time - start_time
        status = "Tìm thấy" if result else "Không thấy"
        
        print(f"{n:<15} | {target_phone:<15} | {elapsed_time:.8f} s | {status:<15}")
        
    print("=" * 80)

if __name__ == "__main__":
    benchmark_searchpatient()