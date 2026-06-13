import datetime
from entities.doctor import Doctor
from structures.linked_list import LinkedList

class Schedule:
    def __init__(self, id, doctor_id, date, time_slot, is_booked=False):
        self.id = id
        self.doctor_id = doctor_id
        self.date = self._validate_date_within_three_months(date) # Kiểm tra và chuẩn hóa ngày, đảm bảo nó nằm trong vòng 3 tháng kể từ hôm nay
        self.time_slot = time_slot
        self.is_booked = bool(is_booked)

    def book(self): # Nếu ca đã được đặt trước đó, trả về False. Nếu chưa, đặt ca và trả về True
        if self.is_booked:
            return False
        self.is_booked = True
        return True

    def unbook(self): # Nếu ca chưa được đặt trước đó, trả về False. Nếu đã đặt, hủy đặt ca và trả về True
        if not self.is_booked:
            return False
        self.is_booked = False
        return True

    def __str__(self): 
        status = 'Đã đặt' if self.is_booked else 'Trống' # Hiển thị trạng thái của ca khám dựa trên thuộc tính is_booked
        date_str = self.date.isoformat() if isinstance(self.date, datetime.date) else str(self.date) # Chuyển đổi ngày thành chuỗi ISO nếu nó là đối tượng datetime.date, nếu không thì giữ nguyên dạng chuỗi ban đầu
        return f"{self.id} - Bác sĩ:{self.doctor_id} - {date_str} {self.time_slot} - {status}"

    def _validate_date_within_three_months(self, date_input):
        
        if isinstance(date_input, datetime.datetime): # Nếu date_input là một đối tượng datetime.datetime, chuyển đổi nó thành datetime.date bằng cách lấy phần ngày
            date_obj = date_input.date()
        elif isinstance(date_input, datetime.date): # Nếu date_input đã là một đối tượng datetime.date, sử dụng nó trực tiếp mà không cần chuyển đổi
            date_obj = date_input
        elif isinstance(date_input, str): # Nếu date_input là một chuỗi
            try:
                date_obj = datetime.date.fromisoformat(date_input) # Cố gắng chuyển đổi chuỗi date_input thành một đối tượng datetime.date sử dụng định dạng ISO (YYYY-MM-DD)
            except Exception:
                raise ValueError('Định dạng ngày không hợp lệ.') 
        else:
            raise ValueError('Loại ngày không được hỗ trợ.') # Nếu date_input không phải là datetime.datetime, datetime.date hoặc str

        today = datetime.date.today() # Lấy ngày hiện tại để so sánh với date_obj
        max_date = today + datetime.timedelta(days=90) # Tính toán ngày tối đa cho phép bằng cách cộng thêm 90 ngày (tương đương với 3 tháng) vào ngày hiện tại
        if not (today <= date_obj <= max_date): # Kiểm tra nếu date_obj nằm ngoài khoảng từ ngày hiện tại đến ngày tối đa
            raise ValueError('Hệ thống chỉ giới hạn quản lý thời gian ca trực trong vòng 3 tháng.')
        return date_obj
