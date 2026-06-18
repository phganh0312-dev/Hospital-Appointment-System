import datetime


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
        mapping_vi = {
            'thứ hai': 0,
            'thứ ba': 1,
            'thứ tư': 2,
            'thứ năm': 3,
            'thứ sáu': 4,
            'thứ bảy': 5,
            'chủ nhật': 6,
        }
        if w in mapping_vi:
            return mapping_vi[w]
        try:
            return int(w)
        except Exception:
            raise ValueError('Ngày không hợp lệ.')
        
    def _to_lower(self, text):
        """Hàm tự xây đổi thành chữ thường không dùng thư viện"""
        res = ""
        for char in str(text):
            if 'A' <= char <= 'Z':
                res += chr(ord(char) + 32)
            else:
                res += char
        return res

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
