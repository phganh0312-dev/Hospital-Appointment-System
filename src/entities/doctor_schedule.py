import datetime


class Schedule:
    def __init__(self, id, doctor_id, date, time_slot, is_booked=False, day_of_week=None, slot_num=None):
        self.id = id
        self.doctor_id = doctor_id
        self.date = self._validate_date_within_three_months(date)
        self.time_slot = time_slot
        self.is_booked = bool(is_booked)
        self.day_of_week = day_of_week
        self.slot_num = slot_num

    def __str__(self):
        status = 'Da dat' if self.is_booked else 'Trong'
        return f"{self.id} - Bac si:{self.doctor_id} - {self.date} {self.time_slot} - {status}"

    def _parse_date(self, date_input):
        if isinstance(date_input, datetime.datetime):
            return date_input.date()
        if isinstance(date_input, datetime.date):
            return date_input
        if isinstance(date_input, str):
            try:
                return datetime.date.fromisoformat(date_input)
            except Exception:
                parts = date_input.split('/')
                if len(parts) == 3:
                    try:
                        return datetime.date(int(parts[2]), int(parts[1]), int(parts[0]))
                    except Exception:
                        pass
        raise ValueError('Dinh dang ngay khong hop le')

    def _validate_date_within_three_months(self, date_input):
        date_obj = self._parse_date(date_input)
        today = datetime.date.today()
        max_date = today + datetime.timedelta(days=90)
        if not (today <= date_obj <= max_date):
            raise ValueError('He thong chi quan ly ca truc trong vong 3 thang')
        return date_obj
