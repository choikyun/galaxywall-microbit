from microbit import *
import random
import music

"""
GALAXY WALL for Micro:bit
Ver. 1.0.1 2018-03-02 / 2018-02-28
Choikyun
"""

# Defines
SHIP_FIX = 512
SHIP_COLOR = 8
WALL_COLOR = 6
AIM_COLOR = 7
FLASH_COLOR = 9
VOID_COLOR = 0

# Globals
ship_x = 2 * SHIP_FIX
aim_point = AIM_COLOR
aim_x = aim_y = 3
aim_blink = 4
buf = [[0 for i in range(5)] for j in range(5)]
flash_buf = [0] * 5
tick = running_time()
frame = score = 0
scroll = 300
scroll_def = 160


def draw_ship():
    draw(ship_x // SHIP_FIX, 4, SHIP_COLOR)


def aim():
    global aim_x, aim_y

    erase_aim()
    x = ship_x // SHIP_FIX
    y = 3
    aim_x = x
    while True:
        if buf[y][x] == VOID_COLOR and y == 0:
            aim_y = y
            break
        elif buf[y][x] >= WALL_COLOR:
            aim_y = y + 1
            break
        y -= 1


def draw_aim():
    global aim_blink, aim_point

    aim_blink -= 1
    if aim_blink == 0:
        aim_blink = 4
        aim_point ^= AIM_COLOR
    if flash_buf[aim_y] == 0:
        buf[aim_y][aim_x] = aim_point


def erase_aim():
    if buf[aim_y][aim_x] == AIM_COLOR:
        buf[aim_y][aim_x] = VOID_COLOR


def shot():
    if button_a.was_pressed():
        buf[aim_y][ship_x // SHIP_FIX] = WALL_COLOR
        music.pitch(1760, duration=8, wait=False)


def check_line():
    for y in range(5):
        hit = 0
        for x in range(5):
            hit += buf[y][x]
        if hit == WALL_COLOR * 5:
            flash_buf[y] = 10


def fill(line):
    global score

    erase_aim()
    score += line * 10
    while line < 4:
        for i in range(5):
            buf[line][i] = buf[line + 1][i]
        flash_buf[line] = flash_buf[line + 1]
        line += 1


def flash():
    for i in range(5):
        if flash_buf[i] == 0:
            continue
        else:
            flash_buf[i] -= 1
            if flash_buf[i] == 0:
                fill(i)
                music.play(["c5:1", "g5"], wait=False)
                break
            for x in range(5):
                buf[i][x] = FLASH_COLOR


def move_ship():
    global ship_x

    draw(ship_x // SHIP_FIX, 4, VOID_COLOR)
    ship_x += accelerometer.get_x()
    if ship_x <= 0:
        ship_x = 0
    elif ship_x >= 4 * SHIP_FIX:
        ship_x = 4 * SHIP_FIX


def new_wall():
    line = buf[0]
    for i in range(5):
        line[i] = WALL_COLOR
    for i in range(random.randrange(1, 5)):
        line[random.randrange(5)] = VOID_COLOR


def scroll_walls(init=False):
    global scroll

    scroll -= 1
    if scroll == 0 or init:
        scroll = scroll_def
        erase_aim()
        for y in range(4, 0, -1):
            for x in range(5):
                buf[y][x] = buf[y-1][x]
            flash_buf[y] = flash_buf[y-1]
        flash_buf[0] = 0
        new_wall()
        music.pitch(440, duration=16, wait=False)


def level_up():
    global scroll_def

    if frame % 600 == 0 and scroll_def > 60:
        scroll_def -= 5


def draw(x, y, col):
    buf[y][x] = col


def disp_buf():
    for y in range(5):
        for x in range(5):
            display.set_pixel(x, y, buf[y][x])


def clear_buf():
    for y in range(5):
        for x in range(5):
            buf[y][x] = 0


def init():
    music.set_tempo(bpm=200)
    line = 2
    while line > 0:
        line -= 1
        scroll_walls(init=True)


def print_score():
    global score

    music.play(music.POWER_DOWN, wait=False)
    display.scroll(str(score)+"  ", loop=True)


def check_over():
    over = False
    for x in range(5):
        if buf[4][x] == WALL_COLOR:
            over = True
    if over:
        music.reset()
        print_score()
        while True:
            pass


def wait():
    global tick

    while True:
        t = running_time()
        if t - tick > 30:
            tick = t
            break


# Main
init()
while True:
    wait()
    frame += 1
    scroll_walls()
    move_ship()
    aim()
    draw_aim()
    shot()
    check_line()
    flash()
    draw_ship()
    disp_buf()
    level_up()
    check_over()
