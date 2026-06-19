from structures.linked_list import LinkedList
from entities.doctor_schedule import Schedule
from managers.base_manager import BaseManager
from managers.file_handler import FileHandler
import datetime


class ScheduleManager(BaseManager):
    def __init__(self, schedules=None):
        self.schedules = schedules or LinkedList()

    def _save_to_file(self):
        FileHandler.save_data(
            "data/schedules.txt",
            self.schedules,
            lambda s: f"{s.id}|{s.doctor_id}|{s.date}|{s.time_slot}|{s.is_booked}|{getattr(s, 'day_of_week', '')}|{getattr(s, 'slot_num', '')}"
        )

    def add_schedule(self, schedule: Schedule):
        if not isinstance(schedule, Schedule):
            raise TypeError('Phai nhap mot lich kham')
        if self.find_schedule_by_id(schedule.id):
            raise ValueError('Ma lich da ton tai')
        if self.is_conflict(schedule):
            raise ValueError('Trung lich voi ca da co')

        self.schedules.append(schedule)
        self._save_to_file()

    def remove_schedule_by_id(self, schedule_id):
        schedule = self.find_schedule_by_id(schedule_id)
        if not schedule:
            return False
        if schedule.is_booked:
            raise ValueError("Khong the xoa lich da co nguoi dat")

        self.schedules.remove(schedule_id)
        self._save_to_file()
        return True

    def update_schedule(self, schedule_id, updates=None, **kwargs):
        schedule = self.find_schedule_by_id(schedule_id)
        if not schedule or not self.can_update_schedule(schedule_id):
            return False
        if getattr(schedule, 'is_booked', False):
            raise ValueError("Khong the sua lich da duoc dat")

        merged_updates = LinkedList()
        if updates and hasattr(updates, 'items'):
            current = updates.items().head
            while current:
                merged_updates.append(current.value)
                current = current.next

        for key in kwargs:
            from structures.hash_table import HashEntry
            merged_updates.append(HashEntry(key, kwargs[key]))

        current = merged_updates.head
        while current:
            key = current.value.key
            value = current.value.value
            if key == "date":
                value = self._parse_date(value)
            if hasattr(schedule, key):
                setattr(schedule, key, value)
            current = current.next

        self._save_to_file()
        return True

    def _parse_date(self, value):
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value
        try:
            return datetime.date.fromisoformat(str(value))
        except Exception:
            parts = str(value).split('/')
            if len(parts) == 3:
                return datetime.date(int(parts[2]), int(parts[1]), int(parts[0]))
        raise ValueError('Dinh dang ngay khong hop le')

    def find_schedule_by_id(self, schedule_id):
        return self.schedules.find_by_attribute('id', schedule_id)

    def book_schedule(self, schedule_id):
        schedule = self.find_schedule_by_id(schedule_id)
        if not schedule or schedule.is_booked:
            return False
        schedule.is_booked = True
        self._save_to_file()
        return True

    def book_slot(self, schedule_id):
        schedule = self.find_schedule_by_id(schedule_id)
        if not schedule:
            raise ValueError('Khong tim thay lich kham tuong ung')
        if getattr(schedule, 'is_booked', False):
            raise ValueError('Lich nay da co nguoi dat')

        schedule.is_booked = True
        self._save_to_file()
        return True

    def release_schedule(self, schedule_id):
        schedule = self.find_schedule_by_id(schedule_id)
        if not schedule:
            return False
        schedule.is_booked = False
        self._save_to_file()
        return True

    def is_conflict(self, new_schedule: Schedule):
        current = self.schedules.head
        while current:
            s = current.value
            if (
                getattr(s, 'doctor_id', None) == getattr(new_schedule, 'doctor_id', None)
                and getattr(s, 'date', None) == getattr(new_schedule, 'date', None)
                and getattr(s, 'time_slot', None) == getattr(new_schedule, 'time_slot', None)
                and getattr(s, 'id', None) != getattr(new_schedule, 'id', None)
            ):
                return True
            current = current.next
        return False

    def can_update_schedule(self, schedule_id):
        schedule = self.find_schedule_by_id(schedule_id)
        if not schedule:
            return False
        from datetime import datetime
        today = datetime.now().date()
        return schedule.date > today

    def search_available_schedules(self, doctor_id, date=None, weekday=None):
        results = LinkedList()
        current = self.schedules.head
        while current:
            s = current.value
            if getattr(s, 'doctor_id', None) == doctor_id:
                match = True
                if date and s.date != self._to_date(date):
                    match = False
                if match and weekday is not None:
                    wd = self._weekday_to_int(weekday)
                    if s.date.weekday() != wd:
                        match = False
                if match and not s.is_booked:
                    results.append(s)
            current = current.next
        return results

    def get_schedules_by_day_of_week(self, doctor_id, day_of_week):
        results = LinkedList()
        current = self.schedules.head
        while current:
            s = current.value
            if getattr(s, 'doctor_id', None) == doctor_id and getattr(s, 'day_of_week', None) == day_of_week:
                results.append(s)
            current = current.next
        return results

    def get_schedules_by_day_of_week_and_slot(self, doctor_id, day_of_week, slot_num):
        results = LinkedList()
        current = self.schedules.head
        while current:
            s = current.value
            if (
                getattr(s, 'doctor_id', None) == doctor_id
                and getattr(s, 'day_of_week', None) == day_of_week
                and getattr(s, 'slot_num', None) == slot_num
            ):
                results.append(s)
            current = current.next
        return results

    def get_schedules_by_slot_number(self, slot_num):
        results = LinkedList()
        current = self.schedules.head
        while current:
            if getattr(current.value, 'slot_num', None) == slot_num:
                results.append(current.value)
            current = current.next
        return results

    def get_schedules_within_days(self, days=30):
        from datetime import datetime, timedelta
        results = LinkedList()
        today = datetime.now().date()
        end_date = today + timedelta(days=days)

        current = self.schedules.head
        while current:
            schedule_date = self._to_date(getattr(current.value, 'date', None))
            if today <= schedule_date <= end_date:
                results.append(current.value)
            current = current.next
        return results
