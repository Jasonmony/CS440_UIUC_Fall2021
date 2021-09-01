class B:
    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return f'B ({self.a})'

    def __str__(self):
        return f'B with {self.a}'

    def __bytes__(self):
        return self.a.to_bytes(4, byteorder='big')

    def __format__(self, spec):
        if spec == 'f':
            return str(self.a)
        return str(self)

b = B(10)
print(repr(b))
print(str(b))
print(bytes(b))
print(format(b, 'f'))