from linked_list import Linked List

class Patient:
    def __init__(self, patient_id, cccd, full_name, phone, province, ward, detailed_address):
        self.id = patient_id            
        self.cccd = cccd                
        self.full_name = full_name
        self.phone = phone
        self.province = province
        self.ward = ward
        self.detailed_address = detailed_address

    def __str__(self):
        return f"Patient(ID: {self.id}, CCCD: {self.cccd}, Name: {self.full_name})"
