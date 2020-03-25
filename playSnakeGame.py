import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from snake import snake
from cube import cube
import time
import sys
import datetime

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

def game_over(s, argv):
    print('Score: ', len(s.body))
    scores.append(len(s.body))
    with open(argv[0][2:] + '_lifetime_log.txt', 'a+') as f:
        f.write('%s\n' % len(s.body))
    # message_box('You Lost!', 'Play again...')
    s.clear_visited()
    s.reset((random.randrange(rows),random.randrange(rows)))


def main(argv):
    global width, rows, s, snack, scores
    width = 500
    scores = []
    rows = 20

    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    flag = True
    redrawWindow(win)
    clock = pygame.time.Clock()
    count = 0


    while flag and count < 50:
        pygame.time.delay(10)
        clock.tick(10)
        s.move_with_mode(argv[0], snack)
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))

        # Lose from collision with wall
        if ((s.body[0].pos[0] == -1) or
            (s.body[0].pos[0] == rows) or
            (s.body[0].pos[1] == -1) or
            (s.body[0].pos[1] == rows)):
            game_over(s, argv)
            count = count +1
        # Lose by collision with body
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                game_over(s, argv)
                count = count + 1
                break

        redrawWindow(win)

    # Save Score results to an outfile
    with open(argv[0] + datetime.datetime.today().strftime('%d-%m-%Y')+ '.txt', 'w') as f:
        for listitem in scores:
            f.write('%s\n' % listitem)



if __name__ == "__main__":
   main(sys.argv[1:])
