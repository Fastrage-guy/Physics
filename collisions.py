import math
from physmath import *

class CollisionResult:
    def __init__(self, intersects, mtv):
        self.intersects = intersects
        # slightly innefficient but who cares
        self.mtv = mtv
        self.normal = self.mtv.normalized()
        self.depth = self.mtv.magnitude()

def GetCircleAxes(circle, polygon):
    axes = []
    for v in polygon.vertices:
        axes.append(Vector(v.x - circle.x, v.y - circle.y).Normalized())
    return axes

def GetProjection(normal, vertices):
    projection = {'min': float('inf'), 'max': float('-inf')}
    for vertex in vertices.values():
        dot = DotProduct(normal, vertex)
        projection['min'] = min(projection['min'], dot)
        projection['max'] = max(projection['max'], dot)
    return projection

def CirclevsCircle(a, b):
    d1 = (b.x - a.x) ** 2 + (a.y - b.y) ** 2
    d2 = (a['radius'] + b['radius']) ** 2
    overlap = d1 <= d2
    offset = math.sqrt(d2) - math.sqrt(d1)
    vector = Vector(a.x - b.x, a.y - b.y).Normalized()
    mtv = Vector(vector.x * offset, vector.y * offset)
    return CollisionResult(overlap, mtv if overlap else Vector())

def CirclevsPolygon(a, b):
    v = b.vertices
    normals = b['normals'] + GetCircleAxes(a, b)
    mtv = Vector(float('inf'), float('inf'))

    overlap = all(n for n in normals if Overlaps(n, a, v, mtv))
    return CollisionResult(overlap, mtv if overlap else Vector())

def PolygonvsCircle(a, b):
    result = CirclevsPolygon(b, a)
    return CollisionResult(result.intersects, Vector(-result.mtv.x, -result.mtv.y))

def PolygonvsPolygon(a, b):
    v1 = a.vertices
    v2 = b.vertices
    normals = a['normals'] + b['normals']
    mtv = Vector(float('inf'), float('inf'))

    overlap = all(n for n in normals if Overlaps(n, v1, v2, mtv))
    return CollisionResult(overlap, mtv if overlap else Vector())

def Overlaps(n, a, b, mtv):
    p1 = GetProjection(n, a)
    p2 = GetProjection(n, b)
    c1 = p1['min'] < p2['max'] and p1['min'] > p2['min']
    c2 = p2['min'] < p1['max'] and p2['min'] > p1['min']

    if c1 or c2:
        m = min(p2['max'] - p1['min'], p2['min'] - p1['max'])
        vector = Vector(n.x * m, n.y * m)
        if vector.MagSquared() < mtv.MagSquared():
            mtv.update(vector)
    return c1 or c2

