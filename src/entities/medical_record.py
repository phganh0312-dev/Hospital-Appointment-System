from structures.linked_list import LinkedList

class MedicalRecord:
    def __init__(self, record_id, appointment_id, symptoms, diagnosis, prescription):
        self.id = record_id  
        self.appointment_id = appointment_id
        self.symptoms = symptoms
        self.diagnosis = diagnosis
        self.prescription = prescription

    def __str__(self):
        return f"Record(ID: {self.id}, Appt_ID: {self.appointment_id}, Diagnosis: {self.diagnosis})"
