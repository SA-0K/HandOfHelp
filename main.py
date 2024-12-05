# Pizzazz technologies 2024
import pynput
import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
import gui
import data
from threading import Thread
from queue import Queue

global donepositioning
donepositioning = False
position = [1162, 198, 1840, 875]  # [0, 0, 0, 0]


def on_press(key):
    global donepositioning
    if (str(key) == "Key.enter"):
        donepositioning = True
        return False


def on_click(x, y, button, pressed):
    global position
    if button == pynput.mouse.Button.left:
        if pressed:
            position[0], position[1] = (x, y)
        else:
            position[2], position[3] = (x, y)
            return False


def get_screen_position():
    listener = pynput.mouse.Listener(on_click=on_click)
    listener.start()

    listener2 = pynput.keyboard.Listener(on_press=on_press)
    listener2.start()

    listener.join()
    listener2.join()


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def main(que):
    global donepositioning

    last = ""

    
    while True:
        if not donepositioning:
            que.put("Not placed")
            get_screen_position()
            que.put("Placed")
            print(position)
        try:
            screen = np.array(ImageGrab.grab(
                bbox=(position[0], position[1], position[2], position[3])))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            # cv2.imshow("winname", screen)

            recognized_text = pytesseract.image_to_string(
                screen, lang="ukr+eng")

            if recognized_text != last:
                last = recognized_text
                que.put(data.find_page(last))

            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                exit()
                break
            elif (cv2.waitKey(1) & 0xFF) == ord('r'):
                get_screen_position()
        except ValueError:
            donepositioning = False
        except Exception as e:
            print(e)


q = Queue()
q.put("Test")


t2 = Thread(target=main, args=(q,))


t2.start()


gui.show(q)
t2.join()
