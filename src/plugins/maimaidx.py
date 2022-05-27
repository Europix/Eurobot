from collections import defaultdict
import json
from PIL import Image
from nonebot import on_command, on_message, on_notice, on_regex, get_driver
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from nonebot.adapters.cqhttp import Message
from aiocqhttp import MessageSegment
import aiohttp, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from src.libraries.tool import hash
from src.libraries.maimaidx_music import *
from src.libraries.image import *
from src.libraries.maimai_best_40 import generate
from src.zyj import *
import re
import time, datetime


def song_txt(music: Music):
    file = f"https://www.diving-fish.com/covers/{music.id}.jpg"
    if music.id == '456':
        img = Image.open(f"src/zyj/2.jpg").convert('RGBA')
        file = f"base64://{str(image_to_base64(img), encoding='utf-8')}"
    if music.id == '571':
        img = Image.open(f"src/zyj/4.jpg").convert('RGBA')
        file = f"base64://{str(image_to_base64(img), encoding='utf-8')}"
    if music.id == '772':
        img = Image.open(f"src/zyj/5.jpg").convert('RGBA')
        file = f"base64://{str(image_to_base64(img), encoding='utf-8')}"
    if music.id == '777':
        img = Image.open(f"src/zyj/7.jpg").convert('RGBA')
        file = f"base64://{str(image_to_base64(img), encoding='utf-8')}"
    if music.id == '301' or music.id == '10301':
        img = Image.open(f"src/zyj/6.jpg").convert('RGBA')
        file = f"base64://{str(image_to_base64(img), encoding='utf-8')}"
    if music.id == '799':
        img = Image.open(f"src/zyj/8.jpg").convert('RGBA')
        file = f"base64://{str(image_to_base64(img), encoding='utf-8')}"
    return Message([
        {
            "type": "text",
            "data": {
                "text": f"{music.id}. {music.title}\n"
            }
        },
        {
            "type": "image",
            "data": {
                "file": file
            }
        },
        {
            "type": "text",
            "data": {
                "text": f"\n{'/'.join(music.level)}"
            }
        }
    ])
def song_txt2(music:Music):
    return Message([
        {
            "type": "text",
            "data": {
                "text": f"{music.id}. {music.title}\n"
            }
        },
        {
            "type": "image",
            "data": {
                "file": f"https://www.diving-fish.com/covers/{music.id}.jpg"
            }
        }
    ])
    
music_aliases = defaultdict(list)
f = open('src/static/aliases.tsv', 'r', encoding='utf-8')
tmp = f.readlines()
f.close()
for t in tmp:
    arr = t.strip().split('\t')
    for i in range(len(arr)):
        if arr[i] != "":
            music_aliases[arr[i].lower()].append(arr[0])


inner_level = on_command('inner_level ', aliases={'!定数查歌 '})

def inner_level_q(ds1, ds2=None):
    result_set = []
    diff_label = ['Bas', 'Adv', 'Exp', 'Mst', 'ReM']
    if ds2 is not None:
        music_data = total_list.filter(ds=(ds1, ds2))
    else:
        music_data = total_list.filter(ds=ds1)
    for music in sorted(music_data, key = lambda i: int(i['id'])):
        for i in music.diff:
            result_set.append((music['id'], music['title'], music['ds'][i], diff_label[i], music['level'][i]))
    return result_set

roll = on_command('.roll') 

@roll.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await roll.finish("roll：" + str(int((random.random() * 100))))

tietie = on_command('Eurobot 贴贴')
white_list = ['3582509520','2567260001']
@tietie.handle()
async def _(bot: Bot, event: Event, state: T_State):
    get_qqs = event.get_user_id()
    if(get_qqs in [ '759381653','1156078034']):
        await tietie.finish("主人贴贴")
    elif get_qqs in white_list:
        await tietie.finish("贴贴qwq")
    await tietie.finish("爬远点")
    
    
wanan = on_command('Eurobot 晚安')
@wanan.handle()
async def _(bot: Bot, event: Event, state: T_State):
    get_qqs = event.get_user_id()
    if(get_qqs in ['759381653']):
        await wanan.finish("主人晚安(´-ω-`)")
    elif get_qqs in white_list:
        await wanan.finish("晚安qwq")
    await wanan.finish("爬远点")


doum = on_command('骂我', aliases={'草我'})
qvq = ['不忍心捏','笨比','让我主人骂','你骂我吧','傻瓜','？','你打maimai像滴蜡熊','抖M头子来了','baka','打死你','变态','你好像那个傻篮子','头套必须给你拽掉 必须打你脸','给你一拳']
@doum.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await doum.finish(random.choice(qvq))


@inner_level.handle()
async def _(bot: Bot, event: Event, state: T_State):
    argv = str(event.get_message()).strip().split(" ")
    if len(argv) > 2 or len(argv) == 0:
        await inner_level.finish("命令格式为\n定数查歌 <定数>\n定数查歌 <定数下限> <定数上限>")
        return
    if len(argv) == 1:
        result_set = inner_level_q(float(argv[0]))
    else:
        result_set = inner_level_q(float(argv[0]), float(argv[1]))
    if len(result_set) > 50:
        await inner_level.finish(f"结果过多（{len(result_set)} 条），请缩小搜索范围。")
        return
    s = ""
    for elem in result_set:
        s += f"{elem[0]}. {elem[1]} {elem[3]} {elem[4]}({elem[2]})\n"
    await inner_level.finish(s.strip())

yinjian = on_command("随个吉安娜推荐歌")
good_songs_id = ['31','207','237','157','212','220','260','101','30','244','106','134','138','236','315','137','117','557','11217','11178','766','242']
@yinjian.handle()
async def _(bot: Bot, event: Event, state: T_State):
    answ = random.choice(good_songs_id)
    musc = total_list.by_id(answ)
    musc_result = song_txt(musc)
    await yinjian.finish(musc_result)

yinjian2 = on_command("随个吉安娜不推荐歌")
bad_songs_id = ['114','11175','556','11143','11146','130','337','75','613','270','848','258','339','233']
@yinjian2.handle()
async def _(bot: Bot, event: Event, state: T_State):
    answ = random.choice(bad_songs_id)
    musc = total_list.by_id(answ)
    musc_result = song_txt(musc)
    await yinjian2.finish(musc_result)

zyj = on_command("随个朱云杰")
@zyj.handle()
async def _(bot: Bot, event: Event, state: T_State):
    fk = int((random.random() * 100) % 17 + 1)
    img = Image.open(f"src/zyj/{fk}.jpg").convert('RGBA')
    await zyj.finish([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(img), encoding='utf-8')}"
            }
        }])
    
spec_rand = on_regex(r"^随个(?:dx|sd|标准)?[绿黄红紫白]?[0-9]+\+?")


@spec_rand.handle()
async def _(bot: Bot, event: Event, state: T_State):
    level_labels = ['绿', '黄', '红', '紫', '白']
    regex = "随个((?:dx|sd|标准))?([绿黄红紫白]?)([0-9]+\+?)"
    res = re.match(regex, str(event.get_message()).lower())
    try:
        if res.groups()[0] == "dx":
            tp = ["DX"]
        elif res.groups()[0] == "sd" or res.groups()[0] == "标准":
            tp = ["SD"]
        else:
            tp = ["SD", "DX"]
        level = res.groups()[2]
        if res.groups()[1] == "":
            music_data = total_list.filter(level=level, type=tp)
        else:
            music_data = total_list.filter(level=level, diff=['绿黄红紫白'.index(res.groups()[1])], type=tp)
        if len(music_data) == 0:
            rand_result = "没有这样的乐曲哦。"
        else:
            rand_result = song_txt(music_data.random())
        await spec_rand.send(rand_result)
    except Exception as e:
        print(e)
        await spec_rand.finish("随机命令错误，请检查语法")


rand_course = on_regex(r"随机[中上特下]级")
@rand_course.handle()
async def _(bot: Bot, event: Event, state: T_State):
    level_labels = ['中', '上', '特']
    regex = "随机([中上特下])级"
    res = re.match(regex, str(event.get_message()).lower())
    mid = ['12','12+','13']
    upp = ['13','13+','14']
    ult = ['14','14+']
    level = random
    rand_s = ''
    print (res.groups())
    if res.groups()[0] == "上":
        music_data = total_list.filter(ds=(float(13.4), float(14.3)))
        #music_data = total_list.filter(level=random.choice(mid))
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '随机段位上级：300血，每首歌回复20血\n'
        rand_s = rand_s + 'GREAT -2/ GOOD -2/ MISS -5 \n'
        rand_s = rand_s + '第1首：'+ rand_result
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '\n第2首：'+ rand_result
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '\n第3首：'+ rand_result
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '\n第4首：'+ rand_result
        await rand_course.finish(rand_s)
    if res.groups()[0] == "特":
        music_data = total_list.filter(ds=(float(14.4), float(14.9)))
        rand_s = rand_s + '随机段位超上级：100血，每首歌回复10血\n'
        rand_s = rand_s + 'GREAT -2/ GOOD -3/ MISS -5 \n'
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '第1首：' + rand_result
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '\n第2首：' + rand_result
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '\n第3首：' + rand_result
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '\n第4首：' + rand_result
        await rand_course.finish(rand_s)
    if res.groups()[0] == "中":
        music_data = total_list.filter(ds=(float(12.0), float(13.3)))
        rand_s = rand_s + '随机段位中级：500血，每首歌回复50血\n'
        rand_s = rand_s + 'GREAT -2/ GOOD -2/ MISS -5 \n'
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '第1首：' + rand_result
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '\n第2首：' + rand_result
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '\n第3首：' + rand_result
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '\n第4首：' + rand_result
        await rand_course.finish(rand_s)
    if res.groups()[0] == "下":
        music_data = total_list.filter(level='15')
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '第1首：'+ rand_result
        music_data = total_list.filter(level='15')
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '\n第2首：'+ rand_result
        music_data = total_list.filter(level='15')
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '\n第3首：'+ rand_result
        music_data = total_list.filter(level='15')
        rand_result = song_txt(music_data.random())
        rand_s = rand_s + '\n第4首：'+ rand_result
        await rand_course.finish(rand_s)
mr = on_regex(r".*mai.*什么")


@mr.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await mr.finish(song_txt(total_list.random()))


search_music = on_regex(r"^查歌.+")


@search_music.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "查歌(.+)"
    name = re.match(regex, str(event.get_message())).groups()[0].strip()
    if name == "":
        return
    res = total_list.filter(title_search=name)
    if len(res) == 0:
        await search_music.send("没有找到这样的乐曲。")
    elif len(res) < 50:
        search_result = ""
        for music in sorted(res, key = lambda i: int(i['id'])):
            search_result += f"{music['id']}. {music['title']}\n"
        await search_music.finish(Message([
            {"type": "text",
                "data": {
                    "text": search_result.strip()
                }}]))
    else:
        await search_music.send(f"结果过多（{len(res)} 条），请缩小查询范围。")

keti = on_command("课题曲",aliases={'本周课题'})
@keti.handle()
async def _(bot: Bot, event: Event, state: T_State):
    anstring = '本周上级课题：\n'
    ketiqu = total_list.by_id('136')
    anstring += song_txt2(ketiqu)
    anstring += f"\n（紫谱）定数: {ketiqu['ds'][3]}\n达成目标：100.00%"
    await keti.send(anstring)
    astring = '本周中级课题：\n'
    ketiqu2 = total_list.by_id('31')
    astring += song_txt2(ketiqu2)
    astring += f"\n（红谱）定数: {ketiqu2['ds'][2]}\n达成目标：非Perfect个数小于等于5"
    await keti.finish(astring)
 
query_chart = on_regex(r"^([绿黄红紫白]?)id([0-9]+)")


@query_chart.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "([绿黄红紫白]?)id([0-9]+)"
    groups = re.match(regex, str(event.get_message())).groups()
    level_labels = ['绿', '黄', '红', '紫', '白']
    if groups[0] != "":
        try:
            level_index = level_labels.index(groups[0])
            level_name = ['Basic', 'Advanced', 'Expert', 'Master', 'Re: MASTER']
            name = groups[1]
            music = total_list.by_id(name)
            chart = music['charts'][level_index]
            ds = music['ds'][level_index]
            level = music['level'][level_index]
            file = f"https://www.diving-fish.com/covers/{music['id']}.jpg"
            if music.id == '456':
                img = Image.open(f"src/zyj/2.jpg").convert('RGBA')
                file = f"base64://{str(image_to_base64(img), encoding='utf-8')}"
            if music.id == '571':
                img = Image.open(f"src/zyj/4.jpg").convert('RGBA')
                file = f"base64://{str(image_to_base64(img), encoding='utf-8')}"
            if music.id == '772':
                img = Image.open(f"src/zyj/5.jpg").convert('RGBA')
                file = f"base64://{str(image_to_base64(img), encoding='utf-8')}"
            if music.id == '777':
                img = Image.open(f"src/zyj/7.jpg").convert('RGBA')
                file = f"base64://{str(image_to_base64(img), encoding='utf-8')}"
            if music.id == '301' or music.id == '10301':
                img = Image.open(f"src/zyj/6.jpg").convert('RGBA')
                file = f"base64://{str(image_to_base64(img), encoding='utf-8')}"
            if music.id == '799':
                img = Image.open(f"src/zyj/8.jpg").convert('RGBA')
                file = f"base64://{str(image_to_base64(img), encoding='utf-8')}"
            if len(chart['notes']) == 4:
                msg = f'''{level_name[level_index]} {level}({ds})
TAP: {chart['notes'][0]}
HOLD: {chart['notes'][1]}
SLIDE: {chart['notes'][2]}
BREAK: {chart['notes'][3]}
谱师: {chart['charter']}'''
            else:
                msg = f'''{level_name[level_index]} {level}({ds})
TAP: {chart['notes'][0]}
HOLD: {chart['notes'][1]}
SLIDE: {chart['notes'][2]}
TOUCH: {chart['notes'][3]}
BREAK: {chart['notes'][4]}
谱师: {chart['charter']}'''
            await query_chart.send(Message([
                {
                    "type": "text",
                    "data": {
                        "text": f"{music['id']}. {music['title']}\n"
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "file": f"{file}"
                    }
                },
                {
                    "type": "text",
                    "data": {
                        "text": msg
                    }
                }
            ]))
        except Exception:
            await query_chart.send("未找到该谱面")
    else:
        name = groups[1]
        music = total_list.by_id(name)
        try:
            file = f"https://www.diving-fish.com/covers/{music['id']}.jpg"
            await query_chart.send(Message([
                {
                    "type": "text",
                    "data": {
                        "text": f"{music['id']}. {music['title']}\n"
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "file": f"{file}"
                    }
                },
                {
                    "type": "text",
                    "data": {
                        "text": f"艺术家: {music['basic_info']['artist']}\n分类: {music['basic_info']['genre']}\nBPM: {music['basic_info']['bpm']}\n版本: {music['basic_info']['from']}\n难度: {'/'.join(music['level'])}"
                    }
                }
            ]))
        except Exception:
            await query_chart.send("未找到该乐曲")


wm_list = ['打CSGO','睡觉', '出勤', '看比赛', '骂人', '色色', '打课题', '打星星歌', '打旧框', '干饭', '干我', '打Apex', '打我']
place_list = ['石1p','石2p','嗨左机1p','嗨左机2p','嗨右机1p','嗨右机2p','凯风左机1p','凯风左机2p','凯风右机1p','凯风右机2p','金牛万达','锦华万达','财旧框左机','财FiNALE左机','财FiNALE右机','财dx左机','财dx右机','仁和','温江合生汇汤姆熊','床上躺','主人床上']
jrwm = on_command('今日运势', aliases={'今日mai'})


@jrwm.handle()
async def _(bot: Bot, event: Event, state: T_State):
    qq = int(event.get_user_id())
    h = hash(qq)
    rp = h % 100
    wm_value = []
    for i in range(11):
        wm_value.append(h & 3)
        h >>= 2
    s = f"今日人品值：{rp}\n"
    s += f"今日幸运推分地点：{random.choice(place_list)}\n"
    for i in range(11):
        if wm_value[i] == 3:
            s += f'宜 {wm_list[i]}\n'
        elif wm_value[i] == 0:
            s += f'忌 {wm_list[i]}\n'
    s += "今日推荐歌曲："
    music = total_list[h % len(total_list)]
    await jrwm.send(Message([
        {"type": "text", "data": {"text": s}}
    ] + song_txt(music)))
    randnum = random.randint(100001,101973)
    card_dir = r"E:\card"
    try:
        img = Image.open(f"{card_dir}/UI_Card_{randnum}.jpg").convert('RGBA')
    except Exception:
        img = Image.open(f"{card_dir}/UI_Card_{(randnum+1)%101974 + 100001}.jpg").convert('RGBA')
    file = f"base64://{str(image_to_base64(img), encoding='utf-8')}"
    await jrwm.finish(Message([
    {"type": "text", "data": {"text": "今日音击抽卡："}},
        {
            "type": "image",
            "data": {
                "file": file
            }
        }
    ]))
    await jrwm.send()
    
    
myscore = on_command("!查分", aliases={'!me','！me','！查分'})


@myscore.handle()
async def _(bot: Bot, event: Event, state: T_State):
    argvs = str(event.get_message()).strip().split(" ")
    if len(argvs) > 2:
        await myscore.finish("请求格式不对捏\n例：!查分 220")
    else:
        try:
            version0 = 'maimai でらっくす PLUS'
            version1 = 'maimai でらっくす Splash'
            version2 = 'maimai でらっくす'
            version3 = 'maimai'
            version4 = 'maimai PLUS'
            version5 = 'maimai GreeN'
            version6 = 'maimai GreeN PLUS'
            version7 = 'maimai ORANGE'
            version8 = 'maimai ORANGE PLUS'
            version9 = 'maimai PiNK'
            version10 = 'maimai PiNK PLUS'
            version11 = 'maimai MURASAKi'
            version12 = 'maimai MURASAKi PLUS'
            version13 = 'maimai MiLK'
            version14 = 'MiLK PLUS'
            # why?
            version15 = 'maimai FiNALE'
            ur_qq = event.get_user_id()
            if len(argvs) == 2 and ur_qq == "759381653":
                ur_qq = argvs[1]
                print(argvs)
            elif len(argvs) == 2 and ur_qq != "759381653":
                await myscore.finish("是不是格式错了呢？\n例：!查分 对立拉窗帘 (名字中不能有空格哦)\n不可以偷偷查别人分哦\n只有主人可以owo")
            json_data = {'qq': ur_qq,
                         'version': [version0, version1, version2, version3, version4, version5, version6, version7,
                                     version8,
                                     version9, version10, version11, version12, version13, version14, version15]}
        except Exception:
            await myscore.finish("未找到该乐曲哦")
        async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/plate",
                                   json=json_data) as resp:
            play_data = await resp.json()
        # play_data = json.load(play_data_raw)
        with open(f'src/json/play_data_{ur_qq}.json', 'w', -1, 'utf-8') as f:
            json.dump(play_data, f, ensure_ascii=False, indent=4)
        with open(f'src/json/play_data_{ur_qq}.json', 'r', encoding ='utf-8') as ff:
            play_data = json.loads(ff.read())
        fs = ''
        level_indexs = ['绿', '黄', '红', '紫', '白']
        id_or_aliase = 0 # 0是id 1是别名
        try:
            dest = int(argvs[0])
        except Exception:
            #id_or_aliase = 1
            name = argvs[0].strip().lower()
            if name not in music_aliases:
                await myscore.finish("未在别名库中找到此歌曲")
                return
            result_set = music_aliases[name]
            if len(result_set) == 1:
                music = total_list.by_title(result_set[0])
                dest = music.id
            else:
                await myscore.finish("这个别名有很多歌,请用id查询")
        Path = f'src/static/mai/cover/{dest}.jpg'
        if not os.path.exists(Path):
                Path = f'src/static/mai/cover/{dest}.png'
        if not os.path.exists(Path):
                Path = f'src/static/mai/cover/31.jpg'
        image = Image.open(Path)
        image = image.resize(size=(400,400))
        image = image.filter(ImageFilter.GaussianBlur(3))# originally 3
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\Torus SemiBold.otf",40)
        font20 = ImageFont.truetype('../msyh.ttc',24)
        font30 = ImageFont.truetype(r"C:\Users\mercu\Desktop\Eurobot\src\plugins\akat\GOTHIC.ttf",23)
        fs = fs + f"你的 id = {dest} 成绩:\n"
        try:
            for song_list in play_data['verlist']:
                if song_list['id'] == int(dest):
                    tit = song_list['title']
                    ap = 'ALL PERFECT'
                    if(song_list['fc'] == 'app'):
                        ap = 'ALL PERFECT +'
                    elif(song_list['fc'] == 'fcp'):
                        ap = 'FULL COMBO +'
                    elif(song_list['fc'] == 'fc'):
                        ap = 'FULL COMBO'
                    elif(song_list['fc'] == ''):
                        ap = ''
                    fs = fs + f" {level_indexs[song_list['level_index']]}->{song_list['title']}: {'%.4f'%song_list['achievements']}% {ap}\n "
                    draw.text((40,73),'Basic: ',fill = (0,0,255), font=font30)
                    if song_list['level_index'] == 0 :
                        draw.text((170,62),'%.4f'%song_list['achievements'] + '%',fill = (84,255,159), font=font)
                    draw.text((40,123),'Advanced: ',fill = (0,0,255), font=font30)
                    if song_list['level_index'] == 1 :
                        draw.text((170,112),'%.4f'%song_list['achievements'] + '%',fill = (255,255,0), font=font)
                    draw.text((40,173),'Expert: ',fill = (0,0,255), font=font30)
                    if song_list['level_index'] == 2 :
                        draw.text((170,162),'%.4f'%song_list['achievements'] + '%',fill = (255,0,0), font=font)
                    draw.text((40,223),'Master: ',fill = (0,0,255), font=font30)
                    if song_list['level_index'] == 3 :
                        draw.text((170,212),'%.4f'%song_list['achievements'] + '%',fill = (255,0,255), font=font)
                    draw.text((40,273),'Re:Master: ',fill = (0,0,255), font=font30)
                    if song_list['level_index'] == 4 :
                        draw.text((170,262),'%.4f'%song_list['achievements'] + '%',fill = (248,248,255), font=font)
                    fs = fs + "\n"
        except Exception:
            await myscore.finish("未获取到玩家数据捏\n请在查分器绑定qq后再查分哦")
        if fs=='':
            #await myscore.finish(argvs[0])
            await myscore.finish("这首歌你还没有玩过哦;w;\n也有可能是你玩过没更新查分器！")
        draw.text((30,20),tit,fill = (0,245,255), font=font20)
        fs = fs + "Generated By Eurobot & Diving-Fish"
        draw.text((20,320),"Generated By Eurobot" ,fill = (255,20,147), font=font20)
        draw.text((20,350),str(datetime.datetime.now()),fill = (255,20,147), font=font20)
        # image.show()
        await myscore.send(Message([{
                "type": "image",
                "data": {
                    "file": f"base64://{str(image_to_base64(image), encoding='utf-8')}"
                }
            }]))
        # await myscore.finish(fs)


def comp(x):
    return x['achievements']


leader_board = on_command("!排行榜", aliases={'!leaderboard', '排行榜'})


@leader_board.handle()
async def _(bot: Bot, event: Event, state: T_State):
    argvs = str(event.get_message()).strip().split(" ")
    level_labels = ['绿', '黄', '红', '紫', '白']
    level_index = 3
    if len(argvs) != 1:
        level_index = level_labels.index(argvs[1])
    basedir = r'C:\Users\mercu\Desktop\Eurobot\src\json'
    list = os.listdir(basedir)
    qwq = []
    max = 0
    max_qq = 0
    ur = 0
    me = 0
    song_name = ""
    try:
        version0 = 'maimai でらっくす PLUS'
        version1 = 'maimai でらっくす Splash'
        version2 = 'maimai でらっくす'
        version3 = 'maimai'
        version4 = 'maimai PLUS'
        version5 = 'maimai GreeN'
        version6 = 'maimai GreeN PLUS'
        version7 = 'maimai ORANGE'
        version8 = 'maimai ORANGE PLUS'
        version9 = 'maimai PiNK'
        version10 = 'maimai PiNK PLUS'
        version11 = 'maimai MURASAKi'
        version12 = 'maimai MURASAKi PLUS'
        version13 = 'maimai MiLK'
        version14 = 'MiLK PLUS'
        # why?
        version15 = 'maimai FiNALE'
        version16 = 'maimai でらっくす Splash+'
        ur_qq = event.get_user_id()
        json_data = {'qq': event.get_user_id(),
                     'version': [version0, version1, version2, version3, version4, version5, version6, version7,
                                 version8,
                                 version9, version10, version11, version12, version13, version14, version15]}
    except Exception:
        await myscore.finish("未找到该乐曲哦")
    async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/plate",
                               json=json_data) as resp:
        play_data = await resp.json()
    try:
        dest = int(argvs[0])
    except Exception:
        name = argvs[0].strip().lower()
        if name not in music_aliases:
            await leader_board.finish(f"未找到歌曲{ [name] }\n有没有一种可能是没有这个别名")
            return
        result_set = music_aliases[name]
        if len(result_set) == 1:
            music = total_list.by_title(result_set[0])
            dest = music.id
        else:
            await leader_board.finish("这个别名有很多歌,请用id查询")
    # print(argvs[0])
    # print(dest)
    # lev = int(argvs[1])
    with open(f'src/json/play_data_{ur_qq}.json', 'w', -1, 'utf-8') as f:
        json.dump(play_data, f, ensure_ascii=False, indent=4)
    with open(f'src/json/play_data_{ur_qq}.json', 'r', encoding='utf-8') as ff:
        play_d = json.loads(ff.read())
        for song_lists in play_d['verlist']:
            if song_lists['id'] == int(dest) and song_lists['level_index'] == level_index:
                ur = song_lists['achievements']
        ff.close()
    with open(f'src/json/play_data_759381653.json', 'r', encoding='utf-8') as f:
        play_da = json.loads(f.read())
        for song_listss in play_da['verlist']:
            if song_listss['id'] == int(dest) and song_listss['level_index'] == level_index:
                me = song_listss['achievements']
        f.close()


    def comp(x):
        return x['achievements']

    for files in list:
        try:
            with open(f'{basedir}\{files}', 'r', encoding='utf-8') as fff:
                play_data = json.loads(fff.read())
                for song_list in play_data['verlist']:
                    if song_list['id'] == int(dest) and song_list['level_index'] == level_index:
                        qwq.append(song_list)
                        song_name = song_list['title']
                        if song_list['achievements'] > max:
                            max = song_list['achievements']
                            max_qq = files.split(".")[0].split("_")[2]
        except:
            pass
    fff.close()
    qwq.sort(key=comp, reverse=True)
    sendf = ""
    sendf += f"歌曲 {song_name}({level_labels[level_index]})\n 在使用过 Eurobot 账号的库中的排行榜：\n"
    sendf += f"第一名是 qq = {max_qq}\n"
    ct = 1
    tt = 0
    ttt = 0
    for songs in qwq:
        if ur == songs['achievements'] and tt == 0:
            sendf += f" (您) #{ct} : {'%.4f'%songs['achievements']}% {songs['fc']}\n"
            tt = 1
        elif me == songs['achievements'] and tt == 0 and ttt == 0:
            sendf += f" (主人) #{ct} : {'%.4f' % songs['achievements']}% {songs['fc']}\n"
            ttt = 1
        else:
            sendf += f" #{ct} : {'%.4f'%songs['achievements']}% {songs['fc']}\n"
        ct += 1
    sendf += "为了保护个人信息，排行榜只显示自己/主人/第一名的信息"
    await leader_board.send(Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(text_to_image(sendf)), encoding='utf-8')}"
                }
        }]))

update = on_command("!update")
@update.handle()
async def _(bot: Bot, event: Event, state: T_State):
    argvs = str(event.get_message()).strip().split(" ")
    sec = time.time()
    version0 = 'maimai でらっくす PLUS'
    version1 = 'maimai でらっくす Splash'
    version2 = 'maimai でらっくす'
    version3 = 'maimai'
    version4 = 'maimai PLUS'
    version5 = 'maimai GreeN'
    version6 = 'maimai GreeN PLUS'
    version7 = 'maimai ORANGE'
    version8 = 'maimai ORANGE PLUS'
    version9 = 'maimai PiNK'
    version10 = 'maimai PiNK PLUS'
    version11 = 'maimai MURASAKi'
    version12 = 'maimai MURASAKi PLUS'
    version13 = 'maimai MiLK'
    version14 = 'MiLK PLUS'
    # why?
    version15 = 'maimai FiNALE'
    ur_qq = event.get_user_id()
    if ur_qq != "759381653" and len(argvs) > 1:
        await update.finish("?")
    if ur_qq == "759381653" and len(argvs) == 1:
        ur_qq = argvs[0]
    json_data = {'qq': ur_qq,
                 'version': [version0, version1, version2, version3, version4, version5, version6, version7, version8,
                             version9, version10, version11, version12, version13, version14, version15]}
    async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/plate",
                               json=json_data) as resp:
        play_data = await resp.json()
    if not play_data['verlist'] :
        await update.finish("更新失败！请检查你的输入捏")
    else :
        sec1 = time.time()
        with open(f'src/json/play_data_{ur_qq}.json', 'w', -1, 'utf-8') as f:
            json.dump(play_data, f, ensure_ascii=False, indent=4)
        await update.finish(f"更新成功！用时{'%.4f'%(sec1-sec)}秒")
myscores = on_command("!filter", aliases={"!分数列表"})


@myscores.handle()
async def _(bot: Bot, event: Event, state: T_State):
    argvs = str(event.get_message()).strip().split(" ")
    sec = time.time()
    version0 = 'maimai でらっくす PLUS'
    version1 = 'maimai でらっくす Splash'
    version2 = 'maimai でらっくす'
    version3 = 'maimai'
    version4 = 'maimai PLUS'
    version5 = 'maimai GreeN'
    version6 = 'maimai GreeN PLUS'
    version7 = 'maimai ORANGE'
    version8 = 'maimai ORANGE PLUS'
    version9 = 'maimai PiNK'
    version10 = 'maimai PiNK PLUS'
    version11 = 'maimai MURASAKi'
    version12 = 'maimai MURASAKi PLUS'
    version13 = 'maimai MiLK'
    version14 = 'MiLK PLUS'
    # why?
    version15 = 'maimai FiNALE'
        # play_data = json.load(play_data_raw)
    sec1 = time.time()
    if len(argvs) <= 3:
        ur_qq = event.get_user_id()
        json_data = {'qq': ur_qq,
                     'version': [version0, version1, version2, version3, version4, version5, version6, version7,
                                 version8,
                                 version9, version10, version11, version12, version13, version14, version15]}
        async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/plate",
                                   json=json_data) as resp:
            play_data = await resp.json()
        with open(f'src/json/play_data_{ur_qq}.json', 'w', -1, 'utf-8') as f:
            json.dump(play_data, f, ensure_ascii=False, indent=4)
        with open(f'src/json/play_data_{ur_qq}.json', 'r', encoding ='utf-8') as ff:
            play_data = json.loads(ff.read())
        fs = ''
        qwq = []
        ct = 0
        level_indexs = ['绿', '黄', '红', '紫', '白']
        for song_list in play_data['verlist']:
            if song_list['level'] == str(argvs[0]) and len(argvs) == 3 and song_list['achievements'] >= float(argvs[1]) \
                    and song_list['achievements'] <= float(argvs[2]):
                qwq.append(song_list)
            elif song_list['level'] == str(argvs[0]) and len(argvs) == 2 and song_list['achievements'] >= float(argvs[1]):
                qwq.append(song_list)
            elif song_list['level'] == str(argvs[0]) and len(argvs) == 1:
                qwq.append(song_list)
        if len(argvs) == 2:
                fs = fs + f"你 Lv{argvs[0]} 中比 {'%.4f'%float(argvs[1])}% 高的成绩：\n"
        elif len(argvs) == 1:
                fs = fs + f"你 Lv{argvs[0]} 的成绩列表：\n"
        elif len(argvs) == 3:
                fs = fs + f"你 Lv{argvs[0]} 中位于 [ {'%.4f'%float(argvs[1])} , {'%.4f'%float(argvs[2])} ]% 中的成绩：\n"
        qwq.sort(key=comp, reverse=True)
        for song_list in qwq:
                ct = ct + 1
                ap = '(ALL PERFECT)'
                if (song_list['fc'] == 'app'):
                    ap = '(ALL PERFECT +)'
                elif (song_list['fc'] == 'fcp'):
                    ap = '(FULL COMBO +)'
                elif (song_list['fc'] == 'fc'):
                    ap = '(FULL COMBO)'
                elif (song_list['fc'] == ''):
                    ap = ''
                fs = fs + f" {level_indexs[song_list['level_index']]}->{song_list['title']}:\n "
                fs = fs + f"{'%.4f'%song_list['achievements']}%   {ap}\n "
        sec2 = time.time()
        d1 = float(sec1-sec)
        d2 = float(sec2-sec1)
        if fs == '':
            await myscores.finish("没有获取到给定范围的数据呢！\n也有可能是你没更新查分器！")
        fs = fs + f"\n共 {ct} 条，Api响应用时 {'%.4f'%d1} s, 处理用时 {'%.4f'%d2} s.\n Generated By Eurobot & Diving-Fish"
        await myscores.send(Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(text_to_image(fs)), encoding='utf-8')}"
                }
        }]))
    else:
        await myscores.finish("格式错误，试试 !filter 13+ 100.5 或 !filter 14")
        
        
find_song = on_regex(r".+是什么歌")


@find_song.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "(.+)是什么歌"
    name = re.match(regex, str(event.get_message())).groups()[0].strip().lower()
    if name not in music_aliases:
        await find_song.finish("未找到此歌曲\n可能是已经寄了")
        return
    result_set = music_aliases[name]
    if len(result_set) == 1:
        music = total_list.by_title(result_set[0])
        await find_song.finish(Message([{"type": "text", "data": {"text": "您要找的是不是"}}] + song_txt(music)))
    else:
        s = '\n'.join(result_set)
        await find_song.finish(f"您要找的可能是以下歌曲中的其中一首：\n{ s }")


query_score = on_command('分数线')


@query_score.handle()
async def _(bot: Bot, event: Event, state: T_State):
    r = "([绿黄红紫白])(id)?([0-9]+)"
    argv = str(event.get_message()).strip().split(" ")
    if len(argv) == 1 and argv[0] == '帮助':
        s = '''此功能为查找某首歌分数线设计。
命令格式：分数线 <难度+歌曲id> <分数线>
例如：分数线 紫799 100
命令将返回分数线允许的 TAP GREAT 容错以及 BREAK 50落等价的 TAP GREAT 数。
以下为 TAP GREAT 的对应表：
GREAT/GOOD/MISS
TAP\t1/2.5/5
HOLD\t2/5/10
SLIDE\t3/7.5/15
TOUCH\t1/2.5/5
BREAK\t5/12.5/25(外加200落)'''
        await query_score.send(Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(text_to_image(s)), encoding='utf-8')}"
            }
        }]))
    elif len(argv) == 2:
        try:
            grp = re.match(r, argv[0]).groups()
            level_labels = ['绿', '黄', '红', '紫', '白']
            level_labels2 = ['Basic', 'Advanced', 'Expert', 'Master', 'Re:MASTER']
            level_index = level_labels.index(grp[0])
            chart_id = grp[2]
            line = float(argv[1])
            music = total_list.by_id(chart_id)
            chart: Dict[Any] = music['charts'][level_index]
            tap = int(chart['notes'][0])
            slide = int(chart['notes'][2])
            hold = int(chart['notes'][1])
            touch = int(chart['notes'][3]) if len(chart['notes']) == 5 else 0
            brk = int(chart['notes'][-1])
            total_score = 500 * tap + slide * 1500 + hold * 1000 + touch * 500 + brk * 2500
            break_bonus = 0.01 / brk
            break_50_reduce = total_score * break_bonus / 4
            reduce = 101 - line
            if reduce <= 0 or reduce >= 101:
                raise ValueError
            await query_chart.send(f'''{music['title']} {level_labels2[level_index]}
分数线 {line}% 允许的最多 TAP GREAT 数量为 {(total_score * reduce / 10000):.2f}(每个-{10000 / total_score:.4f}%),
BREAK 50落(一共{brk}个)等价于 {(break_50_reduce / 100):.3f} 个 TAP GREAT(-{break_50_reduce / total_score * 100:.4f}%)''')
        except Exception:
            await query_chart.send("格式错误，输入“分数线 帮助”以查看帮助信息")

cf_list = ['吃我','吃mai当劳', '吃KFC', '吃烧烤', '吃火锅', '吃校园干锅', '吃港炉烧鹅', '吃鸡公煲', '吃乡村基', '吃大米先生', '吃食其家', '再roll一次', '和滴蜡熊吃星星', '不许吃了', '吃冒菜', '吃米线', '吃拉面', '吃BK' , '吃东百美食','吃一食堂','吃二食堂二楼','吃四食堂二楼','吃茄皇','吃绝赞','吃touch','吃蜀香干锅','吃火锅米线','吃海鲜焖面','吃跷脚牛肉','吃螺蛳粉','吃p去吧','吃手抓饼','吃烤冷面','吃脆皮炸鸡腿','吃本初子午线' ]
chi = on_regex(r".*今天.*吃什么")
@chi.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await chi.finish(random.choice(cf_list))

shi = on_regex(r"^[石,凯,财,风] .+")


@shi.handle()
async def _(bot: Bot, event: Event, state: T_State):
    qwq = str(event.get_message()).strip().split(" ")
    if qwq[1].isdigit() and qwq[1] != 'null':
            ren = qwq[1]
            if(int(qwq[1]) > 29):
                await shi.finish("哪来的 %d 人" % int(qwq[1]))
                return
            tm = time.time()
            hrx = datetime.datetime.now().hour
            miny = datetime.datetime.now().minute
            if hrx < 10:
                await shi.finish("%s你妈\n这才 %d 点 %d, 你要堵门吗？"%(qwq[0], hrx, miny))
                return
            if qwq[0] == '石':
                file = open('qwq/shiji.txt', 'w')
            if qwq[0] == '财':
                file = open('qwq/caiji.txt', 'w')
            if qwq[0] == '凯':
                file = open('qwq/kaiji.txt', 'w')
            if qwq[0] == '风':
                file = open('qwq/fengji.txt','w')
            file.write(ren)
            file.write("\n")
            file.write(str(tm))
            file.write("\n")
            file.write(event.get_user_id())
            file.close()
            await shi.finish("收到(´-ω-`)")
    if qwq[1] == '几':
            hrx = datetime.datetime.now().hour
            miny = datetime.datetime.now().minute
            if hrx < 10:
                await shi.finish("%s你妈\n这才 %d 点 %d, 你要堵门吗？"%(qwq[0], hrx, miny))
                return
            if qwq[0] == '石':
                file2 = open('qwq/shiji.txt')
            if qwq[0] == '财':
                file2 = open('qwq/caiji.txt')
            if qwq[0] == '凯':
                file2 = open('qwq/kaiji.txt')
            if qwq[0] == '风':
                file2 = open('qwq/fengji.txt')
            ren2 = int(file2.readline())
            # ren2 = ren2*114514
            tm2 = float(file2.readline())
            qqq = int(file2.readline())
            file2.close()
            hr = int((time.time() - tm2) / 3600)
            minu = int((time.time() - tm2) / 60 - 60 * hr)
            sec = time.time() - tm2 - 3600 * hr - 60 * minu
            await shi.finish("%s %d , 最后更新于 %d 小时 %d 分钟 %d 秒前 , by qq %d" % (qwq[0], ren2 , hr , minu , sec , qqq))
            

best_40_pic = on_command('bp')

@best_40_pic.handle()
async def _(bot: Bot, event: Event, state: T_State):
    username = str(event.get_message()).strip()
    if username == "":
        payload = {'qq': str(event.get_user_id())}
    else:
        payload = {'username': username}
    img, success = await generate(payload)
    if success == 400:
        await best_40_pic.send("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。")
    elif success == 403:
        await best_40_pic.send("该用户禁止了其他人获取数据。")
    else:
        await best_40_pic.send(Message([
            {
                "type": "image",
                "data": {
                    "file": f"base64://{str(image_to_base64(img), encoding='utf-8')}"
                }
            }
        ]))
        
saicheng = on_command('赛程') 
team1 = ['不被0:16就算成功 vs 对不队 ：', '冲击sjwの韶钢 vs 今天不在状态 : ' ,'A vs 国宴—甄姬八蔡 ：国宴队弃权', '啊对对队 vs FF : 6:16','C4Che King vs free♂man : 周日晚四点半' ,'纯纯的deso车队 vs 暗影双匕 : 16：11 ','变成光守护西南交大 vs 海绵摆摆 : 周六下午四点 ', 'EterN1ty vs 迪大聪明 : 周六晚八点']
@saicheng.handle()
async def _(bot: Bot, event: Event, state: T_State):
    mstring = ''
    ct = 1
    with open('qwq/matches.txt','r',encoding='utf-8') as p:
        for matches in p:
            ctt = (ct + 1)//2
            if ct % 2 == 1:
                mstring += f"{ctt}. {matches}"
            elif ct % 2 == 0:
                mstring += f"{matches}"
            ct += 1
        mstring += "\n详细赛程/小组积分查看：https://challonge.com/swjtucs\n"
    await saicheng.finish(mstring)
    
adds = on_command('!add')
white_list2 = ['759381653','929743035']
@adds.handle()

async def _(bot: Bot, event: Event, state: T_State):
    qq = event.get_user_id()
    if qq not in white_list2:
        await adds.finish("?")
    req = str(event.get_message()).strip().split(" ")  
    print(len(req))
    print("\n")
    print(req[0])
    print(req[1])
    if(len(req) == 2):
        with open('qwq/matches.txt','r+',encoding='utf-8') as p:
            mlist = p.readlines()
            linect = (int(req[0]) - 1) * 2
            mlist[linect] = ' '.join((mlist[linect], req[1]))
            p.close()
        with open('qwq/matches.txt','w+',encoding='utf-8') as q:
            q.writelines(mlist)
            q.close()
        await adds.finish("收到(´-ω-`)")   
    await adds.finish("命令错误捏\n例 !add 1 14:11")
    

