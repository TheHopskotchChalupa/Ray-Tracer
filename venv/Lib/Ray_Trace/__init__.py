import sys
import math
import random
import time
import numba
import numpy

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
    def __init__(self, a = None, b = None):
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

class material:

    def scatter(self, r_in: ray, rec, attenuation: vec3, scattered: ray):
        return

class hit_record:
    t = None
    p = vec3()
    normal = vec3()
    mat = material()

    def __init__(self, set_t = None, set_p = None, set_normal = None, set_mat = None):
        self.t = set_t
        self.p = set_p
        self.normal = set_normal
        self.mat = set_mat

    def __str__(self):
        return '<t: %s\n p: %s\n normal: %s\n material: %s >' % (self.t, self.p, self.normal, self.mat)

def reflect(v: vec3, n: vec3):
    return v - 2 * (v & n) * n

def refract(v, n, ni_over_nt, refracted):
    uv = unit_vector(v)
    dt = uv & n
    discriminant = 1.0 - ni_over_nt * ni_over_nt * (1 - dt * dt)
    if (discriminant > 0):
        refracted = ni_over_nt * (uv - n * dt) - n * math.sqrt(discriminant)
        return True
    else:
        return False

def schlick(cosine, ref):
    r0 = (1-ref) / (1+ref)
    r0 = r0 * r0
    return r0 + (1-r0) * ((1 - cosine) ** 5)

class lambertian(material):
    albedo = vec3()

    def __init__(self, a: vec3): self.albedo = a

    def scatter(self, r_in: ray, rec, attenuation: vec3, scattered: ray):
        scattered.point_a = ray(rec.p, rec.p + rec.normal + random_in_unit_sphere() - rec.p).point_a
        scattered.point_b = ray(rec.p, rec.p + rec.normal + random_in_unit_sphere() - rec.p).point_b
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return True

class metal(material):
    albedo = vec3()
    fuzz = None

    def __init__(self, a: vec3, f):
        self.albedo = a
        if (f < 1): self.fuzz = f
        else: self.fuzz = 1

    def scatter(self, r_in: ray, rec, attenuation: vec3, scattered: ray):
        reflected = reflect(unit_vector(r_in.direction()), rec.normal)
        scattered.point_a = ray(rec.p, reflected + self.fuzz * random_in_unit_sphere()).point_a
        scattered.point_b = ray(rec.p, reflected + self.fuzz * random_in_unit_sphere()).point_b
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return ((scattered.direction() & rec.normal) > 0)

class dielectric(material):
    ref = None

    def __init__(self, ri): self.ref = ri

    def scatter(self, r_in: ray, rec, attenuation: vec3, scattered: ray):
        outward_normal = vec3()
        reflected = reflect(r_in.direction(), rec.normal)
        ni_over_nt = None
        attenuation.x = 1.0
        attenuation.y = 1.0
        attenuation.z = 1.0
        refracted = vec3()
        reflect_prob = None
        cosine = None
        if ((r_in.direction() & (rec.normal)) > 0):
            outward_normal = -(rec.normal)
            ni_over_nt = self.ref
            cosine = self.ref * (r_in.direction() & rec.normal) / r_in.direction().length()
        else:
            outward_normal = rec.normal
            ni_over_nt = 1.0 / self.ref
            cosine = -(r_in.direction() & rec.normal) / r_in.direction().length()
        if (refract(r_in.direction(), outward_normal, ni_over_nt, refracted)):
            reflect_prob = schlick(cosine, self.ref)
        else:
            scattered.point_a = ray(rec.p, reflected).point_a
            scattered.point_b = ray(rec.p, reflected).point_b
            reflect_prob = 1.0
        if (random.random() < reflect_prob):
            scattered.point_a = ray(rec.p, reflected).point_a
            scattered.point_b = ray(rec.p, reflected).point_b
        else:
            scattered.point_a = ray(rec.p, reflected).point_a
            scattered.point_b = ray(rec.p, reflected).point_b
        return True

class hitable:
    def hit(self, r: ray, t_min: float, t_max: float, rec: hit_record): pass

class sphere(hitable):
    center = vec3();
    radius = None
    mat = material()

    def __init__(self, cen: vec3, r: float, m: material):
        self.center = cen
        self.radius = r
        self.mat = m

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
        self.list = l
        self.list_size = n

    def hit(self, r: ray, t_min: float, t_max: float, rec: hit_record):
        temp_rec = hit_record()
        hit_anything = False
        closest_so_far = t_max
        for i in range(0, self.list_size - 1, 1):
            if(self.list[i].hit(r, t_min, closest_so_far, temp_rec)):
                hit_anything = True
                closest_so_far= temp_rec.t
                rec.t = temp_rec.t
                rec.p = temp_rec.p
                rec.normal = temp_rec.normal
                rec.mat = self.list[i].mat
        return hit_anything

def random_in_unit_sphere():
    p = vec3()

    p = 2.0 * vec3(random.random(), random.random(), random.random()) - vec3(1,1,1)
    while(p & p >= 1.0):
        p = 2.0 * vec3(random.random(), random.random(), random.random()) - vec3(1,1,1)

    return p

def random_in_unit_disk():
    p = vec3()

    p = 2.0 * vec3(random.random(), random.random(), 0) - vec3(1, 1, 0)
    while (p & p >= 1.0):
        p = 2.0 * vec3(random.random(), random.random(), 0) - vec3(1, 1, 0)

    return p

def color(r, world: hitable, depth):
    rec = hit_record()
    if (world.hit(r, 0.001, sys.float_info.max, rec)):
        scattered = ray()
        attenuation = vec3()
        if ((depth < 50) & (rec.mat.scatter(r, rec, attenuation, scattered))):
            return attenuation * color(scattered, world, depth + 1).x
        else:
            return vec3(0, 0, 0)
    else:
        unit_direction = unit_vector(r.direction())
        t = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - t) * vec3(1.0, 1.0, 1.0) + t * vec3(0.5, 0.7, 1.0)

class camera:
    u = v = w = None
    lower_left_corner = None
    horizontal = None
    vertical = None
    origin = None
    lens_radius = None

    def __init__(self, lookfrom, lookat, vup, vfov, aspect, aperture, focus_dist):
        self.lens_radius = aperture / 2
        theta = vfov * math.pi/180
        half_height = math.tan(theta/2)
        half_width = aspect * half_height
        self.origin = lookfrom
        self.w = unit_vector(lookfrom - lookat)
        self.u = unit_vector(vup ** self.w)
        self.v = self.w ** self.u
        self.lower_left_corner = self.origin - half_width * focus_dist \
                                 * self.u - half_height * focus_dist * self.v - focus_dist * self.w
        self.horizontal = 2 * half_width * focus_dist * self.u
        self.vertical = 2 * half_height * focus_dist * self.v

    def get_ray(self, s: float, t: float):
        rd = self.lens_radius * random_in_unit_disk()
        offset = self.u * rd.x + self.v * rd.y
        return ray(self.origin + offset, self.lower_left_corner
                   + s * self.horizontal + t * self.vertical - self.origin - offset)


def random_scene():
    list = []
    list.insert(0, sphere(vec3(0, -1000, 0), 1000, lambertian(vec3(0.5, 0.5, 0.5))))
    i = 1
    for a in range(0, 22):
        for b in range(0, 22):
            choose_mat = random.random()
            center = vec3(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())
            if ((center - vec3(4, 0.2, 0)).length() > 0.9):
                if (choose_mat < 0.8):
                    x = random.random() * random.random()
                    y = random.random() * random.random()
                    z = random.random() * random.random()
                    list.insert(i, sphere(center, 0.2, lambertian(vec3(x, y, z))))
                elif (choose_mat < 0.95):
                    x = 0.5 * (1 + random.random())
                    y = 0.5 * (1 + random.random())
                    z = 0.5 * (1 + random.random())
                    f = 0.5 * (1 + random.random())
                    list.insert(i, sphere(center, 0.2,
                            metal(vec3(x, y, z), f)))
                else:
                    list.insert(i, sphere(center, 0.2, dielectric(1.5)))
            i = i + 1

    i += 1
    list.insert(i, sphere(vec3(0, 1, 0), 1.0, dielectric(1.5)))
    i += 1
    list.insert(i, sphere(vec3(-4, 1, 0), 1.0, lambertian(vec3(0.4, 0.2, 0.1))))
    i += 1
    list.insert(i, sphere(vec3(4, 1, 0), 1.0, metal(vec3(0.7, 0.6, 0.5), 0.0)))

    return hitable_list(list, i - 1)

def run():
    start = time.time()
    nx = 20
    ny = 10
    nz = 10
    '''
    lower_left_corner = vec3(-2.0, -1.0, -1.0)
    horizontal = vec3(4.0, 0.0, 0.0)
    vertical = vec3(0.0, 2.0, 0.0)
    origin = vec3(0.0, 0.0, 0.0)
    '''

    output = open("test.ppm", "w+")
    output.write("P3\n%i %i\n255\n" %(nx, ny))
    list = []
    world = random_scene()
    '''
    world.list.insert(0, sphere(vec3(0, 0, -1), 0.5, lambertian(vec3(0, 0, 1))))
    world.list.insert(1, sphere(vec3(0, -100.5, -1), 100, lambertian(vec3(0.8, 0.8, 0.0))))
    world.list.insert(2, sphere(vec3(-1, 0, -1), 0.5, metal(vec3(0.8, 0.6, 0.2), 0)))
    world.list.insert(3, sphere(vec3(1, 0, -1), 0.5, dielectric(1.5)))
    '''
    lookfrom = vec3(3, 3, 2)
    lookat = vec3(0, 0, -1)
    cam = camera(lookfrom, lookat, vec3(0, 1, 0), 100, nx/ny, 2.0, (lookfrom - lookat).length())
    for i in range(ny-1, -1, -1):
        for j in range(0, nx, 1):
            col = vec3(0, 0, 0)
            for k in range(0, nz, 1):
                u = float(j + random.random()) / float(nx)
                v = float(i + random.random()) / float(ny)
                r = cam.get_ray(u, v)
                p = r.point_at_parameter(2.0)
                col += color(r, world, 0)
            col /= float(nz)
            col = vec3(math.sqrt(col.x), math.sqrt(col.y), math.sqrt(col.z))
            ir = int(255.99 * col.x)
            ig = int(255.99 * col.y)
            ib = int(255.99 * col.z)
            output.write("%i %i %i\n" %(ir, ig, ib))

    output.close()
    print("Completed in %.2f seconds" %(time.time() - start))

run()