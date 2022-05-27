from nonebot import on_command, on_message, on_notice, on_regex, get_driver
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from nonebot.adapters.cqhttp import Message
from aiocqhttp import MessageSegment
import aiohttp, os, random
import json, re
from src.libraries.image import *

card_dir = r"E:\card"
img_baseurl = f"https://ongeki-net.com/ongeki-mobile/img/music/"

osearch_music = on_regex(r"音击查歌.+")

@osearch_music.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "音击查歌(.+)"
    name = re.match(regex, str(event.get_message())).groups()[0].strip()
    print(name)
    with open(f'src/static/ongeki_music.json', 'r', encoding='utf-8') as ff:
        play_data = json.loads(ff.read())
    index = name
    s = ''
    count = 0
    
    #patt = re.compile(index)
    for music in play_data:
        if index.lower() in music['title'].lower():
            count = count + 1
            s = s + f"Name : {music['title']}\n"
            s = s + f'Character : {music["character"]}\n'
            lnt = music['lev_lnt'] + "(Lunatic)"
            if music['lev_lnt'] == '':
                lnt = '无Lunatic'
            s = s + f"Level : {music['lev_bas']}/{music['lev_adv']}/{music['lev_exc']}/{music['lev_mas']}/{lnt}\n"
            img_url = img_baseurl + music['image_url']
            if count >= 1:
                #s = s + "结果大于1条，只显示前1条"
                break
    if s == '':
        await osearch_music.finish("查询无结果;w;")
    else:
        await osearch_music.finish(Message([
        {
            "type": "text",
            "data": {
                "text": s
            }
        },
        {
            "type": "image",
            "data": {
                "file": img_url
            }
        }
    ]))

odraw = on_command("音击抽卡")

@odraw.handle()
async def _(bot: Bot, event: Event, state: T_State):
    randnum = random.randint(100001,101973)
    try:
        img = Image.open(f"{card_dir}/UI_Card_{randnum}.jpg").convert('RGBA')
    except Exception:
        img = Image.open(f"{card_dir}/UI_Card_{(randnum+1)%101974 + 100001}.jpg").convert('RGBA')
    file = f"base64://{str(image_to_base64(img), encoding='utf-8')}"
    await osearch_music.finish(Message([
        {
            "type": "image",
            "data": {
                "file": file
            }
        }
    ]))
    
orand = on_command("随个音击", aliases={"随首音击"})

@orand.handle()
async def _(bot: Bot, event: Event, state: T_State):
    with open(f'src/static/ongeki_music.json', 'r', encoding='utf-8') as ff:
        play_data = json.loads(ff.read())
    music = random.choice(play_data)
    s = ''
    s = s + f"Name : {music['title']}\n"
    s = s + f'Character : {music["character"]}\n'
    lnt = music['lev_lnt'] + "(Lunatic)"
    if music['lev_lnt'] == '':
        lnt = '无Lunatic'
    s = s + f"Level : {music['lev_bas']}/{music['lev_adv']}/{music['lev_exc']}/{music['lev_mas']}/{lnt}\n"
    img_url = img_baseurl + music['image_url']
    await osearch_music.finish(Message([
        {
            "type": "text",
            "data": {
                "text": s
            }
        },
        {
            "type": "image",
            "data": {
                "file": img_url
            }
        }
    ]))