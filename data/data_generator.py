import random
import datetime
import os

# Cấu hình dữ liệu
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Dữ liệu mẫu
SURNAMES_VN = ['Nguyễn', 'Trần', 'Phạm', 'Hoàng', 'Phan', 'Vũ', 'Đặng', 'Bùi', 'Đinh', 'Dương', 'Lê', 'Đỗ', 'Hồ', 'Tạ', 'Tô']
MIDDLE_NAMES_VN = ['Thị', 'Văn', 'Đình', 'Quốc', 'Anh', 'Hữu', 'Minh', 'Thanh', 'Khánh', 'Phương', 'Hằng', 'Linh', 'Trang', 'Hương', 'Lan', 'Hà', 'Hiền', 'Uyên', 'Yến', 'Vân']
LAST_NAMES_VN = ['Anh', 'An', 'Bách', 'Bảo', 'Châu', 'Chiến', 'Cảnh', 'Danh', 'Dân', 'Đạo', 'Định', 'Đạt', 'Đức', 'Đông', 'Dung', 'Duy', 'Hải', 'Hải', 'Hào', 'Hòa', 'Hồng', 'Hợp', 'Hùng', 'Hưng', 'Hưỡng', 'Kha', 'Khải', 'Khanh', 'Khôi', 'Kim', 'Kiên', 'Kiệt', 'Kỳ', 'Linh', 'Long', 'Lộc', 'Lợi', 'Lực', 'Lưỡng', 'Lương', 'Luân', 'Lực', 'Lương', 'Ly', 'Mạnh', 'Minh', 'Mộng', 'Mỹ', 'Nam', 'Nhanh', 'Nhân', 'Nhật', 'Ninh', 'Nông', 'Nước', 'Oanh', 'Oánh', 'Phi', 'Phong', 'Phúc', 'Phương', 'Phụng', 'Phước', 'Phú', 'Quyền', 'Quyết', 'Rạng', 'Rên', 'Riêng', 'Sâm', 'Sang', 'Sánh', 'Sáu', 'Sĩ', 'Sinh', 'Sơn', 'Sở', 'Tài', 'Tâm', 'Tâng', 'Tạo', 'Tạp', 'Tâu', 'Tây', 'Thà', 'Thái', 'Thắm', 'Thắn', 'Thắp', 'Than', 'Thành', 'Thạo', 'Thạc', 'Thê', 'Thếp', 'Thêm', 'Thía', 'Thích', 'Thiếm', 'Thiệp', 'Thiều', 'Thiệu', 'Thìn', 'Thinh', 'Thoa', 'Thoại', 'Thoái', 'Thoát', 'Thong', 'Thông', 'Thột', 'Thớ', 'Thục', 'Thuận', 'Thục', 'Thúy', 'Thực', 'Thưa', 'Thương', 'Thước', 'Thứ', 'Tiên', 'Tiếp', 'Tiết', 'Tiểu', 'Tín', 'Tinh', 'Tịnh', 'Tiếu', 'Toàn', 'Toàng', 'Tông', 'Tớ', 'Tự', 'Tú', 'Túc', 'Tuệ', 'Tuy', 'Tuý', 'Tuân', 'Tuấn', 'Túng', 'Tường', 'Tương', 'Tứ', 'Tứng', 'Tược', 'Tưởng', 'Tương', 'Uẩn', 'Úc', 'Ứng', 'Uy', 'Uý', 'Uyên', 'Uyển', 'Uyêu']
SPECIALTIES = ['Cơ bản', 'Tim mạch', 'Thần kinh', 'Tai Mũi Họng', 'Ngoại khoa', 'Da liễu', 'Tiêu hóa', 'Hô hấp', 'Sản phụ khoa', 'Nhi khoa']
GENDERS = ['Nam', 'Nữ']
PROVINCES = ['Hà Nội', 'TP. Hồ Chí Minh', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ', 'Biên Hòa', 'Nha Trang', 'Hải Dương', 'Bắc Ninh', 'Bình Dương']
ADDRESS_DATA = {
    'Hà Nội': {
        'districts': {
            'Cầu Giấy': ['Phường Dịch Vọng', 'Phường Dịch Vọng Hậu', 'Phường Quan Hoa', 'Phường Nghĩa Đô'],
            'Đống Đa': ['Phường Ô Chợ Dừa', 'Phường Trung Tự', 'Phường Láng Thượng', 'Phường Thái Hà'],
            'Hoàn Kiếm': ['Phường Phúc Tân', 'Phường Hàng Trống', 'Phường Hàng Bồ', 'Phường Hàng Gai'],
            'Hai Bà Trưng': ['Phường Bạch Mai', 'Phường Thanh Nhàn', 'Phường Minh Khai', 'Phường Vĩnh Tuy']
        },
        'streets': ['Đường Trần Duy Hưng', 'Đường Nguyễn Văn Cừ', 'Đường Láng', 'Đường Giảng Võ', 'Đường Bưởi']
    },
    'TP. Hồ Chí Minh': {
        'districts': {
            'Quận 1': ['Phường Bến Nghé', 'Phường Bến Thành', 'Phường Tân Định'],
            'Quận 3': ['Phường Võ Thị Sáu', 'Phường 7', 'Phường 8'],
            'Quận 5': ['Phường 2', 'Phường 4', 'Phường 8'],
            'Quận 10': ['Phường 14', 'Phường 15', 'Phường 5']
        },
        'streets': ['Đường Nguyễn Thị Minh Khai', 'Đường Cách Mạng Tháng Tám', 'Đường Lê Văn Sỹ', 'Đường Trường Sa', 'Đường Nguyễn Tri Phương']
    },
    'Đà Nẵng': {
        'districts': {
            'Hải Châu': ['Phường Thạch Thang', 'Phường Hải Châu I', 'Phường Hải Châu II'],
            'Thanh Khê': ['Phường Tam Thuận', 'Phường Tân Chính', 'Phường Hòa Khê'],
            'Ngũ Hành Sơn': ['Phường Mỹ An', 'Phường Khuê Mỹ', 'Phường Hòa Hải']
        },
        'streets': ['Đường Nguyễn Văn Linh', 'Đường 2 Tháng 9', 'Đường Hoàng Sa', 'Đường Võ Nguyên Giáp']
    },
    'Hải Phòng': {
        'districts': {
            'Ngô Quyền': ['Phường Máy Chai', 'Phường Đông Khê', 'Phường Vạn Mỹ'],
            'Lê Chân': ['Phường An Biên', 'Phường An Dương', 'Phường Kênh Dương']
        },
        'streets': ['Đường Lạch Tray', 'Đường Trần Phú', 'Đường Cầu Đất']
    },
    'Cần Thơ': {
        'districts': {
            'Ninh Kiều': ['Phường Tân An', 'Phường An Khánh', 'Phường An Cư'],
            'Bình Thủy': ['Phường An Thới', 'Phường Long Hòa', 'Phường Bùi Hữu Nghĩa']
        },
        'streets': ['Đường 30 Tháng 4', 'Đường Nguyễn Văn Cừ', 'Đường Trần Văn Hoài']
    },
    'Biên Hòa': {
        'districts': {
            'Long Bình Tân': ['Phường Long Bình Tân', 'Phường An Bình', 'Phường Tân Biên'],
            'Trảng Dài': ['Phường Tân Mai', 'Phường Tân Phong']
        },
        'streets': ['Đường Võ Thị Sáu', 'Đường Phạm Văn Thuận', 'Đường Đồng Khởi']
    },
    'Nha Trang': {
        'districts': {
            'Ninh Hiệp': ['Phường Ninh Hiệp', 'Phường Ninh Thạnh'],
            'Vĩnh Hòa': ['Phường Vĩnh Hòa', 'Phường Vĩnh Nguyên']
        },
        'streets': ['Đường Trần Phú', 'Đường Lê Thánh Tôn', 'Đường Phạm Văn Đồng']
    },
    'Hải Dương': {
        'districts': {
            'Hải Dương': ['Phường Tân Bình', 'Phường Quang Trung', 'Phường Trần Hưng Đạo']
        },
        'streets': ['Đường Phạm Ngũ Lão', 'Đường Phạm Hồng Thái', 'Đường Nguyễn Trãi']
    },
    'Bắc Ninh': {
        'districts': {
            'Thị xã Từ Sơn': ['Phường Đình Bảng', 'Phường Đồng Nguyên'],
            'Huyện Thuận Thành': ['Thị trấn Hồ', 'Xã Ninh Xá']
        },
        'streets': ['Đường Kinh Dương Vương', 'Đường Lý Thái Tổ']
    },
    'Bình Dương': {
        'districts': {
            'Thủ Dầu Một': ['Phường Chánh Nghĩa', 'Phường Phú Cường', 'Phường Phú Lợi'],
            'Dĩ An': ['Phường Tân Bình', 'Phường Đông Hòa']
        },
        'streets': ['Đường Nguyễn Trãi', 'Đường Hùng Vương', 'Đường Phú Lợi']
    }
}
TIME_SLOTS = ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '14:00', '14:30', '15:00', '15:30', '16:00']
SESSIONS = {
    1: ("08:00", "09:00"),
    2: ("09:00", "10:00"),
    3: ("10:00", "11:00"),
    4: ("11:00", "12:00"),
    5: ("13:00", "14:00"),
    6: ("14:00", "15:00"),
    7: ("15:00", "16:00"),
    8: ("16:00", "17:00")
}
SPECIALTY_SLOTS = {
    'Cơ bản': 2,
    'Tim mạch': 3,
    'Thần kinh': 3,
    'Tai Mũi Họng': 2,
    'Ngoại khoa': 3,
    'Da liễu': 2,
    'Tiêu hóa': 3,
    'Hô hấp': 2,
    'Sản phụ khoa': 3,
    'Nhi khoa': 3
}
STATUSES = ['Đã đặt', 'Đã khám', 'Đã hoàn thành', 'Đã hủy']
SYMPTOMS = ['Đau đầu', 'Sốt cao', 'Ho', 'Đau họng', 'Tiêu chảy', 'Khó thở', 'Mệt mỏi', 'Chóng mặt', 'Đau bụng', 'Nôn', 'Đau lưng', 'Đau ngực', 'Hụt hơi', 'Phát ban', 'Rối loạn giấc ngủ', 'Viêm mắt', 'Viêm tai', 'Táo bón', 'Suy nhược', 'Sụt cân']
DIAGNOSES = ['Cảm lạnh', 'Viêm họng', 'Viêm phổi', 'Tiêu chảy cấp', 'Đau đầu căng thẳng', 'Huyết áp cao', 'Đái tháo đường', 'Loét dạ dày', 'Hen phế quản', 'Viêm tai giữa', 'Viêm da cơ địa', 'Viêm xoang', 'Viêm đường tiết niệu', 'Rối loạn tiêu hóa', 'Viêm gan', 'Bệnh tim mạch', 'Viêm dây thần kinh', 'Thiếu máu', 'Viêm khớp', 'Viêm amidan']
PRESCRIPTIONS = ['Paracetamol 500mg x3/ngày', 'Amoxicillin 500mg x3/ngày', 'Omeprazole 20mg x2/ngày', 'Aspirin 100mg/ngày', 'Ibuprofen 400mg x3/ngày', 'Vitamin C 500mg x2/ngày', 'Dextromethorphan 10mg x3/ngày', 'Loratadine 10mg/ngày']

def remove_vietnamese_accents(text):
    """Hàm chuyển đổi tiếng Việt có dấu thành không dấu"""
    intab = "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ"
    outab = "aaaaaaaaaaaaaaaaaeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyd"
    intab += intab.upper()
    outab += outab.upper()
    trans_dict = str.maketrans(intab, outab)
    return text.translate(trans_dict)

def generate_random_phone(existing_phones=None):
    """Tạo số điện thoại ngẫu nhiên, tránh trùng"""
    existing_phones = existing_phones or set()
    while True:
        phone = f"0{random.randint(8, 9)}{random.randint(0, 9)}{random.randint(10000000, 99999999)}"
        if phone not in existing_phones:
            existing_phones.add(phone)
            return phone

def generate_random_cccd():
    """Tạo số CCCD ngẫu nhiên"""
    return f"{random.randint(100000000, 999999999)}"

def generate_random_bhyt():
    """Tạo số BHYT ngẫu nhiên (có đầu chữ tỉnh) - 70% có BHYT"""
    if random.random() < 0.7:
        provinces_code = ['HA', 'HP', 'DN', 'HCM', 'CT', 'BH', 'NT', 'HD', 'TG', 'VT', 'BA', 'TA', 'BH', 'CT', 'DA']
        prov_code = random.choice(provinces_code)
        number = f"{random.randint(100000000, 999999999)}"
        return f"{prov_code}{number}"
    return None

def generate_random_bhyt_expiry():
    """Tạo ngày hết hạn BHYT (từ 1 năm đến 3 năm từ hôm nay)"""
    today = datetime.date.today()
    days_ahead = random.randint(365, 1095)
    return (today + datetime.timedelta(days=days_ahead)).isoformat()

def generate_random_username(name, existing_usernames):
    """Tạo username bệnh nhân dựa trên tên không dấu và đảm bảo không trùng"""
    name_no_accent = remove_vietnamese_accents(name)
    normalized = ''.join(ch for ch in name_no_accent.lower() if ch.isalpha() or ch.isspace())
    parts = normalized.split()
    base = parts[-1] if parts else 'patient'
    username = base
    suffix = 1
    while username in existing_usernames:
        username = f"{base}{suffix}"
        suffix += 1
    existing_usernames.add(username)
    return username

def generate_random_password(length=10):
    """Tạo mật khẩu ngẫu nhiên có cả chữ và số"""
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    chars = letters + digits
    password_chars = [random.choice(letters), random.choice(digits)]
    password_chars += [random.choice(chars) for _ in range(length - 2)]
    random.shuffle(password_chars)
    return ''.join(password_chars)

def generate_random_name():
    """Tạo tên người ngẫu nhiên (3+ chữ)"""
    surname = random.choice(SURNAMES_VN)
    middle = random.choice(MIDDLE_NAMES_VN)
    last = random.choice(LAST_NAMES_VN)
    return f"{surname} {middle} {last}"

def generate_random_address(province, district, ward):
    """Tạo địa chỉ ngẫu nhiên với tỉnh/thành, quận/huyện và phường"""
    street = random.choice(ADDRESS_DATA.get(province, {}).get('streets', ['Đường Lê Lợi', 'Đường Nguyễn Huệ', 'Đường Trần Hưng Đạo']))
    number = random.randint(1, 500)
    return f"Số {number}, {street}, {ward}, {district}, {province}"

def generate_doctors(num_doctors=80, existing_phones=None):
    """Sinh dữ liệu bác sĩ"""
    doctors = []
    existing_phones = existing_phones or set()
    for i in range(1, num_doctors + 1):
        doctor_id = f"D{str(i).zfill(4)}"
        name = generate_random_name()
        gender = random.choice(GENDERS)
        specialty = random.choice(SPECIALTIES)
        base_price = 150000 if specialty == 'Cơ bản' else random.choice([300000, 500000, 700000])
        phone = generate_random_phone(existing_phones)
        doctors.append(f"{doctor_id}|{name}|{gender}|{specialty}|{base_price}|{phone}")
    return doctors

def generate_random_email(name, existing_emails=None):
    """Tạo email KHÔNG DẤU từ tên"""
    existing_emails = existing_emails or set()
    name_no_accent = remove_vietnamese_accents(name)
    normalized = ''.join(ch for ch in name_no_accent.lower() if ch.isalpha() or ch.isspace())
    parts = normalized.split()
    base = ''.join(parts) if parts else 'patient'
    
    email = f"{base}@hospital.local"
    counter = 1
    while email in existing_emails:
        email = f"{base}{counter}@hospital.local"
        counter += 1
    existing_emails.add(email)
    return email

def generate_patients(num_patients=250, existing_phones=None):
    """Sinh dữ liệu bệnh nhân"""
    patients = []
    existing_phones = existing_phones or set()
    existing_emails = set()
    for i in range(1, num_patients + 1):
        patient_id = f"B{str(i).zfill(8)}"
        cccd = generate_random_cccd()
        full_name = generate_random_name()
        phone = generate_random_phone(existing_phones)
        email = generate_random_email(full_name, existing_emails)
        province = random.choice(PROVINCES)
        province_data = ADDRESS_DATA.get(province, {})
        districts = list(province_data.get('districts', {}).keys())
        district = random.choice(districts) if districts else 'Quận 1'
        ward_list = province_data.get('districts', {}).get(district, ['Phường 1', 'Phường 2'])
        ward = random.choice(ward_list)
        detailed_address = generate_random_address(province, district, ward)
        bhyt_code = generate_random_bhyt()
        bhyt_expiry = generate_random_bhyt_expiry() if bhyt_code else ""
        patients.append(f"{patient_id}|{cccd}|{full_name}|{phone}|{email}|{province}|{ward}|{detailed_address}|{bhyt_code or ''}|{bhyt_expiry}")
    return patients

def generate_schedules(doctors, num_schedules=350):
    """Sinh dữ liệu lịch khám"""
    schedules = []
    schedule_id_counter = 1
    today = datetime.date.today()
    for _ in range(num_schedules):
        schedule_id = f"L{str(schedule_id_counter).zfill(8)}"
        schedule_id_counter += 1
        doctor_id = random.choice([d.split('|')[0] for d in doctors])
        days_ahead = random.randint(1, 90)
        date = today + datetime.timedelta(days=days_ahead)
        time_slot = random.choice(TIME_SLOTS)
        is_booked = random.choice(['False', 'False', 'True'])
        schedules.append(f"{schedule_id}|{doctor_id}|{date.isoformat()}|{time_slot}|{is_booked}")
    return schedules

def generate_appointments(patients, schedules, num_appointments=300):
    """Sinh dữ liệu cuộc hẹn"""
    appointments = []
    appointment_id_counter = 1
    schedules_list = schedules
    for i in range(min(num_appointments, len(schedules_list))):
        appointment_id = f"A{str(appointment_id_counter).zfill(8)}"
        appointment_id_counter += 1
        patient_id = random.choice([p.split('|')[0] for p in patients])
        schedule_id = schedules_list[i].split('|')[0]
        status = random.choice(STATUSES)
        payment_status = 'Đã thanh toán' if status != 'Đã đặt' else 'Chưa thanh toán'
        appointments.append(f"{appointment_id}|{patient_id}|{schedule_id}|{status}|{payment_status}")
        schedules_list[i] = schedules_list[i].replace('|False', '|True')
    return appointments

def generate_medical_records(appointments, num_records=180):
    """Sinh dữ liệu hồ sơ bệnh án"""
    records = []
    record_id_counter = 1
    for i in range(min(num_records, len(appointments))):
        record_id = f"R{str(record_id_counter).zfill(8)}"
        record_id_counter += 1
        appointment_id = appointments[i].split('|')[0]
        symptoms = ', '.join(random.sample(SYMPTOMS, random.randint(1, 3)))
        diagnosis = random.choice(DIAGNOSES)
        prescription = random.choice(PRESCRIPTIONS)
        records.append(f"{record_id}|{appointment_id}|{symptoms}|{diagnosis}|{prescription}")
    return records

def generate_user_records(patients, doctors, admin_phone='0900000000', admin_email='admin@hospital.local'):
    """Sinh dữ liệu user chung cho admin, bác sĩ, bệnh nhân"""
    users = []
    existing_phones = set()
    user_id_counter = 1
    existing_emails = set()

    def next_user_id():
        nonlocal user_id_counter
        user_id = f"U{str(user_id_counter).zfill(8)}"
        user_id_counter += 1
        return user_id

    admin_password = 'admin123'
    users.append(f"{next_user_id()}|{admin_phone}|{admin_email}|{admin_password}|admin|")
    existing_phones.add(admin_phone)
    existing_emails.add(admin_email)

    for doctor_line in doctors:
        doctor_id, name, _, _, _, phone = doctor_line.split('|')
        email = generate_random_email(name, existing_emails)
        password = generate_random_password(10)
        users.append(f"{next_user_id()}|{phone}|{email}|{password}|doctor|{doctor_id}")
        existing_phones.add(phone)

    for patient_line in patients:
        patient_id = patient_line.split('|')[0]
        phone = patient_line.split('|')[3]
        email = patient_line.split('|')[4]
        if phone in existing_phones:
            continue
        password = generate_random_password(10)
        users.append(f"{next_user_id()}|{phone}|{email}|{password}|patient|{patient_id}")
        existing_phones.add(phone)

    return users

def generate_doctor_weekly_schedules(doctors):
    schedules = []
    schedule_id_counter = 1
    for doctor_line in doctors:
        doctor_id = doctor_line.split('|')[0]
        num_days = random.randint(5, 6)
        selected_days = random.sample(range(1, 7), num_days)
        for day in sorted(selected_days):
            sessions = ['Sáng']
            if random.random() < 0.5:
                sessions.append('Chiều')
            for session in sessions:
                schedule_id = f"L{str(schedule_id_counter).zfill(8)}"
                schedule_id_counter += 1
                schedules.append(f"{schedule_id}|{doctor_id}|{day}|{session}")
    return schedules

def generate_schedules_from_weekly(weekly_schedules, existing_schedules_count=0):
    schedules = []
    schedule_id_counter = existing_schedules_count + 1
    today = datetime.date.today()
    for days_ahead in range(1, 91):
        target_date = today + datetime.timedelta(days=days_ahead)
        target_weekday = target_date.weekday()
        lch_weekday = (target_weekday + 1) % 7
        for ws in weekly_schedules:
            parts = ws.split('|')
            doctor_id = parts[0]
            day_of_week = int(parts[2])
            session = parts[3]
            if day_of_week == lch_weekday:
                if session == 'Sáng':
                    time_slots = ['08:00', '09:00', '10:00', '11:00']
                else:
                    time_slots = ['13:00', '14:00', '15:00', '16:00']
                for time_slot in time_slots:
                    schedule_id = f"S{str(schedule_id_counter).zfill(8)}"
                    schedule_id_counter += 1
                    is_booked = 'False'
                    schedules.append(f"{schedule_id}|{doctor_id}|{target_date.isoformat()}|{time_slot}|{is_booked}")
    return schedules

def generate_doctor_schedules_pattern(doctors):
    patterns = []
    for doctor_line in doctors:
        doctor_id = doctor_line.split('|')[0]
        specialty = doctor_line.split('|')[3]
        num_slots = SPECIALTY_SLOTS.get(specialty, 2)
        num_days = random.randint(5, 6)
        selected_days = sorted(random.sample(range(1, 7), num_days))
        all_slots = list(range(1, 9))
        for day in selected_days:
            slots = sorted(random.sample(all_slots, num_slots))
            for slot in slots:
                patterns.append(f"{doctor_id}|{day}|{slot}")
    return patterns

def generate_schedules_from_pattern(patterns, doctors_dict, days=30):
    schedules = []
    schedule_id_counter = 1
    today = datetime.date.today()
    for days_ahead in range(1, days + 1):
        target_date = today + datetime.timedelta(days=days_ahead)
        lch_weekday = (target_date.weekday() + 1) % 7
        if lch_weekday == 0:
            lch_weekday = 7
        for pattern in patterns:
            parts = pattern.split('|')
            doctor_id = parts[0]
            day_of_week = int(parts[1])
            slot_num = int(parts[2])
            if day_of_week == lch_weekday:
                start_time, end_time = SESSIONS.get(slot_num, ("08:00", "09:00"))
                schedule_id = f"S{str(schedule_id_counter).zfill(8)}"
                schedule_id_counter += 1
                is_booked = 'False'
                schedules.append(f"{schedule_id}|{doctor_id}|{target_date.isoformat()}|{start_time}|{is_booked}|{day_of_week}|{slot_num}")
    return schedules

def save_to_file(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in data:
            f.write(line + '\n')
    print(f"✓ {filename}: {len(data)} dòng")

def main():
    print("🏥 Sinh dữ liệu hệ thống quản lý lịch khám bệnh viện...")
    print("-" * 50)
    
    phones = set()
    doctors = generate_doctors(180, phones)
    patients = generate_patients(700, phones)
    
    schedule_pattern = generate_doctor_schedules_pattern(doctors)
    schedules = generate_schedules_from_pattern(schedule_pattern, None, 30)
    
    appointments = generate_appointments(patients, schedules, 300)
    records = generate_medical_records(appointments, 300)
    users = generate_user_records(patients, doctors)
    
    save_to_file('doctors.txt', doctors)
    save_to_file('patients.txt', patients)
    save_to_file('schedules.txt', schedules)
    save_to_file('appointments.txt', appointments)
    save_to_file('records.txt', records)
    save_to_file('user_credentials.txt', users)
    
    total_lines = len(doctors) + len(patients) + len(schedules) + len(appointments) + len(records) + len(users)
    print("-" * 50)
    print(f"✓ Hoàn thành: {total_lines} dòng dữ liệu")

if __name__ == '__main__':
    main()