import pygame
import random
from collisions import *
from vector import *
from body import *
from common import *
pygame.init()

window = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()

bodies = []
for i in range(128):
    bodies.append(Body(Vector(random.randint(-HALFWIDTH, HALFWIDTH), random.randint(-HALFHEIGHT, HALFHEIGHT)), 0.5, Circle(random.randint(25, 25)), 0.5, False))

running = True
while(running):
    dt = clock.tick()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        elif(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_ESCAPE):
                running = False
    
    window.fill((255, 255, 255))
    bodies[0].position += Vector(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_UP] - keys[pygame.K_DOWN]) * Vector(dt * 0.5)

    for i in bodies:
        for j in bodies:
            if i == j: continue
            intersects, normal, depth = intersectCircles(i, j)
            if(intersects):
                i.Move(normal * depth / 2)
                j.Move(-normal * depth / 2)

    for b in bodies:
        if(b.shapetype == "Circle"):
            pygame.draw.circle(window, (0, 0, 0), b.position.toScreen(), b.shape.radius)

    pygame.display.flip()