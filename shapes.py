from util import *

class Circle:
    def __init__(self, x, y, r):
        self.originalPosition = Vector(x, y)
        self.localPosition = Vector(x, y)
        self.parentPosition = Vector(0, 0)
        self.worldPosition = self.localPosition + self.parentPosition
        self.radius = r
        self.angle = 0

        #temporary for separating axis theorem
        self.vertices = [False, False]
    
    def updateData(self, position, angle):
        self.parentPosition = position
        self.angle = angle

        rot = Matrix.rotation(-self.angle)
        self.localPosition = rot.multiplyVector(self.originalPosition)
        self.worldPosition = self.parentPosition + self.localPosition

        return [self.worldPosition, self.radius]

    def getData(self):
        return [self.worldPosition, self.radius]

    def getInertia(self, mass):
        return (mass * self.radius**2) / 2

class Polygon:
    def __init__(self, x, y, shape):
        self.base = [v for v in shape]
        self.vertices = [v for v in shape]
        self.localPosition = Vector(x, y)
        self.parentPosition = Vector(0, 0)
        self.angle = 0
    
    def updatePosition(self, position):
        self.parentPosition = position
    
    def updateData(self, position, angle):
        self.parentPosition = position
        self.angle = angle
        rot = Matrix.rotation(-self.angle)
        for v in range(len(self.vertices)):
            self.vertices[v] = rot.multiplyVector(self.base[v] + self.localPosition) + self.parentPosition
        self.worldPosition = self.parentPosition + self.localPosition

    def getData(self):
        return self.vertices
    
    def getInertia(self, mass):
        return PolygonMOI(mass, self.base)