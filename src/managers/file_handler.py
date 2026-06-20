import os
from structures.linked_list import LinkedList
from entities.doctor import Doctor
from entities.patient import Patient
from entities.doctor_schedule import Schedule
from entities.appointment import Appointment
from entities.medical_record import MedicalRecord
from entities.user import User


class FileHandler:
    @staticmethod
    def save_data(file_path, data_collection, to_string_func):
        with open(file_path, "w", encoding="utf-8") as f:
            if hasattr(data_collection, 'head'):
                current = data_collection.head
                while current:
                    f.write(to_string_func(current.value) + "\n")
                    current = current.next

    @staticmethod
    def load_data(file_path, split_char='|'):
        data_list = LinkedList()
        if not os.path.exists(file_path):
            return data_list

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    data_list.append(tuple(line.split(split_char)))
        return data_list
