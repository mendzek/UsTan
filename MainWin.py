import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
import os
import json
import sqlite3

root = Tk()
root.title("UsTan")
root.geometry("1200x700")

DATA_FILE = "tests.json"
mainDir = "mainDir/"
dirName = ""
LBBList = list()
fileIcon = PhotoImage(file="fileIMG.png")
fileIconCursor = PhotoImage(file="fileIMG(gray).png")
fileIconChosen = PhotoImage(file="fileIMG(chosen).png")
dirIcon = PhotoImage(file="dirIMG.png")
dirIconCursor = PhotoImage(file="dirIMG(gray).png")
dirIconChosen = PhotoImage(file="dirIMG(chosen).png")
clickedOrNot = False
FilesList = list()


LB_startText = Label(text = "Выберите папку", font = 20)
LB_startText.pack(anchor = NW)
BT_viewReceived = tk.Button(text = "посмотреть какие файлы мне кинули")
BT_viewReceived.pack(anchor = NE)
BT_choose = tk.Button(text="Выбрать")
BT_choose.pack(anchor=SE)

class SendWin(Tk):
    def __init__(self):
        super().__init__()

        self.title("UsTan")
        self.geometry("1200x700")

        sqlPath = "database.db"
        self.UsersList = list()
        self.FilesList = FilesList

        self.connect = sqlite3.connect(sqlPath, timeout=5.0, detect_types=0,
                                       isolation_level='DEFERRED', check_same_thread=True, factory=sqlite3.Connection,
                                       cached_statements=128, uri=False)
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT COUNT(*) FROM users")
        self.numOfRows = self.cursor.fetchone()[0]
        self.tupleFromDB = tuple()
        self.tempList = list()
        for x in range(self.numOfRows + 1):
            self.cursor.execute(f"SELECT * FROM users WHERE id={x}")
            self.tupleFromDB = self.cursor.fetchone()
            self.tempList.append(self.tupleFromDB)
        self.tempList.pop(0)
        for x in self.tempList:
            self.UsersList.append(x[1])
        self.BT_send = tk.Button(self, text="Отправить")
        self.BT_send.bind("<ButtonRelease>", onClickSend)
        self.BT_send.pack(anchor=SE)
        self.LB_startText = Label(self,text="Кому переслать файл/файлы?", font=20)
        self.LB_startText.pack(anchor=NW)
        self.FrameUsers = ttk.Frame(self, borderwidth=1, relief=SOLID)
        for x in range(len(self.UsersList)):
            self.BT_star = tk.Button(self.FrameUsers,text="star")
            self.BT_star.grid(column=0, row=x)
            self.LB_userName = Label(self.FrameUsers, text=self.UsersList[x], font=20)
            self.LB_userName.grid(column=1, row=x)
            self.BT_check = tk.Button(self.FrameUsers, text="check")
            self.BT_check.grid(column=2, row=x)
        self.FrameUsers.place(anchor=NW, x=40, y=100, width= 200, height=400)
        self.FrameFiles = ttk.Frame(self, borderwidth=1, relief=SOLID)
        for x in range(len(self.FilesList)):
            self.LB_fileName = Label(self.FrameFiles, text=self.FilesList[x]["text"], font=20)
            self.LB_fileName.grid(column=0, row=x)
        self.FrameFiles.place(anchor=NW, x=800, y=100, width=200, height=400)


def CheckFileType(dirOrFile):
    if os.path.isdir(dirOrFile):
        return "dir"
    elif os.path.isfile(dirOrFile):
        return "file"
    else:
        return "unknown"

def onClickFiles(event):
    tempLabel = event.widget
    if tempLabel not in FilesList:
        tempLabel["image"] = fileIconChosen
        FilesList.append(tempLabel)
    else:
        tempLabel["image"] = fileIconCursor
        FilesList.remove(tempLabel)

def onClickChoose(event):
    sendWin = SendWin()

def onClickSend(event):
    pass #создать окно результата отправки

def onClickViewReceived(event):
    pass

def enterLeaveFile(event):
    tempLabel = event.widget
    if tempLabel not in FilesList:
        if event.type == '7':
            tempLabel["image"] = fileIconCursor
        elif event.type == '8' :
            tempLabel["image"] = fileIcon

def enterLeaveDir(event):
    tempLabel = event.widget
    tempText = tempLabel["text"] + "(выбрано)"
    if event.type == '7':
        tempLabel["image"] = dirIconCursor
    elif event.type == '8':
        tempLabel["image"] = dirIcon

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
        tempFile = dirName + f"/{x}"
        #temp = os.path.abspath(x)
        tempDir = os.getcwd()
        if CheckFileType(tempFile) == "file":
            labelInList = tk.Label(image = fileIcon, text = f"{x} file", compound = "top", width = 100 ,height = 100) # сделать серый эффект при наведении
            labelInList.bind("<Enter>", enterLeaveFile)
            labelInList.bind("<Leave>", enterLeaveFile)
            labelInList.bind("<ButtonRelease>", onClickFiles)
            labelInList.pack(padx = 10,pady = 10, side = LEFT)
            LBBList.append(labelInList)
            c+=1
            if c == 4:
                c=0
                r+=1
        elif CheckFileType(tempFile) == "dir":
            labelInList = tk.Label(image = dirIcon, text = f"{x} directory",compound = "top", width = 100 ,height = 100) # сделать серый эффект при наведении
            labelInList.bind("<Enter>", enterLeaveDir)
            labelInList.bind("<Leave>", enterLeaveDir)
            labelInList.pack(padx = 10,pady = 10, side = LEFT)
            LBBList.append(labelInList)
            c+=1
            if c == 4:
                c=0
                r+=1


        else:
            showerror("Ошибка","Неизвестный тип файла.")
        r = 1
        c = 0
    LB_startText.config(text = f"Файлы в папке {dirName}")
else:
    while(dirName == ""):
        showerror("Ошибка","Выберите папку с файлами.")
        dirName = filedialog.askdirectory()

BT_viewReceived.bind("<ButtonRelease>", onClickViewReceived)
BT_choose.bind("<ButtonRelease>", onClickChoose)

