WIDTH = 1280
HEIGHT = 720
RESOLUTION = (WIDTH, HEIGHT)
HALFWIDTH = WIDTH // 2
HALFHEIGHT = HEIGHT//2

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 