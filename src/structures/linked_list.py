class LinkedList:
    def __init__(self): # Khởi tạo một danh sách liên kết mới với head và tail ban đầu là None
        self.head = None
        self.tail = None
    def append(self, value):  # Thêm nút vào cuối danh sách, độ phức tạp O(1)
        new_node = Node(value)
        if not self.head:  # Nếu danh sách rỗng, cả head và tail đều trỏ đến nút mới
            self.head = new_node
            self.tail = new_node
        else:  # Nếu danh sách không rỗng, cập nhật tail để trỏ đến nút mới
            self.tail.next = new_node  # Thêm một nút mới vào sau tail hiện tại
            self.tail = new_node  # Bây giờ nút mới trở thành tail
    def remove(self, id_key):  # Xóa nút có id (dạng chuỗi vd: 'D001') cụ thể, độ phức tạp O(n)
        s = str(id_key)
        if not (s and s[0].isalpha() and s[1:].isdigit()): # Kiểm tra định dạng id hợp lệ: phải bắt đầu bằng chữ cái và theo sau là số (vd: 'D001')
            print("ID không hợp lệ.")
            return
        current = self.head
        previous = None  # Biến trỏ đến nút trước đó, ban đầu là None vì ở trước head
        while current:
            entity_id = getattr(current.value, 'id', None) # Nếu thực thể không có id thì trả về None
            if entity_id is not None and str(entity_id) == str(id_key):  # Nếu nút hiện tại không rỗng và có id cần xóa
                if previous:  # Nếu có nút trước đó => nút cần xóa không phải là head
                    previous.next = current.next  # Gán giá trị next của nút trước đó bằng giá trị next của nút hiện tại => bỏ qua nút hiện tại
                else:  # Nếu nút cần xóa là head
                    self.head = current.next  # Cập nhật head trỏ đến nút tiếp theo của nút hiện tại
                if current == self.tail:  # Nếu nút cần xóa là tail
                    self.tail = previous  # Cập nhật tail trỏ đến nút trước nút hiện tại
                return
            previous = current  # Cập nhật previous để trỏ đến nút hiện tại trước khi di chuyển sang nút tiếp theo
            current = current.next  # Di chuyển đến nút tiếp theo
    def find_by_attribute(self, attr_name, value): # Tìm kiếm nút có giá trị của một thuộc tính cụ thể, độ phức tạp O(n)
        s = str(attr_name) # Tên thuộc tính (vd: 'name', 'id', 'phone'...)
        if not s:  # Kiểm tra nếu tên thuộc tính là rỗng hoặc không hợp lệ
            print("Tên thuộc tính không hợp lệ.")
            return None
        s = str(value) 
        if not s:    # Kiểm tra nếu giá trị tìm kiếm là rỗng hoặc không hợp lệ
            print("Giá trị tìm kiếm không hợp lệ.")
            return None
        current = self.head
        while current:
            current_attr_value = getattr(current.value, attr_name, None) # Lấy giá trị của thuộc tính attr_name của nút hiện tại, nếu không tồn tại thì trả về None
            if current_attr_value == value: # Nếu giá trị của thuộc tính đó bằng với giá trị cần tìm
                return current.value  
            current = current.next # Di chuyển đến nút tiếp theo
        return None # Nếu không tìm thấy nút nào có giá trị cần tìm, trả về None
    def display(self):  # Hiển thị tất cả các giá trị trong danh sách, độ phức tạp O(n)
        current = self.head
        if not current: # Nếu danh sách rỗng
            print("") # In ra một dòng trống và trả về
            return
        output = str(current.value) # Xây dựng chuỗi kết quả bắt đầu với giá trị của nút đầu tiên
        current = current.next # Di chuyển đến nút tiếp theo
        while current:
            output += " ; " + str(current.value) # Thêm giá trị của nút hiện tại vào chuỗi kết quả, ngăn cách bằng " ; "
            current = current.next # Di chuyển đến nút tiếp theo
        print(output) # In ra chuỗi kết quả chứa tất cả các giá trị trong danh sách liên kết, ngăn cách bằng " ; "
    def __iter__(self): # Cho phép lặp qua các nút trong LinkedList bằng cách sử dụng vòng lặp for hoặc các hàm lặp khác, độ phức tạp O(n)
        current = self.head
        while current:
            yield current.value # Trả về giá trị của nút hiện tại và tạm dừng cho đến khi được gọi lại lần tiếp theo
            current = current.next # Di chuyển đến nút tiếp theo
