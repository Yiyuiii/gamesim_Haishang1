#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

from game import *
from tkinter import *
from tkinter.simpledialog import askinteger
import os

txtFileName = 'webpage\\jjc.txt'
labelText = "%s\n装备1：%s\n装备2：%s\n装备3：%s"

class windowUnit(Label):
    unit=-1
    equip=[]
    equipNum = []
    equipP=0

    def __init__(self, root):
        super(windowUnit, self).__init__(root)
        self.refresh()

    def refresh(self):
        self.unit = -1
        self.equipP = 0
        self.equip = [0 for i in range(3)]
        self.equipNum = [1 for i in range(3)]

    def appendEquip(self, index, num):
        self.equip[self.equipP] = index
        self.equipNum[self.equipP] = num
        self.equipP=(self.equipP+1)%3

class GameWindow:
    game = None             # Game()
    root = None             # Tk()
    unitListBox = None      # Listbox(root, selectmode)
    equipListBox = None     # Listbox(root, selectmode)
    btnPlay = None
    btnLoad = None
    btnRe = None
    labelWin1 = None
    labelWin2 = None
    labelList = []          # [[windowUnit() for i in range(9)] for i in range(2)]
    labelSelect = None      # Label()

    def __init__(self):
        self.game = Game()
        self.windowInit()
        self.boardInit()
        self.UnitListBoxInit()
        self.EquipListBoxInit()
        self.ButtonInit()

    def windowInit(self):
        self.root = Tk()
        self.root.title("冒险吧!探险家 竞技场模拟器")
        self.root.resizable(0, 0)
        #self.root.geometry("%dx%d" % (550, 600))

    def boardInit(self):
        boardFrame = Frame(self.root)
        self.labelList = [[0 for i in range(9)] for i in range(2)]
        #label
        for side in range(2):
            for i in range(9):
                self.labelList[side][i] = windowUnit(boardFrame)
                self.labelList[side][i].config(text=labelText % ('无', '无', '无', '无'))
                self.labelList[side][i].bind('<Button-1>', self.Onclick_label)
                if side == 0:
                    self.labelList[side][i].grid(row=int(i / 3) + 5, column=i % 3, padx=7, pady=7)
                else:
                    self.labelList[side][i].grid(row=2 - int(i / 3), column=i % 3, padx=7, pady=7)
        #
        self.labelSelect=self.labelList[0][0]
        boardFrame.grid(row=0, column=0)

    def UnitListBoxInit(self):
        self.unitListBox = Listbox(self.root, selectmode=BROWSE)
        for unit in unitList:  # 第一个小部件插入数据
            self.unitListBox.insert(END, unit.name)
        #滚动条
        scrl = Scrollbar(self.root)
        scrl.grid(row=0, column=2, sticky=E + N + S)
        self.unitListBox.configure(yscrollcommand=scrl.set)
        scrl.configure(command=self.unitListBox.yview)
        #按键
        self.unitListBox.bind('<Double-Button-1>', self.Onclick_unitListBox)
        self.unitListBox.curIndex = None
        #将小部件放置到主窗口中
        self.unitListBox.grid(row=0, column=1, sticky=N + S)

    def EquipListBoxInit(self):
        self.equipListBox = Listbox(self.root, selectmode=BROWSE)
        for equip in equipList:  # 第一个小部件插入数据
            self.equipListBox.insert(END, equip.name)
        #滚动条
        scrl = Scrollbar(self.root)
        scrl.grid(row=0, column=4, sticky=E + N + S)
        self.equipListBox.configure(yscrollcommand=scrl.set)
        scrl.configure(command=self.equipListBox.yview)
        #按键
        self.equipListBox.bind('<Double-Button-1>', self.Onclick_equipListBox)
        self.equipListBox.curIndex = None
        #将小部件放置到主窗口中
        self.equipListBox.grid(row=0, column=3, sticky=N + S)

    def ButtonInit(self):
        buttonFrame = Frame(self.root)
        self.btnPlay = Button(buttonFrame, text='运行', width=10, command=self.Onclick_btnPlay)
        self.btnRe = Button(buttonFrame, text='重置', width=10, command=self.Onclick_btnRe)
        self.btnLoad = Button(buttonFrame, text='载入', width=10, command=self.Onclick_btnLoad)
        self.labelWin1 = Label(buttonFrame, width=10)
        self.labelWin2 = Label(buttonFrame, width=10)
        self.labelWin1.grid(row=0, column=0, padx=15)
        self.btnPlay.grid(row=0, column=1, padx=15)
        self.labelWin2.grid(row=0, column=2, padx=15)
        self.btnRe.grid(row=0, column=3, padx=15)
        self.btnLoad.grid(row=0, column=4, padx=15)
        buttonFrame.grid(row=1, column=0, columnspan=3, sticky=E + W + N + S)

    def Onclick_btnPlay(self):
        self.game.refresh()
        for side in range(2):
            for i in range(9):
                if self.labelList[side][i].unit>=0:
                    self.game.battleField.addUnit(unitList[self.labelList[side][i].unit], i, side, 0)
                    for p in range(3):
                        if self.labelList[side][i].equip[p] > 0:
                            for t in range(self.labelList[side][i].equipNum[p]):
                                self.game.battleField.getUnit(i, side).addEquip(equipList[self.labelList[side][i].equip[p]])
        self.game.setRunNum(200)
        winRate = self.game.run()
        self.labelWin1.config(text='1队:%.2f%%' % (winRate[0] * 100))
        self.labelWin2.config(text='2队:%.2f%%' % (winRate[1] * 100))

    def Onclick_btnLoad(self):
        if not os.path.exists(txtFileName):
            print("%s file not exists." % txtFileName)
            return
        for side in range(2):
            for i in range(9):
                self.labelList[side][i].refresh()
        with open(txtFileName, encoding='UTF-8') as file_object:
            content = file_object.read()
            if len(content)>0:
                self.readStr(content)
        for side in range(2):
            for i in range(9):
                self.labelRefresh(self.labelList[side][i])


    def Onclick_btnRe(self):
        self.game.refresh()
        for side in range(2):
            for i in range(9):
                self.labelList[side][i].refresh()
                self.labelRefresh(self.labelList[side][i])

    def Onclick_label(self, event):
        w = event.widget
        self.labelSelect=w

    def Onclick_unitListBox(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        self.labelSelect.unit=index
        self.labelRefresh(self.labelSelect)

    def Onclick_equipListBox(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        num = 1
        if index in range(1, 10):
            num = askinteger("输入框", "数量:")
            if type(num)!=int or num<1:
                return
        self.labelSelect.appendEquip(index, num)
        self.labelRefresh(self.labelSelect)

    def readStr(self, strIn):
        strTeam=re.split('-', strIn)
        for side in range(2):
            strUnits=re.split(';', strTeam[side])
            for strUnit in strUnits:
                if strUnit=="":
                    continue
                attrs = re.split(',', strUnit)
                i = (int(attrs[2])-3)*3+int(attrs[1])
                self.labelList[side][i].unit = unitRevDict[attrs[0]]
                if len(attrs)<4 or attrs[3]=="":
                    continue
                equips = re.split('\|', attrs[3])
                for e in equips:
                    if e == "":
                        continue
                    equipS=re.split(':', e)
                    if equipS[0]=='宝物':
                        equipStr=equipS[1]
                        equipN=1
                    else:
                        equipN=int(equipS[1])
                        equipStr=equipS[0][0:2]
                    self.labelList[side][i].appendEquip(equipRevDict[equipStr], equipN)

    def labelRefresh(self, label):
        if label.unit>=0:
            strUnit=unitList[label.unit].name
        else:
            strUnit='无'
        strEquip=['无' for i in range(3)]
        for i in range(min(3, len(label.equip))):
            if label.equip[i]>0:
                strEquip[i]=equipList[label.equip[i]].name
                if label.equipNum[i]>1:
                    strEquip[i] += 'x' + str(label.equipNum[i])
        label.config(text=labelText % (strUnit, strEquip[0], strEquip[1], strEquip[2]))

    def run(self):
        # 进入消息循环
        self.root.mainloop()
