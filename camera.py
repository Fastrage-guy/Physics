import common

class Camera:
    def __init__(self, x, y, zoom=1):
        self.x = x
        self.y = y
        self.zoom = zoom
    
    def ToScreen(self, point):
        return [(point[0] - self.x) * self.zoom + common.HALFWIDTH,
                common.HALFHEIGHT - (point[1] - self.y) * self.zoom]

    def VerticesToScreen(self, vertices):
        onScreen = []
        for v in vertices:
            onScreen.append(self.ToScreen(v.AsList()))
        return onScreen

    def VectorToScreen(self, vector):
        return self.ToScreen(vector.AsList())