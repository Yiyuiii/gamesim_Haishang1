#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from constraint import *

class UnitStruct:
    name = ''       # str
    strength = 0    # 强度
    dmgType = 0     # 伤害类型 int
    atkNum = 1      # 攻击次数 int
    atkRange = 0    # 攻击距离 int
    race = 0        # 种族 int
    health = 0      # 生命 int
    dmg = 0         # 攻击力 int
    power = [] # 护甲 愤怒 海洋 太阳 雷电 蛇蝎
    dodge = 0       # 闪避 int
    Equip = []      # 装备

    #Fit excel
    def __init__(self, name='', strength=0, dmgType=0, atkRange=0, race=0, health=0, dmg=0,
                 power=[0 for i in range(PowerNum)], dodge=0):
        self.name = str(name)
        self.strength = int(strength)
        if (type(dmgType) == str):
            self.dmgType = DmgTypeDict[dmgType]
        if (type(atkRange) == str):
            self.atkRange = RangeDict[atkRange]
        if (type(race) == str):
            self.race = RaceDict[race]
        self.health = int(health)
        self.dmg = int(dmg)
        if self.dmg<=0:
            self.atkNum = 0
        self.power = power
        self.dodge = int(dodge)
        self.Equip = []

class GameUnitStruct:
    Unit = UnitStruct()
    alive = False
    curHp = 0
    poison = 0
    Equip = [] #[[] for i in range(EquipOppotunityNum)]

    def __init__(self, unit):
        self.addUnit(unit)

    def refresh(self):
        self.Unit = UnitStruct()
        self.alive = False
        self.curHp = 0
        self.poison = 0
        self.Equip = [[] for i in range(EquipOppotunityNum)]

    #This drops any equip added before
    def addUnit(self, unit):
        self.refresh()
        self.Unit = copy.deepcopy(unit)
        for equip in unit.Equip:
            self.addEquip(equip)
        self.alive = True
        self.curHp = self.getHealthLimit()

    def addEquip(self, equip):
        if (equip.dmgType>0):
            self.Unit.dmgType = equip.dmgType
        self.setAtkNum(self.Unit.atkNum * equip.atkNum)
        if (equip.atkRange > self.Unit.atkRange):
            self.Unit.atkRange = equip.atkRange
        if (equip.race > 0):
            self.Unit.race = equip.race
        self.Unit.health += equip.health
        self.Unit.dmg += equip.dmg
        for i in range(PowerNum):
            self.Unit.power[i] += equip.power[i]
        self.Unit.dodge += equip.dodge
        if (equip.opportunity >= 0):
            index=-1
            for i in range(len(self.Equip[equip.opportunity])):
                if self.Equip[equip.opportunity][i].serial==equip.serial:
                    index=i
                    break
            if index>=0:
                preEquip=self.Equip[equip.opportunity][index]
                preEquip.operValue+=equip.operValue
            else:
                self.Equip[equip.opportunity].append(copy.deepcopy(equip))

    def isAlive(self):
        return self.alive

    #==================================== sets and gets ==================================
    #mod:'=','+'

    #This may affect 'alive' mark
    def setHealth(self, health, mod='='):
        health=round(health)
        if mod=='=':
            self.curHp = health
        elif mod=='+':
            self.curHp += health
        if self.curHp<=0:
            self.alive=False
        elif self.curHp > self.getHealthLimit():
            self.curHp = self.getHealthLimit()
        return self.getHealth()

    def getHealth(self):
        return self.curHp

    def setPoison(self, poison, mod='='):
        if self.getRace()==RaceDict['建筑']:
            return 0
        if mod=='=':
            self.poison = poison
        elif mod=='+':
            self.poison += poison
        if self.poison<1:
            self.poison=0
        return self.getPoison()

    def getPoison(self):
        return self.poison

    def setName(self, name):
        self.Unit.name=name
        return self.getName()

    def getName(self):
        return self.Unit.name

    def setDmgType(self, dmgType):
        self.Unit.dmgType=dmgType
        return self.getDmgType()

    def getDmgType(self):
        return self.Unit.dmgType

    def setAtkNum(self, atkNum):
        self.Unit.atkNum=atkNum
        if self.Unit.atkNum>2:
            self.Unit.atkNum=2
        return self.getAtkNum()

    def getAtkNum(self):
        return self.Unit.atkNum

    def setAtkRange(self, atkRange):
        self.Unit.atkRange=atkRange
        return self.getAtkRange()

    def getAtkRange(self):
        return self.Unit.atkRange

    def setRace(self, race):
        self.Unit.race=race
        return self.getRace()

    def getRace(self):
        return self.Unit.race

    # This may affect current health
    def setHealthLimit(self, health, mod='='):
        diff=0
        if mod=='=':
            diff=health-self.getHealthLimit()
            self.Unit.health = health
        elif mod=='+':
            diff=health
            self.Unit.health += health
        if diff>0:
            self.setHealth(diff,'+')
        elif self.getHealth() > self.Unit.health:
            self.setHealth(self.Unit.health)
        return self.getHealthLimit()

    def getHealthLimit(self):
        return self.Unit.health

    def setDmg(self, dmg, mod='='):
        if mod=='=':
            self.Unit.dmg = dmg
        elif mod=='+':
            self.Unit.dmg += dmg
        if self.Unit.dmg<0:
            self.Unit.dmg=0
        return self.getDmg()

    # div atkNum
    def getDmg(self):
        return self.Unit.dmg/self.Unit.atkNum

    def setPower(self, power, mod='=', i=-1):
        if i>=0:
            if mod == '=':
                self.Unit.power[i] = power
            elif mod == '+':
                self.Unit.power[i] += power
        else:
            for i in range(PowerNum):
                self.setPower(power[i], mod, i)
        return self.getPower()

    def getPower(self, i=-1):
        if i >= 0:
            return self.Unit.power[i]
        else:
            return self.Unit.power

    def setDodge(self, dodge, mod='='):
        if mod=='=':
            self.Unit.dodge = dodge
        elif mod=='+':
            self.Unit.dodge += dodge
        if self.Unit.dodge<0:
            self.Unit.dodge=0
        return self.getDodge()

    def getDodge(self):
        return self.Unit.dodge
    # ==================================== sets and gets end ==================================
    # @intro
    # @param
    # @return [dmg, dmgType]
    def dodge(self):
        return random.randint(0, 100)<self.getDodge()

    def getAtkMsg(self):
        return [self.getDmg() + self.getPower()[self.getDmgType()], self.getDmgType()]

    def takePoisonDmg(self):
        poisonDmg=self.getPoison()-self.getPower()[DmgTypeDict['蛇蝎']]
        if poisonDmg<=0:
            poisonDmg=0
        self.setHealth(-poisonDmg,'+')
        self.setPoison(poisonDmg/2)
        return poisonDmg

    def takeDmg(self, dmg, dmgType):
        if (dmgType == DmgTypeDict['神圣']):
            pass
        elif dmgType==DmgTypeDict['愤怒']:
            dmg-=self.getPower()[0]
        else:
            dmg-=self.getPower()[dmgType]
        if(dmg<1):
            dmg=1
        self.setHealth(-dmg,'+')
        return dmg
