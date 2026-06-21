from structures.linked_list import LinkedList

class Doctor:
    def __init__(self, id, name, gender=None, specialty='Cơ bản', base_price=None, phone=None):
        self.id = id
        self.name = name
        self.gender = gender
        self.specialty = specialty
        self.phone = phone
        if base_price is not None:
            try:
                self.base_price = int(base_price)
            except Exception:
                key = (specialty or 'Cơ bản').strip().lower() 
                self.base_price = 150000 if key == 'cơ bản' else 500000 
        else: 
            key = (specialty or 'Cơ bản').strip().lower()
            self.base_price = 150000 if key == 'cơ bản' else 500000 

    def __str__(self): 
        return f"{self.id} - {self.name} - {self.gender} - {self.specialty} - {self.base_price}đ"
