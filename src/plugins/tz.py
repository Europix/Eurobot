
import csv
import pandas as pd
#f = open('tz.csv', 'w', encoding='utf-8')

#csvw = csv.writer(f)
#csvw.writerow(["1","1204371319","0"])
#csvw.writerow(["2","759381653","0"])

data = pd.read_csv("src/static/tz.csv")
import numpy as np
# data = np.array(data)
# print(data)
from nonebot import on_command, on_message, on_notice, on_regex, get_driver
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from nonebot.adapters.cqhttp import Message
from aiocqhttp import MessageSegment
import aiohttp, os, random
import json, re
from src.libraries.image import *

def query_byqq(qq):
    points = 999999
    name = -1
    id = -1
    for i in range(len(data)):
        if str(data['qq'][i]) == qq:
            points = float(data['points'][i])
            name = data['name'][i]
            id = data['id'][i]
            return points,name,id
            
    return points,name,id
        
self_info = on_command("查询战队点数")
@self_info.handle()
async def _(bot: Bot, event: Event, state: T_State): 
    ur_qq = event.get_user_id()
    argvs = str(event.get_message()).strip().split(" ")
    if argvs[0]:
        ur_qq = argvs[0]
    f = ""
    points, name, id = query_byqq(ur_qq)
    if id == -1:
        await self_info.finish("用户不存在哦，请联系bot主人添加数据")
    else :
        f = f + f"{name} ({ur_qq})\nID: {id}\n积分: {points}"
    await self_info.finish(f)

edit = on_command("/edit")
@edit.handle()
async def _(bot: Bot, event: Event, state: T_State): 
    ur_qq = event.get_user_id()
    if ur_qq not in ['759381653','1204371319']:
        await edit.finish("?")
    #argvs = str(event.get_message()).strip().split(" ")
    
        