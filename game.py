#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from constraint import *
from unit import GameUnitStruct,UnitStruct
from equip import EquipStruct

unitList=[]
unitRevDict={}
equipList=[]
equipRevDict={}

class BattleField:
    units = []
    unitCnt = [0, 0]
    frontUnit = [[-1, -1, -1] for i in range(2)]
    actQueue = [-1, -1]
    actFinished = [False, False]
    deathStack = [] #[i, side, n]

    def __init__(self):
        self.refresh()

    def refresh(self):
        self.units=[[[] for i in range(9)] for i in range(2)]
        self.unitCnt = [0, 0]
        self.frontUnit = [[-1, -1, -1] for i in range(2)]

    def unitExist(self, i, side):
        return len(self.units[side][i])>0 and (self.units[side][i][0]).isAlive()

    def frontFresh(self):
        for side in range(2):
            for column in range(3):
                self.frontUnit[side][column] = -1
                for i in range(column,9,3):
                    if self.unitExist(i,side):
                        self.frontUnit[side][column] = i
                        break

    def frontUpdate(self, i, side, oper):
        column=i%3
        if oper=='add':
            if self.frontUnit[side][column]==-1 or self.frontUnit[side][column]>i:
                self.frontUnit[side][column]=i
        elif oper=='del':
            if self.frontUnit[side][column] == i:
                self.frontUnit[side][column]=-1
                for j in range(i+1,9,3):
                    if self.unitExist(i,side):
                        self.frontUnit[side][column]=j
                        break

    def getFront(self, column, side):
        return self.frontUnit[side][column]

    def isFront(self, i, side):
        return self.getFront(i%3, side)==i

    def getUnitN(self, i, side):
        return len(self.units[side][i])-1

    def getUnit(self, i, side, n=-1):
        if not self.unitExist(i, side):
            print('Unit[%d,%d] not exist.'%(i, side))
            return
        if n==-1 or n>=len(self.units[side][i]):
            n= self.getUnitN(i, side)
        return self.units[side][i][n]

    # @intro append()
    # @param
    # @return None
    def addUnit(self, unit, i, side, n=1):
        if type(unit)==UnitStruct:
            unit=GameUnitStruct(unit)
        print('%s加入战场.i=%d,side=%d.' %(unit.getName(), i, side))
        if n>=len(self.units[side][i]):
            self.units[side][i].append(copy.deepcopy(unit))
        else:
            self.units[side][i][n] = copy.deepcopy(unit)
        if len(self.units[side][i])==1:
            self.unitCnt[side] += 1
            if i>self.actQueue[side]:
                self.frontUpdate(i, side, 'add')

    # @intro Pop the last unit
    # @param
    # @return None
    def delUnit(self, i, side, n=-1):
        self.units[side][i].pop(n)
        if not self.unitExist(i,side):
            self.unitCnt[side] -= 1
            self.frontUpdate(i, side, 'del')

    def getRowNearList(self, side, tar):
        rowList = []
        row=tar-tar%3
        for i in range(row,row+3):
            if (i in (tar-1,tar+1)) and self.unitExist(i, side):
                rowList.append(i)
        if len(rowList) == 0:
            rowList.append(-1)
        return rowList

    def getColumnForwardList(self, side, tar):
        columnList = []
        for i in range(tar+3,9,3):
            if self.unitExist(i, side):
                columnList.append(i)
        if len(columnList) == 0:
            columnList.append(-1)
        return columnList

    def getFrontList(self, side):
        frontList = []
        for i in self.frontUnit[side]:
            if i >= 0:
                frontList.append(i)
        if len(frontList) == 0:
            frontList.append(-1)
        return frontList

    def getUnitList(self, side, reverse=False):
        unitList = []
        for i in range(9):
            if self.unitExist(i,side) ^ reverse:
                unitList.append(i)
        if len(unitList) == 0:
            unitList.append(-1)
        return unitList

    # return int
    def pickRandomBlank(self, side):
        pickList = self.getUnitList(side, reverse=True)
        if len(pickList)==0:
            # watch out for -1
            pick=-1
        else:
            pick = random.choice(pickList)
        return pick

    # return int list
    def pickUnit(self, side, pickType, tar=-1):
        pickList = [-1] # watch out for -1
        if pickType in [RangeDict['近战'], RangeDict['金色羽毛']]:
            pickList=self.getFrontList(side)
        elif pickType==RangeDict['远程']:
            pickList = self.getUnitList(side)
        elif pickType==RangeDict['友军']:
            pickList = self.getUnitList(side).remove(tar)
            if type(pickList)!=list:
                return [-1]
            return pickList
        elif pickType==RangeDict['全体']:
            pickList = self.getUnitList(side)
            return pickList
        elif pickType==RangeDict['列']:
            pickList = self.getColumnForwardList(side, tar)
            return pickList
        elif pickType==RangeDict['巨刃剑']:
            pickList = self.getRowNearList(side, tar)
            return pickList
        # random pick
        return [random.choice(pickList)]

    def nextActUnit(self, side, actQueue):
        nxt=-1
        for i in range(actQueue+1,9):
            if self.unitExist(i,side):
                nxt=i
                break
        return nxt

    def unitEnum(self, func):
        self.actQueue = [-1, -1]
        self.actFinished = [False, False]
        for i in range(9):
            for side in range(2):
                if not self.actFinished[side]:
                    self.actQueue[side] = self.nextActUnit(side,self.actQueue[side])
                    if self.actQueue[side]==-1:
                        self.actFinished[side]=True
                    else:
                        for n in range(len(self.units[side][self.actQueue[side]])):
                            if self.units[side][self.actQueue[side]][n].isAlive():
                                func(self.units[side][self.actQueue[side]][n], self.actQueue[side], side, n)

    def isOver(self):
        if(self.unitCnt[0]==0 and self.unitCnt[1]==0):
            return 2
        elif self.unitCnt[0] == 0:
            return 0
        elif self.unitCnt[1] == 0:
            return 1
        else:
            return -1

    # @param all str list
    # trigger = ['远程'/'近战', '队友'/'敌人', '神圣'/'愤怒'/'海洋'/'太阳'/'雷电'/'蛇蝎',
    #           '建筑'/'魔神'/'人类'/'兽人'/'亡灵'/'野兽'/'植物']
    def getEquipActTrigger(self, range=[], side=[], dmgType=[], race=[]):
        return range+side+dmgType+race

    def equipAct(self, equip, unit, i, side, n, iTarget, sideTarget, nTarget, trigger=[], valueMul=1):
        #====================================== trigger test (or) =====================================
        if type(equip.trig)==list and not (True in [x in trigger for x in equip.trig]):
            return []
        if equip.cnt > 0:
            equip.cnt-=1
        if equip.cnt == 0:
            equip.cnt = equip.reg
        else:
            return []
        #====================================== possiblity test =======================================
        if equip.possiblity>0 and equip.possiblity<=random.randint(0,100):
            return []
        #======================================= method pre ============================================
        value = copy.deepcopy(equip.operValue)
        if equip.operValueAdd==DmgTypeDict['伤害']:
            pass
        elif equip.operValueAdd>0:
            value = [x + unit.getPower()[equip.operValueAdd] for x in value]
        value = [x*valueMul for x in value]
        target = []
        # [side, i, (n)] list
        # watch out for invalid target
        if equip.operMethod == OperMethodDict['横劈']:
            target = [[sideTarget, i] for i in self.pickUnit(sideTarget, RangeDict['巨刃剑'], iTarget)]
        elif equip.operTarget == OperTargetDict['BOSS']:
            target = [[side, 5]]
        elif equip.operTarget == OperTargetDict['敌人']:
            target = [[1-side, i] for i in self.pickUnit(1-side, RangeDict['远程'])]
        elif equip.operTarget == OperTargetDict['敌人全体']:
            target = [[1-side, i] for i in self.pickUnit(1-side, RangeDict['全体'])]
        elif equip.operTarget == OperTargetDict['队友']:
            target = [[side, i] for i in self.pickUnit(side, RangeDict['友军'], i)]
        elif equip.operTarget == OperTargetDict['对方']:
            target = [[sideTarget, iTarget, nTarget]]
        elif equip.operTarget == OperTargetDict['己方全体']:
            target = [[side, i] for i in self.pickUnit(side, RangeDict['全体'])]
        elif equip.operTarget == OperTargetDict['自己']:
            target = [[side, i, n]]
        elif equip.operTarget == OperTargetDict['烈焰神剑']:
            target = [[sideTarget, i] for i in self.pickUnit(sideTarget, RangeDict['列'], iTarget)]
        tUnit = []
        for tar in target:
            if len(tar) == 3:
                if self.unitExist(tar[1], tar[0]):
                    tUnit.append(self.getUnit(tar[1], tar[0], tar[2]))
            elif len(tar) == 2:
                for u in self.units[tar[0]][tar[1]]:
                    tUnit.append(u)
        #========================================== method =============================================
        if equip.operMethod == OperMethodDict['BUFF']:
            for i in range(len(value),len(equip.operAttr)):
                value.append(value[0])
            for u in tUnit:
                for i in range(len(equip.operAttr)):
                    if equip.operAttr[i]=='生命':
                        self.unitSetHealth(value[i], '+', u, i, side, n)
                    elif equip.operAttr[i]=='生命上限':
                        u.setHealthLimit(value[i], '+')
                    elif equip.operAttr[i] == '攻击':
                        u.setDmg(value[i], '+')
                    elif equip.operAttr[i] in PowerDict:
                        print(equip.operAttr[i])
                        u.setPower(value[i], '+', PowerDict[equip.operAttr[i]])
                    elif equip.operAttr[i] == '中毒':
                        u.setPoison(value[i], '+')
        elif equip.operMethod == OperMethodDict['反伤加成']:
            # return list
            return value
        elif equip.operMethod == OperMethodDict['防御']:
            #if equip.operAttr[0]==DmgTypeDict['伤害']:
                # return list
                return value
        elif equip.operMethod == OperMethodDict['复活']:
            # unitList depend on serial order
            unit.addUnit(unitList[random.choice(equip.operValue)])
        elif equip.operMethod == OperMethodDict['横劈']:
            [dmg, dmgType]=unit.getAtkMsg()
            for tar in target:
                if tar[1]>=0:
                    self.unitAtk(dmg, dmgType, iTarget=tar[1], sideTarget=tar[0])
        elif equip.operMethod == OperMethodDict['解毒']:
            #注意时机
            unit.setPoison(0)
        elif equip.operMethod == OperMethodDict['连锁闪电']:
            # atkx3-6
            if self.unitCnt[sideTarget]<=1:
                return []
            atkNum=random.randint(3,7)
            for j in range(atkNum):
                iUnit = self.pickUnit(sideTarget, RangeDict['远程'])[0]
                if iUnit>=0:
                    self.unitAtk(value[0], DmgTypeDict['愤怒'], iTarget=iUnit, sideTarget=sideTarget)
        elif equip.operMethod == OperMethodDict['伤害']:
            for tar in target:
                if tar[1]>=0:
                    nUnit = -1
                    if len(tar) == 3:
                        nUnit = tar[2]
                    for num in range(len(equip.operAttr)):
                        self.unitAtk(value[num], DmgTypeDict[equip.operAttr[num]],
                                     iTarget=tar[1], sideTarget=tar[0], nTarget=nUnit)
        elif equip.operMethod == OperMethodDict['死神BUFF']:
            self.unitSetHealth(10, '+', unit, i, side, n)
            unit.setPower([0, 0, 3, 3, 3, 3], '+')
        elif equip.operMethod == OperMethodDict['仙人掌攻击']:
            dmg=0
            for iUnit in self.pickUnit(side, RangeDict['友军'], i):
                if iUnit>=0:
                    u = self.getUnit(iUnit, side)
                    if '仙人掌' in u.getName():
                        dmg+=u.getDmg()
            self.unitAtk(dmg, DmgTypeDict['愤怒'], iTarget=iTarget, sideTarget=sideTarget, nTarget=nTarget)
        elif equip.operMethod == OperMethodDict['召唤']:
            #
            self.addUnit(unitList[random.choice(equip.operValue)], self.pickRandomBlank(side), side)
        elif equip.operMethod == OperMethodDict['叠加召唤']:
            randomBlank=self.pickRandomBlank(side)
            for u in equip.operValue:
                self.addUnit(unitList[u], randomBlank, side)
        elif equip.operMethod == OperMethodDict['指令']:
            # return list
            return equip.operAttr
        return []

    # @intro trigger Phase '减少生命'
    # @param dmg: invalid if dmg<=0
    # @return real dmg, invalid=-1, otherwise>=1
    def unitAtk(self, dmg, dmgType, iTarget, sideTarget, nTarget=-1):
        r=-1
        if dmg>0 and self.unitExist(iTarget, sideTarget):
            unitTarget = self.getUnit(iTarget, sideTarget, nTarget)
            if unitTarget.isAlive():
                r = self.unitTakeDmg(dmg, dmgType, unitTarget, iTarget, sideTarget, nTarget)
        return r

    def unitDeath(self, unit, i, side, n):
        print('%s[%d,%d] 阵亡.'%(unit.getName(), i, side))
        self.unitEquipTrigger(OppotunityDict['死亡后'], unit, i, side, n, i, side, n)
        if not unit.isAlive():
            self.deathStack.append([i, side, n,
                                    self.getEquipActTrigger(race=[RaceRevDict[unit.getRace()]])])
            self.delUnit(i, side, n)

    def unitTakeDmg(self, dmg, dmgType, unit, i, side, n):
        t = unit.takeDmg(dmg, dmgType)
        print('%d伤害.' % t)
        if not unit.isAlive():
            self.unitDeath(unit, i, side, n)
        elif t>0:
            # notice equip phase here
            self.unitEquipTrigger(OppotunityDict['减少生命'], unit, i, side, n, -1, -1, -1)
        return t

    def unitSetHealth(self, value, mod, unit, i, side, n):
        hpBefore=unit.getHealth()
        hpCur = unit.setHealth(value, mod)
        if unit.isAlive():
            if hpCur<hpBefore:
                self.unitEquipTrigger(OppotunityDict['减少生命'], unit, i, side, n, -1, -1, -1)
            elif hpCur>hpBefore:
                self.unitEquipTrigger(OppotunityDict['恢复生命'], unit, i, side, n, -1, -1, -1)
        else:
            self.unitDeath(unit, i, side, n)
        return hpCur

    # @intro trigger Phase '休息'
    # @param
    # @return curhp
    def unitRelax(self, unit, i, side, n):
        r = -1
        self.unitSetHealth(5, '+', unit, i, side, n)
        # notice equip phase here
        self.unitEquipTrigger(OppotunityDict['休息'], unit, i, side, n, i, 1-side, n)
        if unit.isAlive():
            r=unit.getHealth()
        return r

    def unitEquipTrigger(self, phase, unit, i, side, n, iTarget, sideTarget, nTarget, trigger=[],
                         prePhase=-1, prePhaseTrig=-1):
        r=[]
        for equip in unit.Equip[phase]:
            command=[]
            if prePhase>=0 and prePhaseTrig==equip.operMethod:
                for preEquip in unit.Equip[prePhase]:
                    command.extend(self.equipAct(preEquip, unit, i, side, n, iTarget, sideTarget, nTarget, trigger))
            valueMul=1
            for n in command:
                valueMul*=n/100
            r.extend(self.equipAct(equip, unit, i, side, n, iTarget, sideTarget, nTarget, trigger, valueMul))
        return r

    def deathPhase(self):
        while len(self.deathStack)>0:
            [iTarget, sideTarget, nTarget, trigger]=self.deathStack.pop()
            actQueue = [-1, -1]
            actFinished = [False, False]
            for i in range(9):
                for side in range(2):
                    if side==sideTarget:
                        triggerSide = ['队友']
                    else:
                        triggerSide = ['敌人']
                    if not actFinished[side]:
                        actQueue[side] = self.nextActUnit(side, actQueue[side])
                        if actQueue[side] == -1:
                            actFinished[side] = True
                        else:
                            for n in range(len(self.units[side][i])):
                                if self.units[side][i][n].isAlive():
                                    self.unitEquipTrigger(OppotunityDict['产生阵亡'], self.units[side][i][n],
                                                          i, side, n, iTarget, sideTarget, nTarget,
                                                          trigger=self.getEquipActTrigger(side=triggerSide,
                                                                                          race=trigger))

    def unitPreCheck(self, unit, i, side, n):
        if unit.getDmgType()==DmgTypeDict['随机']:
            unit.setDmgType(DmgTypeDict[random.choice(['海洋', '太阳', '雷电', '蛇蝎'])])
            print('%s[%d,%d]的伤害类型成为%s.' % (unit.getName(), i, side, DmgTypeRevDict[unit.getDmgType()]))

    def unitPrePhase(self, unit, i, side, n):
        print('%s[%d,%d]的起始回合.' % (unit.getName(), i, side))
        self.unitEquipTrigger(OppotunityDict['回合开始'], unit, i, side, n, -1, 1-side, -1)

    def unitAtkPhase(self, unit, i, side, n):
        print('%s[%d,%d]的攻击回合.'%(unit.getName(), i, side))
        print(self.getFrontList(1-side))
        if unit.getAtkRange() == RangeDict['远程']:
            triggerRange = '远程'
        else:
            triggerRange = '近战'
        commend = self.unitEquipTrigger(OppotunityDict['行动前'], unit, i, side, n, i, side, n,
                                        trigger=self.getEquipActTrigger(range=[triggerRange], side=['队友'],
                                                                        race=[RaceRevDict[unit.getRace()]]))
        # death detect
        if not unit.isAlive():
            return
        # atk or relax
        if unit.getAtkRange()==RangeDict['近战'] and (not self.isFront(i, side)):
            self.unitRelax(unit, i, side, n)
        else:
            sideTarget = 1 - side
            iTarget=(self.pickUnit(sideTarget, unit.getAtkRange()))[0]
            if iTarget>=0:
                nTarget=self.getUnitN(iTarget, sideTarget)
                UnitTarget=self.getUnit(iTarget, sideTarget, nTarget)
                # phases:'攻击前','被攻击前','攻击后','被攻击后','死亡后'
                for k in range(unit.getAtkNum()):
                    # death detect
                    if not UnitTarget.isAlive():
                        break
                    [dmg, dmgType]=unit.getAtkMsg()
                    commend+= self.unitEquipTrigger(OppotunityDict['攻击前'], unit, i, side, n, iTarget, sideTarget, nTarget,
                                                    trigger=self.getEquipActTrigger(range=[triggerRange], side=['敌人'],
                                                                                    dmgType=[dmgType],
                                                                                    race=[RaceRevDict[UnitTarget.getRace()]]))
                    commendTar = self.unitEquipTrigger(OppotunityDict['被攻击前'], UnitTarget, iTarget, sideTarget, nTarget, i, side, n,
                                                    trigger=self.getEquipActTrigger(range=[triggerRange], side=['敌人'],
                                                                                    dmgType=[dmgType],
                                                                                    race=[RaceRevDict[unit.getRace()]]))
                    # death detect
                    if not (UnitTarget.isAlive() and unit.isAlive()):
                        break
                    #dodge judge
                    if UnitTarget.dodge():
                        print('%s 闪避!!!' % UnitTarget.getName())
                        continue
                    if '转毒' in commend:
                        UnitTarget.setPoison(unit.getDmg(), '+')
                    else:
                        defence=0
                        for n in commendTar:
                            if type(n)==int:
                                defence+=n
                        print('%s[%d,%d] 攻击 %s[%d,%d], 造成' % (
                            unit.getName(), i, side, UnitTarget.getName(), iTarget, sideTarget), end='')
                        self.unitAtk(dmg-defence, dmgType, iTarget, sideTarget, nTarget)
                    if unit.isAlive() and not UnitTarget.isAlive():
                        self.unitEquipTrigger(OppotunityDict['致死后'], unit, i, side, n, iTarget, sideTarget, nTarget,
                                              trigger=self.getEquipActTrigger(range=[triggerRange], side=['敌人'],
                                                                              dmgType=[dmgType],
                                                                              race=[RaceRevDict[UnitTarget.getRace()]]))
                    if unit.isAlive():
                        self.unitEquipTrigger(OppotunityDict['攻击后'], unit, i, side, n, iTarget, sideTarget, nTarget,
                                              trigger=self.getEquipActTrigger(range=[triggerRange], side=['敌人'],
                                                                              dmgType=[dmgType],
                                                                              race=[RaceRevDict[UnitTarget.getRace()]]))
                    if UnitTarget.isAlive():
                        self.unitEquipTrigger(OppotunityDict['被攻击后'], UnitTarget, iTarget, sideTarget, nTarget, i, side, n,
                                              trigger=self.getEquipActTrigger(range=[triggerRange], side=['敌人'],
                                                                              dmgType=[dmgType],
                                                                              race=[RaceRevDict[unit.getRace()]]),
                                              prePhase=OppotunityDict['反伤'], prePhaseTrig=OperMethodDict['伤害'])

    def unitPoisonDmg(self, unit, i, side, n):
        print('%s[%d,%d]的结束回合.' % (unit.getName(), i, side))
        self.unitEquipTrigger(OppotunityDict['毒结算'], unit, i, side, n, -1, -1, -1)
        dmg=unit.takePoisonDmg()
        if dmg>0:
            print('%s[%d,%d]受到%d点毒伤.' % (unit.getName(), i, side, dmg))
        if unit.isAlive():
            if dmg>0:
                self.unitEquipTrigger(OppotunityDict['减少生命'], unit, i, side, n, -1, -1, -1)
        else:
            self.unitDeath(unit, i, side, n)

    # return winner,-1=draw
    def play(self):
        self.unitEnum(self.unitPreCheck)
        for rangeNum in range(RangeNum):
            print('Round %d'%rangeNum)
            # preAct
            self.unitEnum(self.unitPrePhase)
            self.deathPhase()
            self.frontFresh()
            # actPhase
            self.unitEnum(self.unitAtkPhase)
            self.deathPhase()
            self.frontFresh()
            # endPhase
            self.unitEnum(self.unitPoisonDmg)
            self.deathPhase()
            self.frontFresh()
            # isOver
            isOver = self.isOver()
            if isOver == -1:
                continue
            elif isOver == 0 or isOver == 1:
                return 1-isOver
            else:
                return -1
        return -1

class Game:
    battleField = BattleField()
    runNum=200

    # shld run after loadEquipList()
    def loadUnitList(self):
        unitData = pandas.read_excel(UnitFileName).fillna(0)
        unitData.sort_values('序号', ascending=True)
        for i in range(0,len(unitData)):
            data=unitData.iloc[i]
            powerList=[data['护甲'],data['愤怒'],data['海洋'],data['太阳'],data['雷电'],data['蛇蝎']]
            unit=UnitStruct(data['名称'],data['强度'],data['伤害类型'],data['攻击范围'],
                            data['种族'],data['血量'],data['攻击'],powerList,data['闪避'])
            if (data['装备编号'] != 0):
                eList=re.split(',', str(data['装备编号']))
                for equipId in eList:
                    if int(equipId)>0:
                        unit.Equip.append(equipList[int(equipId)])
            unitList.append(unit)
        for i in range(0, len(unitList)):
            unitRevDict[unitList[i].name] = i

    def loadEquipList(self):
        equipData = pandas.read_excel(EquipFileName).fillna(0)
        equipData.sort_values('序号', ascending=True)
        equipList.append(EquipStruct())
        for i in range(0,len(equipData)):
            data=equipData.iloc[i]
            if(type(data['序号'])!=str and data['序号']<0.5):
                continue
            powerList = [data['护甲'], data['愤怒'], data['海洋'], data['太阳'], data['雷电'], data['蛇蝎']]
            equip=EquipStruct(data['序号'],data['名称'],data['介绍'],data['伤害类型'],data['攻击次数'],data['攻击范围'],
                              data['种族'],data['生命'],data['攻击'],powerList,data['闪避'],data['触发时机'],
                              data['触发限定'],data['触发计数'],data['初始计数'],data['概率'],data['操作名称'],
                              data['操作属性'],data['操作对象'],data['操作限定'],data['基础数值'],data['属性加成'])
            equipList.append(equip)
        for i in range(0, len(equipList)):
            equipRevDict[equipList[i].name] = i

    def __init__(self):
        self.loadEquipList()
        self.loadUnitList()
        self.battleField.refresh()

    def readStr(self, strIn):
        strTeam=re.split('-', strIn)
        for side in range(2):
            strUnits=re.split(';', strTeam[side])
            for strUnit in strUnits:
                if strUnit=="":
                    continue
                attrs = re.split(',', strUnit)
                i = (int(attrs[2])-3)*3+int(attrs[1])
                self.battleField.addUnit(unitList[unitRevDict[attrs[0]]], i, side)
                if len(attrs) < 4 or attrs[3]=="":
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
                    for ii in range(equipN):
                        self.battleField.getUnit(i, side).addEquip(equipList[equipRevDict[equipStr]])

    def setRunNum(self, runNum):
        self.runNum = runNum

    def refresh(self):
        self.battleField.refresh()

    # return team winrate
    def run(self):
        winCnt=[0,0,0] # 0队,1队,总
        for i in range(self.runNum):
            tbattleField = copy.deepcopy(self.battleField)
            winNum=tbattleField.play()
            if winNum>=0:
                winCnt[winNum] += 1
            winCnt[2] += 1
        return [winCnt[0]/winCnt[2], winCnt[1]/winCnt[2]]

    def test(self):
        self.battleField.refresh()
        self.battleField.addUnit(GameUnitStruct(unitList[64]), 4, 0)
        self.battleField.addUnit(GameUnitStruct(unitList[69]), 4, 1)
        self.setRunNum(200)
        winRate=self.run()
        print('1队:%.2f%%' % (winRate[0] * 100))
        print('2队:%.2f%%' % (winRate[1] * 100))

