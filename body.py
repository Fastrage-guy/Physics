from shapes import *
from config import *

class Body:
    def __init__(self, x, y, mass, comp=[], color=(15, 15, 15)):
        # Transformation Variables
        self.pos = Vector(x, y)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.angle = 0
        self.rotvel = 0

        # Shape Variables
        self.composition = comp
        if(self.composition == []):
            self.composition = [Circle(x, y, 25)]
        compNum = len(self.composition)

        # Physics Variables
        self.mass = mass
        if(self.mass == 0):
            self.inv_mass = 0
        else:
            self.inv_mass = 1/self.mass
        
        self.inertia = 0
        for c in self.composition:
            self.inertia += c.getInertia(mass / compNum)  # extremely innacurate inertia calculation

        self.friction = 0.05 # temporary friction variable until i get friction calculation working
        self.angFriction = 0.05 # once again for angular friction
        self.restitution = 0.5 # coefficent or restitution (bounciness)

        # Appearance Variables
        self.color = color
        self.borderColor = (0, 0, 0)
        self.borderThickness = 2
        
    def setPosition(self, x, y):
        self.pos.x = x
        self.pos.y = y

    
    def setRotation(self, angle):
        self.angle = angle
        for c in self.composition:
            c.angle = self.angle
    
    def rotate(self, angle):
        self.angle += angle
        for c in self.composition:
            c.angle = self.angle

    def update(self):
        self.vel = self.vel + self.acc
        self.vel *= Vector(1 - self.friction)
        self.rotvel *= 1 - self.angFriction
        self.pos += self.vel
        for c in self.composition:
            c.updateData(self.pos, self.angle)