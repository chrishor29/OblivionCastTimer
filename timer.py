


import threading
def F_castTimer():
   print("- casting -")

timer = threading.Timer(3.0, F_castTimer)
timer.start()

print("Exit\n")

