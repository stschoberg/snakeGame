from cube import cube
import pygame
import random

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, 1)
DOWN = (0, -1)

class snake(object):
    body = []
    visited = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.visited.append(pos)

    def clear_visited(self):
        self.visited.clear()

    def update_dir(self, dirnx, dirny):
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
                c.move(c.dirnx,c.dirny)  # If we haven't reached the edge just move in our current direction

    def move_with_mode(self, mode, fruit):
        if mode == "--shortest":
            self.move_shortest(fruit)
        elif mode == "--human":
            self.move_keys()
        elif mode == "--random":
            self.move_better_random()
        elif mode == "--better-shortest":
            self.move_shortest_enhanced(fruit)
        elif mode == "--hamiltonian":
            self.move_hamiltonian()
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

        self.update_dir(res[0], res[1])
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def body_to_list(self):
        return list(map(lambda i: i.pos, self.body))

    def move_hamiltonian(self):
        for e in pygame.event.get(): None
        self.visited.append(self.head.pos)

        if self.head.pos == (0, 0):
            self.update_dir(UP[0], UP[1])
            self.clear_visited()
        elif self.head.pos[1] == 0:
            self.update_dir(LEFT[0], LEFT[1])

        elif self.head.pos == (19, 1):
            self.update_dir(DOWN[0], DOWN[1])

        elif ((self.head.pos[1] == 1 and self.head.getUpCubeCoords() in self.visited) or
            self.head.pos[1] == 19 and self.head.getDownCubeCoords() in self.visited):
            self.update_dir(RIGHT[0], RIGHT[1])

        elif self.head.pos[0] % 2 == 1:
            self.update_dir(DOWN[0], DOWN[1])

        elif self.head.pos[0] % 2 == 0:
            self.update_dir(UP[0], UP[1])


        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()


        # if (self.head.pos == (19, 0)):
        #     self.move_shortest(cube((0, 0)))
        #     return
        # elif ((self.head.pos[1] == 1 and self.head.getDownCubeCoords() in self.visited) or
        #     self.head.pos[1] == 19 and self.head.getUpCubeCoords() in self.visited):
        #     self.update_dir(RIGHT[0], RIGHT[1])
        #     self.visited.append(self.body[0].getRightCubeCoords())
        #

        # elif self.head.pos[0] % 2 == 1:
        #     self.update_dir(UP[0], UP[1])
        #     print("enetered")
        #     self.visited.append(self.body[0].getUpCubeCoords())




    def traverse_col(self, dir):
        self.update_dir(0, dir)
        for i in range(0, 19):
            self.move_body()


    def move_shortest_enhanced(self, fruit):
        for e in pygame.event.get(): None


        lst = [(self.body[0].getRightCubeCoords(), RIGHT), (self.body[0].getLeftCubeCoords(), LEFT),
        (self.body[0].getUpCubeCoords(), UP), (self.body[0].getDownCubeCoords(), DOWN)]

        availible_dirs = list(filter(lambda i: i[0] not in self.body_to_list(), lst))
        # Reduces bias in picking direction of snake when it cannot get closer to the snack
        random.shuffle(lst)

        # Snake has closed itself in. Choose any direction and restart
        if len(availible_dirs) == 0:
            res = UP
        else: res = min(availible_dirs, key = lambda i: fruit.distToCube(i[0]))[1]
        self.update_dir(res[0], res[1])
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def move_random(self):
        for event in pygame.event.get(): None
        dir = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        self.update_dir(dir[0], dir[1])
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def move_better_random(self):

        for event in pygame.event.get(): None
        dir = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])

        dirs = [(self.head.getUpCubeCoords(), UP),
                (self.head.getDownCubeCoords(), DOWN),
                (self.head.getRightCubeCoords(), RIGHT),
                (self.head.getLeftCubeCoords(), LEFT)]

        dir = random.choice(list(filter(lambda x: x[0] not in self.visited, dirs)))
        self.visited.append(dir[0])
        self.update_dir(dir[1][0], dir[1][1])
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def move_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.update_dir(-1, 0)

                elif keys[pygame.K_RIGHT]:
                    self.update_dir(1, 0)

                elif keys[pygame.K_UP]:
                    self.update_dir(0, -1)

                elif keys[pygame.K_DOWN]:
                    self.update_dir(0, 1)

                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def add_cube(self):
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
