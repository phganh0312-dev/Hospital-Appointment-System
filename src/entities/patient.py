from structures.linked_list import LinkedList

class Patient:
    def __init__(self, patient_id, cccd, full_name, phone, email, province, ward, detailed_address, bhyt_code=None, bhyt_expiry=None):
        self.id = patient_id            
        self.cccd = cccd                
        self.full_name = full_name
        self.phone = phone
        self.email = email
        self.province = province
        self.ward = ward
        self.detailed_address = detailed_address
        self.bhyt_code = bhyt_code
        self.bhyt_expiry = bhyt_expiry

    def __str__(self):
        return f"Patient(ID: {self.id}, CCCD: {self.cccd}, Name: {self.full_name}, BHYT: {self.bhyt_code})"
