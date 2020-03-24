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

    def move_with_mode(self, mode, fruit):
        if mode == "--shortest":
            self.move_bfs(fruit)
        elif mode == "--human":
            self.move_keys()
        elif mode == "--random":
            self.move_random()
        elif mode == "--better-shortest":
            self.move_shortestb_enhanced(fruit)
        else:
            self.move_keys()

    def move_shortest(self, fruit):
        for e in pygame.event.get(): None
        currDir = (self.dirnx, self.dirny)
        rDist = (fruit.distToCube(self.body[0].getRightCubeCoords()), RIGHT)
        lDist = (fruit.distToCube(self.body[0].getLeftCubeCoords()), LEFT)
        upDist = (fruit.distToCube(self.body[0].getUpCubeCoords()), UP)
        downDist = (fruit.distToCube(self.body[0].getDownCubeCoords()), DOWN)

        if currDir == RIGHT:
            res = min([rDist, upDist, downDist], key = lambda i: i[0])[1]
        elif currDir == LEFT:
            res = min([lDist, upDist, downDist], key = lambda i: i[0])[1]
        elif currDir == UP:
            res = min([rDist, upDist, lDist], key = lambda i: i[0])[1]
        elif (currDir == DOWN):
            res = min([rDist, lDist, downDist], key = lambda i: i[0])[1]

        self.updateDir(res[0], res[1])
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def body_to_list(self):
        return list(map(lambda i: i.pos, self.body))

    def move_shortest_enhanced(self, fruit):
        for e in pygame.event.get(): None


        lst = [(self.body[0].getRightCubeCoords(), RIGHT), (self.body[0].getLeftCubeCoords(), LEFT),
        (self.body[0].getUpCubeCoords(), UP), (self.body[0].getDownCubeCoords(), DOWN)]


        availible_dirs = list(filter(lambda i: i[0] not in self.body_to_list(), lst))

        # Snake has closed itself in. Choose any direction and restart
        if len(availible_dirs) == 0:
            res = UP
        else: res = min(availible_dirs, key = lambda i: fruit.distToCube(i[0]))[1]
        self.updateDir(res[0], res[1])
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def move_random(self):
        for event in pygame.event.get(): None
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
