from collisions import *
from vector import *

bodies = []
gravity = Vector(0, -9.81)

def NumBodies():
    return len(bodies)

def AddBody(body):
    bodies.append(body)

def RemoveBody(body):
    bodies.remove(body)

def GetBody(index):
    if(index > 0 and index <= len(bodies) - 1):
        return bodies[index]
    return False

def Step(time):
    # Movement
    for body in bodies:
        body.step(time)

    # Collision
    for i in bodies:
        for j in bodies:
            if(i == j): continue
            intersects, normal, depth = Collide(i, j)
            if(intersects):
                i.Move(-normal * depth / 2)
                j.Move(normal * depth / 2)

def Collide(a, b):
    if(a.shapetype == "Polygon"):
        if(b.shapetype == "Circle"):
            result = intersectCirclePolygon(b, a)
            return [result[0], -result[1], result[2]]
        elif(b.shapetype == "Polygon"):
            return intersectPolygons(a, b)
    elif(a.shapetype == "Circle"):
        if(b.shapetype == "Polygon"):
            return intersectCirclePolygon(a, b)
        elif(b.shapetype == "Circle"):
            return intersectCircles(b, a)
    raise NotImplemented("Collision between " + a.shapetype + " and " + b.shapetype + " isn't implemented")