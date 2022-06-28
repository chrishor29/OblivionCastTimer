
# billentyűt lenyomom
# ha stunlock, akkor nem csinál semmit
# ha fut casttimer már, azt reseteli, kivéve ha 2es
# ha '2' volt a billentyű, akkor elindítja a casttimert
  # ha casttimer végigér, akkor stunlock indul el


# ez csak beállít egy window title nevet -> ez alapján zárja be majd .ahk, ha bezártam obliviont!
from os import system
system("title fastpy")

import threading
import pythoncom, pyWinhook, sys, logging
import time
from pynput.keyboard import Key, Controller
import ctypes
import winsound

keySending = False
thread_cast = None
thread_stun = None
SendInput = ctypes.windll.user32.SendInput


# C struct redefinitions 

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))



# szakdolgozatom:

def Finished_stun():
    global thread_stun
    winsound.Beep(700, 150)
    print("- stunlock finished -")
    thread_stun = None

def Finished_casting():
    global thread_cast, thread_stun, keySending
    print("- casting finished -")
    keySending = True
    thread_cast = None
    thread_stun = threading.Timer(interval = 4, function = Finished_stun)
    thread_stun.start()
    print("- stunlock starts -")
    keyboard = Controller()
    PressKey(0x03) # DirectX keycode!!
    time.sleep(0.1)
    ReleaseKey(0x03) # DirectX keycode!!

def OnKeyboardEvent(event):
    global thread_cast, thread_stun, keySending
    print("Key:", chr(event.Ascii), " (KeyID:", event.KeyID, ")")
    # if chr(event.Ascii) == '2' and keySending == True:
    if event.KeyID == 50 and keySending == True: # numlock 2es miatt kell keyID
        print("- key sending -")
        keySending = False
        return True
    elif thread_stun is not None:
        print("- under stunlock -")
        return False
    # elif chr(event.Ascii) == '2':
    elif event.KeyID == 50:
        if thread_cast is None:
            print("- casting starts -")
            thread_cast = threading.Timer(interval = 3, function = Finished_casting)
            thread_cast.start()
            winsound.Beep(400, 150)
            return False
        else:
            print("- already casting, relax bro -")
            return False
    # elif chr(event.Ascii) != '2' and thread_cast is not None:
    elif event.KeyID != 50 and thread_cast is not None:
        print("- casting canceled -")
        thread_cast.cancel()
        thread_cast = None
        winsound.Beep(200, 150)
    return True
    # ha false return, akkor nem fogad inputot sehol, csak pythonban --> ctrl + alt + del + egérrel tudok kilépni akkor

def OnMouseEvent(event):
    if event.Wheel == 1:
        print('ScrollUp')
       # PressKey(0x09) # DirectX keycode!!
       # time.sleep(0.1)
       # ReleaseKey(0x09) # DirectX keycode!!
    elif event.Wheel == -1:
        print('ScrollDown')
       # PressKey(0x0A) # DirectX keycode!!
       # time.sleep(0.1)
       # ReleaseKey(0x0A) # DirectX keycode!!
    return True


# create the hook mananger
hm = pyWinhook.HookManager()
# register two callbacks
hm.KeyDown = OnKeyboardEvent
hm.MouseWheel = OnMouseEvent
# hook into the mouse and keyboard events
hm.HookKeyboard()
hm.HookMouse()

pythoncom.PumpMessages() # nem zárul be egyből



