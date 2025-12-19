import math
from common import *

class Vector:
    def __init__(self, x, y=None):
        self.x = x
        if(y == None):
            self.y = x
        else:
            self.y = y
    
    def __add__(self, other):
        if(isinstance(other, (int, float))):
            return Vector(self.x + other, self.y + other)
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if(isinstance(other, (int, float))):
            return Vector(self.x - other, self.y - other)
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if(isinstance(other, (int, float))):
            return Vector(self.x * other, self.y * other)
        return Vector(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        if(isinstance(other, (int, float))):
            return Vector(self.x / other, self.y / other)
        return Vector(self.x / other.x, self.y / other.y)
    
    def __floordiv__(self, other):
        if(isinstance(other, (int, float))):
            return Vector(self.x // other, self.y // other)
        return Vector(self.x // other.x, self.y // other.y)
    
    def __neg__(self):
        return Vector(-self.x, -self.y)

    def equals(self, other):
        return self.x == other.x and self.y == other.y

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        mag = self.magnitude()
        self.x /= mag
        self.y /= mag
    
    def normalized(self):
        mag = self.magnitude()
        return Vector(self.x / mag, self.y / mag)
    
    def as_list(self):
        return [self.x, self.y]
    
    def toScreen(self):
        return [HALFWIDTH + self.x, HALFHEIGHT - self.y]

    @staticmethod
    def distance(subject, other):
        return math.sqrt((subject.x - other.x) ** 2 + (subject.y - other.y) ** 2)
    
    @staticmethod
    def dot(a, b):
        return a.x * b.x + a.y * b.y
    
    @staticmethod
    def cross(a, b):
        return a.x * b.y - a.y * b.x
