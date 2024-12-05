# Pizzazz technologies 2024
from multiprocessing import freeze_support
from wsgiref.simple_server import demo_app
import keyboard
import pygame
import win32api
import win32con
import win32gui
from data import *
from queue import Queue
from math import ceil
from time import sleep
pygame.init()
"""a = pygame.image.load('icon.png')
pygame.display.set_icon(a)"""
screen2 = pygame.display.set_mode((400, 150),  pygame.NOFRAME)
done = False
fuchsia = (255, 0, 128)  # Transparency color


# Create layered window
hwnd = pygame.display.get_wm_info()["window"]  # 1530, 875 # 976 563
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 1096, 634, 400, 150, 0)
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

# subprocess.Popen(["wmctrl", "-i", "-r", str(hwnd), "-b", "add,above"])
# Set window transparency color
win32gui.SetLayeredWindowAttributes(
    hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

color = "#C0C0C0"
font = pygame.font.Font('c:\\windows\\fonts\\seguihis.ttf', 20)
font2 = pygame.font.Font('c:\\windows\\fonts\\seguihis.ttf', 15)
font3 = pygame.font.Font('c:\\windows\\fonts\\segoeuil.ttf', 13)


def cut_text(input, block):
    # 40x3
    text = ["", "", ""]
    length = 40
    block_size = length*3
    for i in range(3):
        for j in range(length):
            index = (j+i*length)+block*block_size
            if index < len(input):
                text[i] += input[index]
            else:
                return text

    return text


def show(que: Queue):
    deactivate = False
    counter = 0
    block = 0
    data1 = ""
    i = 0
    prev_flag = False
    next_flag = False
    while 1:

        hide = True

        text = ["", "", ""]
        if not que.empty():
            data1 = que.get()

        if block > ceil(len(data1)/120):
            block -= 1

        text = cut_text(data1, block)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # control
        if (keyboard.is_pressed("right alt") or keyboard.is_pressed("alt gr")) and not deactivate:
            hide = False
        if not keyboard.is_pressed(","):
            prev_flag = False
        if not keyboard.is_pressed("."):
            next_flag = False

        if keyboard.is_pressed("q") and keyboard.is_pressed("w"):
            deactivate = True
        if keyboard.is_pressed("a"):
            deactivate = False
        if keyboard.is_pressed(",") and not prev_flag:
            if block > 0:
                block -= 1
            prev_flag = True
        if keyboard.is_pressed(".") and not next_flag:
            block += 1
            next_flag = True

        screen2.fill(fuchsia)  # Transparent background

        # text
        Header = font.render("Activate Windows", False, color)
        default_text = font2.render(
            "Go to Settings to activate Windows.", False, color)
        text1_render = font3.render(
            text[0], False, color)
        text2_render = font3.render(
            text[1], False, color)
        text3_render = font3.render(
            text[2], False, color)
        text_placed = font3.render(
            "Placed", False, "pink")
        text_not_placed = font3.render(
            "Not placed", False, "pink")

        screen2.blit(Header, (10, 20))

        if counter > 5:
            counter = 0
            data1 = ""
        if hide and data1 == "Placed":
            screen2.blit(text_placed, (10, 46))
            sleep(0.1)
            counter += 1
        elif hide and data1 == "Not placed":
            screen2.blit(text_not_placed, (10, 46))
            sleep(0.1)
            counter += 1
        elif hide:
            screen2.blit(default_text, (10, 46))
        else:
            screen2.blit(text1_render, (10, 46))
            screen2.blit(text2_render, (10, 61))
            screen2.blit(text3_render, (10, 76))

        pygame.display.update()


if __name__ == "__main__":
    freeze_support()
    qu = Queue()
    show(qu)
