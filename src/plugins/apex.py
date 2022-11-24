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
     # 唉 这api真的烂透了 三四次成功一次 这key还是偷的别人的 像弱智 能用用用不了拉倒
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
    file = jsonobj['current']['asset']
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
                "file": file
            }
        }
        ]))
        

apex_player = on_command("!player",aliases = {"!apex查分"})

@apex_player.handle()
async def _(bot: Bot, event: Event, state: T_State):
    auth = '979d0a73104cc447ebf3cd264030a319'
    req = str(event.get_message()).strip().split(" ")
    player = str(req[0])
    platform = 'PC'
    try:
        solve = (requests.get(f"https://api.mozambiquehe.re/bridge?auth={auth}&player={player}&platform={platform}")).json()
        #r = requests.get(f"https://api.mozambiquehe.re/maprotation?auth=a51818179a68b3c2f14e989fffe9c4ec")
        #jsonobj = json.loads(r.text)
        
        if "Error" not in solve.keys():
                # 几组玩家参数
                player_name = f'玩家：{solve["global"]["name"]}'
                player_level = f'等级：{solve["global"]["level"]}'
                player_rank = f'段位：{solve["global"]["rank"]["rankName"]}{solve["global"]["rank"]["rankDiv"]} ('\
                              f'{solve["global"]["rank"]["rankScore"]}) '
                player_rank_icon = f'{solve["global"]["rank"]["rankImg"]}'
                player_player = f'{solve["legends"]["selected"]["LegendName"]}'
                player_player_icon = f'{solve["legends"]["selected"]["ImgAssets"]["icon"]}'
                #print(player_name,player_player,player_rank)

        info = (player_name, player_level, player_rank)
    except Exception:
        await apex_player.finish("获取数据失败！请检查一下id的输入：\n1.目前只支持Origin的ID，请勿用SteamID\n2.目前只支持PC端，其他平台暂时懒得做\n3.api可能获取失败，如果输入没有问题重试一下？")
    print('\n'.join(info))
    await apex_player.finish(Message([
        {
            "type": "text",
                "data": {
                    "text": '\n'.join(info)
                }
        },
        {
            "type": "image",
            "data": {
                "file": player_rank_icon
            }
        }
        ]))    
        
        