import cv2
import time
import keyboard
import numpy as np
from PIL import Image, ImageGrab

tofind = (950, 155, 1335, 685)

parts = [[(482, 279, 482 + 102, 279 + 102), (0, 0)],
[(627, 279, 627 + 102, 279 + 102), (1, 0)],
[(482, 423, 482 + 102, 423 + 102), (0, 1)],
[(627, 423, 627 + 102, 423 + 102), (1, 1)],
[(482, 566, 482 + 102, 566 + 102), (0, 2)],
[(627, 566, 627 + 102, 566 + 102), (1, 2)],
[(482, 711, 482 + 102, 711 + 102), (0, 3)],
[(627, 711, 627 + 102, 711 + 102), (1, 3)]]

def is_in(img, subimg):
    """return if 'subimg' is in 'img'"""
    subimg1 = cv2.cvtColor(np.array(subimg), cv2.COLOR_BGR2GRAY) # need gray image to do the matchTemplate
    res = cv2.matchTemplate(img, subimg1, cv2.TM_CCOEFF_NORMED)
    threshold = 0.65 # error coef
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        return True
    return False

def main(bbox):
    print('[*] Casino Fingerprint')
    im = ImageGrab.grab(bbox)
    im = im.resize((1920,1080))
    sub0_ = im.crop(tofind)
    sub0 = cv2.cvtColor(np.array(sub0_.resize((round(sub0_.size[0] * 0.77), round(sub0_.size[1] * 0.77)))), cv2.COLOR_BGR2GRAY) # need to resize the image because fingerprints parts is smaller than the image + need gray image to do the matchTemplate

    # will store the location of the rights fingerprints
    togo = [part[1] for part in parts if is_in(sub0, im.crop(part[0]))]

    # closing every images
    sub0_.close()
    im.close()

    moves = []

    x, y = 0, 0
    for pos in togo:
        while x != pos[0]:
            if x > pos[0]:
                x -= 1
                moves.append("a")
            else:
                x += 1
                moves.append("d")
        
        while y != pos[1]:
            if y > pos[1]:
                y -= 1
                moves.append("w")
            else:
                y += 1
                moves.append("s")
        moves.append("return")
    moves.append("tab")

    print('-', moves)
    for key in moves:
        keyboard.press_and_release(key)
        time.sleep(0.025)
    print('[*] END')
    print('=============================================')