import json
import os
import sys
import time
import random
from glob import glob

from apng import APNG
from PIL import Image, ImageTk
import io
import tkinter as tk
import threading

window = tk.Tk()
window.overrideredirect(True)
window.configure(background='white')
window.wm_attributes("-topmost", True)
window.wm_attributes("-transparentcolor", "white")
# window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
# window.geometry("+0+0") # 定位到左上角展示

# 定位到右下角展示
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()
window.geometry(f"+{screenWidth - 300}+{screenHeight - 300}")

# 菜单kaishi

# Create a right-click context menu
menu = tk.Menu(window, tearoff=0)
menu.add_command(label="Exit", command=lambda: window.destroy())


# Function to show the context menu
def show_menu(event):
    menu.post(event.x_root, event.y_root)


# Bind the show_menu function to the window
window.bind('<Button-3>', show_menu)

# 菜单结束


# 底部菜单

import pystray
from pystray import MenuItem as item


def on_select(icon, item):
    icon.stop()
    window.after(1, window.destroy)
    # sys.exit()


tryImage = Image.open('D:/develop/opensourcetools/Rising-KaKa/Resources/png/Hello/0.png')
trayMenu = (item('Exit', on_select), item('Open', on_select))
icon = pystray.Icon("name", tryImage, "Lion", trayMenu)
# icon.run() # 直接调用就阻塞了
threading.Thread(target=icon.run).start()


def moveWindow(event):
    window.geometry('+{0}+{1}'.format(event.x_root, event.y_root))


window.bind('<B1-Motion>', moveWindow)


def startAnimation(filePath):
    apng = APNG.open(filePath)
    for frame, infor in apng.frames:
        img = Image.open(io.BytesIO(frame.to_bytes()))
        tkImage = ImageTk.PhotoImage(img)
        # window.geometry("{}x{}+{}+{}".format(infor.width, infor.height, infor.x_offset, infor.y_offset))
        # x = window.winfo_x()
        # y = window.winfo_y()
        # window.geometry(f'+{x}+{y}')
        label = tk.Label(window, image=tkImage, bg='white')
        label.pack()
        window.update()
        time.sleep(infor.delay / 10)
        label.pack_forget()
        # window.destroy()


def startKakaAnimation():
    resourceFolder = './Resources/apng/'
    fileList = os.listdir(resourceFolder)
    random.shuffle(fileList)
    while True:
        for fileName in fileList:
            if fileName.endswith('.png'):
                startAnimation(os.path.join(resourceFolder, fileName))
            if os.path.exists("stop"):
                os.remove("stop")
                on_select(icon, "StopFileDetected")
            # time.sleep(random.randint(1, 120))  # 动画切换时间


def generateApng():
    with open('./Resources/metadata.json') as f:
        data = json.load(f)
    for key in data.keys():
        files = glob('./Resources/png/{}/*.png'.format(key))
        files.sort(key=lambda x: int(os.path.split(x)[1][:-4]))
        APNG.from_files(files, delay=1, delay_den=int(data[key]['FrameRate'])).save(
            "./Resources/apng/{}.png".format(key))
