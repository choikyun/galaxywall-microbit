from microbit import *
import random
import music

"""
GALAXY WALL for micro:bit
Ver. 1.0.1 2018-03-02 / 2018-02-28
Choikyun
"""

# Globals
ship_x = 2 * 512
aim_point = 7
aim_x = aim_y = 3
aim_blink = 4
buf = [[0 for i in range(5)] for j in range(5)]
flash_buf = [0] * 5
tick = running_time()
frame = score = 0
scroll = 300
scroll_def = 160
sound = 1


def draw_ship():
    draw(ship_x // 512, 4, 8)


def aim():
    global aim_x, aim_y
    erase_aim()
    x = ship_x // 512
    y = 3
    aim_x = x
    while True:
        if buf[y][x] == 0 and y == 0:
            aim_y = y
            break
        elif buf[y][x] >= 6:
            aim_y = y + 1
            break
        y -= 1


def draw_aim():
    global aim_blink, aim_point
    aim_blink -= 1
    if aim_blink == 0:
        aim_blink = 4
        aim_point ^= 7
    if flash_buf[aim_y] == 0:
        buf[aim_y][aim_x] = aim_point


def erase_aim():
    if buf[aim_y][aim_x] == 7:
        buf[aim_y][aim_x] = 0


def shot():
    if button_a.was_pressed():
        buf[aim_y][ship_x // 512] = 6
        if sound == 1:
            music.pitch(1760, duration=8, wait=False)


def check_line():
    for y in range(5):
        hit = 0
        for x in range(5):
            hit += buf[y][x]
        if hit == 6 * 5:
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
                if sound == 1:
                    music.play(["c5:1", "g5"], wait=False)
                break
            for x in range(5):
                buf[i][x] = 9


def move_ship():
    global ship_x, sound
    draw(ship_x // 512, 4, 0)
    ship_x += accelerometer.get_x()
    if ship_x <= 0:
        ship_x = 0
    elif ship_x >= 4 * 512:
        ship_x = 4 * 512

    if button_b.was_pressed():
        sound ^= 1



def new_wall():
    line = buf[0]
    for i in range(5):
        line[i] = 6
    for i in range(random.randrange(1, 5)):
        line[random.randrange(5)] = 0


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
        if sound == 1:
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
    line = 3
    while line > 0:
        line -= 1
        scroll_walls(init=True)


def print_score():
    global score
    if sound == 1:
        music.play(music.POWER_DOWN, wait=False)
    display.scroll(str(score)+"  ", loop=True)


def check_over():
    over = False
    for x in range(5):
        if buf[4][x] == 6:
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
