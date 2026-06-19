import ctypes
from structures.linked_list import LinkedList


class HashEntry:
    """Object luu cap key-value, thay cho tuple/dict native."""

    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, size=1024):
        self._size = size
        ArrayType = ctypes.py_object * self._size
        self._buckets = ArrayType()

        for i in range(self._size):
            self._buckets[i] = LinkedList()

    def _hash(self, key):
        return hash(key) % self._size

    def set(self, key, value):
        index = self._hash(key)
        bucket = self._buckets[index]

        current = bucket.head
        while current:
            if current.value.key == key:
                current.value.value = value
                return
            current = current.next

        bucket.append(HashEntry(key, value))

    def get(self, key, default=None):
        index = self._hash(key)
        bucket = self._buckets[index]

        current = bucket.head
        while current:
            if current.value.key == key:
                return current.value.value
            current = current.next

        return default

    def remove(self, key):
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
        current = self._buckets[self._hash(key)].head
        while current:
            if current.value.key == key:
                return True
            current = current.next
        return False

    def keys(self):
        result = LinkedList()
        for i in range(self._size):
            current = self._buckets[i].head
            while current:
                result.append(current.value.key)
                current = current.next
        return result

    def values(self):
        result = LinkedList()
        for i in range(self._size):
            current = self._buckets[i].head
            while current:
                result.append(current.value.value)
                current = current.next
        return result

    def items(self):
        result = LinkedList()
        for i in range(self._size):
            current = self._buckets[i].head
            while current:
                result.append(current.value)
                current = current.next
        return result
