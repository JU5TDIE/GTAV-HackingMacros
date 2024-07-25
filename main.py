import sys
import time
import pynput
from threading import Thread
from win32gui import FindWindow, GetWindowRect
from hacks import casinofingerprint, casinokeypad, cayofingerprint, cayovoltage

def print_banner():
    print('''

██╗░░░░░███████╗░██████╗████████╗███████╗██████╗░  ██╗░░░██╗███████╗██████╗░  ██████╗░░░░░█████╗░
██║░░░░░██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗  ██║░░░██║██╔════╝██╔══██╗  ╚════██╗░░░██╔══██╗
██║░░░░░█████╗░░╚█████╗░░░░██║░░░█████╗░░██████╔╝  ╚██╗░██╔╝█████╗░░██████╔╝  ░░███╔═╝░░░██║░░██║
██║░░░░░██╔══╝░░░╚═══██╗░░░██║░░░██╔══╝░░██╔══██╗  ░╚████╔╝░██╔══╝░░██╔══██╗  ██╔══╝░░░░░██║░░██║
███████╗███████╗██████╔╝░░░██║░░░███████╗██║░░██║  ░░╚██╔╝░░███████╗██║░░██║  ███████╗██╗╚█████╔╝
╚══════╝╚══════╝╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝  ░░░╚═╝░░░╚══════╝╚═╝░░╚═╝  ╚══════╝╚═╝░╚════╝░
                                                                                          ''')

def print_credits():
    print('''
Made by JUSTDIE
Special thanks to RedHeadEmile
    ''')
    
def check_window():
    print('[*] Searching Grand Theft Auto V...')

    while True:
        hwnd = FindWindow(None, "Grand Theft Auto V")
        
        if hwnd:
            print('[*] Grand Theft Auto V Detected!')
            print('')
            print('=============================================')
            return GetWindowRect(hwnd)
        
        time.sleep(1)

def casino_fingerprint(bbox):
    thread = Thread(target=casinofingerprint.main, args=(bbox,))
    thread.start()

def casino_keypad(bbox):
    thread = Thread(target=casinokeypad.main, args=(bbox,))
    thread.start()

def cayo_fingerprint(bbox):
    thread = Thread(target=cayofingerprint.main, args=(bbox,))
    thread.start()

def cayo_voltage(bbox):
    thread = Thread(target=cayovoltage.main, args=(bbox,))
    thread.start()

def shutdown():
    sys.exit()

def main():
    print_banner()
    print_credits()

    bbox = check_window()
    if bbox:
        with pynput.keyboard.GlobalHotKeys({
                '<F4>': shutdown,
                '<F5>': lambda: casino_fingerprint(bbox),
                '<F6>': lambda: casino_keypad(bbox),
                '<F7>': lambda: cayo_fingerprint(bbox),
                '<F8>': lambda: cayo_voltage(bbox)}) as h:
            h.join()

if __name__ == "__main__":
    main()