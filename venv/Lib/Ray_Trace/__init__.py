import sys
import math

nx = 200
ny = 100
output = open("test.ppm", "w+")
output.write("P3\n%i %i\n255\n" %(nx, ny))
for i in range(ny-1, -1, -1):
    for j in range(0, nx, 1):
        r = float(j)/float(nx)
        g = float(i)/float(ny)
        b = 0.2
        ir = int(255.9 * r)
        ig = int(255.9 * g)
        ib = int(255.9 * b)
        output.write("%i %i %i\n" %(ir, ig, ib))

output.close


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