#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from constraint import *

class EquipStruct:
    serial = 0      # 序号 int
    name = ''       # str
    intro = ''      # str
    # 属性叠加
    dmgType = -1    # 伤害类型 int
    atkNum = 1      # 攻击次数 int
    atkRange = 0    # 0-近战 1-金色羽毛 2-远程
    race = 0        # 种族 int
    health = 0      # 生命 int
    dmg = 0         # 攻击力 int
    power = [0 for i in range(PowerNum)]
    dodge = 0       # 闪避 int
    # 发动相关
    opportunity = 0  # 触发时机 int
    trig = 0    # 触发限定 list[str]
    possiblity = 0  # 概率 int
    operMethod = 0  # 操作名称 int
    operAttr = 0    # 操作属性 list[str]
    operTarget = 0  # 操作对象 int
    operTrig = 0    # 操作限定 list[str]
    operValue = 0   # 基础数值 list[int]
    operValueAdd=0  # 属性加成 int
    reg = 0         # 寄存器 int
    cnt = 0         # 计数

    def __init__(self):
        pass

    # Fit excel
    def __init__(self, serial=0, name='', intro='', dmgType=-1, atkNum=1, atkRange=0, race=0,
                 health=0, dmg=0, power=[0 for i in range(PowerNum)], dodge=0, opportunity=0,
                 trig=0, trigReg=0, trigCnt=0, possiblity=0, operMethod=0, operAttr=0,
                 operTarget=0, operTrig=0, operValue=0, operValueAdd=0):
        self.serial = int(serial)
        self.name = str(name)
        self.intro = str(intro)
        if (type(dmgType) == str):
            self.dmgType = DmgTypeDict[dmgType]
        self.atkNum = int(atkNum)
        if (type(atkRange) == str):
            self.atkRange = RangeDict[atkRange]
        if(type(race)==str):
            self.race = RaceDict[race]
        self.health = int(health)
        self.dmg = int(dmg)
        self.power = power
        self.dodge = int(dodge)
        self.opportunity = int(opportunity)
        if type(trig) == str:
            self.trig = re.split(',', trig)
        self.possiblity = possiblity
        if (type(operMethod) == str):
            self.operMethod = OperMethodDict[operMethod]
        if (type(operAttr) == str):
            self.operAttr = re.split(',', operAttr)
        if (type(operTarget) == str):
            self.operTarget = OperTargetDict[operTarget]
        if type(operTrig) == str:
            self.operTrig = re.split(',', operTrig)
        self.operValue = [int(x) for x in re.split(',', str(operValue))]
        if (type(operValueAdd) == str):
            self.operValueAdd = DmgTypeDict[operValueAdd]
        self.reg = int(trigReg)
        self.cnt = int(trigCnt)
