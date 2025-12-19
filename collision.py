from util import *
from shapes import *
import math, random

def sat(o1, o2):
    min_overlap = None
    smallest_axis = None
    vertex_obj = None

    axes = find_axes(o1, o2)
    proj1 = proj2 = 0
    first_shape_axes = get_shape_axes(o1)

    for i in range(len(axes)):
        proj1 = proj_shape_onto_axis(axes[i], o1)
        proj2 = proj_shape_onto_axis(axes[i], o2)
        overlap = min(proj1['max'], proj2['max']) - max(proj1['min'], proj2['min'])
        if overlap < 0:
            return False

        if (proj1['max'] > proj2['max'] and proj1['min'] < proj2['min']) or \
           (proj1['max'] < proj2['max'] and proj1['min'] > proj2['min']):
            mins = abs(proj1['min'] - proj2['min'])
            maxs = abs(proj1['max'] - proj2['max'])
            if mins < maxs:
                overlap += mins
            else:
                overlap += maxs
                axes[i] = -axes[i]

        if min_overlap is None or overlap < min_overlap:
            min_overlap = overlap
            smallest_axis = axes[i]
            if i < first_shape_axes:
                vertex_obj = o2
                if proj1['max'] > proj2['max']:
                    smallest_axis = -axes[i]
            else:
                vertex_obj = o1
                if proj1['max'] < proj2['max']:
                    smallest_axis = -axes[i]

    contact_vertex = proj_shape_onto_axis(smallest_axis, vertex_obj)['coll_vertex']
    # smallest_axis.drawVec(contact_vertex.x, contact_vertex.y, min_overlap, "blue")

    if vertex_obj is o2:
        smallest_axis = -smallest_axis

    return {
        "pen": min_overlap,
        "axis": smallest_axis,
        "vertex": contact_vertex
    }

def proj_shape_onto_axis(axis, obj):
    set_ball_vertices_along_axis(obj, axis)
    min_val = Vector.dot(axis, obj.vertices[0])
    max_val = min_val
    coll_vertex = obj.vertices[0]
    for vertex in obj.vertices:
        p = Vector.dot(axis, vertex)
        if p < min_val:
            min_val = p
            coll_vertex = vertex
        if p > max_val:
            max_val = p
    return {
        "min": min_val,
        "max": max_val,
        "coll_vertex": coll_vertex
    }

def find_axes(o1, o2):
    axes = []
    if isinstance(o1, Circle) and isinstance(o2, Circle):
        if (o2.worldPosition - o1.worldPosition).magnitude() > 0:
            axes.append((o2.worldPosition - o1.worldPosition).normalized())
        else:
            axes.append(Vector(random.uniform(-1, 1), random.uniform(-1, 1)).normalized())
        return axes
    else:
        for obj in (o1, o2):
            if isinstance(obj, Circle):
                axes.append((closest_vertex_to_point(o2, o1.worldPosition) - o1.worldPosition).normalized())
            if isinstance(obj, Polygon):
                lenVertices = len(obj.vertices)
                for v in range(lenVertices):
                    v1 = obj.vertices[v]
                    v2 = obj.vertices[(v + 1) % lenVertices]
                    axes.append((v2 - v1).normalized())

    return axes

def closest_vertex_to_point(obj, p):
    closestVertex = None
    minDist = float('inf')
    for v in obj.vertices:
        if (p - v).magnitude() < minDist:
            closestVertex = v
            minDist = (p - v).magnitude()
    return closestVertex

def get_shape_axes(obj):
    if isinstance(obj, Circle):
        return 1
    if isinstance(obj, Polygon):
        return len(obj.vertices)

def set_ball_vertices_along_axis(obj, axis):
    if isinstance(obj, Circle):
        obj.vertices[0] = obj.worldPosition + (axis.normalized() * (-obj.radius))
        obj.vertices[1] = obj.worldPosition + (axis.normalized() * obj.radius)

def collide(o1, o2):
    bestSat = {
        "pen": 0,
        "axis": None,
        "vertex": None
    }
    for o1_comp in o1.composition:
        for o2_comp in o2.composition:
            sat_result = sat(o1_comp, o2_comp)
            if sat_result:
                if sat_result["pen"] > bestSat["pen"]:
                    bestSat = sat_result
    
    if bestSat["axis"] is not None:
        return bestSat
    else:
        return False