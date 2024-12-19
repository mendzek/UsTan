import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
import os
import sqlite3
import shutil


sqlPath = "database.db"
MainUser = ""
mainDir = "mainDir/"
dirName = ""
LBBList = list()
FilesList = list()
FilesDict = {}

class RecievedWin(Tk):
    def __init__(self):
        super().__init__()

        self.title("UsTan")
        self.geometry("550x400")

        def onClickCheck(event):
            self.tempLabel = event.widget
            if self.tempLabel["text"] == "Отправить":
                self.tempLabel["text"] = "Не отправлять"
                self.SelectedUsersList.append(self.CheckingsDict[self.tempLabel])
            else:
                self.tempLabel["text"] = "Отправить"
                self.SelectedUsersList.remove(self.CheckingsDict[self.tempLabel])

        self.UsersList = list()
        self.CheckingsDict = {}
        self.SelectedUsersList = list()
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
            if x[1] != MainWin.MainUser:
                self.UsersList.append(x[1])
        self.LB_userName = Label(self, text=self.UsersList[x], font=20)
        self.LB_userName.grid(column=1, row=x)
        self.BT_check = tk.Button(self, text="Отправить")
        self.BT_check.grid(column=2, row=x)
        self.BT_check.bind("<ButtonRelease>", onClickCheck)

RecievedWin = RecievedWin()

class MainWin:
    root = Tk()
    root.title("UsTan")
    root.geometry("700x500")


    fileIcon = PhotoImage(file="fileIMG.png")
    fileIconCursor = PhotoImage(file="fileIMG(gray).png")
    fileIconChosen = PhotoImage(file="fileIMG(chosen).png")
    dirIcon = PhotoImage(file="dirIMG.png")
    dirIconCursor = PhotoImage(file="dirIMG(gray).png")
    dirIconChosen = PhotoImage(file="dirIMG(chosen).png")
    clickedOrNot = False



    Frame1=Frame(root)
    Frame1.pack(side=TOP,fill=X)
    Frame2=Frame(root)
    Frame2.pack(side=TOP,fill=X)

    LB_startText = Label(Frame1, text = "Выберите папку", font = 20)
    LB_startText.pack(anchor = NW)
    #BT_viewReceived = tk.Button(text = "посмотреть какие файлы мне кинули")
    #BT_viewReceived.pack(anchor = NE)
    BT_choose = tk.Button(Frame1, text="Выбрать")
    BT_choose.pack(anchor=SE)
    BT_openDir = tk.Button(Frame1, text="выбрать папку")
    BT_openDir.pack(anchor=NW)
    text = tk.Text(Frame2)
    scrollbar = ttk.Scrollbar(Frame2,orient="vertical", command=text.yview)
    scrollbar.grid(row=0,column=1,rowspan=15, columnspan=1, sticky=NS)


    def CheckFileType(self, dirOrFile):
        if os.path.isdir(dirOrFile):
            return "dir"
        elif os.path.isfile(dirOrFile):
            return "file"
        else:
            return "unknown"

    def onClickFiles(self, event):
        tempLabel = event.widget
        if tempLabel not in MainWin.FilesList:
            tempLabel["image"] = MainWin.fileIconChosen
            MainWin.FilesList.append(tempLabel)
        else:
            tempLabel["image"] = MainWin.fileIconCursor
            MainWin.FilesList.remove(tempLabel)

    def onClickChoose(self, event):
        sendWin = SendWin()

    def onCLickOpenDir(self, event):
        MainWin.LBBList.clear()
        MainWin.text.configure(state="normal")
        MainWin.text.delete(1.0, END)
        MainWin.FilesView(filedialog.askdirectory())

    def onClickViewReceived(self, event):
        RecievedWin.__init__()
        pass

    def enterLeaveFile(self, event):
        tempLabel = event.widget
        if tempLabel not in MainWin.FilesList:
            if event.type == '7':
                tempLabel["image"] = MainWin.fileIconCursor
            elif event.type == '8' :
                tempLabel["image"] = MainWin.fileIcon

    def enterLeaveDir(self, event):
        tempLabel = event.widget
        tempText = tempLabel["text"] + "(выбрано)"
        if event.type == '7':
            tempLabel["image"] = MainWin.dirIconCursor
        elif event.type == '8':
            tempLabel["image"] = MainWin.dirIcon

    try:
        os.mkdir("mainDir")
    except Exception as ex:
        pass



    dirName = filedialog.askdirectory()
    def FilesView(self, dirName):
        if dirName != "":
            tempList = os.listdir(dirName)
            r = 1
            c = 0
            for x in tempList:
                tempFile = dirName + f"/{x}"
                tempDir = os.getcwd()
                if MainWin.CheckFileType(tempFile) == "file":
                    labelInList = tk.Label(MainWin.Frame2, image = MainWin.fileIcon, text = f"{x}", compound = "top", width = 100 ,height = 150)
                    labelInList.bind("<Enter>", self.enterLeaveFile)
                    labelInList.bind("<Leave>", self.enterLeaveFile)
                    labelInList.bind("<ButtonRelease>", self.onClickFiles)
                    labelInList.grid(row=r,column=c, padx = 10,pady = 10)
                    MainWin.text.configure(yscrollcommand=MainWin.scrollbar.set)
                    MainWin.text.grid(row=0,column=0)


                    MainWin.LBBList.append(labelInList)
                    MainWin.FilesDict[labelInList] = tempFile
                    c+=1
                    if c == 6:
                        MainWin.text.window_create("end", window=labelInList)
                        MainWin.text.insert("end", "\n")
                        c=0
                        r+=1
                    else:
                        MainWin.text.window_create("end", window=labelInList)
                        MainWin.text.insert("end", "")
                # elif CheckFileType(tempFile) == "dir":
                #     labelInList = tk.Label(image = dirIcon, text = f"{x} directory",compound = "top", width = 100 ,height = 100)
                #     labelInList.bind("<Enter>", enterLeaveDir)
                #     labelInList.bind("<Leave>", enterLeaveDir)
                #     labelInList.pack(padx = 10,pady = 10, side = LEFT)
                #     LBBList.append(labelInList)
                #     c+=1
                #     if c == 4:
                #         c=0
                #         r+=1


                # else:
                #     showerror("Ошибка","Неизвестный тип файла.")
                # r = 1
                # c = 0
            MainWin.text.configure(state="disabled")
            MainWin.LB_startText.config(text = f"Файлы в папке {dirName}")


        else:
            while(dirName == ""):
                showerror("Ошибка","Выберите папку с файлами.")
                dirName = filedialog.askdirectory()
                MainWin.FilesView(dirName)

    FilesView(dirName)


    #BT_viewReceived.bind("<ButtonRelease>", onClickViewReceived)
    BT_choose.bind("<ButtonRelease>", onClickChoose)
    BT_openDir.bind("<ButtonRelease>", onCLickOpenDir)

MainWin = MainWin()

class LogPassWin(Tk):
    def __init__(self):
        super().__init__()

        def AcceptLogPass(event):
            query = 'SELECT * FROM logPass WHERE login = ? AND password = ?'
            LogPassBool = False
            if self.cursorLogPass.execute(query, (self.EntryLog.get(), self.EntryPass.get())).fetchone() != None:
                MainUser = self.cursorLogPass.fetchone()[0][1]
                LogPassBool = True
            self.connectLogPass.commit()

            if LogPassBool:
                print("nice")

                self.destroy()
            else:
                print("not nice")
                showwarning(title="Неверный логин или пароль", message="Неверный логин или пароль, попробуйте снова")

        self.title("UsTan")
        self.geometry("400x300")
        self.EntryLog = ttk.Entry(self, width=15, font=("Arial", 20))
        self.EntryLog.insert(0, "Login")
        self.EntryLog.pack(anchor=CENTER, pady=20)

        self.EntryPass = ttk.Entry(self, width=15, font=("Arial", 20))
        self.EntryPass.config(show="*")
        self.EntryPass.insert(0, "Password")
        self.EntryPass.pack(anchor=CENTER)

        self.BTLogPassAccept = ttk.Button(self, text="Log in", width=20)
        self.BTLogPassAccept.bind("<ButtonRelease>", AcceptLogPass)
        self.BTLogPassAccept.pack(anchor=CENTER)

        self.connectLogPass = sqlite3.connect(sqlPath, timeout=5.0, detect_types=0,
                                              isolation_level='DEFERRED', check_same_thread=True, factory=sqlite3.Connection,
                                              cached_statements=128, uri=False)
        self.cursorLogPass = self.connectLogPass.cursor()
        self.cursorLogPass.execute("CREATE TABLE IF NOT EXISTS logPass (id INTEGER UNIQUE,login TEXT NOT NULL,password TEXT NOT NULL,PRIMARY KEY(id AUTOINCREMENT));")
        self.connectLogPass.commit()
        self.cursorLogPass.execute("INSERT OR REPLACE INTO logPass VALUES(1, \"asd\",\"asd\")")         #zxc
        self.connectLogPass.commit()



class SendWin(Tk):
    def __init__(self):
        super().__init__()

        self.title("UsTan")
        self.geometry("550x400")

        self.UsersList = list()
        self.FilesList = MainWin.FilesList
        self.CheckingsDict = {}
        self.SelectedUsersList = list()
        self.SelectedFilePathsList = list()
        for x in self.FilesList:
            self.SelectedFilePathsList.append(MainWin.FilesDict[x])

        def onClickCheck(event):
            self.tempLabel = event.widget
            if self.tempLabel["text"] == "Отправить":
                self.tempLabel["text"] = "Не отправлять"
                self.SelectedUsersList.append(self.CheckingsDict[self.tempLabel])
            else:
                self.tempLabel["text"] = "Отправить"
                self.SelectedUsersList.remove(self.CheckingsDict[self.tempLabel])

        def onClickSend(event):
            self.connect = sqlite3.connect(sqlPath, timeout=5.0, detect_types=0,
                                           isolation_level='DEFERRED', check_same_thread=True,
                                           factory=sqlite3.Connection,
                                           cached_statements=128, uri=False)
            self.cursor = self.connect.cursor()
            for x in self.SelectedUsersList:
                self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {x["text"]} (id INTEGER NOT NULL, fileName TEXT, fromWho TEXT, PRIMARY KEY (id AUTOINCREMENT))")
                self.connect.commit()
                for y in self.FilesList:
                    self.cursor.execute(f"INSERT INTO {x["text"]} (fileName, fromWho) VALUES (\"{y["text"]}\", \"{MainWin.MainUser}\")")
                    self.connect.commit()
                    for z in self.SelectedFilePathsList:
                        if not os.path.exists(MainWin.mainDir+f"{x["text"]}"):
                            os.makedirs(MainWin.mainDir+f"{x["text"]}")
                            shutil.copy(z, MainWin.mainDir+f"{x["text"]}")
                        else:
                            shutil.copy(z, MainWin.mainDir + f"{x["text"]}")
            self.SuccessWin = SuccessWin()
            self.destroy()




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
        self.BT_send = tk.Button(self, text="Продолжить")
        self.BT_send.bind("<ButtonRelease>", onClickSend)
        self.BT_send.pack(anchor=SE)
        self.LB_startText = Label(self,text="Кому переслать файл/файлы?", font=20)
        self.LB_startText.pack(anchor=NW)
        self.FrameUsers = ttk.Frame(self, borderwidth=1, relief=SOLID)
        for x in range(len(self.UsersList)):
            # self.BT_star = tk.Button(self.FrameUsers,text="star")
            # self.BT_star.grid(column=0, row=x)
            self.LB_userName = Label(self.FrameUsers, text=self.UsersList[x], font=20)
            self.LB_userName.grid(column=1, row=x)
            self.BT_check = tk.Button(self.FrameUsers, text="Отправить")
            self.BT_check.grid(column=2, row=x)
            self.BT_check.bind("<ButtonRelease>", onClickCheck)
            self.CheckingsDict[self.BT_check] = self.LB_userName
        self.FrameUsers.place(anchor=NW, x=10, y=100, width= 200, height=250)
        self.FrameFiles = ttk.Frame(self, borderwidth=1, relief=SOLID)
        for x in range(len(self.FilesList)):
            self.LB_fileName = Label(self.FrameFiles, text=self.FilesList[x]["text"], font=20)
            self.LB_fileName.grid(column=0, row=x)
        self.FrameFiles.place(anchor=N, x=350, y=100, width=200, height=250)

class SuccessWin(Tk):
    def __init__(self):
        super().__init__()

        def onClickClose(event):
            self.destroy()

        self.title("UsTan")
        self.geometry("300x100")
        self.LB_MainText = Label(self,text="Успешно отправлено")
        self.LB_MainText.pack(anchor=CENTER)
        self.BT_Close = ttk.Button(self, text="Выбрать новые файлы для отправки(назад)")
        self.BT_Close.pack(anchor=S)
        self.BT_Close.bind("<ButtonRelease>", onClickClose)