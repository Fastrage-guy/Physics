import math
from physmath import *
from common import *

class AABB:
    def __init__(self, minimum=Vector(0), maximum=Vector(0)):
        self.minimum = minimum
        self.maximum = maximum
    
    def toRect(self, halfw, halfh):
        starting = self.minimum
        size = self.maximum - self.minimum
        return [halfw + starting.x, halfh - starting.y - size.y, size.x, size.y]
    
    def dimensions(self):
        return self.maximum - self.minimum

    @staticmethod
    def getfrom(vertices):
        minimum = Vector(float('inf'))
        maximum = Vector(float('-inf'))

        for v in vertices:
            if(v.x < minimum.x): minimum.x = v.x
            if(v.y < minimum.y): minimum.y = v.y
            if(v.x > maximum.x): maximum.x = v.x
            if(v.y > maximum.y): maximum.y = v.y
        
        return AABB(minimum, maximum)

    def expanded(self, amount):
        return AABB(self.minimum - amount/2, self.maximum + amount/2)

class Body:
    def __init__(self, position, shape, shapeParams, mass, restitution=0.5, color=(0, 0, 0)):
        # constants
        self.shapetype = shape
        if(shape == ShapeType.polygon):
            self.shape = [v for v in shapeParams]
        else:
            self.shape = shapeParams
        self.shapeParams = shapeParams
        self.mass = mass
        self.restitution = restitution
        self.color = color

        # position related stuff
        self.position = position
        self.velocity = Vector()
        self.acceleration = Vector()
        if(shape == ShapeType.polygon):
            self.vertices = [v for v in shapeParams]
        else:
            self.radius = shapeParams

        # rotation related stuff
        self.inertia = 0
        self.rotation = 0
        self.angularVelocity = 0
        if(self.shapetype == ShapeType.polygon): self.updateVertices()
        self.updateAABB()
    
    def updateVertices(self):
        sinAngle = math.sin(self.rotation)
        cosAngle = math.cos(self.rotation)
        for v in range(len(self.vertices)):
            self.vertices[v] = Vector(
                cosAngle * self.vertices[v].x - sinAngle * self.vertices[v].y + self.position.x, 
                sinAngle * self.vertices[v].x + cosAngle * self.vertices[v].y + self.position.y
            )
        return self.vertices
    
    def updateAABB(self):
        if(self.shapetype == ShapeType.polygon):
            minimum = Vector(float('inf'))
            maximum = Vector(float('-inf'))

            for v in self.vertices:
                if(v.x < minimum.x): minimum.x = v.x
                if(v.y < minimum.y): minimum.y = v.y

                if(v.x > maximum.x): maximum.x = v.x
                if(v.y > maximum.y): maximum.y = v.y
            
            self.aabb = AABB(minimum, maximum)
        else:
            minimum = self.position - self.shape
            maximum = self.position + self.shape
            self.aabb = AABB(minimum, maximum)
        
        return self.aabb
    
    def updateShape(self):
        if(self.shapetype == ShapeType.polygon):
            self.updateVertices()
        self.updateAABB()

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

def generateVertices(sides, vertexDist):
    vertices = []
    for i in range(sides):
        angle = (i / sides) * 2 * math.pi - (math.pi)/sides
        vertices.append(Vector(math.sin(angle), math.cos(angle)) * vertexDist)
    return vertices