#Snake Tutorial Python
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from snake import snake
from cube import cube
import time

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows, surface)
    pygame.display.update()


def randomSnack(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break

    return (x,y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def game_over(s):
    print('Score: ', len(s.body))
    # message_box('You Lost!', 'Play again...')
    s.reset((random.randrange(rows),random.randrange(rows)))


def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    flag = True

    redrawWindow(win)
    clock = pygame.time.Clock()
    print("done sleeping")

    while flag:
        pygame.time.delay(50)
        clock.tick(25)
        # s.move_keys()
        s.move_random()
        # s.move_bfs(snack)
        # s.move_bfs(snack)
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))

        # Lose from collision with wall
        if ((s.body[0].pos[0] == 19 and s.body[0].dirnx == -1) or
            (s.body[0].pos[0] == 0 and s.body[0].dirnx == 1) or
            (s.body[0].pos[1] == 0 and s.body[0].dirny == 1) or
            (s.body[0].pos[1] == 19 and s.body[0].dirny == -1)):
            game_over(s)
        # Lose by collision with body
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                game_over(s)
                break




        redrawWindow(win)

main()
