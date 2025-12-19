import math

class Vector:
    def __init__(self, x=0, y=False):
        self.x = x
        if(y == False):
            self.y = x
        else:
            self.y = y
    
    def set(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if(isinstance(other, int) or isinstance(other, float)):
            other = Vector(other, other)
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if(isinstance(other, int) or isinstance(other, float)):
            other = Vector(other, other)
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if(isinstance(other, int) or isinstance(other, float)):
            other = Vector(other, other)
        return Vector(self.x * other.x, self.y * other.y)
    
    def __truediv__(self, other):
        if(isinstance(other, int) or isinstance(other, float)):
            other = Vector(other, other)
        return Vector(self.x / other.x, self.y / other.y)
    
    def __str__(self):
        return f"[x: {self.x}, y: {self.y}]"
    
    def __repr__(self):
        return self.__str__()
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def magnitude(self):
        return (self.x**2 + self.y**2)**0.5
    
    def normalized(self):
        mag = self.magnitude()
        if(mag == 0):
            return Vector(0, 0)
        else:
            return self / mag

    def normalize(self):
        mag = self.magnitude()
        self.x = self.x / mag
        self.y = self.y / mag

    def normal(self):
        return Vector(-self.y, self.x).normalized()
    
    def asList(self):
        return [self.x, self.y]
    
    @staticmethod
    def dot(v1, v2):
        return v1.x*v2.x + v1.y*v2.y
    
    @staticmethod
    def cross(v1, v2):
        return v1.x*v2.y - v1.y*v2.x

class Matrix:
    def __init__(self, rows, cols, data=[]):
        self.rows = rows
        self.cols = cols
        self.data = data

        for i in range(rows):
            self.data.append([])
            for j in range(cols):
                self.data[i].append(0)
    
    def multiplyVector(self, vector):
        result = Vector(0, 0)
        result.x = self.data[0][0]*vector.x + self.data[0][1]*vector.y
        result.y = self.data[1][0]*vector.x + self.data[1][1]*vector.y
        return result
    
    @staticmethod
    def rotation(angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        return Matrix(2, 2, [
            [cos, -sin],
            [sin, cos]
        ])

def PolygonMOI(mass, vertices):
    # I have no idea what i'm doing
    totalTop = 0
    totalBottom = 0

    lenVertices = len(vertices)
    for n in range(len(vertices)):
        v1 = vertices[n]
        v2 = vertices[(n + 1) % lenVertices]
        v1Mag = v1.magnitude()
        v2Mag = v2.magnitude()

        normcross = math.acos(Vector.dot(v1, v2) / (v1Mag * v2Mag)) * v1Mag * v2Mag
        totalTop += normcross * Vector.dot(v1, v1) + Vector.dot(v1, v2) + Vector.dot(v2, v2)

        totalBottom += normcross
    totalBottom *= 6

    return mass * (totalTop/totalBottom)

def generateVertices(sides, vertexDist):
    vertices = []
    for i in range(sides):
        angle = (i / sides) * 2 * math.pi - (math.pi)/sides
        vertices.append(Vector(math.sin(angle), math.cos(angle)) * vertexDist)
    return vertices