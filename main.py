import pygame
from random import randint
from collisions import *
from vector import *
from body import *
from config import *
import world
pygame.init()

window = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()

world.AddBody(Body(Vector(0, 0), 0.5, GenerateBox(50, 50), 0.5, False))

for i in range(64):
    shape = randint(0, 1)
    if(shape == 0):
        shape = GenerateBox(randint(25, 50), randint(25, 50))
    elif(shape == 1):
        shape = GenerateCircle(randint(10, 25))
    
    world.AddBody(Body(Vector(randint(-HALFWIDTH, HALFWIDTH), randint(-HALFHEIGHT, HALFHEIGHT)), 0.5, shape, 0.5, False))


running = True
while(running):
    dt = clock.tick() / 1000
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        elif(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_ESCAPE):
                running = False
    
    window.fill((255, 255, 255))

    magnitude = dt * 250
    dx = 0
    dy = 0
    if(keys[pygame.K_UP]): dy += 1
    if(keys[pygame.K_DOWN]): dy -= 1
    if(keys[pygame.K_RIGHT]): dx += 1
    if(keys[pygame.K_LEFT]): dx -= 1
    direction = Vector(dx, dy)

    world.bodies[0].Move(direction * magnitude)
    world.Step(dt)

    for b in world.bodies:
        if(b.shapetype == "Polygon"):
            pygame.draw.polygon(window, (0, 0, 0), [v.toScreen() for v in b.shape.vertices])
        elif(b.shapetype == "Circle"):
            pygame.draw.circle(window, (0, 0, 0), b.position.toScreen(), b.shape.radius)

    pygame.display.flip()