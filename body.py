import math
from vector import *


class Body:
    def __init__(self, position, vertices, mass, restitution=0.5, color=(0, 0, 0)):
        
        self.shape = [v for v in vertices]
        self.mass = mass
        self.restitution = restitution
        self.color = color

        # current state
        self.vertices = [v for v in vertices]
        self.position = position
        self.rotation = 0
        
        # variables
        self.velocity = Vector(0)
        self.acceleration = Vector(0)

        # initializing
        self.updateVertices()

    def rotate(self, amount):
        self.rotation += amount

    def move(self, amount):
        self.position += amount

    def updateVertices(self):
        transform = Transform(self.position, self.rotation)
        for v in range(len(self.vertices)):
            self.vertices[v] = Vector.transform(self.shape[v], transform)
        return self.vertices

    def accelerate(self, amount):
        self.acceleration = amount

    def step(self, dt):
        self.position += self.velocity * dt + (self.acceleration * dt ** 2)/2
        self.velocity += self.acceleration * dt
    
    def copy(self):
        return Body(self.position, self.vertices, self.mass)

def generateVertices(sides, vertexDist):
    vertices = []
    for i in range(sides):
        angle = (i / sides) * 2 * math.pi - (math.pi)/sides
        vertices.append(Vector(math.sin(angle), math.cos(angle)) * vertexDist)
    return vertices

def generateBox(width, height):
    left = -width / 2
    right = width / 2
    bottom = -height / 2
    top = height / 2

    vertices = [Vector(left, top),
                Vector(right, top),
                Vector(right, bottom),
                Vector(left, bottom)]

    return vertices