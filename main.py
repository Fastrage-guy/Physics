import sys
import time
import pygame
from random import randint, uniform
from config import *
from body import *
from vector import *
from scene import *
pygame.init()

window = pygame.display.set_mode(WINDOWSIZE)
clock = pygame.time.Clock()

scene = Scene()
scene.gravity = Vector(0, -500)

def initBodies():
    scene = Scene()
    scene.add(Body(Vector(-HALFWIDTH / 2, 0), generateBox(50, 50), 10, color=(51, 170, 255)))
    
    for i in range(4):
        scene.add(Body(Vector(randint(-HALFWIDTH//2, HALFWIDTH//2), randint(-HALFHEIGHT//2, HALFHEIGHT//2)), generateVertices(randint(3, 10), randint(25, 50)), 1, color=(randint(0, 255), randint(0, 255), randint(0, 255))))

    scene.add(Body(Vector(0, -HALFHEIGHT / 2), generateBox(WIDTH * 0.75, 25), -1, 0.5, static=True))

    scene.add(Body(Vector(-WIDTH, 0), generateBox(WIDTH, HEIGHT), -1, 0.5, static=True))
    scene.add(Body(Vector(WIDTH, 0), generateBox(WIDTH, HEIGHT), -1, 0.5, static=True))
    scene.add(Body(Vector(0, HEIGHT), generateBox(WIDTH*3, HEIGHT), -1, 0.5, static=True))
    scene.add(Body(Vector(0, -HEIGHT), generateBox(WIDTH*3, HEIGHT), -1, 0.5, static=True))


def toScreen(v):
    return [HALFWIDTH + v.x, HALFHEIGHT - v.y]

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

    acceleration = 1000
    moveAmount = Vector(keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_w] - keys[pygame.K_s])
    scene.bodies[0].accelerate(moveAmount * acceleration)

    scene.step(dt)

    for body in scene.bodies:
        body.updateVertices()
        pygame.draw.polygon(window, body.color, [toScreen(v) for v in body.vertices])

    pygame.display.flip()