class vec3:
    x = 0
    y = 0
    z = 0

    def __init__(self, x = None, y = None, z = None):
        self.x = x
        self.y = y
        self.z = z

    def x(self): return x

    def y(self): return y

    def z(self): return z

    # String represntation
    def __str__(self):
        return '<%s, %s, %s>' % (self.x, self.y, self.z)

    # Produce a copy of itself
    def __copy(self):
        return vec3(self.x, self.y, self.z)

    # Signing
    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z)

    # Scalar Multiplication
    def __mul__(self, number):
        return vec3(self.x * number, self.y * number, self.z * number)

    def __rmul__(self, number):
        return self.__mul__(number)

    # Division
    def __truediv__(self, number):
        return self.__copy() * (number ** -1)

    # Arithmetic Operations
    def __add__(self, operand):
        return vec3(self.x + operand.x, self.y + operand.y, self.z + operand.z)

    def __sub__(self, operand):
        return self.__copy() + -operand

    # Cross product
    # cross = a ** b
    def __pow__(self, operand):
        return vec3(self.y * operand.z - self.z * operand.y,
                            self.z * operand.x - self.x * operand.z,
                            self.z * operand.y - self.y * operand.x)

    # Dot Project
    # dp = a & b
    def __and__(self, operand):
        return (self.x * operand.x) + \
               (self.y * operand.y) + \
               (self.z * operand.z)

    # Operations

    def normal(self):
        return self.__copy() / self.magnitude()

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** (.5)

    def length(self): return math.sqrt(self.x**2 + self.y**2 + self.z**2)