from ui.menu_utils import print_header, print_divider, get_input
from ui.admin_ui import admin_menu
from ui.patient_ui import patient_menu
from ui.doctor_ui import doctor_menu

def main_menu(managers):
    user_manager = managers["user"]
    
    while True:
        print_header("HỆ THỐNG BỆNH VIỆN ĐA KHOA MẶT TRỜI NHỎ")
        print("1. Dang nhap")
        print("2. Dang ky tai khoan benh nhan")
        print("0. Thoat chuong trinh")
        print_divider()
        
        choice = get_input("Nhap lua chon cua ban (0-2): ")
        
        if choice == "1":
            print_header("MAN HINH DANG NHAP")
            username = get_input("Nhap SDT hoac Email: ")
            password = get_input("Nhap mat khau: ")
            
            try:
                status, result = user_manager.authenticate(username, password)

                if status:
                    user = result
                    role = user.role

                    print(f"Dang nhap thanh cong! Quyen truy cap: {role}")

                    if role == "admin":
                        admin_menu(managers, user)
                    elif role == "doctor":
                        doctor_menu(managers, user)
                    elif role == "patient":
                        patient_menu(managers, user)
                    else:
                        print("Loi: Vai tro tai khoan khong hop le.")
                else:
                    print(result)
            except Exception as e:
                print(f"Loi xac thuc: {str(e)}")
                
        elif choice == "2":
            print_header("DANG KY TAI KHOAN BENH NHAN")
            phone = get_input("Nhap so dien thoai: ")
            email = get_input("Nhap email: ")
            cccd = get_input("Nhap so CCCD: ")
            full_name = get_input("Nhap ho ten day du: ")
            province = get_input("Nhap Tinh / Thanh pho: ")
            ward = get_input("Nhap Quan / Huyen / Phuong: ")
            detailed_address = get_input("Nhap dia chi nha chi tiet: ")
            password = get_input("Nhap mat khau: ")
            confirm_password = get_input("Nhap lai mat khau xac nhan: ")
            
            try:
                status, message = user_manager.register_patient(
                    phone=phone,
                    email=email,
                    cccd=cccd,
                    full_name=full_name,
                    province=province,
                    ward=ward,
                    detailed_address=detailed_address,
                    password=password,
                    confirm_password=confirm_password
                )

                print(message)
            except Exception as e:
                print(f"Dang ky that bai: {str(e)}")
                
        elif choice == "0":
            print("Dang tien hanh ghi du lieu va dong toan bo he thong...")
            for key in managers:
                m = managers[key]
                if hasattr(m, "_save_to_file"):
                    m._save_to_file()
            print("Du lieu da duoc dong bo an toan. Tam biet!")
            break
        else:
            print("Lua chon khong dung. Vui long kiem tra lai.")