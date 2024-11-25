import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
import os

root = Tk()
root.title("UsTan")
root.geometry("1200x700")

mainDir = "mainDir/"
dirName = ""
LBBList = list()
fileIcon = PhotoImage(file="images.png")

LB_startText = Label(font = 20)
LB_startText.grid(row = 0, column = 0)
BT_hz = tk.Button(text = "посмотреть какие файлы мне кинули")
BT_hz.grid(row = 0, column = 1)



try:
    os.mkdir("mainDir")
except Exception as ex:
    pass
dirName = filedialog.askdirectory()
if dirName != "":
    tempList = os.listdir(dirName)
    r = 1
    c = 0
    for x in tempList:
        labelInList = tk.Label(name = f"{x}", image = fileIcon, text = f"{x}",compound = "top", width = 100 ,height = 100) # сделать серый эффект при наведении
        labelInList.grid(row = r, column = c, padx = 10,pady = 10)
        c+=1
        if c == 4:
            c=0
            r+=1
    r = 1
    c = 0
    LB_startText.text = f"Файлы в папке {dirName}"
else:
    while(dirName == ""):
        showerror("Ошибка","Выберите папку с файлами.")
        dirName = filedialog.askdirectory()
