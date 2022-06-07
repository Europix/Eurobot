from nonebot import on_command, on_message, on_notice, on_regex, get_driver
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from nonebot.adapters.cqhttp import Message
from aiocqhttp import MessageSegment
import aiohttp, os, random, requests
import json, re
from src.libraries.image import *
from apex_legends import ApexLegends



apex_map = on_command("!map",aliases = {"地图轮换"})

@apex_map.handle()
async def _(bot: Bot, event: Event, state: T_State):
    URL = f"https://api.mozambiquehe.re/maprotation?auth=979d0a73104cc447ebf3cd264030a319"
    try:
        res = requests.get(URL, timeout = 50)
    except Exception as e:
        await apex_map.finish("获取api超时，这破网站看脸，要么再来一次？")
    jsonobj = json.loads(res.text)
    print(jsonobj)
    pname = jsonobj['current']['map'] 
    plevel = jsonobj['current']['readableDate_end'] 
    prankscore = jsonobj['next']['map'] 
    prankname = jsonobj['next']['readableDate_end']
    timeleft = jsonobj['current']['remainingTimer']
    name = "当前地图：" + pname
    level = "结束于：" + plevel + "( UTC+0 )"
    time = "剩余时间：" + timeleft
    rankscore = "下一个地图：" + prankscore
    rankname = "结束于：" + prankname + "( UTC+0 )"

    info=(name,level,time,rankscore,rankname)

    await apex_map.finish(Message([
        {
            "type": "text",
                "data": {
                    "text": '\n'.join(info)
                }
        },
        {
            "type": "image",
            "data": {
                "file": jsonobj['current']['asset']
            }
        }
        ]))
        

apex_player = on_command("!player",aliases = {"!apex查分"})

@apex_player.handle()
async def _(bot: Bot, event: Event, state: T_State):                
    apex = ApexLegends("f4cba3f7-84c5-4ad2-81f9-84fb55d0706d")
    headers = { 'TRN-Api-Key':'Eurobot'}
    URL = "https://apex.tracker.gg/api"
    res = requests.get(URL, headers, timeout = 30)
    player = apex.player('NRG_dizzy')

    print(player)

    for legend in player.legends:
        print(legend.legend_name)
        print(legend.icon)
        print(legend.damage)
        
        
        
        