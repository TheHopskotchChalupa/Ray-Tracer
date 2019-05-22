import sys
import math

#vec3 is a copy of the TripleVecotr class by davidnuon from https://gist.github.com/davidnuon/3816736
class vec3:
    x = 0
    y = 0
    z = 0

    def __init__(self, x = 0, y = 0, z = 0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def x(self): return x

    def y(self): return y

    def z(self): return z

    # String represntation
    def __str__(self):
        return '<%s, %s, %s>' % (self.x, self.y, self.z)

    # Produce a copy of itself
    def __copy(self):
        return TripleVector(self.x, self.y, self.z)

    # Signing
    def __neg__(self):
        return TripleVector(-self.x, -self.y, -self.z)

    # Scalar Multiplication
    def __mul__(self, number):
        return TripleVector(self.x * number, self.y * number, self.z * number)

    def __rmul__(self, number):
        return self.__mul__(number)

    # Division
    def __div__(self, number):
        return self.__copy() * (number ** -1)

    # Arithmetic Operations
    def __add__(self, operand):
        return TripleVector(self.x + operand.x, self.y + operand.y, self.z + operand.z)

    def __sub__(self, operand):
        return self.__copy() + -operand

    # Cross product
    # cross = a ** b
    def __pow__(self, operand):
        return TripleVector(self.y * operand.z - self.z * operand.y,
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

'''
class vec3:
    e = [3]

    def vec3(): e = None
    def vec3(e0, e1, e2):
        e[0] = e0
        e[1] = e1
        e[2] = e2

    def x(): return e[0]
    def y(): return e[1]
    def z(): return e[2]
    def r(): return e[0]
    def g(): return e[1]
    def b(): return e[2]

    def __add__(): return self
    def __sub__(): return vec3(-e[0], -e[1], -e[2])
    def __getitem__(i): return e[i]

    def length():
        return sqrt(e[0]*e[0] + e[1]*e[1] + e[2]*e[2])
    def squared_length(): return e[0]*e[0] + e[1]*e[1] + e[2]*e[2]
    def make_unit_vector(): pass
'''

class ray:
    point_a = vec3()
    point_b = vec3()
    def ray(self): pass
    def ray(a, b):
        point_a = a
        point_b = b
    def origin(self): return point_a
    def direction(self): return point_b
    def point_at_parameter(r): return point_a + t*point_b

''' ##original ppm generaotr##
nx = 200
ny = 100
output = open("test.ppm", "w+")
output.write("P3\n%i %i\n255\n" %(nx, ny))
for i in range(ny-1, -1, -1):
    for j in range(0, nx, 1):
        col = vec3(float(j)/float(nx), float(i)/float(ny), 0.2)
        ir = int(255.9 * col.x)
        ig = int(255.9 * col.y)
        ib = int(255.9 * col.z)
        output.write("%i %i %i\n" %(ir, ig, ib))
'''

output.close