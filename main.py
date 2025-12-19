import pygame
from collision import *
from body import *
from shapes import *
from config import *
from util import *
pygame.init()

window = pygame.display.set_mode(WINSIZE)
clock = pygame.time.Clock()

BODIES = []
BODIES.append(Body(0, 0, 10, comp=[Circle(0, 0, 50), Circle(0, -100, 50), Polygon(0, 100, generateVertices(6, 25))]))
BODIES.append(Body(0, 200, 10, comp=[Circle(0, 0, 50), Circle(0, -100, 50), Polygon(0, 100, generateVertices(6, 25))]))

def toScreen(p):
    return [HALFWIDTH + p.x, HALFHEIGHT - p.y]

running = True
while running:
    clock.tick(60)
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    window.fill(CLEARCOLOR)

    for b in BODIES:
        b.update()

    for a in BODIES:
        for b in BODIES:
            if a != b:
                result = collide(a, b)
                if result:
                    print("intersected")
                else:
                    print("didn't intersect")
    
    #for c in collisions:
    #    c.resolvePenetration()
    #    c.resolveVelocity()
    
    for b in BODIES:
        b.rotate(0.025)
        for c in b.composition:
            data = c.getData()
            if(isinstance(c, Circle)):
                pygame.draw.circle(window, b.color, toScreen(data[0]), data[1])
            if(isinstance(c, Polygon)):
                pygame.draw.polygon(window, b.color, [toScreen(v) for v in data])

    pygame.display.flip()