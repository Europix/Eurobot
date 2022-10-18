from collections import defaultdict
import json
from PIL import Image
from nonebot import on_command, on_message, on_notice, on_regex, get_driver
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from nonebot.adapters.cqhttp import Message
from aiocqhttp import MessageSegment
import aiohttp, os
from src.libraries.tool import hash
from src.libraries.maimaidx_music import *
from src.libraries.image import *
from src.libraries.maimai_best_40 import generate
from src.zyj import *
import re
import time, datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests, json, time, math


def full(mode, bpitem, ID, module):
    global creator
    page = math.ceil(bpitem / 100)
    item = bpitem - (page - 1) * 100 - 1
    sect = time.time()
    if mode == 'Relax':
        var = 1
    else:
        var = 0

    url = 'http://akatsuki.pw/api/v1/users/scores/' + module + '?mode=0&p=' + str(page) + '&l=100&rx=1&id=' + str(ID)
    url2 = 'https://akatsuki.pw/api/v1/users/full?id=' + str(ID)
    try:
        r = requests.get(url ,timeout = 50)
        r2 = requests.get(url2 , timeout = 50)
    except Exception as e:
        print(e)
        return ("获取api超时，这破网站看脸，要么再来一次？")
    result = json.loads(r.text)
    result2 = json.loads(r2.text)
    scores = result['scores']
    name = result2['username']
    width = 900
    height = 300
    image = Image.new('RGB', (width, height), (255, 255, 255))
    image2 = Image.new('RGB', (900, 250), (0, 0, 0))
    font1 = ImageFont.truetype('akat/arial.ttf', 36)
    font11 = ImageFont.truetype('akat/arial.ttf', 24)
    font12 = ImageFont.truetype('akat/arial.ttf', 12)
    font2 = ImageFont.truetype(r'C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\ARLRDBD.ttf', 150)
    font21 = ImageFont.truetype(r'C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\ARLRDBD.ttf', 36)
    font22 = ImageFont.truetype(r'C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\ARLRDBD.ttf', 24)
    font3 = ImageFont.truetype(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\digifaw.ttf", 32)
    # font4=ImageFont.truetype('GOTHIC.ttf',65)
    font41 = ImageFont.truetype(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\Torus SemiBold.otf", 50)
    url11 = 'https://assets.ppy.sh/beatmaps/'
    setid = str(scores[item]['beatmap']['beatmapset_id'])
    url12 = '/covers/cover.jpg'
    fullurl = url11 + setid + url12
    try:
        url3 = 'https://old.ppy.sh/api/get_beatmaps?k=41a40b9c34b5f28e51c588aa9cba1ea335f6cb24&b=' + str(
            scores[item]['beatmap']['beatmap_id'])
        r3 = requests.get(url3)
        result3 = json.loads(r3.text)
        songname = result3[0]['artist'] + ' - ' + result3[0]['title'] + ' [' + result3[0]['version'] + ']'
        maxcombomap = str(result3[0]['max_combo'])
    except IndexError:
        songname = scores[item]['beatmap']['song_name']
        maxcombomap = str(scores[item]['beatmap']['max_combo'])
    else:
        creator = ' (Beatmap by ' + result3[0]['creator'] + ')'

    try:
        response = requests.get(fullurl)
        response = response.content
        BytesIOOBj = BytesIO()
        BytesIOOBj.write(response)
        img = Image.open(BytesIOOBj)
    except OSError:
        image.paste(image2, (0, 50))
        draw = ImageDraw.Draw(image)
    else:
        img = Image.blend(img, image2, 0.7)
        image.paste(img, (0, 50))
        draw = ImageDraw.Draw(image)

    itemdes = ''
    if module == 'best':
        itemdes = 'Your BP' + str(bpitem) + ' is:'
    elif module == 'recent':
        itemdes = 'Your recent performance (' + str((page - 1) * 100 + item + 1) + ') is:'

    draw.text((10, 8), itemdes, font=font1, fill=(0, 0, 0))
    try:
        draw.text((815 - 9 * len(creator), 9), creator, font=font11, fill=(0, 0, 0))
    except NameError:
        pass
    else:
        pass

    maxcombo = str(scores[item]['max_combo']) + '/'
    count300 = 'x' + str(scores[item]['count_300'])
    count100 = 'x' + str(scores[item]['count_100'])
    count50 = 'x' + str(scores[item]['count_50'])
    countgeki = 'x' + str(scores[item]['count_geki'])
    countkatu = 'x' + str(scores[item]['count_katu'])
    countmiss = 'x' + str(scores[item]['count_miss'])
    playtime = 'Playtime: ' + scores[item]['time']
    acc = str(scores[item]['accuracy']) + '%'
    pp = str(round(scores[item]['pp'], 2)) + 'pp'
    rank = scores[item]['rank']
    beatmapid = 'Beatmap ID: ' + str(scores[item]['beatmap']['beatmap_id'])
    player = 'Player: ' + name
    mods = scores[item]['mods']
    sect2 = time.time() - sect
    
    if rank == 'A':
        draw.text((10, 100), rank, font=font2, fill=(0, 255, 0))
    elif rank == 'B':
        draw.text((10, 100), rank, font=font2, fill=(0, 0, 255))
    elif rank == 'C':
        draw.text((10, 100), rank, font=font2, fill=(199, 21, 133))
    elif rank == 'SS':
        draw.text((5, 100), 'S', font=font2, fill=(255, 255, 0))
        draw.text((20, 100), 'S', font=font2, fill=(255, 255, 0))
    elif rank == 'SSH':
        draw.text((5, 100), 'S', font=font2, fill=(245, 245, 220))
        draw.text((20, 100), 'S', font=font2, fill=(245, 245, 220))
    elif rank == 'S':
        draw.text((10, 100), 'S', font=font2, fill=(255, 255, 0))
    elif rank == 'SH':
        draw.text((10, 100), 'S', font=font2, fill=(245, 245, 220))
    elif rank == 'D':
        draw.text((10, 100), 'D', font=font2, fill=(255, 0, 0))

    draw.text((120, 55), songname, font=font11, fill=(255, 255, 255))
    draw.text((120, 90), '300', font=font3, fill=(0, 245, 255))
    draw.text((200, 100), count300, font=font11, fill=(255, 255, 255))
    draw.text((350, 90), 'geki', font=font3, fill=(0, 245, 255))
    draw.text((440, 100), countgeki, font=font11, fill=(255, 255, 255))
    draw.text((120, 120), '100', font=font3, fill=(0, 238, 0))
    draw.text((200, 130), count100, font=font11, fill=(255, 255, 255))
    draw.text((350, 120), 'katu', font=font3, fill=(0, 238, 0))
    draw.text((450, 130), countkatu, font=font11, fill=(255, 255, 255))
    draw.text((120, 150), '50', font=font3, fill=(255, 215, 0))
    draw.text((180, 160), count50, font=font11, fill=(255, 255, 255))
    draw.text((350, 150), 'X', font=font21, fill=(255, 0, 0))
    draw.text((380, 160), countmiss, font=font11, fill=(255, 255, 255))

    draw.text((120, 200), beatmapid, font=font11, fill=(255, 255, 255))
    draw.text((120, 230), player, font=font11, fill=(255, 255, 255))
    draw.text((120, 260), playtime, font=font22, fill=(255, 255, 255))

    draw.text((510, 100), acc, font=font41, fill=(255, 255, 255))
    draw.text((510, 200), pp, font=font41, fill=(255, 255, 255))
    draw.text((510, 150), maxcombo + maxcombomap, font=font41, fill=(255, 255, 255))

    if mode == 'Relax':
        modsafter = mods - 128
    else:
        modsafter = mods

    comb = [1, 2, 4, 8, 16, 32, 64, 256, 576, 1024, 4096, 16416]
    comc = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    imgdt = Image.open(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\DT.jpg")
    imgez = Image.open(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\EZ.jpg")
    imgfl = Image.open(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\FL.jpg")
    imghd = Image.open(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\HD.jpg")
    imghr = Image.open(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\HR.jpg")
    imght = Image.open(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\HT.jpg")
    imgnc = Image.open(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\NC.jpg")
    imgso = Image.open(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\SO.jpg")
    imgnf = Image.open(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\NF.png")
    imgtd = Image.open(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\TD.jpg")
    imgsd = Image.open(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\SD.png")
    imgpf = Image.open(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\PF.png")
    imgrx = Image.open(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\RX.png")
    term = 11
    while modsafter > 0:
        if modsafter < comb[term]:
            term -= 1
        else:
            modsafter -= comb[term]
            comc[term] += 1
            term -= 1

    n = 1
    if len(songname) >= 58:
        ycoor = 90
    else:
        ycoor = 50

    if comc[0] == 1:
        image.paste(imgnf, (810, ycoor))
        n += 1
    else:
        pass

    if comc[1] == 1:
        image.paste(imgez, (810 + (n - 1) % 2 * 45, ycoor + (n - 1) // 2 * 45))
        n += 1
    else:
        pass

    if comc[2] == 1:
        image.paste(imgtd, (810 + (n - 1) % 2 * 45, ycoor + (n - 1) // 2 * 45))
        n += 1
    else:
        pass

    if comc[3] == 1:
        image.paste(imghd, (810 + (n - 1) % 2 * 45, ycoor + (n - 1) // 2 * 45))
        n += 1
    else:
        pass

    if comc[4] == 1:
        image.paste(imghr, (810 + (n - 1) % 2 * 45, ycoor + (n - 1) // 2 * 45))
        n += 1
    else:
        pass

    if comc[5] == 1:
        image.paste(imgsd, (810 + (n - 1) % 2 * 45, ycoor + (n - 1) // 2 * 45))
        n += 1
    else:
        pass

    if comc[6] == 1:
        image.paste(imgdt, (810 + (n - 1) % 2 * 45, ycoor + (n - 1) // 2 * 45))
        n += 1
    else:
        pass

    if comc[7] == 1:
        image.paste(imght, (810 + (n - 1) % 2 * 45, ycoor + (n - 1) // 2 * 45))
        n += 1
    else:
        pass

    if comc[8] == 1:
        image.paste(imgnc, (810 + (n - 1) % 2 * 45, ycoor + (n - 1) // 2 * 45))
        n += 1
    else:
        pass

    if comc[9] == 1:
        image.paste(imgfl, (810 + (n - 1) % 2 * 45, ycoor + (n - 1) // 2 * 45))
        n += 1
    else:
        pass

    if comc[10] == 1:
        image.paste(imgso, (810 + (n - 1) % 2 * 45, ycoor + (n - 1) // 2 * 45))
        n += 1
    else:
        pass

    if comc[11] == 1:
        image.paste(imgpf, (810 + (n - 1) % 2 * 45, ycoor + (n - 1) // 2 * 45))
        n += 1
    else:
        pass

    if mode == 'Relax':
        image.paste(imgrx, (810 + (n - 1) % 2 * 45, ycoor + (n - 1) // 2 * 45))
    else:
        pass

    localtime = time.asctime(time.localtime(time.time()))
    stime = "ProcTime:" + str(int(sect2*1000)) + 'ms'
    draw.text((740, 280), localtime, font=font12, fill=(255, 255, 255))
    draw.text((740, 267), stime, font=font12, fill=(255, 255, 255))
    x = int(time.time())
    #image.save(f'{x}.png')
    image.save('result.png')
    return x


# 输出某玩家的bp xx #
def rbp(bpitem, ID):
    y = full('Relax', bpitem, ID, 'best')
    return y

# 输出某玩家的最近 xx 个成绩 #
def rrc(bpitem, ID):
    y = full('Relax', bpitem, ID, 'recent')
    return y



command_rrc = on_command("!rrc")


@command_rrc.handle()
async def _(bot: Bot, event: Event, state: T_State):
    argv = str(event.get_message()).strip().split(" ")
    if len(argv) != 1:
        await command_rrc.finish("指令有误，只能传一个参数 userid 哦！\n 例如 !rrc 4396")
    y = full('Relax', 1, argv[0], 'recent')
    img = Image.open("result.png").convert('RGBA')
    await command_rrc.finish([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(img), encoding='utf-8')}"
            }
        }])

command_rbp = on_command("!rbp")


@command_rbp.handle()
async def _(bot: Bot, event: Event, state: T_State):
    argv = str(event.get_message()).strip().split(" ")
    if len(argv) != 2:
        await command_rbp.finish("指令有误，需要2个参数 <bp*> <userid> 哦！\n 例如 !rbp 1000 4396")
    y = full('Relax', int(argv[0]), int(argv[1]), 'best')
    try:
        img = Image.open("result.png").convert('RGBA')
    except Exception:
        await command_rbp.finish("看起来像是获取失败了哦")
    await command_rbp.finish([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(img), encoding='utf-8')}"
            }
        }])


command_todaybp = on_command("!todaybp")

@command_todaybp.handle()
async def _(bot: Bot, event: Event, state: T_State):
    argv = str(event.get_message()).strip().split(" ")
    if len(argv) != 1:
        await command_rbp.finish("指令有误，需要1个参数 <userid> 哦！\n 例如 !todaybp 4396")
    url0 = 'http://akatsuki.pw/api/v1/users/scores/best?mode=0&p='
    page = 1
    pagestr = str(page)
    url1 = '&l=100&rx=1&id='
    url2 = argv[0]
    url = url0 + pagestr + url1 + url2
    r = requests.get(url)
    result = json.loads(r.text)
    scores = result['scores']
    ticks = int(time.time())
    item = 0
    information = ''
    acc = 0
    pp = 0
    max_combomap = 0
    max_comboyou = 0
    time_span = 86400*2
    f = ''
    f = f + f"在过去的 48h 内，你留了在BP { 100 * (page - 1) + 1} ~ { 100 * page} 之内的以下成绩：\n"
    while item < 100:
        timeset = scores[item]['time']
        timeArray = time.strptime(timeset, "%Y-%m-%dT%H:%M:%SZ")
        timeStamp = int(time.mktime(timeArray))
        if ticks - timeStamp <= time_span + 28800:
            information = scores[item]['beatmap']['song_name']
            acc = scores[item]['accuracy']
            pp = scores[item]['pp']
            max_combomap = scores[item]['beatmap']['max_combo']
            max_comboyou = scores[item]['max_combo']
            miss = scores[item]["count_miss"]
            f = f + f"#{item + 1 + 100 * (page - 1)} : {information} \n [ {acc} % / {max_comboyou}x / {miss} miss / {pp}pp ]\n"
            item += 1
        else:
            item += 1
    f = f + f"Generated By Eurobot & Murmurtwins @{datetime.datetime.now()}"
    await command_todaybp.finish(Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(text_to_image(f)), encoding='utf-8')}"
                }
        }]))

def firstcount(ID):
	url = 'https://akatsuki.pw/api/v1/users/scores/first?mode=0&p=1&l=100&rx=1&id=' + str(ID)
	url2 = 'https://akatsuki.pw/api/v1/users/full?id=' + str(ID)
	r = requests.get(url)
	r2 = requests.get(url2)
	result = json.loads(r.text)
	result2 = json.loads(r2.text)
	totalcount = result['total']
	name = result2['username']
	if totalcount > 0:
		msg = '玩家 ' + name + ' 在 Akatsuki 服 RX 模式下目前有 ' + str(totalcount) + ' 个 #1'
	else:
		msg = '玩家 ' + name + ' 在 Akatsuki 服 RX 模式下目前没有 #1，继续努力吧少年'
	return msg

command_first = on_command("!first")

@command_first.handle()
async def _(bot: Bot, event: Event, state: T_State):
    argv = str(event.get_message()).strip().split(" ")
    if len(argv) != 1:
        await command_rbp.finish("指令有误，需要1个参数 <userid> 哦！\n 例如 !first 4396")
    f = firstcount(argv[0])
    await command_first.finish(f)
    
def search_user(username):
	url = 'https://akatsuki.pw/api/v1/users/whatid?name=' + str(username)
	r = requests.get(url)
	result = json.loads(r.text)
	code_num = result['code']
	if code_num == 404:
		msg = '没有符合查找条件的用户！'
		return msg
	elif code_num == 200:
		id = result['id']
		msg = '用户 ' + str(username) + ' 的 ID 为 ' + str(id)
		return msg
        
command_name = on_command("!name")

@command_name.handle()
async def _(bot: Bot, event: Event, state: T_State):
    argv = str(event.get_message()).strip().split(" ", 0)
    print(argv)
    id = search_user(argv[0])
    await command_name.finish(id)