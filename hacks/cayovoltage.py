import cv2
import time
import keyboard
import numpy as np
from PIL import ImageGrab

DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 0, 1): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9
}

RIGHT_SYMBOLS = {
    (0, 1): 10,
    (1, 0): 2,
    (0, 0): 1
}

moves = {
    (0, 0, 1, 1, 2, 2): ['enter', 'return', 'enter', 'return', 'enter', 'return'], # (1-1) + (2-2) + (3-3)
    (0, 0, 1, 2, 2, 1): ['enter', 'return', 'enter', 's', 'return', 'enter', 'return'], # (1-1) + (2-3) + (3-2)
    (0, 1, 1, 0, 2, 2): ['enter', 's', 'return', 'enter', 'w', 'return', 'enter', 'return'], #(1-2) + (2-1) + (3-3)
    (0, 1, 1, 2, 2, 0): ['enter', 's', 'return', 'enter', 'return', 'enter', 'return'], # (1-2) + (2-3) + (3-1)
    (0, 2, 1, 0, 2, 1): ['enter', 'w', 'return', 'enter', 'w', 'return', 'enter', 'return'], # (1-3) + (2-1) + (3-2)
    (0, 2, 1, 1, 2, 0): ['enter', 'w', 'return', 'enter', 'return', 'enter', 'return'] # (1-3) + (2-2) + (3-1) 
}

# objective numbers
objectivenumber_height = [123, 137, 137, 154, 173, 173, 195] #objective numbers have same height
objectivenumber_length_0 = [865, 849, 881, 865, 849, 881, 865] # first number
objectivenumber_length_1 = [955, 939, 971, 955, 939, 971, 955] # second number
objectivenumber_length_2 = [1043, 1029, 1061, 1043, 1029, 1061, 1043] # third number

# left numbers
leftnumber_length = [509, 495, 527, 509, 495, 527, 509] # left nubmers have same length
leftnumber_height_0 = [271, 287, 287, 303, 323, 323, 343] # first number
leftnumber_height_1 = [507, 522, 522, 540, 557, 557, 579] # second number
leftnumber_height_2 = [741, 755, 755, 773, 791, 791, 813] # third number

# right symbols
rightsymbol_length = [1351, 1349] # right symbols have same length
rightsymbol_height_0 = [305, 277] # first symbol
rightsymbol_height_1 = [541, 513] # second symbol
rightsymbol_height_2 = [775, 747] # third symbol

def pixel_check(x, y, img, maximum, dictionary):
    hints = []

    for i in range(0, maximum):
        pixel = img[y[i]:y[i] + 1, x[i]:x[i] + 1]

        if np.mean(pixel):
            hints.append(1)
        else:
            hints.append(0)
            
    return dictionary[tuple(hints)]

def objective_number(img):
    value = (100 * (pixel_check(objectivenumber_length_0, objectivenumber_height, img, 7, DIGITS_LOOKUP))) + (10 * (pixel_check(objectivenumber_length_1, objectivenumber_height, img, 7, DIGITS_LOOKUP))) + pixel_check(objectivenumber_length_2, objectivenumber_height, img, 7, DIGITS_LOOKUP)
    return value

def left_numbers(img):
    values = []
    values.append(pixel_check(leftnumber_length, leftnumber_height_0, img, 7, DIGITS_LOOKUP))
    values.append(pixel_check(leftnumber_length, leftnumber_height_1, img, 7, DIGITS_LOOKUP))
    values.append(pixel_check(leftnumber_length, leftnumber_height_2, img, 7, DIGITS_LOOKUP))

    return values

def right_symbols(img):
    values = []
    values.append(pixel_check(rightsymbol_length, rightsymbol_height_0, img, 2, RIGHT_SYMBOLS))
    values.append(pixel_check(rightsymbol_length, rightsymbol_height_1, img, 2, RIGHT_SYMBOLS))
    values.append(pixel_check(rightsymbol_length, rightsymbol_height_2, img, 2, RIGHT_SYMBOLS))

    return values

def calculate(a, b, c):
    try:
        for i in range(0, 6):
            keys = []
            keys.append(list(tuple(moves)[i]))

            for z, x, v, n, k, l in keys:
                if (a == b[z] * c[x] + b[v] * c[n] + b[k] * c[l]):
                    print('-', moves[tuple(moves)[i]])
                    for key in (moves[tuple(moves)[i]]):
                        keyboard.press_and_release(key)
                        if key == 's' or 'w' or 'enter':
                            time.sleep(0.025)
                        if key == 'return':
                            time.sleep(1.3)
                    raise NotImplementedError
    except:
        print('[*] END')
        print('=============================================')

def main(bbox):
    print('[*] Cayo Voltage Hack')

    im = ImageGrab.grab(bbox)
    im = im.resize((1920,1080))

    grayImage = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

    objectivenumber = objective_number(blackAndWhiteImage)
    leftnumbers = left_numbers(blackAndWhiteImage)
    rightnumbers = right_symbols(blackAndWhiteImage)

    print('- ', objectivenumber, leftnumbers, rightnumbers)

    calculate(objectivenumber, leftnumbers, rightnumbers)