import ctypes
from structures.linked_list import LinkedList

class HashEntry:
    """Lớp đối tượng lưu trữ cặp Key-Value, thay thế cho Tuples/Dict"""
    def __init__(self, key, value):
        self.key = key
        self.value = value

class HashTable:
    def __init__(self, size=1024):
        self._size = size
        
        # SỬ DỤNG CTYPES: Cấp phát mảng tĩnh kiểu C, KHÔNG dùng mảng động [] của Python
        # Đây là minh chứng rõ ràng nhất cho việc tự cài đặt cấu trúc dữ liệu cấp thấp
        ArrayType = ctypes.py_object * self._size
        self._buckets = ArrayType()
        
        # Khởi tạo mỗi bucket là một LinkedList rỗng
        for i in range(self._size):
            self._buckets[i] = LinkedList()

    def _hash(self, key):
        """Hàm băm cơ bản chia lấy dư"""
        return hash(key) % self._size

    def set(self, key, value):
        """Thêm hoặc cập nhật giá trị"""
        index = self._hash(key)
        bucket = self._buckets[index]
        
        # Duyệt LinkedList để tìm xem key đã tồn tại chưa
        current = bucket.head
        while current:
            if current.value.key == key:
                # Cập nhật giá trị nếu key đã tồn tại
                current.value.value = value
                return
            current = current.next
            
        # Nếu chưa tồn tại, nối thêm HashEntry mới vào cuối LinkedList
        bucket.append(HashEntry(key, value))

    def get(self, key, default=None):
        """Lấy giá trị theo key"""
        index = self._hash(key)
        bucket = self._buckets[index]
        
        current = bucket.head
        while current:
            if current.value.key == key:
                return current.value.value
            current = current.next
            
        return default

    def remove(self, key):
        """Xóa một phần tử khỏi Hash Table"""
        index = self._hash(key)
        bucket = self._buckets[index]
        
        current = bucket.head
        previous = None
        
        while current:
            if current.value.key == key:
                if previous:
                    previous.next = current.next
                else:
                    bucket.head = current.next
                    
                if current == bucket.tail:
                    bucket.tail = previous
                return True
            previous = current
            current = current.next
            
        return False

    def contains(self, key):
        """Kiểm tra key có tồn tại không"""
        return self.get(key) is not None

    def keys(self):
        """Trả về danh sách các key dưới dạng LinkedList thay vì List []"""
        result = LinkedList()
        for i in range(self._size):
            current = self._buckets[i].head
            while current:
                result.append(current.value.key)
                current = current.next
        return result

    def values(self):
        """Trả về danh sách các value dưới dạng LinkedList thay vì List []"""
        result = LinkedList()
        for i in range(self._size):
            current = self._buckets[i].head
            while current:
                result.append(current.value.value)
                current = current.next
        return result