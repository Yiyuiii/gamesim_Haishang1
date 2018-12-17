#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import numpy as np
import random
import pandas
import copy
import re

#沉默权杖
def print(*args, **kwargs):
    pass

EquipOppotunityNum=15
PowerNum=6
RangeNum=25
EquipFileName = 'res\\宝物.xlsx'
UnitFileName = 'res\\怪物.xlsx'

PowerDict=  {'护甲':0, '随机':0, '愤怒':1, '海洋':2, '太阳':3, '雷电':4, '蛇蝎':5}
DmgTypeDict={'神圣':0, '愤怒':1, '海洋':2, '太阳':3, '雷电':4, '蛇蝎':5, '随机':6, '伤害':7}
RangeDict=  {'近战':0, '金色羽毛':1, '远程':2, '友军':3, '全体':4, '列':5, '巨刃剑':6}
RaceDict=   {'':0, '建筑':1, '魔神':2, '人类':3, '兽人':4, '亡灵':5, '野兽':6, '植物':7}
OppotunityDict={'':0, '回合开始':1, '行动前':2, '休息':3, '攻击前':4, '攻击后':5, '致死后':6,
                '被攻击前':7, '被攻击后':8, '死亡后':9, '产生阵亡':10, '恢复生命':11,
                '减少生命':12, '毒结算':13, '反伤':14}
OperMethodDict={'':0, 'BUFF':1, '反伤加成':2, '防御':3, '复活':4, '横劈':5, '解毒':6, '连锁闪电':7,
                ' ':8,'伤害':9, '死神BUFF':10, '仙人掌攻击':11, '召唤':12, '叠加召唤':13,
                '指令':14}
OperTargetDict={'BOSS':0, '敌人':1, '敌人全体':2, '队友':3, '对方':4, '己方全体':5, '自己':6,
                '烈焰神剑':7}

DmgTypeRevDict={0:'神圣', 1:'愤怒', 2:'海洋', 3:'太阳', 4:'雷电', 5:'蛇蝎', 6:'伤害'}
RaceRevDict=   {0:'', 1:'建筑', 2:'魔神', 3:'人类', 4:'兽人', 5:'亡灵', 6:'野兽', 7:'植物'}
# @intro append()
# @param
# @return None