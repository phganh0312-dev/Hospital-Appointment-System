class User:
    def __init__(self, user_id, phone, email, password, role, linked_id=None):
        self.user_id = user_id
        self.phone = phone
        self.email = email
        self.password = password
        self.role = role
        self.linked_id = linked_id

    def __str__(self):
        return f"{self.user_id}|{self.phone}|{self.email}|{self.password}|{self.role}|{self.linked_id}"
