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
                self.base_price = int(base_price) # Chuyển đổi base_price thành số nguyên
            except Exception:
                key = (specialty or 'Cơ bản').strip().lower() 
                self.base_price = 150000 if key == 'cơ bản' else 500000 # Nếu không chuyển đổi được, xác định base_price dựa trên specialty: nếu specialty là 'Cơ bản' thì base_price là 150000, ngược lại là 500000
        else: # Nếu base_price không được cung cấp
            key = (specialty or 'Cơ bản').strip().lower()
            self.base_price = 150000 if key == 'cơ bản' else 500000 

    def __str__(self): 
        return f"{self.id} - {self.name} - {self.gender} - {self.specialty} - {self.base_price}đ"
