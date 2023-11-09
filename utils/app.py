import json
import os
import time
import random
from glob import glob

from apng import APNG
from PIL import Image, ImageTk
import io
import tkinter as tk

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
window.geometry(f"+{screenWidth - 200}+{screenHeight - 200}")


def moveWindow(event):
    window.geometry('+{0}+{1}'.format(event.x_root, event.y_root))


window.bind('<B1-Motion>', moveWindow)


def startAnimation(filePath):
    apng = APNG.open(filePath)
    for frame, infor in apng.frames:
        img = Image.open(io.BytesIO(frame.to_bytes()))
        tkImage = ImageTk.PhotoImage(img)
        # window.geometry("{}x{}+{}+{}".format(infor.width, infor.height, infor.x_offset, infor.y_offset))
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
            # time.sleep(random.randint(1, 120))  # 动画切换时间


def generateApng():
    with open('./Resources/metadata.json') as f:
        data = json.load(f)
    for key in data.keys():
        files = glob('./Resources/png/{}/*.png'.format(key))
        files.sort(key=lambda x: int(os.path.split(x)[1][:-4]))

        APNG.from_files(files, delay=1, delay_den=int(data[key]['FrameRate'])).save(
            "./Resources/apng/{}.png".format(key))
