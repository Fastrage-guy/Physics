import math

class Vector:
    def __init__(self, x=0.0, y=False):
        self.x = x
        if not y:
            self.y = x
        else:
            self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        else:
            return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)
        else:
            return Vector(self.x / other, self.y / other)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            return Vector(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            return Vector(self.x - other, self.y - other)

    def MagSquared(self):
        return self.x * self.x + self.y * self.y

    def Magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def Rotate(self, radians):
        c = math.cos(radians)
        s = math.sin(radians)
        xp = self.x * c - self.y * s
        yp = self.x * s + self.y * c
        self.x = xp
        self.y = yp

    def Normalize(self):
        mag = self.Magnitude()
        if mag > 0:
            invmag = 1.0 / mag
            self.x *= invmag
            self.y *= invmag
        else:
            self.x = 0
            self.y = 0
        
    def Normalized(self):
        mag = self.Magnitude()
        if mag > 0:
            invmag = 1.0 / mag
            return Vector(self.x * invmag, self.y * invmag)
        else:
            return Vector(0, 0)
    
    def AsList(self):
        return [self.x, self.y]

    @staticmethod
    def fromList(l):
        return Vector(l[0], l[1])

class Mat2:
    def __init__(self, a=0.0, b=0.0, c=0.0, d=0.0, radians=0.0):
        if isinstance(radians, float):
            c = math.cos(radians)
            s = math.sin(radians)
            self.m00 = c
            self.m01 = -s
            self.m10 = s
            self.m11 = c
        else:
            self.m00 = a
            self.m01 = b
            self.m10 = c
            self.m11 = d

    def set(self, radians):
        c = math.cos(radians)
        s = math.sin(radians)
        self.m00 = c
        self.m01 = -s
        self.m10 = s
        self.m11 = c

    def abs(self):
        return Mat2(abs(self.m00), abs(self.m01), abs(self.m10), abs(self.m11))

    def axis_x(self):
        return Vector(self.m00, self.m10)

    def axis_y(self):
        return Vector(self.m01, self.m11)

    def transpose(self):
        return Mat2(self.m00, self.m10, self.m01, self.m11)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.m00 * other.x + self.m01 * other.y, self.m10 * other.x + self.m11 * other.y)
        elif isinstance(other, Mat2):
            return Mat2(
                self.m00 * other.m00 + self.m01 * other.m10,
                self.m00 * other.m01 + self.m01 * other.m11,
                self.m10 * other.m00 + self.m11 * other.m10,
                self.m10 * other.m01 + self.m11 * other.m11
            )

def DotProduct(a, b):
    return a.x * b.x + a.y * b.y

def CrossProduct(a, b):
    return a.x * b.y - a.y * b.x

def Equal(a, b, tolerance=0.01):
    return abs(a-b) < tolerance

def Clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def BiasGreaterThan(a, b):
    k_biasRelative = 0.95
    k_biasAbsolute = 0.01
    return a >= b * k_biasRelative + a * k_biasAbsolute