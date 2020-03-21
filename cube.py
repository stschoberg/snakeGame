import pygame
global LEFT, RIGHT, UP, DOWN

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, 1)
DOWN = (0, -1)



class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    # Distance between a cube and a coord of form (x, y)
    # Return (distance_to_cell, coord of form: (x, y))
    def distToCube(self, coord):
        return (abs(self.pos[0] - coord[0]) + abs(self.pos[1] - coord[1]), coord)

    def getRightCubeCoords(self):
        return (self.pos[0] + 1, self.pos[1])

    def getLeftCubeCoords(self):
        return (self.pos[0] - 1, self.pos[1])

    def getUpCubeCoords(self):
        return (self.pos[0] , self.pos[1] + 1)

    def getDownCubeCoords(self):
        return (self.pos[0], self.pos[1] - 1)

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
