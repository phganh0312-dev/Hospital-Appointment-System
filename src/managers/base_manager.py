import datetime

# ==========================================
# CÁC CLASS EXCEPTION TỰ ĐỊNH NGHĨA
# ==========================================
class ValidationError(Exception):
    pass

class DataConsistencyError(Exception):
    pass

# ==========================================
# QUẢN LÝ TRẠNG THÁI CUỘC HẸN (KHÔNG DÙNG DICT/LIST)
# ==========================================
class AppointmentStatus:
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

    @staticmethod
    def is_valid(status):
        # Sử dụng tuple () thay vì list []
        return status in (
            AppointmentStatus.PENDING, 
            AppointmentStatus.CONFIRMED, 
            AppointmentStatus.COMPLETED, 
            AppointmentStatus.CANCELLED
        )

    @staticmethod
    def normalize(status):
        if not status:
            return AppointmentStatus.PENDING
        s = str(status).strip().upper()
        # Đã là mã chuẩn (tiếng Anh) thì giữ nguyên
        if AppointmentStatus.is_valid(s):
            return s
        # Tiếng Việt (có dấu và không dấu) -> mã chuẩn
        if s in ("ĐÃ ĐẶT", "CHỜ KHÁM", "DA DAT", "CHO KHAM"):
            return AppointmentStatus.PENDING
        if s in ("ĐÃ XÁC NHẬN", "DA XAC NHAN"):
            return AppointmentStatus.CONFIRMED
        if s in ("ĐÃ KHÁM", "ĐÃ HOÀN THÀNH", "DA KHAM", "DA HOAN THANH"):
            return AppointmentStatus.COMPLETED
        if s in ("ĐÃ HỦY", "DA HUY"):
            return AppointmentStatus.CANCELLED
        return s

class AppointmentStateMachine:
    @staticmethod
    def can_transition(current_status, new_status):
        # Không dùng Dictionary chứa rules, rẽ nhánh thủ công hoàn toàn
        if current_status == AppointmentStatus.PENDING:
            return new_status in (AppointmentStatus.CONFIRMED, AppointmentStatus.CANCELLED)
        if current_status == AppointmentStatus.CONFIRMED:
            return new_status in (AppointmentStatus.COMPLETED, AppointmentStatus.CANCELLED)
        return False

    @staticmethod
    def transition(appointment, new_status):
        if not AppointmentStateMachine.can_transition(appointment.status, new_status):
            raise ValidationError(f"Không thể chuyển trạng thái từ '{appointment.status}' sang '{new_status}'")
        appointment.status = new_status


# ==========================================
# BASE MANAGER CHỨA CÁC THUẬT TOÁN DÙNG CHUNG
# ==========================================
class BaseManager:
    def _to_date(self, date_input):
        if isinstance(date_input, datetime.datetime):
            return date_input.date()
        if isinstance(date_input, datetime.date):
            return date_input
        if isinstance(date_input, str):
            return datetime.date.fromisoformat(date_input)
        raise ValueError('Invalid date')

    def _weekday_to_int(self, weekday):
        if isinstance(weekday, int):
            return weekday
        w = str(weekday).strip().lower()
        
        # ĐÃ XÓA DICTIONARY, THAY BẰNG IF/ELIF TUYẾN TÍNH
        if w == 'thứ hai': return 0
        elif w == 'thứ ba': return 1
        elif w == 'thứ tư': return 2
        elif w == 'thứ năm': return 3
        elif w == 'thứ sáu': return 4
        elif w == 'thứ bảy': return 5
        elif w == 'chủ nhật': return 6
        
        try:
            return int(w)
        except Exception:
            raise ValueError('Ngày không hợp lệ.')
        
    def _to_lower(self, text):
        upper = (
            "AĂÂBCDĐEÊGHIKLMNOÔƠPQRSTUƯVXY"
            "ÁÀẢÃẠẮẰẲẴẶẤẦẨẪẬ"
            "ÉÈẺẼẸẾỀỂỄỆ"
            "ÍÌỈĨỊ"
            "ÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢ"
            "ÚÙỦŨỤỨỪỬỮỰ"
            "ÝỲỶỸỴ"
        )

        lower = (
            "aăâbcdđeêghiklmnoôơpqrstuưvxy"
            "áàảãạắằẳẵặấầẩẫậ"
            "éèẻẽẹếềểễệ"
            "íìỉĩị"
            "óòỏõọốồổỗộớờởỡợ"
            "úùủũụứừửữự"
            "ýỳỷỹỵ"
        )

        result = ""

        for ch in str(text):
            found = False

            for i in range(len(upper)):
                if ch == upper[i]:
                    result += lower[i]
                    found = True
                    break

            if not found:
                result += ch

        return result

    def _custom_find_substring(self, main_str, sub_str):
        """Thuật toán Linear Search tìm chuỗi con"""
        if not sub_str: return True
        if not main_str: return False
        
        len_main = 0
        for _ in main_str: len_main += 1
        len_sub = 0
        for _ in sub_str: len_sub += 1
        
        if len_sub > len_main: return False
        
        for i in range(len_main - len_sub + 1):
            match = True
            for j in range(len_sub):
                if main_str[i+j] != sub_str[j]:
                    match = False
                    break
            if match:
                return True
        return False