import csv
import pandas as pd

# f = open('tz.csv', 'w', encoding='utf-8')


from tinydb import TinyDB
from tinydb import where
from tinydb import Query
db = TinyDB('db.json')
a = Query()
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
#       新人  1级      一段  二段  三   四     五     六    七     八     九    十
num_dan = ['新人','1级','初段','二段','三段','四段','五段','六段','七段','八段','九段','十段']
dan_num = ['100','100','200','300','400','500','600','700','800','900','1000','1500']
ini = ['0','0','100','150','200','250','300','350','400','450','500','750']
def info(id):
    count = 1
    try:
        an = db.search(where('id') == id)[0]
    except Exception:
        return Message([
                {
                    "type": "text",
                    "data": {
                        "text": f"未找到玩家！"
                    }
                }
            ])
    dan = an['dan']
    prog = an['prog']
    for i in db.all():
        if i['dan'] > dan:
            count = count + 1
        if i['dan'] == dan and i['prog']> prog:
            count = count + 1
    return Message([
                {
                    "type": "text",
                    "data": {
                        "text": f"玩家 {an['id']} 数据:\n段位： {num_dan[an['dan']]} ({an['prog']}/{dan_num[an['dan']]})\n最近顺位：{an['sw']}\n交大内排名：{count}"
                    }
                }
            ])
def find_byid(id):
    an = db.search(where('id') == id)
    if an:
        return 1
    return -1

find_info = on_command("!吃鱼")
@find_info.handle()
async def _(bot: Bot, event: Event, state: T_State):
    argvs = str(event.get_message()).strip().split(" ")
    if find_byid(argvs[0]) == -1:
        await find_info.finish("未找到此玩家捏")
    else:
        await find_info.finish(info(argvs[0]))

initial = on_command("!交大公式战注册")
@initial.handle()
async def _(bot: Bot, event: Event, state: T_State):
    argvs = str(event.get_message()).strip().split(" ")
    if find_byid(argvs[0]) == 1:
        await initial.finish("已有重名玩家捏")
    db.insert({'id':argvs[0],'dan':0, 'prog':0, 'avg':0, 'cnt':0, 'sw': 0, 'qq': event.get_user_id()})
    await initial.finish("成功喵")
upload = on_command("!报分")
@upload.handle()
async def _(bot: Bot, event: Event, state: T_State):
    argvs = str(event.get_message()).strip().split(" ")
    scores = argvs[0].split(",")
    if len(scores)!= 4:
        await upload.finish("指令有误！请检查是不是输入了四个数据\n 样例：!报分 q1:50000,q2:25000,q3:15000,q4:10000")
    ans = ""
    # 1位 (+5)
    r1 = scores[0].split(":")
    ans = ans + f"一位：{r1[0]}, 点数：{ (int(r1[1]))/1000+5}\n"
    if  find_byid(r1[0]) == -1:
        await upload.finish("数据有误：一位id未注册")
    # 2 (-15)
    r2 = scores[1].split(":")
    ans = ans + f"二位：{r2[0]}, 点数：{ (int(r2[1]))/1000-15}\n"
    if  find_byid(r1[0]) == -1:
        await upload.finish("数据有误：二位id未注册")
    if int(r1[1])<int(r2[1]):
        await upload.finish("数据有误：一位分比二位低")
    # 3 (-35)
    r3 = scores[2].split(":")
    ans = ans + f"三位：{r3[0]}, 点数：{ (int(r3[1]))/1000-35}\n"
    if  find_byid(r3[0]) == -1:
        await upload.finish("数据有误：三位id未注册")
    if int(r2[1])<int(r3[1]):
        await upload.finish("数据有误：二位分比三位低")
    # 4 (-55)
    r4 = scores[3].split(":")
    ans = ans + f"慈善位：{r4[0]}, 点数：{ (int(r4[1]))/1000-55}\n"
    if  find_byid(r4[0]) == -1:
        await upload.finish("数据有误：四位id未注册")
    if int(r2[1])<int(r3[1]):
        await upload.finish("数据有误：三位分比四位低")
    if int(r2[1])+int(r3[1])+int(r1[1])+int(r4[1]) != 100000:
        await upload.finish("数据有误：总分不为100000")
    await upload.send(ans)
    upf = ""
    #一位存分
    an = db.search(where('id') == r1[0])[0]
    dan = an['dan']
    prog = an['prog']
    sw = an['sw']
    db.update({'sw': (sw*10+1)%10000000}, a.id == r1[0])
    #升段
    if  int(int(r1[1])/1000+5) +  int(prog) >=  int(dan_num[dan]):
        db.update({'dan': dan+1}, a.id == r1[0])
        db.update({'prog': ini[dan+1]}, a.id == r1[0])
        upf = upf + f"恭喜{r1[0]}升段！ ({num_dan[dan]} -> {num_dan[dan+1]})\n"
    else:
        db.update({'prog':  (int(prog) + int(r1[1])/1000+5)}, a.id == r1[0])
        upf = upf + f"{r1[0]} ({num_dan[dan]}): {prog}(+{ (int(r1[1]))/1000+5})/{dan_num[dan]}\n"
    #2位存分
    an = db.search(where('id') == r2[0])[0]
    dan = an['dan']
    prog = an['prog']
    sw = an['sw']
    db.update({'sw': (sw * 10 + 2) % 10000000}, a.id == r2[0])
    #升段
    if int(int(r2[1])/1000-15) + int(prog) >= int(dan_num[dan]):
        db.update({'dan': dan+1}, a.id == r2[0])
        db.update({'prog': ini[dan+1]}, a.id == r2[0])
        upf = upf + f"恭喜{r2[0]}升段！ ({num_dan[dan]} -> {num_dan[dan + 1]})\n"
    else:
        db.update({'prog': int(prog) + int(r2[1])/1000-15}, a.id == r2[0])
        upf = upf + f"{r2[0]} ({num_dan[dan]}): {prog}(+{int(r2[1])/1000-15})/{dan_num[dan]}\n"
#3位存分
    an = db.search(where('id') == r3[0])[0]
    dan = an['dan']
    prog = an['prog']
    sw = an['sw']
    db.update({'sw': (sw * 10 + 3) % 10000000}, a.id == r3[0])
    #升段
    if  int(int(r3[1])/1000-35) +  int(prog) >=  int(dan_num[dan]):
        db.update({'dan': dan+1}, a.id == r3[0])
        db.update({'prog': ini[dan+1]}, a.id == r3[0])
        upf = upf + f"恭喜{r3[0]}升段！ ({num_dan[dan]} -> {num_dan[dan + 1]})\n"
    #掉段 (新人 1级 初段不掉段—
    elif  int(int(r3[1]))/1000-35 + int(prog) < 0:
        if dan == 0 or dan == 1:
            upf = upf + f"{r3[0]}({num_dan[dan]}) 有三位保护机制，不掉分\n"
        if dan == 2:
            db.update({'prog': 0}, a.id == r3[0])
            upf = upf + f"{r3[0]}({num_dan[dan]}) 有段位保护机制，不掉段\n"
        if dan>2:
            db.update({'dan': dan - 1}, a.id == r3[0])
            db.update({'prog': ini[dan-1]}, a.id == r3[0])
            upf = upf + f"恭喜{r3[0]}掉段！ ({num_dan[dan]} -> {num_dan[dan -1]})\n"
    else:
        db.update({'prog':  (int(prog) + int(r3[1])/1000-35)}, a.id == r3[0])
        upf = upf + f"{r3[0]} ({num_dan[dan]}): {prog}({ (int(r3[1]))/1000-35})/{dan_num[dan]}\n"
# 四位存分
    an = db.search(where('id') == r4[0])[0]
    dan = an['dan']
    prog = an['prog']
    sw = an['sw']
    db.update({'sw': (sw * 10 + 4) % 10000000}, a.id == r4[0])
    #掉段 (新人 1级 初段不掉段—
    if  int(int(r4[1])/1000 - 55) +  int(prog) < 0:
        if dan>2:
            db.update({'dan': dan - 1}, a.id == r4[0])
            db.update({'prog': ini[dan-1]}, a.id == r4[0])
            upf = upf + f"恭喜{r4[0]}掉段！ ({num_dan[dan]} -> {num_dan[dan - 1]})\n"
        else:
            db.update({'prog': 0}, a.id == r4[0])
            upf = upf + f"{r4[0]}({num_dan[dan]}) 有段位保护机制，不掉段\n"
    #新人 1级 不掉分
    else:
        if dan == 0 or dan == 1:
            upf = upf + f"{r4[0]}({num_dan[dan]}) 有四位保护机制，不掉分\n"
            pass
        else:
            db.update({'prog':  int(prog) + int(int(r4[1])/1000-55)}, a.id == r4[0])
            upf = upf + f"{r4[0]} ({num_dan[dan]}): {prog}({ (int(r4[1])) / 1000 -55})/{dan_num[dan]}\n"
    await upload.finish(upf)
# self_info = on_command("查询战队点数")
