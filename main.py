import sys
import time
import pygame
from random import randint, uniform
from config import *
from body import *
from vector import *
pygame.init()

window = pygame.display.set_mode(WINDOWSIZE)
clock = pygame.time.Clock()
bodies = []

def initBodies():
    global bodies
    bodies = []
    bodies.append(Body(Vector(-HALFWIDTH / 2, 0), generateBox(50, 50), 10, color=(51, 170, 255)))
    
    for i in range(16):
        bodies.append(Body(Vector(randint(-HALFWIDTH//2, HALFWIDTH//2), randint(-HALFHEIGHT//2, HALFHEIGHT//2)), generateVertices(randint(3, 10), randint(25, 50)), 1, color=(randint(0, 255), randint(0, 255), randint(0, 255))))
    
    bodies.append(Body(Vector(0, -HALFHEIGHT / 2), generateBox(WIDTH * 0.75, 25), -1, 0.5, static=True))

    bodies.append(Body(Vector(-WIDTH, 0), generateBox(WIDTH, HEIGHT), -1, 0.5, static=True))
    bodies.append(Body(Vector(WIDTH, 0), generateBox(WIDTH, HEIGHT), -1, 0.5, static=True))
    bodies.append(Body(Vector(0, HEIGHT), generateBox(WIDTH*3, HEIGHT), -1, 0.5, static=True))
    bodies.append(Body(Vector(0, -HEIGHT), generateBox(WIDTH*3, HEIGHT), -1, 0.5, static=True))


def toScreen(v):
    return [HALFWIDTH + v.x, HALFHEIGHT - v.y]

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


initBodies()
running = True
while(running):
    dt = clock.tick() / 1000

    pygame.display.set_caption("FPS: " + str(1 // dt) if dt > 0 else "INF")

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        elif(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_ESCAPE):
                running = False
            elif(event.key == pygame.K_r):
                initBodies()
    
    window.fill((51, 51, 51))

    moveAmount = Vector(0)
    speed = 1000
    if(keys[pygame.K_d]): moveAmount.x += 1
    if(keys[pygame.K_a]): moveAmount.x -= 1
    if(keys[pygame.K_w]): moveAmount.y += 1
    if(keys[pygame.K_s]): moveAmount.y -= 1
    bodies[0].accelerate(moveAmount * speed)
    
    moveAmount = Vector(0)
    speed = 1000
    if(keys[pygame.K_RIGHT]): moveAmount.x += 1
    if(keys[pygame.K_LEFT]): moveAmount.x -= 1
    if(keys[pygame.K_UP]): moveAmount.y += 1
    if(keys[pygame.K_DOWN]): moveAmount.y -= 1
    bodies[1].accelerate(moveAmount * speed)

    for body in bodies:
        body.step(dt)
    
    for a in bodies:
        for b in bodies:
            if a == b or (a.static and b.static): continue
            intersects, normal, depth = intersectBodies(a, b)
            if(intersects):
                if(a.static):
                    b.move(normal * depth)
                elif(b.static):
                    a.move(-normal * depth)
                else:
                    a.move(-normal * depth / 2)
                    b.move(normal * depth / 2)

                relativeVelocity = b.velocity - a.velocity
                if(not Vector.dot(relativeVelocity, normal) > 0):
                    e = min(a.restitution, b.restitution)

                    j = -(1 + e) * Vector.dot(relativeVelocity, normal)
                    j /= a.invmass + b.invmass

                    impulse = normal * j

                    a.velocity -= impulse * a.invmass
                    b.velocity += impulse * b.invmass

    for body in bodies:
        body.updateVertices()
        pygame.draw.polygon(window, body.color, [toScreen(v) for v in body.vertices])

    pygame.display.flip()