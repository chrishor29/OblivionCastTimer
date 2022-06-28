import pyWinhook
import pythoncom

def OnMouseEvent(event):
    if event.Wheel == 1:
        print('ScrollUp')
    elif event.Wheel == -1:
        print('ScrollDown')
    return True

# create the hook mananger
hm = pyWinhook.HookManager()
# register two callbacks
hm.MouseWheel = OnMouseEvent
# hook into the mouse and keyboard events
hm.HookMouse()

pythoncom.PumpMessages()

