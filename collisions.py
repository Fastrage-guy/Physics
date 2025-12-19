import sys
from vector import *

def findMiddle(vertices):
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

def projectCircle(position, radius, axis):
    direction = axis.normalized()
    directionAndRadius = direction * radius

    p1 = position + directionAndRadius
    p2 = position - directionAndRadius

    minimum = Vector.dot(p1, axis)
    maximum = Vector.dot(p2, axis)

    if(minimum > maximum):
        temp = minimum
        minimum = maximum
        maximum = temp
    
    return [minimum, maximum]

def closestPoint(point, points):
    result = points[0]
    minDist = float('inf')
    for p in points:
        dist = Vector.distance(p, point)
        if(dist < minDist):
            minDist = dist
            result = p
    return result

def intersectCirclePolygon(circle, poly):
    normal = Vector(0)
    depth = float('inf')
    lenA = len(poly.shape.vertices)

    for i in range(lenA):
        va = poly.shape.vertices[i]
        vb = poly.shape.vertices[(i + 1) % lenA]
        edge = vb - va
        axis = Vector(-edge.y, edge.x)
        minA, maxA = projectVertices(poly.shape.vertices, axis)
        minB, maxB = projectCircle(circle.position, circle.shape.radius, axis)

        if(minA >= maxB or minB >= maxA):
            return (False, Vector(-1), -1)
        
        axisDepth = min(maxB - minA, maxA - minB)
        if(axisDepth < depth):
            depth = axisDepth
            normal = axis
    
    closest = closestPoint(circle.position, poly.shape.vertices)
    axis = closest - circle.position

    minA, maxA = projectVertices(poly.shape.vertices, axis)
    minB, maxB = projectCircle(circle.position, circle.shape.radius, axis)

    if(minA >= maxB or minB >= maxA):
        return (False, Vector(-1), -1)
        
    axisDepth = min(maxB - minA, maxA - minB)
    if(axisDepth < depth):
        depth = axisDepth
        normal = axis
    
    depth /= normal.magnitude()
    normal.normalize() # make the normal a real normal

    polyCenter = findMiddle(poly.shape.vertices)
    direction = polyCenter - circle.position

    if(Vector.dot(direction, normal) < 0):
        normal = -normal

    return (True, normal, depth)

def intersectPolygons(polyA, polyB):
    normal = Vector(0)
    depth = float('inf')
    lenA = len(polyA.shape.vertices)
    lenB = len(polyB.shape.vertices)
    for i in range(lenA):
        va = polyA.shape.vertices[i]
        vb = polyA.shape.vertices[(i + 1) % lenA]
        edge = vb - va
        axis = Vector(-edge.y, edge.x)
        minA, maxA = projectVertices(polyA.shape.vertices, axis)
        minB, maxB = projectVertices(polyB.shape.vertices, axis)

        if(minA >= maxB or minB >= maxA):
            return (False, Vector(-1), -1)
        
        axisDepth = min(maxB - minA, maxA - minB)
        if(axisDepth < depth):
            depth = axisDepth
            normal = axis
    
    for i in range(lenB):
        va = polyB.shape.vertices[i]
        vb = polyB.shape.vertices[(i + 1) % lenB]
        edge = vb - va
        axis = Vector(-edge.y, edge.x)
        minA, maxA = projectVertices(polyB.shape.vertices, axis)
        minB, maxB = projectVertices(polyA.shape.vertices, axis)

        if(minA >= maxB or minB >= maxA):
            return (False, Vector(-1), -1)
    
        axisDepth = min(maxB - minA, maxA - minB)
        if(axisDepth < depth):
            depth = axisDepth
            normal = axis

    depth /= normal.magnitude()
    normal.normalize() # make the normal a real normal

    centerA = findMiddle(polyA.shape.vertices)
    centerB = findMiddle(polyB.shape.vertices)
    direction = centerB - centerA

    if(Vector.dot(direction, normal) < 0):
        normal = -normal

    return (True, normal, depth)


def intersectCircles(circle1, circle2):
    distance = Vector.distance(circle1.position, circle2.position)
    radii = circle1.shape.radius + circle2.shape.radius

    if(distance >= radii):
        return (False, -1, -1)
    
    normal = (circle1.position - circle2.position).normalized()
    depth = radii - distance
    return (True, normal, depth)