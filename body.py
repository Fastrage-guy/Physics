import math
from vector import *

class Box:
    def __init__(self, w, h):
        self.width = w
        self.height = h
    
    def area(self):
        return self.w * self.h

class Circle:
    def __init__(self, r):
        self.radius = r

    def area(self):
        return math.pi * self.radius * self.radius

class Body:
    def __init__(self, position, density, shape, restitution, static):
        self.position = position
        self.linearVelocity = Vector(0, 0)
        self.rotation = 0
        self.rotationalVelocity = 0
        

        self.restitution = restitution
        self.area = shape.area()
        self.density = density
        self.mass = self.area * self.density

        self.static = False
        self.shapetype = shape.__class__.__name__
        self.shape = shape
    
    def Move(self, amount):
        self.position += amount
    
    def MoveTo(self, pos):
        self.position = pos