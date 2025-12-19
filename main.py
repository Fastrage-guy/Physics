from physmath import *
from collisions import *
from body import *
from common import *
from camera import *
import pygame
import random
pygame.init()

window = pygame.display.set_mode(SCREENSIZE)
clock = pygame.time.Clock()
camera = Camera(0, 0)

bodies = [Body(Vector(0, 0), ShapeType.circle, 25, 10)]

for i in range(500):
    bodies.append(Body(Vector(random.uniform(-1, 1) * WIDTH, random.uniform(-1, 1) * HEIGHT), ShapeType.polygon, generateVertices(random.randint(3, 10), random.randint(25, 50)), 10, color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))


dragging = False
prevMouse = [HALFWIDTH, HALFHEIGHT]
running = True
while(running):
    dt = clock.tick()
    events = pygame.event.get()
    mouse = pygame.mouse.get_pos()
    for event in events:
        if(event.type == pygame.QUIT):
            running = False
        elif(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_ESCAPE):
                running = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y < 0:
                camera.x -= (HALFWIDTH - mouse[0]) / camera.zoom 
                camera.y += (HALFHEIGHT - mouse[1]) / camera.zoom
                camera.zoom /= 1.1
                camera.x += (HALFWIDTH - mouse[0]) / camera.zoom 
                camera.y -= (HALFHEIGHT - mouse[1]) / camera.zoom
            else:
                camera.x -= (HALFWIDTH - mouse[0]) / camera.zoom 
                camera.y += (HALFHEIGHT - mouse[1]) / camera.zoom
                camera.zoom *= 1.1
                camera.x += (HALFWIDTH - mouse[0]) / camera.zoom 
                camera.y -= (HALFHEIGHT - mouse[1]) / camera.zoom
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging = True
                prevMouse = mouse
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
    
    if(dragging):
        camera.x -= (mouse[0] - prevMouse[0]) / camera.zoom
        camera.y += (mouse[1] - prevMouse[1]) / camera.zoom
        prevMouse = [mouse[0], mouse[1]]
    
    window.fill((255, 255, 255))

    for b in bodies:
        if(b.shapetype == ShapeType.polygon):
            pygame.draw.polygon(window, b.color, camera.VerticesToScreen(b.vertices))
        elif(b.shapetype == ShapeType.circle):
            pygame.draw.circle(window, b.color, camera.VectorToScreen(b.position), b.radius * camera.zoom)

    pygame.display.flip()