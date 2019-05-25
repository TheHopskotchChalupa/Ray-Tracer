import sys
import math
from typing import NamedTuple
'''

##original ppm generaotr##
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

output.close

##old vec3##
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
#vec3 is a modified copy of the TripleVecotr class by davidnuon from https://gist.github.com/davidnuon/3816736
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

class ray:
    point_a = vec3()
    point_b = vec3()
    def __init__(self, a, b):
        self.point_a = a
        self.point_b = b
    def origin(self): return self.point_a
    def direction(self): return self.point_b
    def point_at_parameter(self, t): return self.point_a + t * self.point_b


def unit_vector(v = vec3()):
    return v / v.length()

def hit_sphere(center: vec3, radius, r: ray):
    oc = r.origin() - center
    a = r.direction() & r.direction()
    b = 2.0 * (oc & r.direction())
    c = (oc & oc) - radius*radius
    discriminant = (b*b) - 4 * a * c
    if(discriminant < 0):
        return -1.0
    else:
        return ((-b) - (math.sqrt(discriminant))) / (2.0*a)

class hit_record:
    t = None
    p = vec3()
    normal = vec3()

    def __init__(self, set_t = None, set_p = None, set_normal = None):
        t = set_t
        p = set_p
        normal = set_normal

    def __str__(self):
        return '<t: %s\n p: %s\n normal: %s>' % (self.t, self.p, self.normal)

class hitable:
    def hit(self, r: ray, t_min: float, t_max: float, rec: hit_record): pass

class sphere(hitable):
    center = vec3();
    radius = None
    def __init__(self, cen: vec3, r: float):
        self.center = cen
        self.radius = r

    def hit(self, r: ray, t_min: float, t_max: float, rec):
        oc = r.origin() - self.center
        a = r.direction() & r.direction()
        b = oc & r.direction()
        c = (oc & oc) - self.radius * self.radius
        discriminant = b ** 2 - a * c
        if (discriminant > 0):
            temp = (-b - math.sqrt(b * b - a * c)) / a
            if ((temp < t_max) & (temp > t_min)):
                rec.t = temp
                rec.p = r.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center) / self.radius
                return True
            temp = (-b + math.sqrt(b * b - a * c)) / a
            if ((temp < t_max) & (temp > t_min)):
                rec.t = temp
                rec.p = r.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center) / self.radius
                return True
        return False

class hitable_list(hitable):
    list = None
    list_size = 0

    def __init__(self, l: hitable, n: int):
        self.list = []
        self.list_size = n

    def hit(self, r: ray, t_min: float, t_max: float, rec: hit_record):
        temp_rec = hit_record()
        hit_anything = False
        closest_so_far = t_max
        for i in range(0, self.list_size, 1):
            if(list[i].hit(r, t_min, closest_so_far, temp_rec)):
                hit_anything = True
                closest_so_far= temp_rec.t
                rec.t = temp_rec.t
                rec.p = temp_rec.p
                rec.normal = temp_rec.normal
        return hit_anything


def color(r, world: hitable):
    rec = hit_record()
    #t = hit_sphere(vec3(0,0,-1), 0.5 , r)
    if (world.hit(r, 0.0, sys.float_info.max, rec)):
        return 0.5 * vec3(rec.normal.x + 1, rec.normal.y + 1, rec.normal.z + 1)
    else:
        unit_direction = unit_vector(r.direction())
        t = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - t) * vec3(1.0, 1.0, 1.0) + t * vec3(0.5, 0.7, 1.0)

nx = 1000
ny = 500
output = open("test.ppm", "w+")
output.write("P3\n%i %i\n255\n" %(nx, ny))
lower_left_corner = vec3(-2.0, -1.0, -1.0)
horizontal = vec3(4.0, 0.0, 0.0)
vertical = vec3(0.0, 2.0, 0.0)
origin = vec3(0.0, 0.0, 0.0)
list = []
list.insert(0, sphere(vec3(0, 0, -1), 0.5))
list.insert(1, sphere(vec3(0, -100.5, -1), 100))
world = hitable_list(list, 2)
for j in range(ny-1, -1, -1):
    for i in range(0, nx, 1):
        u = float(i) / float(nx)
        v = float(j) / float(ny)
        r = ray(origin, lower_left_corner + u * horizontal + v * vertical)
        p = r.point_at_parameter(2.0)
        col = color(r, world)
        ir = int(255.99 * col.x)
        ig = int(255.99 * col.y)
        ib = int(255.99 * col.z)
        output.write("%i %i %i\n" %(ir, ig, ib))

output.close()