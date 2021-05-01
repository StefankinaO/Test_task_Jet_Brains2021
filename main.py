from PIL import Image, ImageGrab
import os
from pywinauto import Application
import subprocess,time,psutil
import win32gui
import win32ui, win32com, win32process
import psutil
from win32gui import GetForegroundWindow
def enum_window_callback(hwnd, pid):
    tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
    if pid == current_pid and win32gui.IsWindowVisible(hwnd):
        windows.append(hwnd)



for root, dirs, files in os.walk("./2021-test-assignment-main"):
    for file in files:
        if file.endswith(".py"):
             process = subprocess.Popen(['notepad.exe', os.path.join(root, file)])

             notepads = [item for item in psutil.process_iter() if item.name() == 'notepad.exe']
             print(notepads)  # [<psutil.Process(pid=4416, name='notepad.exe') at 64362512>]

             # Просто pid первого попавшегося процесса с именем файла notepad.exe:
             pid = next(item for item in psutil.process_iter() if item.name() == 'notepad.exe').pid
             # (вызовет исключение StopIteration, если Блокнот не запущен)
             # pid = 4416  # pid уже получен на предыдущем этапе
             windows = []

             win32gui.EnumWindows(enum_window_callback, pid)

             print(win32gui.GetWindowRect(GetForegroundWindow()))
             app = Application().connect(process=pid)
             app.top_window().set_focus()
             bbox = win32gui.GetWindowRect(GetForegroundWindow())
             img = ImageGrab.grab(bbox)

             img.save(file + '.png', "png")
             time.sleep(3)
             pobj = psutil.Process(process.pid)
             # list children & kill them
             for c in pobj.children(recursive=True):
                 c.kill()
             pobj.kill()