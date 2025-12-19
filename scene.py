from vector import *

def findCenter(vertices):
    sumX = 0
    sumY = 0
    verticesLen = len(vertices)

    for v in vertices:
        sumX += v.x
        sumY += v.y

    return Vector(sumX / verticesLen, sumY / verticesLen)

def projectVertices(vertices, axis):
    minimum = float('inf')
    maximum = float('-inf')

    for v in vertices:
        proj = Vector.dot(v, axis)
        if(proj < minimum): minimum = proj
        if(proj > maximum): maximum = proj
    
    return [minimum, maximum]

def intersectBodies(polyA, polyB):
    normal = Vector(0)
    depth = float('inf')

    lenA = len(polyA.vertices)
    lenB = len(polyB.vertices)

    for i in range(lenA):
        va = polyA.vertices[i]
        vb = polyA.vertices[(i + 1) % lenA]
        edge = vb - va
        axis = Vector(-edge.y, edge.x).normalized()
        minA, maxA = projectVertices(polyA.vertices, axis)
        minB, maxB = projectVertices(polyB.vertices, axis)

        if(minA >= maxB or minB >= maxA):
            return (False, Vector(-1), -1)
        
        axisDepth = min(maxB - minA, maxA - minB)
        if(axisDepth < depth):
            depth = axisDepth
            normal = axis

    
    for i in range(lenB):
        va = polyB.vertices[i]
        vb = polyB.vertices[(i + 1) % lenB]
        edge = vb - va
        axis = Vector(-edge.y, edge.x).normalized()
        minA, maxA = projectVertices(polyB.vertices, axis)
        minB, maxB = projectVertices(polyA.vertices, axis)

        if(minA >= maxB or minB >= maxA):
            return (False, Vector(-1), -1)
        
        axisDepth = min(maxB - minA, maxA - minB)
        if(axisDepth < depth):
            depth = axisDepth
            normal = axis

    centerA = findCenter(polyA.vertices)
    centerB = findCenter(polyB.vertices)
    direction = centerB - centerA

    if(Vector.dot(direction, normal) < 0):
        normal = -normal

    return (True, normal, depth)

class Scene:
    def __init__(self, bodies=[]):
        self.bodies = bodies
        self.gravity = Vector(0)
    
    def add(self, body):
        self.bodies.append(body)

    def step(self, dt, iterations=1):
        for i in range(iterations):
            for body in self.bodies:
                body.step(dt/iterations, self.gravity)
                body.updateVertices()
            
            for bodyA in self.bodies:
                for bodyB in self.bodies:
                    if((bodyB is bodyA) or (bodyA.static and bodyB.static)): continue
                    intersects, normal, depth = intersectBodies(bodyA, bodyB)
                    if(intersects):
                        if(bodyA.static):
                            bodyB.move(normal * depth)
                        elif(bodyB.static):
                            bodyA.move(-normal * depth)
                        else:
                            bodyA.move(-normal * depth / 2)
                            bodyB.move(normal * depth / 2)

                        relativeVelocity = bodyB.velocity - bodyA.velocity
                        if(not Vector.dot(relativeVelocity, normal) > 0):
                            e = min(bodyA.restitution, bodyB.restitution)

                            j = -(1 + e) * Vector.dot(relativeVelocity, normal)
                            j /= bodyA.invmass + bodyB.invmass

                            impulse = normal * j

                            bodyA.velocity -= impulse * bodyA.invmass
                            bodyB.velocity += impulse * bodyB.invmass