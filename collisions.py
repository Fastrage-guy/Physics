from vector import *

def intersectCircles(circle1, circle2):
    distance = Vector.distance(circle1.position, circle2.position)
    radii = circle1.shape.radius + circle2.shape.radius

    if(distance >= radii):
        return (False, -1, -1)
    
    normal = (circle1.position - circle2.position).normalized()
    depth = radii - distance
    return (True, normal, depth)