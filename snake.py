from cube import cube
import pygame
import random
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, 1)
DOWN = (0, -1)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def updateDir(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny

    def move_body(self):
        for i, c in enumerate(self.body):
            p = c.pos[:]

            #If there is a turn
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                # If the cube reaches the edge of the screen we will make it appear on the opposite side
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)  # If we haven't reached the edge just move in our current direction

    def move_bfs(self, fruit):
        currDir = (self.dirnx, self.dirny)
        print("entered")
        rDist = (fruit.distToCube(self.body[0].getRightCubeCoords()), RIGHT)
        lDist = (fruit.distToCube(self.body[0].getLeftCubeCoords()), LEFT)
        upDist = (fruit.distToCube(self.body[0].getUpCubeCoords()), UP)
        downDist = (fruit.distToCube(self.body[0].getDownCubeCoords()), DOWN)

        if currDir == RIGHT:
            res = min([rDist, upDist, downDist], key = lambda i: i[0])[1]
        elif currDir == LEFT:
            res = (min([lDist, upDist, downDist], key = lambda i: i[0])[1])
        elif currDir == UP:
            res = (min([rDist, upDist, lDist], key = lambda i: i[0])[1])
        elif (currDir == DOWN):
            res = (min([rDist, lDist, downDist], key = lambda i: i[0])[1])
        else:


            print("ERROR")
        self.updateDir(res[0], res[1])
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def move_random(self):
        dir = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        self.updateDir(dir[0], dir[1])
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()


    def move_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.updateDir(-1, 0)

                elif keys[pygame.K_RIGHT]:
                    self.updateDir(1, 0)

                elif keys[pygame.K_UP]:
                    self.updateDir(0, -1)

                elif keys[pygame.K_DOWN]:
                    self.updateDir(0, 1)

                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)
