import math
from transform import *
from vector import *

class Polygon:
    def __init__(self, vertices=[], triangles=[], area=0):
        self.vertices = vertices
        self.shape = [v for v in self.vertices]
        self.triangles = triangles
        self._area = area
    
    def area(self):
        return self._area
        

class Circle:
    def __init__(self, r):
        self.radius = r

    def area(self):
        return math.pi * self.radius * self.radius

class Body:
    def __init__(self, position, density, shape, restitution, static=False):
        self.position = position
        self.linearVelocity = Vector(0)
        self.rotation = 0
        self.rotationalVelocity = 0

        self.restitution = restitution
        self.area = shape.area()
        self.density = density
        self.mass = self.area * self.density

        self.static = False
        self.shapetype = shape.__class__.__name__
        self.shape = shape

        self.static = False

        if(self.shapetype == "Polygon"):
            self.updateVertices()
    
    def step(self, time):
        self.position += self.linearVelocity * time
        self.rotation += self.rotationalVelocity * time
        if(self.shapetype == "Polygon"):
            self.updateVertices()

    def updateVertices(self):
        transform = Transform(self.position, self.rotation)
        for v in range(len(self.shape.vertices)):
            self.shape.vertices[v] = Vector.transform(self.shape.shape[v], transform)
        return self.shape.shape

    def Move(self, amount):
        self.position += amount
        if(self.shapetype == "Polygon"):
            self.updateVertices()
    
    def MoveTo(self, pos):
        self.position = pos
        if(self.shapetype == "Polygon"):
            self.updateVertices()
    
    def Rotate(self, angle):
        self.rotation += angle
        if(self.shapetype == "Polygon"):
            self.updateVertices()


def GenerateBox(width, height):
    left = -width / 2
    right = width / 2
    bottom = -height / 2
    top = height / 2

    vertices = [Vector(left, top),
                Vector(right, top),
                Vector(right, bottom),
                Vector(left, bottom)]

    triangles = [[0, 1, 2],
                 [0, 2, 3]]
    
    return Polygon(vertices, triangles, width * height)

def GenerateCircle(radius):
    return Circle(radius)