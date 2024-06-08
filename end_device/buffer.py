BUFFER_MAX_SIZE = 2048

class UtilsBuffer:
    def __init__(self, size_of_object = 1):
        self.tail = 0
        self.head = 0
        self.count = 0
        self.size_of_object = size_of_object
        self.buffer = bytearray(BUFFER_MAX_SIZE)

    def push(self, obj):
        if not isinstance(obj, bytes):
            raise TypeError("Object must be of type bytes")
        if len(obj) != self.size_of_object:
            raise ValueError("Object size must match buffer object size")
        
        if self.is_full():
            return False

        for i in range(self.size_of_object):
            self.buffer[self.head] = obj[i]
            self.head = (self.head + 1) % BUFFER_MAX_SIZE
        return True

    def pop(self):
        if not self.is_available():
            return None

        data = bytearray(self.size_of_object)
        for i in range(self.size_of_object):
            data[i] = self.buffer[self.tail]
            self.tail = (self.tail + 1) % BUFFER_MAX_SIZE
        return bytes(data)

    def is_available(self):
        if self.head >= self.tail:
            return (self.head - self.tail >= self.size_of_object)
        else:
            return (BUFFER_MAX_SIZE - self.tail + self.head >= self.size_of_object)

    def is_full(self):
        if self.head >= self.tail:
            remain = BUFFER_MAX_SIZE - (self.head - self.tail)
        else:
            remain = self.tail - self.head
        return remain < self.size_of_object

    def drop_all(self):
        self.head = 0
        self.tail = 0
        self.count = 0
        self.buffer = bytearray(BUFFER_MAX_SIZE)
        return True
