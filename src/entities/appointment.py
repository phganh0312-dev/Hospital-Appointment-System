from structures.linked_list import LinkedList

class Appointment:
    def __init__(
        self,
        appointment_id,
        patient_id,
        schedule_id,
        status="Đã đặt",
        payment_status="Chưa thanh toán"
    ):
        self.id = appointment_id
        self.patient_id = patient_id
        self.schedule_id = schedule_id
        self.status = status
        self.payment_status = payment_status

    def __str__(self):
        return (
            f"Appointment("
            f"ID: {self.id}, "
            f"Patient_ID: {self.patient_id}, "
            f"Schedule_ID: {self.schedule_id}, "
            f"Status: {self.status})"
        )