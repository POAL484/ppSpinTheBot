from twitchio.ext import commands
from twitchio import PartialUser
import twitchio as tio
import os
from random import randint, choice, shuffle
from time import sleep
import threading as thrd
import asyncio
import ast
import datetime as dt
import requests as req
import json
import dill as pckl
import nlpcloud as nlp
import subprocess
import urllib.request
import urllib.request as ulr
import openai as oai
import cv2 as cv
import codecs as cdcs
import webbrowser as wb
import telebot as tb
from telebot import types
import nest_asyncio
import sys
import pandas as pd
#from webptools import webpmux_getframe, dwebp, grant_permission
import websockets as wbscks
from PIL import Image, ImageDraw, ImageFont

#grant_permission()

global cd

cd = []

CFGf = open("config.realconfig", 'r')
CFG = json.load(CFGf)
CFGf.close()
    
api_weather_ya =      CFG['api_weather_ya']
api_weather_op =      CFG['api_weather_op']
api_geocode =             CFG['api_geocode']
api_openai =                 CFG['api_openai']
sp_client_id =              CFG['sp_client_id']
sp_client_secret =   CFG['sp_client_secret']

#based_smiles = {'clear': "рџЊ¤", 'partly-cloudy': "рџЊҐ", 'cloudy': "вЃ", 'overcast': "рџЊ§", 'drizzle': "рџЊ§", 'light-rain': "рџЊ§", 'rain': "рџЊ§", 'moderate-rain': "рџЊ§", 'heavy-rain': "рџЊ§рџЊ§", 'continuous-heavy-rain': "рџЊ§рџЊ§рџЊ§рџЊ§", 'showers': "рџЊ§рџЊ§рџЊ§", 'wet-snow': "рџЊ§рџЊЁ", 'light-snow': "рџЊЁ", 'snow': "рџЊЁ", 'snow-showers': "рџЊЁрџЊЁ", 'hail': "рџЊ§", 'thunderstorm': "рџЊ©", 'thunderstorm-with-rain': "в›€", 'thunderstorm-with-hail': "в›€"}
#based_sit       =  {'clear': "РЇСЃРЅРѕ", 'partly-cloudy': "РњР°Р»РѕРѕР±Р»Р°С‡РЅРѕ", 'cloudy': "РћР±Р»Р°С‡РЅРѕ СЃ РїСЂРѕСЏСЃРЅРµРЅРёСЏРјРё", 'overcast': "РџР°СЃРјСѓСЂРЅРѕ", 'drizzle': "РњРѕСЂРѕСЃСЊ", 'light-rain': "РќРµР±РѕР»СЊС€РѕР№ РґРѕР¶РґСЊ", 'rain': "Р”РѕР¶РґСЊ", 'moderate-rain': "РЈРјРµСЂРµРЅРЅРѕ СЃРёР»СЊРЅС‹Р№ РґРѕР¶РґСЊ", 'heavy-rain': "РЎРёР»СЊРЅС‹Р№ РґРѕР¶РґСЊ", 'continuous-heavy-rain': "РґР»РёС‚РµР»СЊРЅС‹Р№ СЃРёР»СЊРЅС‹Р№ РґРѕР¶РґСЊ", 'showers': "Р›РёРІРµРЅСЊ", 'wet-snow': "РЎРЅРµРіРѕРґРѕР¶РґСЊ", 'light-snow': "РќРµР±РѕР»СЊС€РѕР№ СЃРЅРµРі", 'snow': "СЃРЅРµРі", 'snow-showers': "РЎРЅРµРіРѕРїР°Рґ", 'hail': "Р“СЂР°Рґ", 'thunderstorm': "Р“СЂРѕР·Р°", 'thunderstorm-with-rain': "Р”РѕР¶РґСЊ СЃ РіСЂРѕР·РѕР№", 'thunderstorm-with-hail': "Р“СЂРѕР·Р° СЃ РіСЂР°РґРѕРј"}

elpsd = dt.datetime.now()

oai.api_key = api_openai

class str0list0split:
    def __init__(self, objstr: str, listcut = None, strcut = None):
        self.str = objstr
        self.list = objstr.split()
        if not listcut is None:
            try: listcut[0], listcut[1]
            except IndexError: self.str = "str0list0split Error: listcut arg should have 0 and 1 indexes"
            for i in range(listcut[0], listcut[1]+1):
                self.list.pop(listcut[0])
            self.str = ''
            for i in range(len(self.list)):
                self.str += self.list[i]
                self.str += ' '
            self.str = self.str[0:len(self.str)-1]
        if not strcut is None:
            try: strcut[0], strcut[1]
            except IndexError: self.str =  "str0list0split Error: strcut arg should have 0 and indexes"
            self.str = self.str[strcut[0]:strcut[1]]
            self.list = self.str.split()
    def strcut(self, fr, to):
        self.str = self.str[fr:to]
        self.list = self.str.split()
    def listcut(self, fr, to):
        for i in range(fr, to+1):
            self.list.pop(fr)
        self.str = ''
        for i in range(len(self.list)):
            self.str += self.list[i]
            self.str += ' '
        self.str = self.str[0:len(self.str)-1]

def fastListToStr(l):
    e = ''
    for i in range(len(l)):
        e += l[i]
        e += ' '
    return e

def cooldown(name):
    global cd
    cd.append(name)
    sleep(120)
    cd.remove(name)
    return

def timecount(afk, name):
    a = afk[name]["time"]
    c = dt.datetime(int(a.split()[0].split('-')[0]), int(a.split()[0].split('-')[1]), int(a.split()[0].split('-')[2]), int(a.split()[1].split(':')[0]), int(a.split()[1].split(':')[1]), int(a.split()[1].split('.')[0].split(':')[2]))
    delta = dt.datetime.now() - c
    sec = int(delta.total_seconds())
    rtrn = ''
    secs = sec//86400
    if secs != 0: rtrn += f'{secs} дней '
    sec -= secs*86400
    secs = sec//3600
    if secs != 0: rtrn += f'{secs} часов'
    sec -= secs*3600
    secs = sec//60
    if secs != 0: rtrn += f'{secs} мин '
    sec -= secs*60
    rtrn += f'{sec} сек'
    return rtrn

def timecount_nonafk(dte):
    delta = dt.datetime.now() - dte
    sec = int(delta.total_seconds())
    rtrn = ''
    secs = sec//86400
    if secs != 0: rtrn += f'{secs} дней '
    sec -= secs*86400
    secs = sec//3600
    if secs != 0: rtrn += f'{secs} часов '
    sec -= secs*3600
    secs = sec//60
    if secs != 0: rtrn += f'{secs} мин '
    sec -= secs*60
    rtrn += f'{sec} сек'
    return rtrn

def dankthread(ctx, cnt, i, botinok_):
    if cnt == "raise OPENERROR":
        botinok_.danks[i]['Return'] = "OPENERROR"
        botinok_.danks[i]['Error'] = '2'
        return
    if cnt == "raise HARAMERROR":
        botinok_.danks[i]['Return'] = "HARAMERROR"
        botinok_.danks[i]['Error'] = '3'
        return
    try:
    #if True:
        #print(cnt)
        #print(i)
        botinok_.danks[i]['Return'] = "To return Something , write =r \"Something\""
        exec(cnt)
        botinok_.danks[i]['Error'] = '-1'
        return
    except Exception as e:
        botinok_.danks[i]['Error'] = '1'
        botinok_.danks[i]['Return'] = e
        return

async def aexec(code, **kwargs):
    # Don't clutter locals
    locs = {}
    # Restore globals later
    globs = globals().copy()
    args = ", ".join(list(kwargs.keys()))
    exec(f"async def func({args}):\n    " + code.replace("\n", "\n    "), {}, locs)
    # Don't expect it to return from the coro.
    result = await locs["func"](**kwargs)
    try:
        globals().clear()
        # Inconsistent state
    finally:
        globals().update(**globs)
    return result

class Bot(commands.Bot):

    def __init__(self): #РёРЅРёС‚ РіРѕРІРЅР°
        super().__init__(token=CFG['oauth_ppSpin'], prefix='*', initial_channels=["POAL48", "pwgood", "alexproduct", "tatt04ek", "the_il_", "enihei", "shadowdemonhd_", "Alexoff35", "red3xtop", "orlega_", "wanderning_", "echoinshade", "erynga"])    
        self.msgs = []
        self.pwe = True
        self.pwr = " РЅРѕ "
        self.afk = {}
        self.loc = {}
        self.eventctx = ''
        self.USERDATA={'bans': [], 'notify': {'pwgood': {'stream': False}}}
        self.evtimer = dt.datetime.now()
        self.tgfw = ''
        self.turningOn = 1
        self.avaGame = json.load(open("avaGame.data", 'r'))
        self.avaGameAdd = json.load(open("avaGameAdd.data", 'r'))
        self.loop_ = {'enabled': False}
        self.testDataLoop = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5}
        self.isLastMsgPpSpin = {'poal48': False, 'tatt04ek': False, 'the_il_': False, 'enihei': False, 'shadowdemonhd_': False, 'red3xtop': False, 'orlega_': False, 'wanderning_': False, 'echoinshade': False}
        self.isReconnect7tvEvents = False
        

    async def event_ready(self): #РєРѕРіРґР° СЂР°Р±РѕС‚Р°РµС‚
        print("Importing data...", end=' ')
        asd = cdcs.open("temp.emt", 'w', 'utf8')
        asd.write(req.get("https://7tv.io/v3/emote-sets/6301dcecf7723932b45c06b0").text)
        asd.close()
        asd = cdcs.open("temp.emt", 'r', 'utf8')
        self.emts = json.load(asd)
        asd.close()
        os.remove("temp.emt")
        self.emts = self.emts['emotes']
        self.emtsil = req.get("https://7tv.io/v3/emote-sets/62b36e38765d72b656d6e985").json()['emotes']
        self.emtshei = req.get("https://7tv.io/v3/emote-sets/63c43185219a2920cb348329").json()['emotes']
        self.emtsdemon = req.get("https://7tv.io/v3/emote-sets/6330291d9474f0aac65a0488").json()['emotes']
        self.emts04 = req.get("https://7tv.io/v3/emote-sets/6106a52a3ed2ea3f60da4d58").json()['emotes']
        self.emtsoff = req.get("https://7tv.io/v3/emote-sets/6414ce0a220f8400b8783ce6").json()['emotes']
        self.emtsred3x = req.get("https://7tv.io/v3/emote-sets/63191283b2ef04bef5df01a3").json()['emotes']
        self.emtsorl = req.get("https://7tv.io/v3/emote-sets/63e146945d4acdefd44791d5").json()['emotes']
        self.emtswand = req.get("https://7tv.io/v3/emote-sets/631db3cc4f3e0f1fc59fa8d9").json()['emotes']
        self.emtsecho = req.get("https://7tv.io/v3/emote-sets/647ef56b28b72684e122574c").json()['emotes']
        self.emtserynga = req.get("https://7tv.io/v3/emote-sets/64a2c96712c2ceffb1120915").json()['emotes']
        print("\nEmotes loaded!\n")
        elpsd = dt.datetime.now()
        self.danks = []
        THIS = cdcs.open("USERDATA.data", 'r', 'utf-8')
        self.USERDATA = json.load(THIS)
        THIS.close()
        print(f"\n\n\nImported Data: {self.USERDATA}\n\n\n")
        resp = req.get("https://7tv.io/v3/emote-sets/61c802080bf6300371940381").json() #pwgood's emotes
        for i in range(len(resp['emotes'])):
            if resp['emotes'][i]['name'] in self.USERDATA['pwemts'].keys(): pass
            else:
                self.USERDATA['pwemts'][resp['emotes'][i]['name']] = {'id': resp['emotes'][i]['id'], 'used': 0, 'pause': False}
        allemts = []
        for i in range(len(resp['emotes'])): allemts.append(resp['emotes'][i]['name'])
        resp = req.get("https://7tv.io/v3/emote-sets/62cdd34e72a832540de95857").json() #7tv globals emotes
        for i in range(len(resp['emotes'])):
            if resp['emotes'][i]['name'] in self.USERDATA['pwemts'].keys(): pass
            else:
                self.USERDATA['pwemts'][resp['emotes'][i]['name']] = {'id': resp['emotes'][i]['id'], 'used': 0, 'pause': False}
        for i in range(len(resp['emotes'])): allemts.append(resp['emotes'][i]['name'])
        for i in self.USERDATA['pwemts'].keys():
            if not i in allemts and not self.USERDATA['pwemts'][i]['pause']:
                self.USERDATA['pwemts'][i]['pause'] = True
                await self.get_channel("poal48").send(f"Эмоут {i} поставлен на паузу PauseChamp")
            if i in allemts and self.USERDATA['pwemts'][i]['pause']:
                self.USERDATA['pwemts'][i]['pause'] = False
                await self.get_channel("poal48").send(f"Эмоут {i} снят с паузы ❌   PauseChamp")
        self.saveUserData()
        print("\nPWGood 7tv emotes loaded!\n")
        '''spF = open("spotify.stare", 'r')
        self.sp_data = json.load(spF)
        spF.close()
        print(f"Imported spotify: {self.sp_data.keys()}")'''
        self.sp_data = json.load(open("spotify.spdata", 'r'))
        for i in self.sp_data.keys():
            try:
                resp = req.post("https://accounts.spotify.com/api/token", params={\
                    'grant_type': "refresh_token",\
                    'refresh_token': self.sp_data[i]['refresh']}, headers={\
                    'Authorization': f"Basic {CFG['sp_based']}", \
                    'Content-Type': "application/x-www-form-urlencoded"}).json()
                self.sp_data[i]['access'] = resp['access_token']
                try: self.sp_data[i]['refresh'] = resp['refresh_token']
                except KeyError: print("refresh token get failed, use old refresh token")
                thrd.Thread(target=self.spreauth, args=(i, )).start()
            except Exception as e: print(f"Failed re-auth {i}, use old data. \n       {e} \n")
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        self.eventctx = self.get_channel("poal48")
        self.testThat = False
        state = "Connected"
        try:
            if sys.argv[1] == "-rec": state = "Reconnected"
        except IndexError: pass
        await self.eventctx.send(f"{state} ppSpin")

    async def event_message(self, message): #РѕР±СЂР°Р±РѕС‚РєР° Р»СЋР±РѕРіРѕ СЃРѕРѕР±С‰РµРЅРёСЏ, РґР°Р¶Рµ Р±РµР· РїСЂРµС„РёРєСЃР°
        if message.echo: #С‡С‚РѕР± РЅР° СЃРµР±СЏ РЅРµ СЂРµРіР°Р»
            return

        '''if message.content == "wtf" and message.author.name == "mraak69":
            ctx = commands.Context(message, self.__init__)
            await ctx.send("@Mraak69, wtf")

        if message.content == "wtf" and message.author.name == "mraak96":
            ctx = commands.Context(message, self.__init__)
            await ctx.send("@Mraak96, wtf")'''

        if "tgСЂ1" in message.content and message.author.name == "supibot": #С‚СЂРёРіРµСЂС‹
            author = str(message.content.split()[1])[:len(message.content.split()[1])-1]
            ctx = commands.Context(message, self.__init__)
            try:
                br = int(open(f"{author}.txt", 'r').read())
            except FileNotFoundError:
                nf = open(f"{author}.txt", 'w')
                nf.write("10")
                nf.close()
                br = int(open(f"{author}.txt", 'r').read())
            br -= 2
            bw = open(f"{author}.txt", 'w')
            bw.write(str(br))
            bw.close()

        if "tgСЂ2" in message.content and message.author.name == "supibot":
            author = str(message.content.split()[1])[:len(message.content.split()[1])-1]
            ctx = commands.Context(message, self.__init__)
            try:
                br = int(open(f"{author}.txt", 'r').read())
            except FileNotFoundError:
                nf = open(f"{author}.txt", 'w')
                nf.write("10")
                nf.close()
                br = int(open(f"{author}.txt", 'r').read())

        if "tgСЂ3" in message.content and message.author.name == "supibot":
            author = str(message.content.split()[1])[:len(message.content.split()[1])-1]
            ctx = commands.Context(message, self.__init__)
            try:
                br = int(open(f"{author}.txt", 'r').read())
            except FileNotFoundError:
                nf = open(f"{author}.txt", 'w')
                nf.write("10")
                nf.close()
                br = int(open(f"{author}.txt", 'r').read())
            br += 5
            bw = open(f"{author}.txt", 'w')
            bw.write(str(br))
            bw.close()

        '''if "tuck POAL48" in message.content:
            ctx = commands.Context(message, self.__init__)
            await ctx.send(f"{message.author.display_name} , СЃРїР°СЃРёР±Рѕ Р·Р° tuck! catSleep ")

        if "ppSpin Р»РѕС…" in message.content:
            ctx = commands.Context(message, self.__init__)
            await ctx.send(f"РЎР°Рј С‚Р°РєРѕР№ CryAboutIt")'''

        ctx = commands.Context(message, self.__init__)

        '''for i in list(self.afk.keys()):
            if i == ctx.author.name and message.content != "*off":
                if self.afk[i]["type"] != "none":
                    if self.afk[i]["type"] == "afk":
                        await ctx.send(f"{ctx.author.display_name} Р±РѕР»СЊС€Рµ РЅРµ afk POGGERS : {self.afk[i]['msg']} ({timecount(self.afk, ctx.author.name)})")
                        self.afk[i]["type"] = "none"
                        self.afk[i]["rafk"] = "afk"
                        wafk = open("afk.txter", 'w')
                        wafk.write(str(self.afk))
                        wafk.close()
                    if self.afk[i]["type"] == "gn":
                        await ctx.send(f"{ctx.author.display_name} РїСЂРѕСЃРЅСѓР»СЃСЏ pwgoodWoke : {self.afk[i]['msg']} ({timecount(self.afk, ctx.author.name)})")
                        self.afk[i]["type"] = "none"
                        self.afk[i]["rafk"] = "gn"
                        wafk = open("afk.txter", 'w')
                        wafk.write(str(self.afk))
                        wafk.close()
                    if self.afk[i]["type"] == "shower":
                        await ctx.send(f"Р°РІСЃРѕРј Р±РѕР»СЃ {ctx.author.display_name} С‚РµРїРµСЂСЊ Р±РѕР»РµРµ Р°РІСЃРѕРј Smirk : {self.afk[i]['msg']} ({timecount(self.afk, ctx.author.name)})")
                        self.afk[i]["type"] = "none"
                        self.afk[i]["rafk"] = "shower"
                        wafk = open("afk.txter", 'w')
                        wafk.write(str(self.afk))
                        wafk.close()
                    if self.afk[i]["type"] == "play":
                        await ctx.send(f"catRave {ctx.author.display_name} РЅР°РёРіСЂР°Р»СЃСЏ РІ {self.afk[i]['msg']} ({timecount(self.afk, ctx.author.name)})")
                        self.afk[i]["type"] = "none"
                        self.afk[i]["rafk"] = "play"
                        wafk = open("afk.txter", 'w')
                        wafk.write(str(self.afk))
                        wafk.close()'''


        if "vanishme" in message.content.lower():
            if message.channel.name == "poal48":
                httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token'])
                pu = PartialUser(httpi, 276061388, 'poal48')
                await pu.timeout_user(CFG['api_token'], 276061388, ctx.author.id, 1, "пипо ваниш")
            if message.channel.name == "asty_t0ka":
                httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token'])
                pu = PartialUser(httpi, 453786010, 'asty_t0ka')
                await pu.timeout_user(CFG['api_token'], 276061388, ctx.author.id, 1, "пипо ваниш")
            if message.channel.name == "the_il_":
                httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token'])
                pu = PartialUser(httpi, 781210561, 'the_il_')
                await pu.timeout_user(CFG['api_token'], 276061388, ctx.author.id, 1, "пипо ваниш")
            if message.channel.name == "enihei":
                httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                pu = PartialUser(httpi, 592154330, 'enihei')
                await pu.timeout_user(CFG['api_token_ppSpin'], 841491788, ctx.author.id, 1, "пипо ваниш")
            if message.channel.name == "shadowdemonhd_":
                httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                pu = PartialUser(httpi, 521683891, 'shadowdemonhd_')
                await pu.timeout_user(CFG['api_token_ppSpin'], 841491788, ctx.author.id, 1, "пипо ваниш")
            if message.channel.name == "tatt04ek":
                httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                pu = PartialUser(httpi, 244668427, 'tatt04ek')
                await pu.timeout_user(CFG['api_token_ppSpin'], 841491788, ctx.author.id, 1, "пипо ваниш")
            if message.channel.name == "red3xtop":
                httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                pu = PartialUser(httpi, 489926403, 'red3xtop')
                await pu.timeout_user(CFG['api_token_ppSpin'], 841491788, ctx.author.id, 1, "пипо ваниш")
            if message.channel.name == "orlega_":
                httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                pu = PartialUser(httpi, 511985939, 'orlega_')
                await pu.timeout_user(CFG['api_token_ppSpin'], 841491788, ctx.author.id, 1, "пипо ваниш")
            if message.channel.name == "wanderning_":
                httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                pu = PartialUser(httpi, 738421324, 'wanderning_')
                await pu.timeout_user(CFG['api_token_ppSpin'], 841491788, ctx.author.id, 1, "пипо ваниш")
            if message.channel.name == "echoinshade":
                httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                pu = PartialUser(httpi, 423469896, 'echoinshade')
                await pu.timeout_user(CFG['api_token_ppSpin'], 841491788, ctx.author.id, 1, "пипо ваниш")
                    

        self.msgs.append(message)

        if self.eventctx:
            if (dt.datetime.now() - self.evtimer).total_seconds() > 10.0:
                self.evtimer = dt.datetime.now()
                info = await self.fetch_channel("276061388")
                if self.USERDATA['notify']['poal48']['title'] != info.title:
                    self.USERDATA['notify']['poal48']['title'] = info.title
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 276061388, 'poal48')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"PagMan Название стрима изменено 👉  {info.title}", color="orange")
                info = await self.search_channels("poal48")
                for i in range(len(info)):
                    if info[i].name == "poal48":
                        info = info[i]
                        break
                if info.live and not self.USERDATA['notify']['poal48']['stream']:
                    self.USERDATA['notify']['poal48']['stream'] = True
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 276061388, 'poal48')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"PagMan СТРИМ НАЧАЛСЯ!!!", color="orange")
                if not info.live and self.USERDATA['notify']['poal48']['stream']:
                    self.USERDATA['notify']['poal48']['stream'] = False
                    self.saveUserData()
                    if not self.turningOn: print("Трансляция закончилась")
                    
                info = await self.fetch_channel("116738112")
                if self.USERDATA['notify']['pwgood']['title'] != info.title:
                    self.USERDATA['notify']['pwgood']['title'] = info.title
                    self.saveUserData()
                    if not self.turningOn: await self.eventctx.send(f"Пакет сменил титл 👉 {info.title}")
                info = await self.search_channels("pwgood")
                for i in range(len(info)):
                    if info[i].name == "pwgood":
                        info = info[i]
                        break
                if info.live and not self.USERDATA['notify']['pwgood']['stream']:
                    self.USERDATA['notify']['pwgood']['stream'] = True
                    self.saveUserData()
                    if not self.turningOn: await self.eventctx.send("Пакет начал стрим!")
                if not info.live and self.USERDATA['notify']['pwgood']['stream']:
                    self.USERDATA['notify']['pwgood']['stream'] = False
                    self.saveUserData()
                    if not self.turningOn: await self.eventctx.send("Пакет кончил!")

                info = await self.fetch_channel("781210561")
                if self.USERDATA['notify']['the_il_']['title'] != info.title:
                    self.USERDATA['notify']['the_il_']['title'] = info.title
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 781210561, 'the_il_')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"Название изменено 👉 {info.title}")
                info = await self.search_channels("the_il_")
                for i in range(len(info)):
                    if info[i].name == "the_il_":
                        info = info[i]
                        break
                if info.live and not self.USERDATA['notify']['the_il_']['stream']:
                    self.USERDATA['notify']['the_il_']['stream'] = True
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 781210561, 'the_il_')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"ppBounce the_IL_ Стримит!! ppBounce")
                    if not self.turningOn: await self.more500send(self.get_channel("the_il_"), " ".join(self.USERDATA['IL']['massping']), "ppBounce", "ppBounce")
                if not info.live and self.USERDATA['notify']['the_il_']['stream']:
                    self.USERDATA['notify']['the_il_']['stream'] = False
                    self.saveUserData()
                    if not self.turningOn: await self.get_channel("the_il_").send("the_IL_ Кончил Sadge")

                info = await self.fetch_channel("592154330")
                if self.USERDATA['notify']['enihei']['title'] != info.title:
                    self.USERDATA['notify']['enihei']['title'] = info.title
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 592154330, 'enihei')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"PagMan Название изменено 👉 {info.title}")
                info = await self.search_channels("enihei")
                for i in range(len(info)):
                    if info[i].name == "enihei":
                        info = info[i]
                        break
                if info.live and not self.USERDATA['notify']['enihei']['stream']:
                    self.USERDATA['notify']['enihei']['stream'] = True
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 592154330, 'enihei')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"Enihei Стримит!! NOWAY")
                    if not self.turningOn: await self.more500send(self.get_channel("enihei"), " ".join(self.USERDATA['enihei']['massping']), "NOWAY", "NOWAY")
                if not info.live and self.USERDATA['notify']['enihei']['stream']:
                    self.USERDATA['notify']['enihei']['stream'] = False
                    self.saveUserData()
                    if not self.turningOn: await self.get_channel("enihei").send("GachiPls NeSpravedlivo")

                info = await self.fetch_channel("521683891")
                if self.USERDATA['notify']['demon']['title'] != info.title:
                    self.USERDATA['notify']['demon']['title'] = info.title
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 521683891, 'shadowdemonhd_')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"PagMan Название изменено 👉 {info.title}")
                info = await self.search_channels("shadowdemonhd_")
                for i in range(len(info)):
                    if info[i].name == "shadowdemonhd_":
                        info = info[i]
                        break
                if info.live and not self.USERDATA['notify']['demon']['stream']:
                    self.USERDATA['notify']['demon']['stream'] = True
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 521683891, 'enihei')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"ShadowDemonHD_ Стримит!! NOWAY")
                    if not self.turningOn: await self.more500send(self.get_channel("shadowdemonhd_"), " ".join(self.USERDATA['demon']['massping']), "NOWAY", "NOWAY")
                if not info.live and self.USERDATA['notify']['demon']['stream']:
                    self.USERDATA['notify']['demon']['stream'] = False
                    self.saveUserData()
                    if not self.turningOn: await self.get_channel("shadowdemonhd_").send("gachiBASS NeSpravedlivo")

                info = await self.fetch_channel("244668427")
                if self.USERDATA['notify']['tatt04ek']['title'] != info.title:
                    self.USERDATA['notify']['tatt04ek']['title'] = info.title
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 244668427, 'tatt04ek')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"PagMan Название изменено 👉 {info.title}")
                info = await self.search_channels("tatt04ek")
                for i in range(len(info)):
                    if info[i].name == "tatt04ek":
                        info = info[i]
                        break
                if info.live and not self.USERDATA['notify']['tatt04ek']['stream']:
                    self.USERDATA['notify']['tatt04ek']['stream'] = True
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 244668427, 'tatt04ek')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"plink TaTT04ek Стримит!! plonk")
                    if not self.turningOn: await self.more500send(self.get_channel("tatt04ek"), " ".join(self.USERDATA['tatt04ek']['massping']), "plink", "plonk")
                if not info.live and self.USERDATA['notify']['tatt04ek']['stream']:
                    self.USERDATA['notify']['tatt04ek']['stream'] = False
                    self.saveUserData()
                    if not self.turningOn: await self.get_channel("tatt04ek").send("gachiBASS NeSpravedlivo")

                info = await self.fetch_channel("489926403")
                if self.USERDATA['notify']['red3x']['title'] != info.title:
                    self.USERDATA['notify']['red3x']['title'] = info.title
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 489926403, 'red3xtop')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"PagMan Название изменено 👉 {info.title}")
                info = await self.search_channels("red3xtop")
                for i in range(len(info)):
                    if info[i].name == "red3xtop":
                        info = info[i]
                        break
                if info.live and not self.USERDATA['notify']['red3x']['stream']:
                    self.USERDATA['notify']['red3x']['stream'] = True
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 489926403, 'red3xtop')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"ReD3xTop Стримит!! cat3")
                    if not self.turningOn: await self.more500send(self.get_channel("red3xtop"), " ".join(self.USERDATA['red3x']['massping']), "cat3", "cat3")
                if not info.live and self.USERDATA['notify']['red3x']['stream']:
                    self.USERDATA['notify']['red3x']['stream'] = False
                    self.saveUserData()
                    if not self.turningOn: await self.get_channel("red3xtop").send("gachiBASS SadgeCry")

                info = await self.fetch_channel("511985939")
                if self.USERDATA['notify']['orlega_']['title'] != info.title:
                    self.USERDATA['notify']['orlega_']['title'] = info.title
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 511985939, 'orlega_')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"Pag Название изменено 👉 {info.title}")
                info = await self.search_channels("orlega_")
                for i in range(len(info)):
                    if info[i].name == "orlega_":
                        info = info[i]
                        break
                if info.live and not self.USERDATA['notify']['orlega_']['stream']:
                    self.USERDATA['notify']['orlega_']['stream'] = True
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 511985939, 'orlega_')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"orlega Стримит!! stare")
                    if not self.turningOn: await self.more500send(self.get_channel("orlega_"), " ".join(self.USERDATA['orlega_']['massping']), "stare", "stare")
                if not info.live and self.USERDATA['notify']['orlega_']['stream']:
                    self.USERDATA['notify']['orlega_']['stream'] = False
                    self.saveUserData()
                    if not self.turningOn: await self.get_channel("orlega_").send("gachiBASS peepoSad")

                info = await self.fetch_channel("738421324")
                if self.USERDATA['notify']['wanderning_']['title'] != info.title:
                    self.USERDATA['notify']['wanderning_']['title'] = info.title
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 738421324, 'wanderning_')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"PagMan Название изменено 👉 {info.title}")
                info = await self.search_channels("wanderning_")
                for i in range(len(info)):
                    if info[i].name == "wanderning_":
                        info = info[i]
                        break
                if info.live and not self.USERDATA['notify']['wanderning_']['stream']:
                    self.USERDATA['notify']['wanderninig_']['stream'] = True
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 738421324, 'wanderning_')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"wanderning Стримит!! Zaebok")
                    if not self.turningOn: await self.more500send(self.get_channel("wanderning_"), " ".join(self.USERDATA['wanderning_']['massping']), "Zaebok", "Zaebok")
                if not info.live and self.USERDATA['notify']['wanderning_']['stream']:
                    self.USERDATA['notify']['wanderning_']['stream'] = False
                    self.saveUserData()
                    if not self.turningOn: await self.get_channel("wanderning_").send("GachiPls sadCat")

                info = await self.fetch_channel("423469896")
                if self.USERDATA['notify']['echo']['title'] != info.title:
                    self.USERDATA['notify']['echo']['title'] = info.title
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 423469896, 'echoinshade')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"SHTO Название изменено 👉 {info.title}")
                info = await self.search_channels("echoinshade")
                for i in range(len(info)):
                    if info[i].name == "echoinshade":
                        info = info[i]
                        break
                if info.live and not self.USERDATA['notify']['echo']['stream']:
                    self.USERDATA['notify']['echo']['stream'] = True
                    self.saveUserData()
                    httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
                    pu = PartialUser(httpi, 423469896, 'echoinshade')
                    if not self.turningOn: await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"Эхо чарм стримит!! catBombing")
                    if not self.turningOn: await self.more500send(self.get_channel("echoinshade"), " ".join(self.USERDATA['echo']['massping']), "catBombing", "catBombing")
                if not info.live and self.USERDATA['notify']['echo']['stream']:
                    self.USERDATA['notify']['echo']['stream'] = False
                    self.saveUserData()
                    if not self.turningOn: await self.get_channel("echoinshade").send("Sadge")
                                        
                if self.tgfw:
                    if self.tgfw == "[]pingtotw[]poal[]":
                        await self.get_channel("poal48").send("Пинг из телеграмма uuh")
                        self.tgfw = ''
                    elif self.tgfw == "[]pingtotw[]pw[]":
                        await self.get_channel("pwgood").send("Пинг из телеграмма (проверка, сори uuh )")
                        self.tgfw = ''
                    else:
                        fw = "(New post at tg-pwgоod): "
                        await asyncio.sleep(3)
                        fw += self.tgfw
                        self.tgfw = ""
                        print(fw)
                        if not self.USERDATA['notify']['pwgood']['stream']:
                            if not self.turningOn: await self.more500send(self.get_channel("pwgood"), fw, delay=1)
                        else:
                            if not self.turningOn: await self.more500send(self.get_channel("poal48"), "Хотел отправить к пугоду, а у него стрим stare Post: " + fw)
                    
                        #await self.more500send(self.get_channel("poal48"), fw, start="ApuScience")
                wping = open("ping", 'w')
                wping.write(str(dt.datetime.now()))
                wping.close()

        if message.channel.name == "pwgood":
            cnte = message.content.split()
            for i in range(len(cnte)):
                try:
                    if not self.USERDATA['pwemts'][cnte[i]]['pause']: self.USERDATA['pwemts'][cnte[i]]['used'] += 1
                    self.saveUserData()
                except KeyError: pass

        if message.channel.name == "pwgood" and not ctx.author.name in self.avaGame.keys() and not self.USERDATA['notify']['pwgood']['stream'] and not ctx.author.name in self.avaGameAdd['ignore']:
            tUser = await ctx.author.user()
            self.avaGame[ctx.author.name] = {'image': tUser.profile_image, 'display': ctx.author.display_name}
            avaf = open("avaGame.data", 'w')
            json.dump(self.avaGame, avaf)
            avaf.close()

        if message.channel.name in self.isLastMsgPpSpin.keys():
            if self.isLastMsgPpSpin[message.channel.name]:
                self.isLastMsgPpSpin[message.channel.name] = False
            
        if ("pnrtscr.com/gz5n0s" in message.content):
            chnlUs = await message.channel.user(force=True)
            pu = self.create_user(chnlUs.id, message.channel.name)
            await pu.ban_user(CFG['api_token_ppSpin'], 841491788, message.author.id, "pwgood4")


        if message.channel.name == "pwgood" and message.author.name == "pwgud" and message.content == "ppSpin":
            await self.get_channel("pwgood").send("PWGud NaM")
                
        #if message.author.name == "poal48": await asyncio.sleep(1)

        if not message.author.name in self.USERDATA['bans']:
            await self.handle_custom_commands(message)
            await self.handle_commands(message)

    def pwec(self, channel):
        if not self.pwe: return False
        else:
            if channel.name.lower() == "poal48": return False
            else: return True

    '''def offtimer(self):
        sleep(60)
        wafk = open("afk.txter", 'w')
        wafk.write(str(self.afk))
        wafk.close()
        print("\n\nBot ready to close connection\n\n")'''

    '''#СЃР°РјС‹Р№ РїСЂРёРјРёС‚РёРІРЅС‹Р№ РїСЂРёРјРµСЂ РєРѕРјР°РЅРґС‹
    @commands.command(name="h", aliases=['hello']) #РЅР°Р·РІР°РЅРёРµ
    async def hello(self, ctx: commands.Context): 
        await ctx.send(f'Hello {ctx.author.name}! yo ') #СЃРѕРѕР±С‰РµРЅРёРµ'''

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        cnt = str0list0split(ctx.message.content, listcut=(0, 0)).str
        await ctx.send(f"plink Плиньк! {cnt} Бот в работе: {timecount_nonafk(elpsd)}!")

    @commands.command(name="clear")
    async def clear(self, ctx: commands.Context):
        self.msgs = []
        await ctx.send("Буфер очищен! Zaebok ")

    '''@commands.command(name="b", aliases = ['balance', 'showbalance'])
    async def balance(self, ctx: commands.Context):
        if self.pwec(ctx.channel):
            await ctx.send(self.pwr)
            return
        try:
            content = self.msgs[len(self.msgs)-1].content.split()[1]
            authorD = content
            author = content
        except IndexError: 
            author = ctx.author.name
            authorD = ctx.author.display_name
        try:
            br = int(open(f"{author}.txt", 'r').read())
        except FileNotFoundError:

            await ctx.send(f"РџРѕР»СЊР·РѕРІР°С‚РµР»СЊ {authorD} РЅРµ РЅР°Р№РґРµРЅ pwgoodSussy ")
            return
        await ctx.send(f"Р‘Р°Р»Р°РЅСЃ {authorD} :   {br} pwgoodBusiness ")'''

    '''@commands.command(name="edit")
    async def edit(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            try:
                content = self.msgs[len(self.msgs)-1].content.split()[1]
                nb = self.msgs[len(self.msgs)-1].content.split()[2]
                authorD = content
                author = content
            except IndexError:
                try:
                    nb = self.msgs[len(self.msgs)-1].content.split()[1]
                except IndexError:
                    nb = '10'
                author = ctx.author.name
                authorD = ctx.author.display_name
            try:
                br = int(open(f"{author}.txt", 'r').read())
            except FileNotFoundError:
                nf = open(f"{author}.txt", 'w')
                nf.write("10")
                nf.close()
                br = int(open(f"{author}.txt", 'r').read())
            bw = open(f"{author}.txt", 'w')
            bw.write(nb)
            bw.close()
            brn = open(f"{author}.txt", 'r').read()
            await ctx.send(f"Р‘Р°Р»Р°РЅСЃ {authorD} РёР·РјРµРЅРµРЅ:  {br} --> {brn} pwgoodBusiness ")
        else:
            await ctx.send("Something")'''
        
    '''@commands.command(name="delete")
    async def delete(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            content = self.msgs[len(self.msgs)-1].content.split()[1]
            try:
                os.remove(content)
                await ctx.send(f"{content} СѓРґР°Р»РµРЅ pwgoodPooping ")
            except Exception: await ctx.send("РћС€РёР±РєР° Disappointed ")
        else:
            await ctx.send("Something")'''

    '''@commands.command(name="chat_array")
    async def chat_array(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            msgsc = []
            for i in range(len(self.msgs)):
                msgsc.append(self.msgs[i].content)
            await self.more500send(ctx, str(msgsc))
        else:
            await ctx.send("Something")'''

    '''@commands.command(name="leader", aliases=['lider', 'leaderboard'])
    async def leader(self, ctx: commands.Context):
        if self.pwec(ctx.channel):
            await ctx.send(self.pwr)
            return
        os.chdir("C://Users//pbrag//AppData//Local//Programs//Python//Python311//ppSpinTheBot")
        lf = os.listdir()
        lf.remove("ppSpinTheBot.py")
        lf.remove("afk.txter")
        lf.remove("weather.POOOG")
        lf.remove("welpsd.time")
        lf.remove("loc.txter")
        fln = []
        fls = []
        for i in range(len(lf)):
            fln.append(str(lf[i])[:len(str(lf[i]))-4])
            fls.append(int(open(lf[i], 'r').read()))
        ldbn = []
        ldbs = []
        for i in range(3):
            cri = fls.index(max(fls))
            print(fln[cri])
            print(fls[cri])
            ldbn.append(fln[cri])
            fln.remove(fln[cri])
            ldbs.append(fls[cri])
            fls.remove(fls[cri])
            print(ldbn)
            print(ldbs)
        await ctx.send(f"Р›РёРґРµСЂР‘РѕСЂРґ! pwgoodSubs 1: {ldbn[0]} - {ldbs[0]}; 2: {ldbn[1]} - {ldbs[1]}; 3: {ldbn[2]} - {ldbs[2]}.") '''
        
    '''@commands.command(name="antileader", aliases=['antilider', 'antileaderboard'])
    async def antileader(self, ctx: commands.Context):
        if self.pwec(ctx.channel):
            await ctx.send(self.pwr)
            return
        os.chdir("C://Users//pbrag//AppData//Local//Programs//Python//Python311//ppSpinTheBot")
        lf = os.listdir()
        lf.remove("ppSpinTheBot.py")
        lf.remove("afk.txter")
        lf.remove("weather.POOOG")
        lf.remove("welpsd.time")
        lf.remove("loc.txter")
        fln = []
        fls = []
        for i in range(len(lf)):
            fln.append(str(lf[i])[:len(str(lf[i]))-4])
            fls.append(int(open(lf[i], 'r').read()))
        ldbn = []
        ldbs = []
        for i in range(3):
            cri = fls.index(min(fls))
            ldbn.append(fln[cri])
            fln.remove(fln[cri])
            ldbs.append(fls[cri])
            fls.remove(fls[cri])
        await ctx.send(f"РђРЅС‚Рё Р›РёРґРµСЂР‘РѕСЂРґ! pwgoodSussy 1: {ldbn[0]} - {ldbs[0]}; 2: {ldbn[1]} - {ldbs[1]}; 3: {ldbn[2]} - {ldbs[2]}.") '''


    '''@commands.command(name="coin", aliases=['roulette', 'c', 'r', 'casino'])
    async def coin(self, ctx: commands.Context):
        if self.pwec(ctx.channel):
            await ctx.send(self.pwr)
            return
        try:
            content = self.msgs[len(self.msgs)-1].content.split()[1]
        except IndexError:
            content = 0
        try:
            content = int(content)
        except ValueError:
            if content != "all" and content != "РІСЃРµ" and content != "РІСЃС‘" and content != "half" and content != "РїРѕР»РѕРІРёРЅР°":
                await ctx.send("Р’РІРµРґРµРЅР° РЅРµ С†РёС„СЂР° DinkDonk")
                return
            elif content == "all" or content == "РІСЃРµ" or content== "РІСЃС‘":
                try:
                    content = int(open(f"{ctx.author.name}.txt", 'r').read())
                except FileNotFoundError:
                    await ctx.send("РўС‹ РЅРѕРІС‹Р№ РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ, РјРѕР¶РµС€СЊ РїРѕРґРѕР¶РґРµС€СЊ РїСЂРµР¶РґРµ РІСЃРµ СЃС‚Р°РІРёС‚СЊ? pwgoodStare ")
                    return
            elif content == "half" or content == "РїРѕР»РѕРІРёРЅР°":
                try:
                    content = int(open(f"{ctx.author.name}.txt", 'r').read())//2
                except FileNotFoundError:
                    await ctx.send("РџРѕРіРѕРґРё, РїРѕСЃС‚Р°РІСЊ СЃР°Рј: *coin 5 pwgoodStare ")
                    return
            else:
                return
        try:
            br = int(open(f"{ctx.author.name}.txt", 'r').read())
        except FileNotFoundError:
            nf = open(f"{ctx.author.name}.txt", 'w')
            nf.write('10')
            nf.close()
            br = int(open(f"{ctx.author.name}.txt", 'r').read())
        if content > br:
            await ctx.send(f"РќРµ СЃР»РёС€РєРѕРј С‚С‹ РјРЅРѕРіРѕ РїРѕСЃС‚Р°РІРёР»? pwgood3 |Р‘Р°Р»Р°РЅСЃ: {br}")
            return
        if content < 0:
            await ctx.send(" pwgoodWeird ")
            return
        if randint(1,2) == 1:
            bw = open(f"{ctx.author.name}.txt", 'w')
            bw.write(str(br+content))
            bw.close()
            await ctx.send(f"РњРѕРЅРµС‚РєР°!|РЎС‚Р°РІРєР°: {content}|РџРѕР±РµРґР°! CatBop |Р‘Р°Р»Р°РЅСЃ: {br+content}")
        else:
            bw = open(f"{ctx.author.name}.txt", 'w')
            bw.write(str(br-content))
            bw.close()
            await ctx.send(f"РњРѕРЅРµС‚РєР°!|РЎС‚Р°РІРєР°: {content}|РџРѕСЂР°Р¶РµРЅРёРµ! Disappointed |Р‘Р°Р»Р°РЅСЃ: {br-content}")'''


    '''@commands.command(name="PLEASE")
    async def pls(self, ctx: commands.Context):
        global cd
        if self.pwec(ctx.channel):
            await ctx.send(self.pwr)
            return
        try:
            br = int(open(f"{ctx.author.name}.txt", 'r').read())
        except FileNotFoundError:
            await ctx.send("РўС‹ Рё С‚Р°Рє РЅРѕРІРµРЅСЊРєРёР№, С‚РµР±Рµ 10 РїСЂРё СЃС‚Р°СЂС‚Рµ РґР°РґСѓС‚ pwgood3 ")
            return
        if br <= 0:
            if not ctx.author.name in cd:
                bw = open(f"{ctx.author.name}.txt", 'w')
                bw.write('5')
                bw.close()
                await ctx.send("Рљ С‚РµР±Рµ СЃРїСѓСЃС‚РёР»Р°СЃСЊ Р±РѕР¶СЊСЏ Р±Р»Р°РіРѕРґР°С‚СЊ Рё РїРѕРґР°СЂРёР»Р° РїСЏС‚СЊ РґРµРЅРµРі Zaebok ")
                s = thrd.Thread(target = cooldown, args=(ctx.author.name,))
                s.start()
            else:
                await ctx.send("РўС‹ СЃРµР№С‡Р°СЃ РІ РєРґ, РїРѕРґРѕР¶РґРё РЅРµРјРЅРѕРіРѕ pwgood3")
        else:
            await ctx.send("РЈ С‚РµР±СЏ Рё С‚Р°Рє РІСЃРµ РїСЂРµРєСЂР°СЃРЅРѕ pwgood3 ")'''

    @commands.command(name="off")
    async def off(self, ctx: commands.Context):
        if self.modCheck(ctx.author.name.lower()):
            await ctx.send("Бот отключен frame145delay007s ")
            await self.close()
            wafk = open("afk.txter", 'w')
            wafk.write(str(self.afk))
            wafk.close()
            print("\n\nConection Closed!\n\n")
            wping = open("ping", 'w')
            wping.write("==off==")
            wping.close()
        else:
            await ctx.send("Something")

    '''@commands.command(name="tpwe")
    async def toggle_pwgood_enabled(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            if self.pwe:
                self.pwe = False
                await ctx.send("Р‘РѕС‚ РІ С‡Р°С‚Рµ РїСѓРіРѕРґР° (Рё РґСЂСѓРіРёС… РєСЂРѕРјРµ POAL48) РћС‚РєР»СЋС‡РµРЅ sadCat")
            else:
                self.pwe = True
                await ctx.send("Р‘РѕС‚ РІ С‡Р°С‚Рµ РїСѓРіРѕРґР° (Рё РґСЂСѓРіРёС… РєСЂРѕРјРµ POAL48) Р’РєР»СЋС‡РµРЅ URA")
        else:
            await ctx.send("Something")'''

    '''@commands.command(name="afk",aliases=["Р°С„Рє"])
    async def afk(self, ctx: commands.Context):
        contentL = self.msgs[len(self.msgs)-1].content.split()[1:]
        contentL.reverse()
        content = ''
        for i in range(len(contentL)):
            content += contentL.pop()
            content += ' '
        try: content.remove("afk")
        except Exception: pass
        self.afk[ctx.author.name] = {"msg": content, "type": "afk", "rafk": "afk", "time": str(dt.datetime.now())}
        wafk = open("afk.txter", 'w')
        wafk.write(str(self.afk))
        wafk.close()
        await ctx.send(f"{ctx.author.display_name} С‚РµРїРµСЂСЊ afk ppHop : {content}")

    @commands.command(name="rafk", aliases=["resumeafk", "СЂР°С„Рє"])
    async def rafk(self, ctx: commands.Context):
        try: self.afk[ctx.author.name]
        except KeyError:
            await ctx.send("РќРµ РЅР°Р№РґРµРЅ Р°С„Рє СЃС‚Р°С‚СѓСЃ PauseChamp ")
            return
        self.afk[ctx.author.name]["type"] = self.afk[ctx.author.name]["rafk"]
        wafk = open("afk.txter", 'w')
        wafk.write(str(self.afk))
        wafk.close()
        await ctx.send(f"Afk СЃС‚Р°С‚СѓСЃ ({self.afk[ctx.author.name]['rafk']}) РІРѕСЃС‚РѕРЅРѕРІР»РµРЅ ppHop : {self.afk[ctx.author.name]['msg']}")

    @commands.command(name="gn",aliases=["goodnight", "sleep", "РіРЅ", "СЃРїР°С‚СЊ"])
    async def gn(self, ctx: commands.Context):
        contentL = self.msgs[len(self.msgs)-1].content.split()[1:]
        contentL.reverse()
        content = ''
        for i in range(len(contentL)):
            content += contentL.pop()
            content += ' '
        try: content.remove("gn")
        except Exception: pass
        self.afk[ctx.author.name] = {"msg": content, "type": "gn", "rafk": "gn", "time": str(dt.datetime.now())}
        wafk = open("afk.txter", 'w')
        wafk.write(str(self.afk))
        wafk.close()
        await ctx.send(f"{ctx.author.display_name} РїРѕС€РµР» СЃРїР°С‚СЊ catSleep : {content}")

    @commands.command(name="shower",aliases=["РґСѓС€"])
    async def shower(self, ctx: commands.Context):
        contentL = self.msgs[len(self.msgs)-1].content.split()[1:]
        contentL.reverse()
        content = ''
        for i in range(len(contentL)):
            content += contentL.pop()
            content += ' '
        try: content.remove("shower")
        except Exception: pass
        self.afk[ctx.author.name] = {"msg": content, "type": "shower", "rafk": "shower", "time": str(dt.datetime.now())}
        wafk = open("afk.txter", 'w')
        wafk.write(str(self.afk))
        wafk.close()
        await ctx.send(f"{ctx.author.display_name} РјРѕРµС‚СЃСЏ Smirk : {content}")

    @commands.command(name="play",aliases=["game", "РёРіСЂР°С‚СЊ", "РёРіСЂР°СЋ"])
    async def play(self, ctx: commands.Context):
        contentL = self.msgs[len(self.msgs)-1].content.split()[1:]
        contentL.reverse()
        content = ''
        for i in range(len(contentL)):
            content += contentL.pop()
            content += ' '
        try: content.remove("play")
        except Exception: pass
        self.afk[ctx.author.name] = {"msg": content, "type": "play", "rafk": "play", "time": str(dt.datetime.now())}
        wafk = open("afk.txter", 'w')
        wafk.write(str(self.afk))
        wafk.close()
        await ctx.send(f"catRave {ctx.author.display_name} РёРіСЂР°РµС‚ РІ {content}")

    @commands.command(name="tuck",aliases=["С‚СѓРє", "СѓР»РѕР¶РёС‚СЊ"])
    async def tuck(self, ctx: commands.Context):
        contentL = self.msgs[len(self.msgs)-1].content.split()[1:]
        contentL.reverse()
        content = ''
        for i in range(len(contentL)):
            content += contentL.pop()
            content += ' '
        try: content.remove("tuck")
        except Exception: pass
        cnnt = ''
        for i in content.split()[1:]:
            cnnt += i
            cnnt += ' '
        await ctx.send(f"РўС‹ СѓР»РѕР¶РёР» {content.split()[0]} СЃРїР°С‚СЊ catSleep : {cnnt}")'''

    '''@commands.command(name="inforestart")
    async def inforestart(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            await ctx.send("РЎРµР№С‡Р°СЃ Р±СѓРґРµС‚ СЂРµСЃС‚Р°СЂС‚ Р±РѕС‚Р° PauseChamp ")
        else:
            await ctx.send("Something")'''

    '''def offtimering(self, ctx):
        asyncio.get_event_loop().create_task(self.offtimer(ctx))'''

    '''@commands.command(name="offing")
    async def offing(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            await ctx.send("Р’СЃРµ afk СЃС‚Р°С‚СѓСЃС‹ СЃРѕС…СЂРѕРЅСЏС‚СЃСЏ С‡РµСЂРµР· 60 СЃРµРєСѓРЅРґ, Р·Р°С‚РµРј РІРµСЂРѕСЏС‚РЅРµРµ РІСЃРµРіРѕ Р±РѕС‚ РІС‹РєР»СЋС‡РёС‚СЃСЏ NeSpravedlivo ")
            thrd.Thread(target = self.offtimer).start()
        else:
            await ctx.send("Something")'''

    '''@commands.command(name="spyid")
    async def spyid(self, ctx: commands.Context):
        contentL = self.msgs[len(self.msgs)-1].content.split()[1:]
        contentL.reverse()
        try: contentL[0]
        except IndexError: contentL.append(ctx.author.name)
        await ctx.send(str(ctx.get_user(contentL[0]).id))
        print(ctx.get_user(contentL[0]).id)'''

    '''@commands.command(name="setloc", aliases=["setlocation"])
    async def setloc(self, ctx: commands.Context):
        content = str0list0split(ctx.message.content, listcut = (0, 0)).str
        geo = req.get("https://api.geoapify.com/v1/geocode/search", params={'text': content, 'apiKey': api_geocode})
        lonn = geo.json()['features'][0]['properties']['lon']
        latn = geo.json()['features'][0]['properties']['lat']
        wloc = open("loc.txter", 'w')
        self.loc[ctx.author.name] = {'lat': latn, 'lon': lonn, 'city': geo.json()['features'][0]['properties']['city']}
        json.dump(self.loc, wloc)
        wloc.close()
        await ctx.send(f"Локация устоновлена 👉 {geo.json()['features'][0]['properties']['city']}, {latn}, {lonn}")'''

    '''@commands.command(name="scannew")
    async def scannew(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            wth = req.get("https://api.weather.yandex.ru/v2/informers?", headers={'X-Yandex-API-Key': api_weather_ya}, params={'lat': "55.755863", 'lon': "37.6177"}).json()
            wff = open("weather.POOOG", 'w')
            json.dump(wth, wff)
            wte = open("welpsd.time", 'w')
            wte.write(str(dt.datetime.now()))
            await ctx.send("РќРѕРІС‹Рµ РґР°РЅРЅС‹Рµ peepoAwesome")
        else:
            await ctx.send("Something")'''

    '''@commands.command(name="yaweather", aliases=["yawether", "yandexweather", "yandexwether", "СЏРїРѕРіРѕРґР°", "СЏРЅРґРµРєСЃРїРѕРіРѕРґР°", "СЏРЅРґРµРєСЃРїСѓРіРѕРґР°", "РїРђРіРѕРґР°", "СЏРїР°Рі", "СЏРїРѕРі"])
    async def yawether(self, ctx: commands.Context):
        sleep(1)
        try:
            self.loc[ctx.author.name]
        except KeyError:
            await ctx.send("Локация не устоновлена! Установи ее при помощи *setloc <локация(на английском) BASED )> и повтори попытку!")
            return
        contentL = self.msgs[len(self.msgs)-1].content.split()[1:]
        contentL.reverse()
        try: contentL[0]
        except IndexError: contentL.append("now")
        if contentL[0] == "now" or contentL[0] == "url" or contentL[0] == "next" or contentL[0] == "predict" or contentL[0] == "prediction" or contentL[0] == "help" or contentL[0] == "forecast" or contentL[0] == "all":
            a = open("welpsd.time", 'r').read()
            c = dt.datetime(int(a.split()[0].split('-')[0]), int(a.split()[0].split('-')[1]), int(a.split()[0].split('-')[2]), int(a.split()[1].split(':')[0]), int(a.split()[1].split(':')[1]), int(a.split()[1].split('.')[0].split(':')[2]))
            if True: #int((dt.datetime.now() - c).total_seconds()) > 1800:
                wth = req.get("https://api.weather.yandex.ru/v2/informers?", headers={'X-Yandex-API-Key': api_weather_ya}, params={'lat': "55.755863", 'lon': "37.6177"}).json()
                wff = open("weather.POOOG", 'w')
                json.dump(wth, wff)
                wff.close()
                wte = open("welpsd.time", 'w')
                te = str(dt.datetime.now())
                wte.write(str(dt.datetime.now()))
                #await ctx.send("РќРѕРІС‹Рµ РґР°РЅРЅС‹Рµ peepoAwesome")
                #sleep(1)
            else:
                te = open('welpsd.time', 'r').read()
            wff = open("weather.POOOG", 'r')
            wth = json.load(wff)
            icon_smile = based_smiles[wth['fact']['condition']]
            await ctx.send(f"РџРѕ РґР°РЅРЅС‹Рј СЏРЅРґРµРєСЃ.РїРѕРіРѕРґС‹ ({self.loc[ctx.author.name]['city']}): | {icon_smile} Jebaited {based_sit[wth['fact']['condition']]} | РўРµРјРїРµСЂР°С‚СѓСЂР°: {wth['fact']['temp']} C | Р§СѓРІСЃС‚РІСѓРµС‚: {wth['fact']['feels_like']} C | Р’РµС‚РµСЂ РµР±Р°С€РёС‚: {wth['fact']['wind_speed']} Рј/СЃ | Р•Р±Р°С€РёС‚ РґРѕ: {wth['fact']['wind_gust']} Рј/СЃ | Р”Р°РІР»РµРЅРёРµ: {wth['fact']['pressure_mm']} РјРј СЂ. СЃ. | Р’Р»Р°Р¶РЅРѕСЃС‚СЊ: {wth['fact']['humidity']}%")
            #await self.more500send(ctx, str(wth))
        else:
            await ctx.send("Р’РІРµРґРµРЅ РЅРµ РїСЂР°РІРёР»СЊРЅС‹Р№ РїР°СЂР°РјРµС‚СЂ. Р’РІРµРґРё *yaweather help РґР»СЏ РїСЂРѕСЃРјРѕС‚СЂР° РІСЃРµС… РїР°СЂР°РјРµС‚СЂРѕРІ stare")'''
        

    '''@commands.command(name="weather")
    async def weather(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            print(req.get("https://api.openweathermap.org/data/2.5/weather?", params={'lat': "55.755863", 'lon': "37.6177", 'appid': api_weather_op}))
            await ctx.send(str(req.get("https://api.openweathermap.org/data/2.5/weather?", params={'lat': "55.755863", 'lon': "37.6177", 'appid': api_weather_op})))
        else:
            await ctx.send("Something")'''

    @commands.command(name="clck")
    async def clck(self, ctx: commands.Context):
        content = str0list0split(ctx.message.content, listcut=(0, 0)).str
        await ctx.send(f"Ссылка сокращена 👉  {req.get('https://clck.ru/--', params={'url': content}).text[:400]}")

    '''@commands.command(name="yesno")
    async def belike(self, ctx: commands.Context):
        resp = req.get("https://yesno.wtf/api")
        await ctx.send(resp.json()['answer'])'''

    '''@commands.command(name="advice", aliases=["СЃРѕРІРµС‚"])
    async def advice(self, ctx: commands.Context):
        nlpcl = nlp.Client("nllb-200-3-3b", "a03b223190a92e7198a9d8cc6d575d0406266700")
        resp1 = req.get("https://api.adviceslip.com/advice")
        resp2 = nlpcl.translation(resp1.json()['slip']['advice'], 'eng_Latn', 'rus_Cyrl')   
        await ctx.send(f"{resp2['translation_text']}")'''

    '''@commands.command(name="img")
    async def img(self, ctx: commands.Context):
        contentL = self.msgs[len(self.msgs)-1].content.split()[1:]
        contentL.reverse()
        content = ''
        for i in range(len(contentL)):
            content += contentL.pop()
            content += ' '
        await ctx.send("PauseChamp ppCircle ... ")
        nlpcl = nlp.Client("stable-diffusion", "a03b223190a92e7198a9d8cc6d575d0406266700", True)
        try: resp1 = nlpcl.image_generation(content)
        except Exception:
            await ctx.send("РўС‹ РґРѕСЃС‚РёРі Р»РёРјРёС‚Р° (1С‡)")
            return
        urllib.request.urlretrieve(resp1['url'], "img.png")
        a = subprocess.run('curl "https://gachi.gay/api/upload" -F "file=@/Users/pbrag/AppData/Local/Programs/Python/Python311/ppSpinTheBot/img.png"', stdout=subprocess.PIPE)
        out = str(a.stdout)
        out = out[2:len(out)-1]
        await ctx.send(ast.literal_eval(out)['link'])'''
        
    '''@commands.command(name="restore")
    async def restore(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            await self.start()
            await ctx.send("Р’СЃРµ РєР°РЅР°Р»С‹ СЃР±СЂРѕС€РµРЅС‹")
        else:
            await ctx.send("Something")'''

    '''@commands.command(name="chadd")
    async def chadd(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            contentL = self.msgs[len(self.msgs)-1].content.split()[1:]
            contentL.reverse()
            content = ''
            for i in range(len(contentL)):
                content += contentL.pop()
                content += ' '
            await self.join_channels(["feelsdyslexiaman"])
            await ctx.send(f"РџРѕРґРєР»СЋС‡Р°СЋСЃСЊ Рє {content}, СЃРѕРѕР±С‰РµРЅРёРµ Рѕ РїРѕРґРєР»СЋС‡РµРЅРёРё РїСЂРёРґРµС‚ РІ РєРѕРЅСЃРѕР»СЊ stare")
        else:
            await ctx.send("Something")'''

    '''async def event_channel_join(self, channel):
        print(f"\nРџРѕРґРєР»СЋС‡РёР»СЃСЏ Рє {channel}")'''

    async def more500send(self, ctx, objstr: str, start=str(), end=str(), delay = 0):
        obj = str0list0split(objstr)
        print(obj.list[0])
        while len(obj.str) > 500 - len(start) - len(end):
            ind = 0
            i = 0
            thsind = 0
            while ind < 490 - len(start) - len(end):
                ind += len(obj.list[i]) + 1
                thsind = len(obj.list[i]) + 1
                i += 1
            ind -= thsind
            await ctx.send(start + ' ' + obj.str[:ind] + ' ' + end)
            await asyncio.sleep(delay)
            obj.strcut(ind, len(obj.str))
        await ctx.send(start + ' ' + obj.str + ' ' + end)


    '''@commands.command(name="bl")
    async def bl(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            await self.more500send(ctx, """Р’РѕС‚ РІР°Рј СЏСЂРєРёР№ РїСЂРёРјРµСЂ СЃРѕРІСЂРµРјРµРЅРЅС‹С… С‚РµРЅРґРµРЅС†РёР№ вЂ” РЅР°С‡Р°Р»Рѕ РїРѕРІСЃРµРґРЅРµРІРЅРѕР№ СЂР°Р±РѕС‚С‹ РїРѕ С„РѕСЂРјРёСЂРѕРІР°РЅРёСЋ РїРѕР·РёС†РёРё, Р° С‚Р°РєР¶Рµ СЃРІРµР¶РёР№ РІР·РіР»СЏРґ РЅР° РїСЂРёРІС‹С‡РЅС‹Рµ РІРµС‰Рё вЂ” Р±РµР·СѓСЃР»РѕРІРЅРѕ РѕС‚РєСЂС‹РІР°РµС‚ РЅРѕРІС‹Рµ РіРѕСЂРёР·РѕРЅС‚С‹ РґР»СЏ РїРѕР·РёС†РёР№, Р·Р°РЅРёРјР°РµРјС‹С… СѓС‡Р°СЃС‚РЅРёРєР°РјРё РІ РѕС‚РЅРѕС€РµРЅРёРё РїРѕСЃС‚Р°РІР»РµРЅРЅС‹С… Р·Р°РґР°С‡. РЎР»РѕР¶РЅРѕ СЃРєР°Р·Р°С‚СЊ, РїРѕС‡РµРјСѓ РёРЅС‚РµСЂР°РєС‚РёРІРЅС‹Рµ РїСЂРѕС‚РѕС‚РёРїС‹ РјРѕРіСѓС‚ Р±С‹С‚СЊ Р°СЃСЃРѕС†РёР°С‚РёРІРЅРѕ СЂР°СЃРїСЂРµРґРµР»РµРЅС‹ РїРѕ РѕС‚СЂР°СЃР»СЏРј. РЇРІР»СЏСЏСЃСЊ РІСЃРµРіРѕ Р»РёС€СЊ С‡Р°СЃС‚СЊСЋ РѕР±С‰РµР№ РєР°СЂС‚РёРЅС‹, СЏРІРЅС‹Рµ РїСЂРёР·РЅР°РєРё РїРѕР±РµРґС‹ РёРЅСЃС‚РёС‚СѓС†РёРѕРЅР°Р»РёР·Р°С†РёРё РїСЂРµРґСЃС‚Р°РІР»РµРЅС‹ РІ РёСЃРєР»СЋС‡РёС‚РµР»СЊРЅРѕ РїРѕР»РѕР¶РёС‚РµР»СЊРЅРѕРј СЃРІРµС‚Рµ. Р‘Р°РЅР°Р»СЊРЅС‹Рµ, РЅРѕ РЅРµРѕРїСЂРѕРІРµСЂР¶РёРјС‹Рµ РІС‹РІРѕРґС‹, Р° С‚Р°РєР¶Рµ РёРЅС‚РµСЂР°РєС‚РёРІРЅС‹Рµ РїСЂРѕС‚РѕС‚РёРїС‹ РЅР°Р±РёСЂР°СЋС‚ РїРѕРїСѓР»СЏСЂРЅРѕСЃС‚СЊ СЃСЂРµРґРё РѕРїСЂРµРґРµР»РµРЅРЅС‹С… СЃР»РѕРµРІ РЅР°СЃРµР»РµРЅРёСЏ, Р° Р·РЅР°С‡РёС‚, РґРѕР»Р¶РЅС‹ Р±С‹С‚СЊ РїСЂРёР·РІР°РЅС‹ Рє РѕС‚РІРµС‚Сѓ. РЇСЃРЅРѕСЃС‚СЊ РЅР°С€РµР№ РїРѕР·РёС†РёРё РѕС‡РµРІРёРґРЅР°: РєСѓСЂСЃ РЅР° СЃРѕС†РёР°Р»СЊРЅРѕ-РѕСЂРёРµРЅС‚РёСЂРѕРІР°РЅРЅС‹Р№ РЅР°С†РёРѕРЅР°Р»СЊРЅС‹Р№ РїСЂРѕРµРєС‚ РѕРґРЅРѕР·РЅР°С‡РЅРѕ РѕРїСЂРµРґРµР»СЏРµС‚ РєР°Р¶РґРѕРіРѕ СѓС‡Р°СЃС‚РЅРёРєР° РєР°Рє СЃРїРѕСЃРѕР±РЅРѕРіРѕ РїСЂРёРЅРёРјР°С‚СЊ СЃРѕР±СЃС‚РІРµРЅРЅС‹Рµ СЂРµС€РµРЅРёСЏ РєР°СЃР°РµРјРѕ РЅРѕРІС‹С… РїСЂРµРґР»РѕР¶РµРЅРёР№. Р—Р°РґР°С‡Р° РѕСЂРіР°РЅРёР·Р°С†РёРё, РІ РѕСЃРѕР±РµРЅРЅРѕСЃС‚Рё Р¶Рµ РїРµСЂСЃРїРµРєС‚РёРІРЅРѕРµ РїР»Р°РЅРёСЂРѕРІР°РЅРёРµ РѕР±РµСЃРїРµС‡РёРІР°РµС‚ С€РёСЂРѕРєРѕРјСѓ РєСЂСѓРіСѓ (СЃРїРµС†РёР°Р»РёСЃС‚РѕРІ) СѓС‡Р°СЃС‚РёРµ РІ С„РѕСЂРјРёСЂРѕРІР°РЅРёРё РїРµСЂРІРѕРѕС‡РµСЂРµРґРЅС‹С… С‚СЂРµР±РѕРІР°РЅРёР№. Р РЅРµС‚ СЃРѕРјРЅРµРЅРёР№, С‡С‚Рѕ СЂРµРїР»РёС†РёСЂРѕРІР°РЅРЅС‹Рµ СЃ Р·Р°СЂСѓР±РµР¶РЅС‹С… РёСЃС‚РѕС‡РЅРёРєРѕРІ, СЃРѕРІСЂРµРјРµРЅРЅС‹Рµ РёСЃСЃР»РµРґРѕРІР°РЅРёСЏ РїСЂРµРґСЃС‚Р°РІР»СЏСЋС‚ СЃРѕР±РѕР№ РЅРµ С‡С‚Рѕ РёРЅРѕРµ, РєР°Рє РєРІРёРЅС‚СЌСЃСЃРµРЅС†РёСЋ РїРѕР±РµРґС‹ РјР°СЂРєРµС‚РёРЅРіР° РЅР°Рґ СЂР°Р·СѓРјРѕРј Рё РґРѕР»Р¶РЅС‹ Р±С‹С‚СЊ СЃРјРµС€Р°РЅС‹ СЃ РЅРµ СѓРЅРёРєР°Р»СЊРЅС‹РјРё РґР°РЅРЅС‹РјРё РґРѕ СЃС‚РµРїРµРЅРё СЃРѕРІРµСЂС€РµРЅРЅРѕР№ РЅРµСѓР·РЅР°РІР°РµРјРѕСЃС‚Рё, РёР·-Р·Р° С‡РµРіРѕ РІРѕР·СЂР°СЃС‚Р°РµС‚ РёС… СЃС‚Р°С‚СѓСЃ Р±РµСЃРїРѕР»РµР·РЅРѕСЃС‚Рё. Р”Р»СЏ СЃРѕРІСЂРµРјРµРЅРЅРѕРіРѕ РјРёСЂР° СЃРїР»РѕС‡С‘РЅРЅРѕСЃС‚СЊ РєРѕРјР°РЅРґС‹ РїСЂРѕС„РµСЃСЃРёРѕРЅР°Р»РѕРІ РёРіСЂР°РµС‚ РІР°Р¶РЅСѓСЋ СЂРѕР»СЊ РІ С„РѕСЂРјРёСЂРѕРІР°РЅРёРё РЅРѕРІС‹С… РїСЂРµРґР»РѕР¶РµРЅРёР№.""",\
                              start = "xd", end = "peepoSnow")
        else:
            await ctx.send("Something")'''

    '''@commands.command(name="eventset")
    async def eventset(self, ctx: commands.Context):
        if self.modCheck(ctx.author.name):
            self.eventctx = ctx
        else:
            await ctx.send("Something")'''

    @commands.command(name="autosr", aliases=['a'])
    async def autosr(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            await asyncio.sleep(1)
            #await ctx.send("РђРІС‚Рѕ СЃСЂ РїСЂРѕРёСЃС…РѕРґРёС‚ ppHop")
            await asyncio.sleep(1)
            listsr = ["https://youtu.be/DGDWb1IkEGs", "https://youtu.be/sVx1mJDeUjY", "https://youtu.be/9FSVPnVLUUQ", "https://youtu.be/_dA85TulgmI", "https://youtu.be/5FzbYVSOsY8", "https://youtu.be/vJe7diwiyHc", "https://youtu.be/UShhxwD5hi0", "https://youtu.be/qslNFQ2CeZY", "https://youtu.be/AROZspDa_tQ", "https://youtu.be/w8KQmps-Sog", "https://youtu.be/sxF9PGRiabw", "https://youtu.be/UYRdtfo5Ix0", "https://youtu.be/91GTuZWCQmY", "https://youtu.be/c69eHlQrKaY"]
            for i in range(len(listsr)):
                #print(listsr[i])
                await self.more500send(ctx, f"!sr {listsr[i]}")
                if i != len(listsr)-1: await asyncio.sleep(125)
            await asyncio.sleep(5)
            #await ctx.send("РђРІС‚Рѕ СЃСЂ Р·Р°РєРѕРЅС‡РµРЅ! stare рџ‘Ќ ")
        else:
            await ctx.send("Something")


    @commands.command(name="dalle")
    async def dalle(self, ctx: commands.Context):
        #if ctx.author.name == "poal48":
        if True:
            contentL = self.msgs[len(self.msgs)-1].content.split()[1:]
            contentL.reverse()
            try: contentL.remove("dalle")
            except Exception: pass
            content = ''
            for i in range(len(contentL)):
                content += contentL.pop()
                content += ' '
        #print("РќР°С‡Р°Р»Рѕ РіРµРЅРµСЂРёСЂРѕРІР°РЅРёСЏ")
        await ctx.send("Генерирую... pwgoodPooping ppCircle")
        asd = await oai.Image.acreate(prompt=content, n=6, size = "512x512")
        urllib.request.urlretrieve(asd['data'][0]['url'], "img.png")
        img = cv.imread("asd.png")
        _img = cv.imread("img.png")
        #print("РќР°С‡РёРЅР°СЋ РєРѕРїРёСЂРѕРІР°С‚СЊ РїРµСЂРІРѕРµ РёР·РѕР±СЂР°Р¶РµРЅРёРµ...")
        img[0:511, 0:511] = _img[0:511, 0:511]
        urllib.request.urlretrieve(asd['data'][1]['url'], "img.png")
        _img = cv.imread("img.png")
        img[0:511, 512:1023] = _img[0:511, 0:511]
        urllib.request.urlretrieve(asd['data'][2]['url'], "img.png")
        _img = cv.imread("img.png")
        img[0:511, 1024:1535] = _img[0:511, 0:511]
        urllib.request.urlretrieve(asd['data'][3]['url'], "img.png")
        _img = cv.imread("img.png")
        img[512:1023, 0:511] = _img[0:511, 0:511]
        urllib.request.urlretrieve(asd['data'][4]['url'], "img.png")
        _img = cv.imread("img.png")
        img[512:1023, 512:1023] = _img[0:511, 0:511]
        urllib.request.urlretrieve(asd['data'][5]['url'], "img.png")
        _img = cv.imread("img.png")
        img[512:1023, 1024:1535] = _img[0:511, 0:511]
        cv.imwrite("_img.png", img)
        #print("Р“Р°С‡Рё РіРµР№РёРЅРі...")
        a = req.post("https://gachi.gay/api/upload", files={'file': open("_img.png", 'rb')})
        #out = str(a.stdout)
        #out = out[2:len(out)-1]
        #print("Р“РѕС‚РѕРІРѕ")
        await ctx.reply(ast.literal_eval(a.text)['link'])
            
        

    @commands.command(name="JABA")
    async def jaba(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            httpi = tio.http.TwitchHTTP(self, api_token = CFG['api_token_ppSpin'])
            pu = PartialUser(httpi, 489926403, 'red3xtop')
            await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, "JABA TeaTime", color="orange")
        else:
            await ctx.send("Something")

    '''@commands.command(name="write"   )
    async def write(self, ctx: commands.Context):
        sleep(1)
        contentL = self.msgs[len(self.msgs)-1].content.split()[1:]
        contentL.reverse()
        content = ''
        for i in range(len(contentL)):
            content += contentL.pop()
            content += ' '
        if ';' in content:
            await ctx.send("РЅРµ РјРѕРіСѓ Р·Р°РїРёСЃР°С‚СЊ РІ СЃРїРёСЃРѕРє! pwgoodG")
            return
        peepoRead = open("peepoList.peepo", 'r').read()
        peepoWrite = open("peepoList.peepo", 'w')
        peepoWrite.write(peepoRead + f"; {content}")
        peepoWrite.close()
        widepeepoRead = open("widepeepoList.widepeepo", 'r').read()
        widepeepoWrite = open("widepeepoList.widepeepo", 'w')
        widepeepoWrite.write(widepeepoRead + f"\n{ctx.author.name}: {content}")
        widepeepoWrite.close()
        await ctx.send(f'Р—Р°РїРёСЃР°Р» "{content}" РІ СЃРїРёСЃРѕРє! DankG')

    @commands.command(name="read")
    async def read(self, ctx: commands.Context):
        await self.more500send(ctx, f"РЎРїРёСЃРѕРє: {open('peepoList.peepo', 'r').read()}")'''
        
    @commands.command(name="Fridge")
    async def fridge(self, ctx: commands.Context):
        await ctx.send("ВОРУЮ ИЗ ТВОЕГО Fridge")
        await asyncio.sleep(10)
        await ctx.send("СВОРОВАЛ SOLE ИЗ ТВОЕГО Fridge")

    @commands.command(name="YOURMOM")
    async def yourmom(self, ctx: commands.Context):
        await asyncio.sleep(1)
        await ctx.reply(choice([
		"Yo mama is so fat that her bellybutton gets home 15 minutes before she does.",
		"Yo mama is so fat that when she was diagnosed with a flesh-eating disease, the doctor gave her ten years to live.",
		"Yo mama is so fat that the National Weather Service names each one of her farts.",
		"Yo mama is so fat that when she wears a yellow raincoat, people yell \"taxi!\"",
		"Yo mama is so fat and dumb that the only reason she opened her email was because she heard it contained spam.",
		"Yo mama is so fat she threw on a sheet for Halloween and went as Antarctica.",
		"Yo mama is so fat that she looked up cheat codes for Wii Fit",
		"Yo mama is so fat that the only exercise she gets is when she chases the ice cream truck.",
		"Yo mama is so fat that she sat on a dollar and squeezed a booger out George Washington's nose.",
		"Yo mama is so fat that when she gets in an elevator, it has to go down.",
		"Yo mama is so fat that when her beeper goes off, people think she's backing up.",
		"Yo mama is so fat that she has to iron her pants on the driveway.",
		"Yo mama is so fat that she left the house in high heels and came back wearing flip flops.",
		"Yo mama is so fat that people jog around her for exercise.",
		"Yo mama is so fat that she was floating in the ocean and Spain claimed her for the New World.",
		"Yo mama is so fat that when she walked in front of the TV, I missed 3 seasons of Breaking Bad.",
		"Yo mama is so fat that you have to grease the door frame and hold a twinkie on the other side just to get her through!",
		"Yo mama is so fat that that when she sits on the beach, Greenpeace shows up and tries to tow her back into the ocean...",
		"Yo mama is so fat that when she bungee jumps, she brings down the bridge too.",
		"Yo mama is so fat that when she talks to herself, itgs a long distance call.",
		"Yo mama is so fat that the last time she saw 90210, it was on a scale.",
		"Yo mama is so fat that light bends around her.",
		"Yo mama is so fat that I took a picture of her last Christmas and it's still printing!",
		"Yo mama is so fat that when she sat on Wal-Mart, she lowered the prices.",
		"Yo mama is so fat that when she sat on an iphone, it turned into an ipad.",
		"Yo mama is so fat that even god can't lift her spirit.",
		"Yo mama is so fat that she gets group insurance.",
		"Yo mama is so fat that she was zoned for commercial development.",
		"Yo mama is so fat that she walked into the Gap and filled it.",
		"Yo mama is so fat that she comes at you from all directions.",
		"Yo mama is so fat that when she climbed onto a diving board at the beach, the lifeguard told your dad \"sorry, you can't park here\".",
		"Yo mama is so fat that her cereal bowl came with a lifeguard.",
		"Yo mama is so fat that she looks like shegs smuggling a Volkswagen.",
		"Yo mama is so fat that when she got her shoes shined, she had to take the guygs word for it.",
		"Yo mama is so fat that when she sings, itgs over for everybody.",
		"Yo mama is so fat that when she ran away, they had to use all four sides of the milk carton to display her picture.",
		"Yo mama is so fat that when she was growing up she didngt play with dolls, she played with midgets.",
		"Yo mama is so fat that she uses two buses for roller-blades.",
		"Yo mama's so fat she blew up the Deathstar.",
		"Yo mama is so fat that when she goes to a buffet, she gets the group rate.",
		"Yo mama is so fat that she has to put her belt on with a boomerang.",
		"Yo mama is so fat that she broke the Stairway to Heaven.",
		"Yo mama is so fat that she doesngt eat with a fork, she eats with a forklift.",
		"Yo mama is so fat that the last time the landlord saw her, he doubled the rent.",
		"Yo mama is so fat that Weight Watchers wongt look at her.",
		"Yo mama is so fat that the highway patrol made her wear a sign saying \"Caution! Wide Turn\".",
		"Yo mama is so fat that when she sits around the house, she SITS AROUND THE HOUSE!",
		"Yo mama is so fat that when she steps on a scale, it reads \"one at a time, please\".",
		"Yo mama is so fat that she fell in love and broke it.",
		"Yo mama is so fat that when she gets on the scale it says \"We don't do livestock\".",
		"Yo mama is so fat that when she tripped on 4th Ave, she landed on 12th.",
		"Yo mama is so fat that God couldn't light the Earth until she moved!",
		"Yo mama is so fat that even Bill Gates couldn't pay for her liposuction!",
		"Yo mama is so fat that she has to pull down her pants to get into her pockets.",
		"Yo mama is so fat that she was born on the fourth, fifth, and sixth of June.",
		"Yo mama is so fat that she could fall down and wouldngt even know it.",
		"Yo mama is so fat that the sign inside one restaurant says, “Maximum occupancy: 300, or Yo momma.”",
		"Yo mama is so fat that she puts mayonnaise on aspirin.",
		"Yo mama is so fat that she was born with a silver shovel in her mouth.",
		"Yo mama is so fat that when she hauls ass, she has to make two trips.",
		"Yo mama is so fat that she had to go to Sea World to get baptized.",
		"Yo mama is so fat that her bellybuttongs got an echo.",
		"Yo mama is so fat that when she turns around people throw her a welcome back party.",
		"Yo mama is so fat that her belly button doesngt have lint, it has sweaters.",
		"Yo mama is so fat that a picture of her would fall off the wall.",
		"Yo mama is so fat that when she takes a shower, her feet dongt get wet.",
		"Yo mama is so fat that she puts on her lipstick with a paint-roller!",
		"Yo mama is so fat that she could sell shade.",
		"Yo mama is so fat that I ran around her twice and got lost.",
		"Yo mama is so fat that the shadow of her butt weighs 100 pounds.",
		"Yo mama is so fat that when shegs standing on the corner police drive by and yell, “Hey, break it up.”",
		"Yo mama is so fat that her blood type is Ragu.",
		"Yo mama is so fat that when she runs the fifty-yard dash she needs an overnight bag.",
		"Yo mama is so fat that she cangt even fit into an AOL chat room.",
		"Yo mama is so fat when she goes skydiving she doesn't use a parachute to land, she uses a twin-engine plane!",
		"Yo mama is so fat MTX audio's subwoofers couldn't rattle her bones!",
		"Yo mama is so fat her headphones are a pair of PA speakers connected to a car amplifier.",
		"Yo mama is so fat that she doesngt have a tailor, she has a contractor.",
		"Yo mama is so fat that eating contests have banned her because she is unfair competition.",
		"Yo mama is so fat that she measures 36-24-36, and the other arm is just as big.",
		"Yo mama is so fat that she gets her toenails painted at Luckygs Auto Body.",
		"Yo mama is so fat that when she goes to an amusement park, people try to ride HER!",
		"Yo mama is so fat that when she jumps up in the air she gets stuck!",
		"Yo mama is so fat that she has more Chins than a Chinese phone book!",
		"Yo mama is so fat that she influences the tides.",
		"Yo mama is so fat that when she plays hopscotch, she goes \"New York, L.A., Chicago...\"",
		"Yo mama is so fat that NASA has to orbit a satellite around her!",
		"Yo mama is so fat that when she sits on my face I can't hear the stereo.",
		"Yo mama is so fat that they have to grease the bath tub to get her out!",
		"Yo mama is so fat that she's on both sides of the family!",
		"Yo mama is so fat that at the zoo, the elephants throw HER peanuts.",
		"Yo mama is so fat you have to roll over twice to get off her.",
		"Yo mama is so fat that she sets off car alarms when she runs.",
		"Yo mama is so fat that she cant reach into her back pocket.",
		"Yo mama is so fat that she has her own gravity field.",
		"Yo mama is so fat that she stepped on a rainbow and made Skittles.",
		"Yo mama is so fat that the only pictures you have of her were taken by satellite cameras.",
		"Yo mama is so fat that when she wears a \"Malcolm X\" T-shirt, helicopters try to land on her back!",
		"Yo mama is so fat that it took Usain Bolt 3 years to run around her.",
		"Yo mama so fat that she sweats more than a dog in a chinese restaurant.",
		"Yo mama so fat, that went she stepped in the water, Thailand had to declare another tsunami warning.",
		"Yo mama is so fat that that she cant tie her own shoes.",
		"Yo mama is so fat that when she lays on the beach, people run around yelling Free Willy.",
		"Yo mama is so fat that she uses redwoods to pick her teeth",
		"Yo mama is so fat that she cut her leg and gravy poured out",
		"Yo mama is so fat that she was in the Macygs Thanksgiving Day Parade... wearing ropes.",
		"Yo mama is so fat that she went on a light diet. As soon as itgs light she starts eating.",
		"Yo mama is so fat that shegs half Italian, half Irish, and half American.",
		"Yo mama is so fat that her waist size is the Equator.",
		"Yo mama is so fat that she cant even jump to a conclusion.",
		"Yo mama is so fat that she uses a mattress for a tampon.",
		"Yo mama is so fat that when she got hit by a bus, she said, \"Who threw that rock at me?\"",
		"Yo mama is so fat that we went to the drive-in and didn't have to pay for her because we dressed her up as a Toyota.",
		"Yo mama is so fat that when she was born, she gave the hospital stretch marks.",
		"Yo mama is so fat that she was cut from the cast of E.T., because she caused an eclipse when she rode the bike across the moon.",
		"Yo mama is so fat that when you get on top of her your ears pop.",
		"Yo mama is so fat that she got hit by a car and had to go to the hospital to have it removed.",
		"Yo mama is so fat that she eats \"Wheat Thicks\".",
		"Yo mama is so fat that we're in her right now!",
		"Yo mama is so fat that she went to the movie theatre and sat next to everyone.",
		"Yo mama is so fat that she has been declared a natural habitat for condors.",
		"Yo mama is so fat that when she wants to shake someones hand, she has to give directions!",
		"Yo mama is so fat that even Dora can't explore her!",
		"Yo mama is so fat that when she gets on the scale it says \"to be continued\".",
		"Yo mama is so fat that when she goes to a resturant, she looks at the menu and says \"okay!\"",
		"Yo mama is so fat that even Chuck Norris couldn't run around her.",
		"Yo mama is so fat that her neck looks like a dozen hot dogs!",
		"Yo mama is so fat that when she bungee jumps she goes straight to hell!",
		"Yo mama is so fat that she's got her own area code!",
		"Yo mama is so fat that she looks like she's smuggling a Volkswagon!",
		"Yo mama is so fat that she has to buy three airline tickets.",
		"Yo mama is so fat that whenever she goes to the beach the tide comes in!",
		"Yo mama is so fat that she's got Amtrak written on her leg.",
		"Yo mama is so fat that her legs are like spoiled milk - white & chunky!",
		"Yo mama is so fat that I had to take a train and two buses just to get on the her good side!",
		"Yo mama is so fat that she wakes up in sections!",
		"Yo mama so fat, all she wants for Christmas is to see her feet.",
		"Yo mama is so fat that when she lies on the beach no one else gets any sun!",
		"Yo mama is so fat that that her senior pictures had to be taken from a helicopter!",
		"Yo mama is so fat that everytime she walks in high heels, she strikes oil!",
		"Yo mama is so fat that she fell and created the Grand Canyon!",
		"Yo mama is so fat that her butt drags on the ground and kids yell - \"there goes santa claus with his bag of toys!\"",
		"Yo mama is so fat that even her clothes have stretch marks!",
		"Yo mama is so fat that she has to use a VCR as a beeper!",
		"Yo mama is so fat that when she asked for a waterbed, they put a blanket over the ocean!",
		"Yo mama is so fat that she got hit by a parked car!",
		"Yo mama is so fat that they use the elastic in her underwear for bungee jumping.",
		"Yo mama is so fat that when we were playing Call of Duty, I got a 20 kill streak for killing her.",
		"Yo mama is so fat that Dracula got Type 2 Diabetes after biting her neck.",
		"Yo mama is so fat that when she visited Toronto's City Hall, she was arrested for attempting to smuggle 500 lbs of crack into Mayor Rob Ford's office.",
		"Yo mama is so fat that when she fell over she rocked herself asleep trying to get up again.",
		"Yo mama is so fat that that when I tried to drive around her I ran out of gas.",
		"Yo mama is so fat that when she went to church and sat on a bible, Jesus came out and said \"LET MY PEOPLE GO!\"",
		"Yo mama is so fat that when she dances at a concert the whole band skips.",
		"Yo mama is so fat that she stands in two time zones.",
		"Yo mama is so fat that she went to the fair and the kids thought she was a bouncy castle.",
		"Yo mama is so fat that when she goes to an all you can eat buffet, they have to install speed bumps.",
		"Yo mama is so fat that the camera TAKES AWAY 10 lbs from her appearance.",
		"Yo mama is so fat that her sedan can fit 5 people... or just yo mama with the front seats removed.",
		"Yo mama is so fat that when she went to seaworld the whales started singing \"We Are Family\".",
		"Yo mama is so fat that she fell out of both sides of her bed.",
		"Yo mama is so fat that the stripes on her pajamas never end.",
		"Yo mama is so fat, Al Gore accuses her of global warning everytime she farts!",
		"Yo mama is so fat that she's got every caterer in the city on speed dial!",
		"Yo mama's so fat that when she goes on a scale, it shows her own phone number.",
		"Yo mama's so fat that she doesn't need the internet - she's worldwide.",
		"Yo mama's so fat that when she goes on a scale, it reads \"lose some weight\".",
		"Yo mama's so fat that she doesn't get dreams, she gets movies!",
		"Yo mama's so fat that when she walks, she changes the earth's rotation!",
		"Yo mama is so fat that she uses the entire country of Mexico as her tanning bed.",
		"Yo mama is so ugly that when she went to a beautician it took 12 hours... to get a quote!",
		"Yo mama is so ugly that she looked out the window and got arrested for mooning.",
		"Yo mama is so ugly that people go as her for Halloween.",
		"Yo mama is so ugly that she turned Medusa to stone!",
		"Yo mama is so ugly that the government moved Halloween to her birthday!",
		"Yo mama is so ugly that she scares the roaches away.",
		"Yo mama is so ugly that she scared the crap out of the toilet.",
		"Yo mama is so ugly that... well... look at you!",
		"Yo mama is so ugly that when she looks in the mirror, the reflection looks back and shakes its head.",
		"Yo mama is so ugly that she looks like she's been in a dryer filled with rocks.",
		"Yo mama is so ugly that she makes blind children cry.",
		"Yo mama is so ugly that she climbed the ugly ladder and didn't miss a step.",
		"Yo mama is so ugly that the last time I saw something that looked like her, I pinned a tail on it.",
		"Yo mama is so ugly that we put her in the kennel when we go on vacation.",
		"Yo mama is so ugly that her shadow ran away from her.",
		"Yo mama is so ugly that she could scare the flies off a shit wagon.",
		"Yo mama is so ugly that her birth certificate contained an apology letter from the condom factory.",
		"Yo mama is so ugly that that your father takes her to work with him so that he doesn't have to kiss her goodbye.",
		"Yo mama is so ugly that she tried to take a bath and the water jumped out!",
		"Yo mama is so ugly that when she walks down the street in September, people say \"Wow, is it Halloween already?\"",
		"Yo mama is so ugly that her mom had to be drunk to breast feed her.",
		"Yo mama is so ugly that when she walks into a bank, they turn off the surveillence cameras.",
		"Yo mama is so ugly that they didn't give her a costume when she auditioned for Star Wars.",
		"Yo mama is so ugly that even Rice Krispies won't talk to her!",
		"Yo mama is so ugly that when she uploaded a photo of herself to a computer, it was rejected by the anti-virus software.",
		"Yo mama is so ugly that when she joined an ugly contest, they said \"Sorry, no professionals.\"",
		"Yo mama is so ugly that she could make a freight train take a dirt road.",
		"Yo mama is so ugly that when she drove past area 51, she was thought to be extraterrestrial life. They took her away never to be seen again.",
		"Yo mama is so ugly that they pay her to put her clothes on in strip joints",
		"Yo mama is so ugly that you have to tie a steak around her neck so the dog will play with her!",
		"Yo mama is so ugly that she made an onion cry!",
		"Yo mama is so ugly that when I last saw a mouth like hers, it had a hook in it.",
		"Yo mama is so ugly that she gets 364 extra days to dress up for Halloween!",
		"Yo mama is so ugly that when she plays Mortal Kombat, Scorpion tells her to \"Stay Over There!\"",
		"Yo mama is so ugly that neither Jacob nor Edward want her on their team.",
		"Yo mama is so ugly that they push her face into dough to make gorilla cookies.",
		"Yo mama is so ugly that when she goes to the therapist, he makes her lie on the couch face down.",
		"Yo mama is so ugly that she gives Freddy Kreuger nightmares.",
		"Yo mama is so ugly that when she walks in the kitchen, the rats jump on the table and start screaming.",
		"Yo mama is so ugly that even Bill Clinton wouldn't sleep with her.",
		"Yo mama is so ugly that when she was born, the doctor slapped her AND her parents!",
		"Yo mama is so ugly that she didn't get hit with the ugly stick, she got hit by the whole damn tree.",
		"Yo mama is so ugly that she has 7 years bad luck just trying to look at herself in the mirror.",
		"Yo mama is so ugly that she practices birth control by leaving the lights on.",
		"Yo mama is so ugly that she threw a boomerang and it wouldn't even come back.",
		"Yo mama is so ugly that she'd scare the monster out of Loch Ness.",
		"Yo mama is so ugly that it looks like she's been bobbing for french fries.",
		"Yo mama is so ugly that her pillow cries at night.",
		"Yo mama is so ugly that people at the circus pay money not to see her.",
		"Yo mama is so ugly that when she looks in the mirror it says \"viewer discretion is advised.\"",
		"Yo mama is so ugly that she can look up a camel's butt and scare the hump off of it.",
		"Yo mama is so ugly that when she moved into the projects, all her neighbors chipped in for curtains.",
		"Yo mama is so ugly that Santa pays an elf to drop off her gifts at Christmas.",
		"Yo mama is so ugly that people hang her picture in their cars so their radios don't get stolen.",
		"Yo mama is so ugly that I took her to a haunted house and she came out with a job application.",
		"Yo mama is so ugly that if she was a scarecrow, the corn would run away.",
		"Yo mama is so ugly that she could be the poster child for birth control.",
		"Yo mama is so ugly that I took her to the zoo, guy at the door said \"\"",
		"Yo mama is so ugly that when she went to a beautician it took 12 hours... to get a quote!",
		"Yo mama is so ugly that she looked out the window and got arrested for mooning.",
		"Yo mama is so ugly that people go as her for Halloween.",
		"Yo mama is so ugly that she turned Medusa to stone!",
		"Yo mama is so ugly that the government moved Halloween to her birthday!",
		"Yo mama is so ugly that she scares the roaches away.",
		"Yo mama is so ugly that she scared the crap out of the toilet.",
		"Yo mama is so ugly that... well... look at you!",
		"Yo mama is so ugly that when she looks in the mirror, the reflection looks back and shakes its head.",
		"Yo mama is so ugly that she looks like she's been in a dryer filled with rocks.",
		"Yo mama is so ugly that she makes blind children cry.",
		"Yo mama is so ugly that she climbed the ugly ladder and didn't miss a step.",
		"Yo mama is so ugly that the last time I saw something that looked like her, I pinned a tail on it.",
		"Yo mama is so ugly that we put her in the kennel when we go on vacation.",
		"Yo mama is so ugly that her shadow ran away from her.",
		"Yo mama is so ugly that she could scare the flies off a shit wagon.",
		"Yo mama is so ugly that her birth certificate contained an apology letter from the condom factory.",
		"Yo mama is so ugly that that your father takes her to work with him so that he doesn't have to kiss her goodbye.",
		"Yo mama is so ugly that she tried to take a bath and the water jumped out!",
		"Yo mama is so ugly that when she walks down the street in September, people say \"Wow, is it Halloween already?\"",
		"Yo mama is so ugly that her mom had to be drunk to breast feed her.",
		"Yo mama is so ugly that when she walks into a bank, they turn off the surveillence cameras.",
		"Yo mama is so ugly that they didn't give her a costume when she auditioned for Star Wars.",
		"Yo mama is so ugly that even Rice Krispies won't talk to her!",
		"Yo mama is so ugly that when she uploaded a photo of herself to a computer, it was rejected by the anti-virus software.",
		"Yo mama is so ugly that when she joined an ugly contest, they said \"Sorry, no professionals.\"",
		"Yo mama is so ugly that she could make a freight train take a dirt road.",
		"Yo mama is so ugly that that when she sits in the sand on the beach, cats try to bury her.",
		"Yo mama is so ugly that when she drove past area 51, she was thought to be extraterrestrial life. They took her away never to be seen again.",
		"Yo mama is so ugly that they pay her to put her clothes on in strip joints",
		"Yo mama is so ugly that you have to tie a steak around her neck so the dog will play with her!",
		"Yo mama is so ugly that she made an onion cry!",
		"Yo mama is so ugly that when I last saw a mouth like hers, it had a hook in it.",
		"Yo mama is so ugly that she gets 364 extra days to dress up for Halloween!",
		"Yo mama is so ugly that when she plays Mortal Kombat, Scorpion tells her to \"Stay Over There!\"",
		"Yo mama is so ugly that neither Jacob nor Edward want her on their team.",
		"Yo mama is so ugly that they push her face into dough to make gorilla cookies.",
		"Yo mama is so ugly that when she goes to the therapist, he makes her lie on the couch face down.",
		"Yo mama is so ugly that she gives Freddy Kreuger nightmares.",
		"Yo mama is so ugly that when she walks in the kitchen, the rats jump on the table and start screaming.",
		"Yo mama is so ugly that even Bill Clinton wouldn't sleep with her.",
		"Yo mama is so ugly that when she was born, the doctor slapped her AND her parents!",
		"Yo mama is so ugly that she didn't get hit with the ugly stick, she got hit by the whole damn tree.",
		"Yo mama is so ugly that she has 7 years bad luck just trying to look at herself in the mirror.",
		"Yo mama is so ugly that she practices birth control by leaving the lights on.",
		"Yo mama is so ugly that she threw a boomerang and it wouldn't even come back.",
		"Yo mama is so ugly that she'd scare the monster out of Loch Ness.",
		"Yo mama is so ugly that it looks like she's been bobbing for french fries.",
		"Yo mama is so ugly that her pillow cries at night.",
		"Yo mama is so ugly that people at the circus pay money not to see her.",
		"Yo mama is so ugly that when she looks in the mirror it says \"viewer discretion is advised.\"",
		"Yo mama is so ugly that she can look up a camel's butt and scare the hump off of it.",
		"Yo mama is so ugly that when she moved into the projects, all her neighbors chipped in for curtains.",
		"Yo mama is so ugly that Santa pays an elf to drop off her gifts at Christmas.",
		"Yo mama is so ugly that people hang her picture in their cars so their radios don't get stolen.",
		"Yo mama is so ugly that I took her to a haunted house and she came out with a job application.",
		"Yo mama is so ugly that if she was a scarecrow, the corn would run away.",
		"Yo mama is so ugly that she could be the poster child for birth control.",
		"Yo mama is so ugly that I took her to the zoo, guy at the door said \"Thanks for bringing her back.\"",
		"Yo mama is so ugly that when she went to Taco Bell everyone ran for the border.",
		"Yo mama is so ugly that her face is blurred on her driver's license.",
		"Yo mama is so ugly that when she walked out of her house, the neighbours called animal control.",
		"Yo mama is so ugly that the FCC requires her face to be blurred when she's on TV, because of decency rules.",
		"Yo mama is so ugly that a sculpture of her face is used when torturing prisoners at Guantanamo Bay.",
		"Yo mama is so ugly that government intelligence agencies have to pixelize her face when spying on her.",
		"Yo mama is so ugly that she's never seen herself 'cause the mirrors keep breaking.",
		"Yo mama is so ugly that it looks like someone did the stanky leg dance on her face.",
		"Yo mama is so ugly that when she was born she was put in an incubator with tinted windows.",
		"Yo mama is so ugly that she put the Boogie Man out of business!",
		"Yo mama is so ugly that she made Barack Obama lose hope!",
		"Yo mama was such an ugly baby that her parents had to feed her with a slingshot.",
		"Yo mama is like a hockey player, she only showers after three periods.",
		"Yo mama is like a chicken coop, cocks fly in and out all day.",
		"Yo mama has so many teeth missing, that it looks like her tongue is in jail.",
		"Yo mama's mouth is so big that she speaks in surround sound.",
		"Yo mama is so grouchy that the McDonalds she works in doesn't even serve Happy Meals.",
		"You suck... yo mama does too, but she charges.",
		"Yo mama is like a paper towel, she picks up all kinds of slimy wet stuff.",
		"Yo mama is like Bazooka Joe, 5 cents a blow.",
		"Yo mama is like a telephone, even a 3 year old can pick her up.",
		"Yo mama is like a Christmas tree, everybody hangs balls on her.",
		"Yo mama is like the sun, look at her too long and you'll go blind.",
		"Yo mama is like a library, she's open to the public.",
		"Yo mama is like a fine restaurant, she only takes deliveries in the rear.",
		"Yo mama is like an ATM, open 24 hours.",
		"Yo mama is like a bowling ball... round, heavy, and you can fit three fingers in.",
		"Yo mama is like a basketball hoop, everybody gets a shot.",
		"Yo mama is like a Discover card, she gives cash back.",
		"Yo mama is like a championship ring, everybody puts a finger in her.",
		"Yo mama is like Dominoes Pizza, one call does it all.",
		"Yo mama is like a microwave, press one button and she's hot.",
		"Yo mama is like a mail box, open day and night.",
		"Yo mama is like a bowling ball, she always winds up in the gutter.",
		"Yo mama is like a bus, guys climb on and off her all day long.",
		"Yo mama is like a door knob, everybody gets a turn.",
		"Yo mama is like a light switch, even a little kid can turn her on.",
		"Yo mama's such a ho that \"who's your daddy?\" is a multiple-choice question.",
		"You'll never be the man Yo mama was.",
		"Yo mama... 'nuff said.",
		"Yo mama is so lazy that she thinks a two-income family is where yo daddy has two jobs.",
		"Yo mama is so lazy that she's got a remote control just to operate her remote!",
		"Yo mama's arms are so short that she has to tilt her head to scratch her ear.",
		"Yo mama's lips are so big that Chapstick had to invent a spray.",
		"Yo mama is so lazy that she came in last place in a recent snail marathon.",
		"What's the difference between yo momma and a walrus? One has whiskers and smells of fish... the other one is a walrus!",
		"Yo mama is missing a finger and can't count past nine.",
		"Yo mama is so flat that she makes the walls jealous!",
		"Yo mama's gums are so black that she spits Yoo-hoo.",
		"It took yo mama 10 tries to get her drivers license - she couldn't get used to the front seat!",
		"Yo mama's so fat that when she asked me \"what's up?\" I said \"your weight!\"",
		"Yo mama is twice the man you are.",
		"Yo mama is cross-eyed and watches TV in stereo.",
		"Yo mama is so stupid that she was born on Independence Day and can't remember her birthday.",
		"Yo mama's head is so small that she uses a tea-bag as a pillow.",
		"Yo mama's face is so wrinkled, that she has to screw her hat on.",
		"Yo mama's hips are so big that people set their drinks on them.",
		"Yo mama's hair is so nappy that she has to take Tylenol just to comb it.",
		"Yo mama's feet are so big that her shoes need to have license plates on them!",
		"Yo mama's so lonely that she buys hot dogs and nuts wishing she could have sex with them.",
		"Yo mama is so bald that even a wig wouldn't help!",
		"Yo mama is so bald that you can see what's on her mind.",
		"Yo mama is so bald that she took a shower and got brain-washed!",
		"Yo mama's teeth are so yellow that when she smiles everyone sings \"We're Walking on Sunshine.\"",
		"Yo mama is like a slaughter house - everybody's hanging their meat up in her.",
		"Yo mama is like the new AOL 4.0: Fun, Fast, Easy and Free!",
		"Yo mama is like a carpenter's dream - flat as a board and easy to nail.",
		"Yo mama is like Humpty Dumpty - First she gets humped, then she gets dumped.",
		"Yo mama is like a bag of potato chips, \"Free-To-Lay.\"",
		"Yo mama is like a turtle - once she's on her back she's fucked.",
		"Yo mama is like a fan - she's always blowing someone.",
		"Yo mama is like Pizza Hut - if she isn't there in 30 minutes... it's Free!",
		"Yo mama is like a goalie - she only changes her pads after three periods.",
		"Yo mama is like a gas station - you gotta pay before you pump!",
		"Yo mama is like Sprint - 10 cents a minute anywhere in the country.",
		"Yo mama is like a Chinese restaurant - All you can eat for only $9.95!",
		"Yo mama smells so bad that the doctor diagnosed her with breath cancer.",
		"Yo mama's breath smells so bad that when she yawns her teeth duck out of the way.",
		"What's the difference between yo mama and a Lay-Z-Boy? One's soft, squishy, and always has someone in it. The other is a chair.",
		"What's the difference between yo mama and a 747? About 20 pounds.",
		"Yo mama's like a shotgun, one cock and she blows.",
		"Yo mama's like the Bermuda Triangle, they both swallow a lot of seamen.",
		"Yo mama's like cake mix, 15 servings per package!",
		"Yo mama's like a 5 foot tall basketball hoop, it ain't that hard to score.",
		"Yo mama's like a vacuum cleaner... she sucks, blows, and then gets laid in the closet.",
		"Yo mama's like the Pillsbury dough boy - everybody pokes her.",
		"Yo mama's like a brick, dirty, flat on both sides, and always getting laid by Mexicans.",
		"Yo mama's like a nickel, she ain't worth a dime.",
		"Yo mama's like a streetlamp, you can find her turned on at night on any street corner.",
		"Yo mama's like a telephone booth, open to the public, costs a quarter, and guys go in and out all day.",
		"Yo mama's like a Reese's Peanut Butter Cup, there's no wrong way to eat her.",
		"Yo mama's like a postage stamp, you lick her, stick her, then send her away.",
		"Yo mama's like a screen door, after a couple of bangs she loosens up.",
		"Yo mama's like a dollar bill, she gets handled all across the country.",
		"Yo mama's like school at 3 o'clock... children keep coming out and nobody can remember all the fathers.",
		"Yo mama's like a bowling ball, she gets picked up, fingered, thrown down the gutter, and she still comes back for more.",
		"Yo mama's like a set of speakers - loud, ugly, lives in a box, and you can turn her up, down, on, and off.",
		"Yo mama's like a birthday cake, everybody gets a piece.",
		"Yo mama's like 7-Eleven - open all night, hot to go, and for 89 cents you can get a slurpy.",
		"Yo mama's like a vacuum cleaner - a real good suck.",
		"Yo mama's like a Snickers bar, packed with nuts.",
		"Yo mama's like a race car driver - she burns a lot of rubbers.",
		"Yo mama's like a parking garage, three bucks and you're in.",
		"Yo mama's like a pool table, she likes balls in her pocket.",
		"Yo mama's got 1 toe & 1 knee and they call her Tony.",
		"Yo mama's got a \"wait\" problem, she can't wait to eat.",
		"Yo mama's got a 4 dollar weave and don't know when to leave.",
		"Yo mama's teeth are so yellow, when she smiles it looks like a Kraft Singles pack.",
		"Yo mama's got Play-Doh teeth.",
		"Yo mama's like the Panama Canal, vessels full of seamen pass through her everyday.",
		"Yo mama likes to applaud, 'cause she's got clap",
		"Yo mama's got 1 leg longer than the other so they call her call her hip hop.",
		"Yo mama's got an eating disorder, she be eating dis order, dat order, she be eating all the damn orders!",
		"Yo mama sucks so much dick her butt chin turned into a nut chin!",
		"Yo mama's got more chins than a Chinese phone book.",
		"Yo mama's like a bungee cord... 100 dollars for 30 seconds and if that rubber breaks, your ass is dead!",
		"Yo mama's like a squirrel, she's always got some nuts in her mouth.",
		"Yo mama's like a refrigerator, everyone puts their meat in her.",
		"Yo mama's like a tricycle, she's easy to ride.",
		"yo mamas like a hardware store. 25 cents a screw.",
		"Yo mama's like mustard, she spreads easy.",
		"Yo mama's like peanut butter: brown, creamy, and easy to spread.",
		"Yo mama's like McDonalds... Billions and Billions served.",
		"Yo mama's like an elevator, guys go up and down on her all day.",
		"Yo mama's like a railroad track, she gets laid all over the country.",
		"Yo mama's like lettuce, 25 cents a head.",
		"Yo mama's got an eagle's nest wig.",
		"Yo mama's twice the man you are.",
		"Yo mama's got more crust than a bucket of Kentucky Fried Chicken.",
		"Yo mama's got more weave than a dog in traffic.",
		"Yo mama's only got one finger and runs around stealing key rings.",
		"Yo mama's got a peanut butter wig with jelly sideburns.",
		"Yo mama's got a leather wig with suede sideburns.",
		"Yo mama got hit upside the head with an ugly stick.",
		"Yo mama's got so much weave, when a fly goes by her hair swats at it.",
		"Yo mama's got no ears and was trying on sunglasses.",
		"Yo mama's got so much weave, AT&T uses her extensions as backup lines.",
		"Yo mama's got so much dandruff, she needs to defrost it before she combs her hair.",
		"Yo mama's so bald that I can tell fortunes on her head.",
		"Yo mama's so bald that you could draw a line down the middle of her head and it would look like my ass.",
		"Yo mama's so bald that when she goes to bed, her head slips off the pillow.",
		"Yo mama's so bald that when she braids her hair, it looks like stitches.",
		"yo mama's breath is so stanky, she eats odour eaters.",
		"Yo mama's like an iPod, fun to touch!",
		"Yo mama's got one leg and people call her Ilene.",
		"Yo mama's been on welfare so long that her picture is on food stamps.",
		"Yo mama's like Wal-Mart... She's got different discounts everyday.",
		"Yo mama's so hunchbacked, she has to look up to tie her shoes.",
		"Yo mama's nostrils are so huge she makes Patrick Ewing jealous.",
		"Yo mama's so hunchbacked, she has to wear goggles to wash dishes.",
		"Yo mama's so hunchbacked, she can stand on her feet and her head at the same time.",
		"Yo mama's so hunchbacked, she hits her head on speed bumps.",
		"Yo mama's so fat that the Sorting Hat put her in all four houses!",
		"Yo mama's so fat that a wingardium leviosa spell couldn't lift her.",
		"Yo mama's so fat, she makes Hagrid look like \"Mini-me\".",
		"Yo mama's so fat, she tried to eat Cornelius Fudge.",
		"Yo mama's so ugly, even a dementor wouldn't kiss her!",
		"Yo mama's so fat the Sorting Hat assigned her to the House of Pancakes.",
		"Yo mama's so old, she used to babysit Dumbledore.",
		"Yo mama's so stupid, she thinks Sirius Black is a hip hop station on satellite radio.",
		"Yo mama's so ugly that the whomping willow saw her and died.",
		"Yo mama's so stupid she thinks Patronus is a kind of Tequlia.",
		"Yo Mama's so fat, her Patronus is a Double-Whopper with Cheese.",
		"Yo mama's so nasty, the Forbidden Forrest was named after her.",
		"Yo mama's the reason that Dumbledore turned gay.",
		"Yo mama's so old, her boobs look like two upside down Sorting Hats!",
		"Yo mama's so fat, she used the invisibility cloak as a bib.",
		"Yo Mama's so ugly, everybody calls her \"She-Who-Must-Not-Be-Naked\"",
		"Yo mama's so fat that even the Dementors can't suck her soul out in one sitting.",
		"Yo mama's so pasty, she makes Ron Weasely look like George Hamilton.",
		"Yo mama's so fat, she looked in the mirror of Erised and saw a ham!",
		"Yo mama's so old she gave Nicholas Flamel his first kiss.",
		"Yo mama's so ugly that the Dementor's Kiss was swapped out for a hearty handshake and a promise to give her a call sometime.",
		"Yo mama's so stupid, she drowned in a pensieve",
		"Yo mama's so dumb she thought that she could talk to snakes if she put parsley on her tongue",
		"Yo mama's so nasty, every pair of her panties has the Dark Mark on them.",
		"Yo mama's so fat that if she confronted a boggart it would morph into a treadmill.",
		"Yo Mama's so ugly that even Voldemort won't say her name.",
		"Yo Mama's so poor she can't even afford a Gringotts account.",
		"Yo mama's so fat that the sorting hat couldn't decide where to put her - she couldn't fit in any of the houses!!",
		"Yo mama's the only mute prostitue in Hogsmeade. They call her \"dumb-le-whore\"!",
		"Yo mama's so fat, she ate the Death Eaters.",
		"Yo mama's so masculine that Dumbledore would sleep with her!",
		"Yo mama's so nasty that the order of the phoenix was \"stay away from that woman!\"",
		"Yo mama's so poor that Dobby gave her a sock to keep her foot warm.",
		"Yo mama's such a tramp that she's given more rides than the Hogwarts Express!",
		"Yo mama's so fat even Grawp can't pick her up!",
		"Yo mama's so smelly, Bertie Bott made her his next jelly bean flavor.",
		"Yo mama's so fat that it takes two boggarts to shape-shift into her!",
		"Yo mama's so ugly that she lost a beauty contest to Mountain Troll.",
		"Yo mama's so ugly that when the bassalisk snuck up on her and saw her face, HE dropped dead.",
		"Yo mama's breath is the secret ingredient in the Weasly's Butterscotch Barf-ies.",
		"Yo mama's so ugly that when she walked into Gringotts Wizarding Bank, they gave her a job application.",
		"Yo mama's so ugly she turned the Basilisk to stone.",
		"Yo mama's such a tramp that she's like a quidditch broomstick - everyone gets a ride.",
		"Yo mama's so skanky that the reason you're called a Half-Blood Prince is because she has no idea who your father is!",
		"Yo mama's so dumb that a stupify spell actually made her smarter.",
		"Yo mama's so stanky that not even dobby would accept one of her socks.",
		"Yo mama's so fat that even her Quidditch robes have stretch marks.",
		"Yo mama's so old she makes Dumbledore look like a teenager.",
		"Yo mama's so fat they'd have to use transfiguration to sneak her through the hole in the Gryffindor Tower.",
		"Ya mama's so fat, her wand is a Slim Jim.",
		"Yo mama's so fat the core of her wand has a creame filling.",
		"Yo mama's so poor she had to go to the Weasley's for a loan.",
		"Yo mama's so ugly, she thought that Hogwarts were the growth on her thigh.",
		"Yo mama's so ugly that as a baby they had to use the Confundus Charm so the family would play with her.",
		"Yo mama's such a ho that she lets ANYONE enter her \"chamber of secrets\".",
		"Yo mama's so ugly she scares the Dementors away.",
		"Yo mama's so ugly that when she asked Crabbe to take her to the Yule Ball, he decided to go with Goyle instead!",
		"Yo mama's so fat that a $700 billion bailout would only keep her fed for a week.",
		"Yo mama's so fat that the housing bubble popped because she sat on it!",
		"Yo mama's so stupid, she thinks the G8 is a Value Meal at McDonald's.",
		"Yo mama's so fat that she supported the bailout just because she wanted a 'barrel of pork'.",
		"Yo mama's so stupid that she thinks sub-prime is a way to cut steak.",
		"Yo mama's so fat that even Mitt Romney couldn't afford to take her out to dinner!",
		"Yo mama's so fat that her biography is called \"The Audacity of Hardee's\".",
		"Yo mama's so greasy that her face could free the U.S. from its dependence on foreign oil.",
		"Yo mama's so fat that Sarah Palin can see her from her house.",
		"Yo mama's so fat that Sarah Palin can't see Russia anymore!.",
		"Yo mama's so ugly that you could put lipstick on a pig and it would look ten times better than her!",
		"Yo mama's so fat that \"ACORN\" registered her to vote eight times!",
		"Yo mama's so fat that even the Death Star couldn't blow her up!",
		"Yo mama's so fat that Spock couldn't find a pressure point to perform the Vulcan Death Grip on her.",
		"Yo mama's so ugly that Wuher said 'We don't serve your kind here'.",
		"Yo mama's so fat the odds against not finding her fat are approximately 3,720 to 1.",
		"Yo mama's so fat that she thought the opening line of Kirk's monologue was \"Spice, the final Frontier...\"",
		"Yo mama's so stupid that when the borg had to choose between assimilating her and a tree, they chose the tree.",
		"Yo mama's so fat that if she were placed beside a changeling during regeneration, no one would know the difference.",
		"Yo mama's so fat that she tried to fly through a temporal anomoly but she didn't fit.",
		"Yo mama's so fat she makes Riker's belly look 3 atoms thick.",
		"Yo mama's so fat that when she tried to captain a galaxy class they had to separate the saucer so she could fit.",
		"Yo mama's so fat that she makes the USS Enterprise look like a micro machines racer.",
		"Yo mama's so flatulent that she forced the Mustafarians to wear masks!",
		"Yo mama's so dumb that she tried to rent a car from The Enterprise.",
		"Yo mama's so fat that Dexster Jettster mistook her for his wife.",
		"Yo mama's so ugly that the term 'bantha poodoo' wasn't used metaphorically with reference to her.",
		"Yo mama's so fat that only half her body was able to come out frozen from the carbon freezing chamber in Cloud City.",
		"Yo mama's so ugly that Dr. Evazan looks like a male supermodel next to her.",
		"Yo mama's so fat that when she beams to a ship, the ship beams inside of her.",
		"Yo mama's so such a ho that she slept with me... therefore, I AM YOUR FATHER!",
		"Yo mama's so dumb that when she found a vulcan, she tried to call Santa to take him back to the north pole.",
		"Yo mama's so fat that the passengers of the Millenium Falcon mistook her for a small moon.",
		"Yo mama's so fat that Gardulla the Hutt had a boost in self-esteem after seeing her.",
		"Yo mama's so ugly that she made doctor McCoy say \"Damnit Jim, I'm a doctor, not a Zoologist!\"",
		"Yo mama's so fat that she fell to the dark side and couldn't get back up.",
		"Yo mama's so fat that if she was thrown into the second Death Star's reactor core, she could have blown up the entire Imperial fleet.",
		"Yo mama's so fat that the Kaminoans couldn't use her as a host for clones since they couldn't pierce her skin deep enough to draw blood.",
		"Yo mama's so weak-minded that I got her to lead me to Jabba without using a jedi mind trick!",
		"Yo mama's so fat that she caused Kamino to flood when her water broke.",
		"Yo mama's so ugly that she's probably a Shi'ido Clawdite that stays in her regular form all the time.",
		"Yo mama's so fat that her lack of balance caused her to stumble into an Utapau sinkhole.",
		"Yo mama's so fat that she crushed Boga as soon as she mounted her.",
		"Yo Mama's so fat, that in an attempt to beam her up, the ship ended up being pulled down to the surface.",
		"Yo Mama's so ugly even Data would need special eye googles to look at her.",
		"Yo mama is so hairy that the only language she can speak is wookie.",
		"Yo mama's so ugly her Kazon hairdo is an improvement!",
		"Yo Mama's so ugly even a Ferengi would dress her in clothes.",
		"Yo mama's so old even Guinan refers to her as \"old bag\".",
		"Yo Mama's so fat that when she walks into a room the replicators stop working.",
		"Yo Mama's so fat, Data feels strong emotions of disgust and self-terminates.",
		"Yo Mama's so stupid the Borg wouldn't assimilate her!",
		"Yo Mama's so fat she wears her own inertia dampener.",
		"Yo Mama's so ugly she did the truly impossible: she made Captain James T Kirk's penis go limp.",
		"Yo Mama's so fat, she managed to contain a warp core breach.",
		"Yo Mama's so fat, she got stuck trying to enter the Nexus.",
		"Yo Mama's so fat, when she fell over, she punched a hole in the fabric of space/time.",
		"Yo mama's so fat that when she stepped on the scale, her weight was OVER 9000!!!",
		"Yo Mama's so fat, she walked in front of the TV and I missed three seasons of Inuyasha!",
		"Yo mama's so fat, Naruto couldnt make enough clones to see all sides of her.",
		"Yo mama's so ugly, even Tamaki wouldn't hit on her.",
		"Yo mama's so fat that the Dragon Ball Z crew uses her to make craters on set.",
		"Yo mama's so ugly, she's the real reason sasuke left the village.",
		"Yo mama's so fat that when she sat down on a park bench, she caused the Naruto timeskip.",
		"Yo mama's so ugly that she's like a Death Note. Get someone to look at her, and they'll die!",
		"Yo mama's so ugly, Jiraiya saw her and turned gay!",
		"Yo mama's so hairy Naruto thought she was a Summon.",
		"Yo mama's so fat, she scared L into giving up all sweets.",
		"Yo mama's so ugly that she made Spike Spiegel choke on his cigarette",
		"Yo mama's so ugly that she makes Sailor Bubba feel dirty.",
		"Yo mama's so fat that she cant even fit in the expanding plug suit.",
		"Yo mama's so ugly that she made Loz cry.",
		"Yo mama's so dumb that when she was handed the death note, she thought they were asking for her autograph.",
		"Yo mama's so fat that she broke the HP limit!",
		"Yo mama's so hairy and ugly that she got used as Ashitare's stunt double.",
		"Yo mama's so stupid she makes Tristan look like Einstein!",
		"Yo mama's so fat, she makes Vash look anorexic!",
		"Yo mama's so hairy that she has to go to Furfest to meet a man.",
		"Yo mama's breath is so nasty that it chases away Miasma.",
		"Yo mama's so round that she makes a Pokéball look flat!",
		"Yo mama's so ugly, Saya thought she was a Chiropteran.",
		"Yo mama's so dumb, she failed out of Cromartie High School.",
		"Yo mama's so old and fat they use her wrinkles as set terrain for Dragon Ball Z.",
		"Yo mama's nosehairs are so long that they make Bobobo jealous!",
		"Yo mama's so fat that she was mistaken for Mt. Fuji at the Sakura festival.",
		"Yo mama's so fat she makes a Snorlax look like a chihuahua!",
		"Yo mama's so fat that it took the entire Dragon Ball Z crew 1 week just to lift her off the ground.",
		"Yo mama's cosplay is so bad that she got beat by a Narutard in the masquerade!",
		"Yo mama's so ugly that when Kakashi looked directly at her, he lost an eye.",
		"Yo mama's so fat that she tried to eat someone dressed as a box of Pocky!",
		"Yo mama's so ugly that she makes Orochimaru look beautiful.",
		"Yo mama's so fat, Choji told her to lose weight.",
		"Yo mama is so old that her birth certificate says \"expired\" on it.",
		"Yo mama is so old that that when she was in school there was no history class.",
		"Yo mama is so old that she knew Burger King while he was still a prince.",
		"Yo mama is so old that her social security number is 1.",
		"Yo mama is so old that her birth certificate is written in Roman numerals.",
		"Yo mama is so old that she has Adam & Eve's autographs.",
		"Yo mama is so old that she co-wrote the Ten Commandments.",
		"Yo mama is so old that she has an autographed bible.",
		"Yo mama is so old she remembers when the Mayans published their calendar.",
		"Yo mama is so old that the candles cost more than the birthday cake.",
		"Yo mama is so old that when she farts, dust comes out.",
		"Yo mama is so old that she owes Fred Flintstone a food stamp.",
		"Yo mama is so old that she drove a chariot to high school.",
		"Yo mama is so old that she took her drivers test on a dinosaur.",
		"Yo mama is so old that she DJ'd at the Boston Tea Party.",
		"Yo mama is so old that she walked into an antique store and they kept her.",
		"Yo mama is so old that she baby-sat for Jesus.",
		"Yo mama is so old that she knew Mr. Clean when he had an afro.",
		"Yo mama is so old that she knew the Beetles when they were the New Kids on the Block.",
		"Yo mama is so old that when God said \"Let there be light\" she was there to flick the switch.",
		"Yo mama is so old that she needed a walker when Jesus was still in diapers.",
		"Yo mama is so old that when Moses split the red sea, she was on the other side fishing.",
		"Yo mama is so old that she learned to write on cave walls.",
		"Yo mama is so old that her memory is in black and white.",
		"Yo mama is so old that she's mentioned in the shout out at the end of the bible.",
		"Yo mama is so old that she planted the first tree at Central Park.",
		"Yo mama is so old that she sat next to Jesus in third grade.",
		"Yo mama is so old that she has a picture of Moses in her yearbook.",
		"Yo mama is so old that she knew Cap'n Crunch while he was still a private.",
		"Yo mama is so old that she called the cops when David and Goliath started to fight.",
		"Yo mama is so old that when she was born, the Dead Sea was just getting sick.",
		"Yo mamags so old, when she breast feeds, people mistake her for a fog machine.",
		"Yo mama is so old that when she was young rainbows were black and white.",
		"Yo mama is so old that she was a waitress at the Last Supper.",
		"Yo mama is so old that she owes Jesus a dollar.",
		"Yo mama is so old that she ran track with dinosaurs.",
		"Yo mama is so stupid that it took her 2 hours to watch 60 Minutes!",
		"Yo mama is so stupid that when your dad said it was chilly outside, she ran out the door with a spoon.",
		"Yo mama is so stupid that when she saw the \"Under 17 not admitted\" sign at a movie theatre, she went home and got 16 friends.",
		"Yo mama is so stupid that when she went for a blood test, she asked for time to study.",
		"Yo mama is so stupid that she got locked in a grocery store and starved!",
		"Yo mama is so stupid that you have to dig for her IQ!",
		"Yo mama is so stupid that she tripped over a cordless phone!",
		"Yo mama is so stupid that she sold her car for gas money!",
		"Yo mama is so stupid that she told everyone that she was \"illegitimate\" because she couldn't read.",
		"Yo mama is so stupid that that she tried to put M&M's in alphabetical order!",
		"Yo mama is so stupid that she took the Pepsi challenge and chose Dr. Pepper.",
		"Yo mama is so stupid that she thought Delta Airlines was a sorority.",
		"Yo mama is so stupid that she thinks Fleetwood Mac is a new hamburger at McDonalds!",
		"Yo mama is so stupid that she bought a videocamera to record cable tv shows at home.",
		"Yo mama is so stupid that when she read on her job application to not write below the dotted line she put \"OK\".",
		"Yo mama is so stupid that she thought Grape Nuts was an STD.",
		"Yo mama is so stupid that she spent twenty minutes lookin' at an orange juice box because it said \"concentrate\".",
		"Yo mama is so stupid that she asked me what yield meant, I said \"Slow down\" and she said \"What... does.... yield... mean?\"",
		"Yo mama is so stupid that she thought Dunkin' Donuts was a basketball team!",
		"Yo mama is so stupid that she put a phone up her ass and thought she was making a booty call.",
		"Yo mama is so stupid that she thinks Tiger Woods is a forest in India.",
		"Yo mama is so stupid that she put on her glasses to watch 20/20.",
		"Yo mama is so stupid that she climbed over a glass wall to see what was behind it.",
		"Yo mama is so stupid that she failed a survey.",
		"Yo mama is so stupid that she stopped at a stop sign and waited for it to say go.",
		"Yo mama is so stupid, she went to the aquarium to buy a Blu-Ray.",
		"Yo mama is so stupid that I told her I was reading a book by Homer and she asked if I had anything written by Bart.",
		"Yo mama is so stupid that she needs twice as much sense to be a half-wit.",
		"Yo mama is so stupid that she thought brownie points were coupons for a bake sale.",
		"Yo mama is so stupid that when the computer said \"Press any key to continue\", she couldn't find the 'Any' key.",
		"Yo mama is so stupid that she thought Tupac Shakur was a Jewish holiday.",
		"Yo mama is so stupid that when I was drowning and yelled for a life saver, she said \"Cherry or Grape?\"",
		"Yo mama is so stupid that she sat in a tree house because she wanted to be a branch manager.",
		"Yo mama is so stupid that I saw her jumping up and down, asked what she was doing, and she said she drank a bottle of medicine and forgot to shake it.",
		"Yo mama is so stupid that when she locked her keys in the car, it took her all day to get Yo family out.",
		"Yo mama is so stupid that she got locked out of a convertible car with the top down.",
		"Yo mama is so stupid that when she pulled into the drive-thru at McDonald's, she drove through the window.",
		"Yo mama is so stupid that she put 2 quarters in her ears and thought she was listening to 50 cent.",
		"Yo mama is so stupid that she was on the corner with a sign that said \"Will eat for food.\"",
		"Yo mama is so stupid that in the 'No Child Left Behind' act there's a provision that exempts yo mama.",
		"Yo mama is so stupid that she got locked in a Furniture store and slept on the floor.",
		"Yo mama is so stupid that she peals M&M's to make chocolate chip cookies.",
		"Yo mama is so stupid that she leaves the house for the Home Shopping Network.",
		"Yo mama is so stupid that she brought a cup to the movie \"Juice.\"",
		"Yo mama is so stupid that she thinks fruit punch is a gay boxer.",
		"Yo mama is so stupid that she uses Old Spice for cooking.",
		"Yo mama is so stupid that she threw a rock the ground and missed.",
		"Yo mama is so stupid that she went to the store to buy a color TV and asked what colors they had.",
		"Yo mama is so stupid that she tries to email people by putting envelopes into her computer's disk drive.",
		"Yo mama is so stupid that when she took an IQ test, the results came out negative.",
		"Yo mama's so stupid that she though Jar-Jar came with Pickles-Pickles.",
		"Yo mama is so stupid that she thought St. Ides was a Catholic church.",
		"Yo mama is so stupid that she puts lipstick on her head just to make-up her mind",
		"Yo mama is so stupid that she thought she needed a token to get on Soul Train.",
		"Yo mama is so stupid, that she thought Moby Dick was a sexually transmitted disease.",
		"Yo mama is so stupid that she makes Beavis and Butt-Head look like Nobel Prize winners.",
		"Yo mama is so stupid that she took a spoon to the superbowl.",
		"Yo mama is so stupid that that she thought Boyz II Men was a day care center.",
		"Yo mama is so stupid that she got stabbed in a shoot out.",
		"Yo mama is so stupid that she sits on the TV, and watches the couch!",
		"Yo mama is so stupid that she took a umbrella to see Purple Rain.",
		"Yo mama is so stupid that she ordered her sushi well done.",
		"Yo mama is so stupid that she got fired from the M&M factory for throwing away all the W's.",
		"Yo mama is so stupid that she put on a coat to chew winterfresh gum.",
		"Yo mama is so stupid that she put a quarter in a parking meter and waited for a gumball to come out.",
		"Yo mama is so stupid that she ordered a cheese burger from McDonald's and said \"Hold the cheese.\"",
		"Yo mama is so stupid that she thinks Taco Bell is a Mexican Phone Company.",
		"Yo mama is so stupid that she thinks Christmas Wrap is Snoop Dogg's holiday album.",
		"Yo mama is so stupid that she ran outside with a purse because she heard there was change in the weather.",
		"Yo mama is so stupid that I told her Christmas was just around the corner and she went looking for it.",
		"Yo mama is so stupid that she wiped her ass before she took a shit.",
		"Yo mama is so stupid that she tries to insult you with yo mama jokes.",
		"Yo mama is so stupid that she put a peephole in a glass door.",
		"Yo mama is so stupid that I saw her in the frozen food section with a fishing rod.",
		"Yo mama is so stupid that when she heard 90% of all crimes occur around the home, she moved.",
		"Yo mama is so stupid that when she saw a \"Wrong Way\" sign in her rearview mirror, she turned around.",
		"Yo mama is so stupid that she shoved a AA battery up her butt and said \"I got the power!\"",
		"Yo mama is so stupid that she called the 7-11 to see when they closed.",
		"Yo mama is so stupid that she sold the house to pay the mortgage.",
		"Yo mama is so stupid that when I asked her about X-Men she said \"Sure, there's Bobby my first baby daddy, Roger the guy I see on Thursdays...\"",
		"Yo mama is so stupid that she thought meow mix was a record for cats.",
		"Yo mama is so stupid that she took lessons for a player piano.",
		"Yo mama is so stupid that she said \"what's that letter after x\" and I said Y she said \"Cause I wanna know\".",
		"Yo mama is so stupid that when she asked me what kinda jeans I wore, I said Guess and she said \"Ummm... Levis?\"",
		"Yo mama is so stupid that if she spoke her mind, she'd be speechless.",
		"Yo mama is so stupid that it takes her an hour to cook minute rice.",
		"Yo mama is so stupid that she asked for a price check at the dollar store.",
		"Yo mama is so stupid that on her job application where it says emergency contact she put 911.",
		"Yo mama is so stupid that she can't make Jello because she can't fit 2 quarts of water in the box.",
		"Yo mama is so stupid that she thinks a stereotype is the brand on her clock-radio.",
		"Yo mama is so stupid that she thought a lawsuit was something you wear to court.",
		"Yo mama is so stupid that she thinks sexual battery is something in a dildo.",
		"Yo mama is so stupid that the first time she used a vibrator, she cracked her two front teeth.",
		"Yo mama is so stupid that she sent me a fax with a stamp on it.",
		"Yo mama is so stupid that I saw her walking down the street yelling into an envelope, asked what she was doing, and she said sending a voice mail.",
		"Yo mama is so stupid that she tried to drown a fish.",
		"Yo mama is so stupid that if you gave her a penny for her thoughts, you'd get change.",
		"Yo mama is so stupid that she thought Mick Jagger was a breakfast sandwich!",
		"Yo mama is so stupid that when she heard her neighbour was spanking the monkey, she called the humane society.",
		"Yo mama is so stupid that when she took you to the airport and a sign said \"Airport Left,\" she turned around and went home.",
		"Yo mama is so stupid that when she went to take the 44 bus, she took the 22 twice instead.",
		"Yo mama is so stupid that she asked you \"What is the number for 911?\"",
		"Yo mama is so stupid that she thinks a quarterback is a refund!",
		"Yo mama is so stupid that she bought a solar-powered flashlight!",
		"Yo mama is so stupid that she took a ruler to bed to see how long she slept.",
		"Yo mama is so stupid that she thought menopause was a button on the VCR.",
		"Yo mama is so stupid that she picked up the phone and asked \"What button do I push?\"",
		"Yo mama is so stupid that when she worked at McDonald's and someone ordered small fries, she said \"Hey Boss, all the small one's are gone.\"",
		"Yo mama is so stupid that she got hit by a parked car.",
		"Yo mama is so stupid that when her husband lost his marbles she ran to the store and bought him new ones.",
		"Yo mama is so stupid that when they said they were playing craps she went and got toilet paper.",
		"Yo mama is so stupid that when I asked her if she wanted to play one on one, she said \"Ok, but what's the teams?\"",
		"Yo mama is so stupid that she thinks Johnny Cash is a pay toilet!",
		"Yo mama is so stupid that when the judge said \"Order in the court,\" she said \"I'll have a hamburger and a Coke.\"",
		"Yo mama is so stupid that she wiped her ass before she took a shit.",
		"Yo mama is so stupid that she thinks socialism means partying!",
		"Yo mama is so stupid that when asked on an application, \"Sex?\", she marked, \"M, F, and wrote sometimes Wednesday too.\"",
		"Yo mama is so stupid that she thinks deadbeat is a type of music.",
		"Yo mama is so stupid that she thinks Tiger Woods is a forest.",
		"Yo mama is so stupid that she put two M&M's in her ears and thought she was listening to Eminem.",
		"Yo mama is so stupid that at bottom of application where it says Sign Here - she put Scorpio.",
		"Yo mama is so stupid that she wouldn't know up from down if she had three guesses.",
		"Yo mama is so stupid that she put on bug spray before going to the flea market.",
		"Yo mama is so stupid that she stole free bread.",
		"Yo mama is so stupid that she locked her keys inside a motorcycle.",
		"Yo mama's so stupid that she got locked inside a motorcycle.",
		"Yo mama's so stupid that she went to the dentist to get a bluetooth.",
		"Yo mama's so stupid that she bought tickets to Xbox Live.",
		"Yo mama's so stupid that whenever someone rings the doorbell, she checks the microwave.",
		"Yo mama's so stupid that when she broke her VCR, she bought a video tape on how to fix your VCR.",
		"Yo mama is so stupid that she tried to drop acid but the car battery fell on her foot.",
		"Yo mama so dumb, she lost a spelling bee to Hodor",
		"Yo Mama so dumb, she thought Bran Stark was a type of muffin.",
		"Yo mama so fat, they've been calling her \"the wall\" for thousands of years!",
		"Yo mama so fat, she Winter-fell and couldn't get up!",
		"Yo mama so old, the old gods pray to HER!",
		"Yo Mama So Fat, she can't fit through the moon door.",
		"Yo Mama so Ugly, she got turned down for \"Girls Gone Wilding\"",
		"Yo mama so ugly, winter turned around and left!",
		"Yo mama so fat, even Roose Bolton won't touch her",
		"Yo mama so bad at sex, the only kind of head she gives is severed.",
		"Yo mama is so poor that she was in K-Mart with a box of Hefty bags and when I asked her what she was doing she said, \"Buying luggage.\"",
		"Yo mama is so poor that when she goes to KFC, she has to lick other people's fingers!",
		"Yo mama is so poor that she went to McDonald's and put a milkshake on layaway.",
		"Yo mama is so poor that she can't afford to pay attention!",
		"Yo mama is so poor that when I saw her kicking a can down the street, I asked her what she was doing, and she said \"moving.\"",
		"Yo mama is so poor that she waves around a popsicle stick and calls it air conditioning.",
		"Yo mama is so poor that I saw her running after a garbage truck with a shopping list.",
		"Yo mama is so poor that the bank repossesed her cardboard box.",
		"Yo mama is so poor she couldn't afford to apply for Medicare!",
		"Yo mama is so poor that she has to wear her McDonald's uniform to church.",
		"Yo mama is so poor that she's got more furniture on her porch than in her house.",
		"Yo mama is so poor that I came over for dinner and she read me recipes.",
		"Yo mama is so poor that she has to take the trash IN.",
		"Yo mama is so poor that she had to get a second mortgage on her cardboard box.",
		"Yo mama is so poor that she lives in a two story Dorrito bag with a dog named Chip.",
		"Yo mama is so poor that I went through her front door and ended up in the back yard.",
		"Yo mama is so poor that her front and back doors are on the same hinge.",
		"Yo mama is so poor that I saw her wrestling a squirrel for a peanut.",
		"Yo mama is so poor that the closest thing to a car she has is a low-rider shopping cart with a box on it.",
		"Yo mama is so poor that she can't even put her two cents in this conversation.",
		"Yo mama is so poor that when I saw her walking down the street with one shoe and said \"Hey miss, lost a shoe?\" she said \"Nope, just found one!\"",
		"Yo mama is so poor that her face is on the front of a foodstamp.",
		"Yo mama is so poor that I went to her house and tore down some cob webs, and she said \"Who's tearing down the drapes?\"",
		"Yo mama is so poor that I stepped on her skateboard and she said \"Hey, get off the car!\"",
		"Yo mama is so poor that I walked into her house, asked to use the bathroom, and she said \"3rd bucket to your right.\"",
		"Yo mama is so poor that when I walked inside her house and put out a cigarette, she said \"who turned off the heater?\"",
		"Yo mama is so poor that your TV got 2 channels: ON and OFF.",
		"Yo mama is so poor that she watches TV on an Etch-A-Sketch.",
		"Yo mama is so poor that she can't even afford to go to the free clinic.",
		"Yo mama is so poor that she washes paper plates.",
		"Yo mama is so poor that her idea of a fortune cookie is a tortilla with a food stamp in it.",
		"Yo mama is so poor that when yo family watches TV, they go to Sears.",
		"Yo mama is so poor that burglars break in and leave money.",
		"Yo mama is so poor that she married young just to get the rice!",
		"Yo mama is so poor that when I went over to her house for dinner and grabbed a paper plate, she said \"Don't use the good china!\"",
		"Yo mama is so poor that when I saw her rolling some trash cans around in an alley, I asked her what she was doing, she said \"Remodeling.\"",
		"Yo mama is so poor that I threw a rock at a trash can and she popped out and said \"Who knocked?\"",
		"Yo mama is so poor that we were on a road trip and she stopped by a dumpster and got out. I said \"what are you doing\" and she said I'm \"booking a hotel!\"",
		"Yo mama is so poor that I walked into her house and swatted a firefly and Yo Mama said, \"Who turned off the lights?\"",
		"Yo mama is so poor that when I asked what was for dinner, she pulled her shoelaces off and said \"Spagetti.\"",
		"Yo mama is so poor that after I pissed in your yard, she thanked me for watering the lawn.",
		"Yo mama is so poor that your family ate cereal with a fork to save milk.",
		"Yo mama is so poor that when I ring the doorbell she says,\"DING!\"",
		"Yo mama is so poor that she got in an elevator and thought it was a mobile home.",
		"Yo mama's so poor, that her doormat doesn't say \"welcome\", it says \"welfare\".",
		"Yo mama is so poor that for halloween, her trick was the treat.",
		"Yo mama is so poor that when she tells people her address, she says \"it's in the second alley from main street, beside the yellow dumpster.\"",
		"Yo mama is so poor that her idea of a timeshare is a few days camped out under a bridge.",
		"Yo mama is so poor that when I saw her in the park digging up plants, she said she was \"getting groceries\".",
		"Yo mama is so poor that when I ring the doorbell I hear the toilet flush!",
		"Yo mama's so fat that she expresses her weight in scientific notation.",
		"Yo mama's so fat that scientists track her position by observing anomalies in Pluto's orbit.",
		"Yo mama's so fat that a recursive function computing her weight causes a stack overflow.",
		"Yo mama's so fat that the long double numeric variable type in C++ is insufficient to express her weight.",
		"Yo mama's so fat that THX can't even surround her.",
		"Yo mama's a convenient proof that the universe is still expanding exponentially.",
		"Yo mamags so big that she has a gravitational pull equal to that of the sun.",
		"Yo mama's so big that doctors use scuba divers as nanobots to clean her arteries.",
		"The mass of yo mama at rest is approximately equal to that of a neutron star traveling at (1-(10^-1000))c.",
		"Yo mama's so slow and dumb that she can be emulated on a 286.",
		"Yo mama conforms to Planck's law - the greater the frequency with which she screws, the more energetic she gets.",
		"Yo mama's like a converging lens - she's wider in the middle than she is on either end.",
		"Yo mama's dumber than an augmented rat.",
		"Yo mama's so fat that she and the great wall of China are used as reference points when astronauts look back at the Earth.",
		"Yo mama's such a ho that even the noble gases are attracted to her.",
		"Yo mama's so promiscuous that electrons have a positive charge when they're around her.",
		"Yo mama's so stupid that her exchange particle is a \"moron\".",
		"Yo mama's so fat that China uses her to block the internet.",
		"Yo mama's so fat that NASA shot a rocket into her ass looking for water.",
		"Yo mama's so dumb that she went to the dentist and asked for a bluetooth.",
		"Yo mama's so fat that she doesn't just have a low center of gravity, she has an elliptical orbit.",
		"Yo mama's so fat that IEEE is working on a wifi protocol so people can get the signals to reach users on opposite sides of her. It's called 802.11 Draft Fat Momma",
		"If we were to code your mom in a C++ function she would look like this: double mom (double fat){ mom(fat);return mom;}; //your mom is recursively fat.",
		"Yo mama's so old that she goes on carbon dates.",
		"Yo mama's so fat, the cyberman DOWNgraded her.",
		"Yo mama's so ugly that Dalek's don't actually say 'Exterminate' when they see her, because they figure somebody else already got there first!",
		"Yo mama's such a drunk, that her sonic screwdriver is made of vodka and orange juice.",
		"Yo mama's so ugly that when she looks into the Tardis, the Tardis doesn't look into her.",
		"Yo mama's so ugly that when the Daleks Exterminate her, it's not for domination.",
		"Yo mama's such a hoe that the nickname for her vagina (Bad Wolf) is scattered across time and space.",
		"Yo mama's so fat, she's bigger than both the outside AND the inside of the Tardis",
		"Yo mama's so ugly that when Captain Jack Harkness saw her, he actually died.",
		"Yo mama's so fat, the Pirate Planet tried to take her over.",
		"Yo mama's so lazy, she's a \"part-time\" lord",
		"Yo Mama's so fat that when she got upgraded by the cybermen, they turned her into an ice cream truck",
		"Yo mama's so stupid that when Cassandra says \"Moisturize!\", she begins to sweat.",
		"Yo mama's so fat, the Doctor caught her eating his psychic paper, thinking it was a burger.",
		"Yo mama's such a noisy hoe, her nickname is the sonic screwdriver!",
		"Yo mama's so fat, it doesn't matter that the Tardis is bigger on the inside. She can't get through the door.",
		"Yo mama is so skinny that she turned sideways and disappeared.",
		"Yo mama is so skinny that she hula hoops with a Cheerio.",
		"Yo mama is so skinny that she has to wear a belt with spandex.",
		"Yo mama is so skinny that she swallowed a meatball and thought she was pregnant.",
		"Yo mama is so skinny that she can see out a peephole with both eyes.",
		"Yo mama is so skinny that she uses a Band-Aid as a maxi-pad.",
		"Yo mama is so skinny that you can save her from drowning by tossing her a Fruit Loop.",
		"Yo mama is so skinny that she has to run around in the shower to get wet.",
		"Yo mama is so skinny that when she wore her yellow dress, she looked like an HB pencil.",
		"Yo mama is so skinny that if she had a sesame seed on her head, she'd look like a push pin.",
		"Yo mama is so skinny that her nipples touch.",
		"Yo mama is so skinny that I could blind-fold her with dental floss.",
		"Yo mama is so skinny that she looks like a mic stand.",
		"Yo mama is so skinny that she only has one stripe on her pajamas.",
		"Yo mama is so skinny that she can dodge rain drops.",
		"Yo mama is so skinny that she inspires crack whores to diet.",
		"Yo mama is so skinny that she uses Chapstick for deodorant.",
		"Yo mama is so small that she goes paragliding on a Dorito.",
		"Yo mama is so skinny that if she turned sideways and stuck out her tongue, she would look like a zipper.",
		"Yo mama is so skinny that she goes hot tubbing with the Mini Wheats Man.",
		"Yo mama is so skinny that when she takes a bath and lets the water out, her toes get caught in the drain.",
		"Yo mama is so skinny that her bra fits better when she wears it backwards.",
		"Yo mama is so skinny that she had to stand in the same place twice to cast a shadow.",
		"Yo mama is so skinny that if she had a yeast infection she'd be a Quarter Pounder with Cheese.",
		"Yo mama is so skinny that her pants only have one belt loop.",
		"Yo mama is so skinny that if she had dreads I'd grab her by the ankles and use her to mop the floor.",
		"Yo mama is so skinny that instead of calling her your parent, you call her transparent.",
		"Yo mama is so tall that she tripped in Michigan and bumped her head in Florida.",
		"Yo mama is so tall that she tripped over a rock and hit her head on the moon.",
		"Yo mama is so tall that if she did a back-flip she'd kick Jesus in the mouth.",
		"Yo mama's so tall, she can see her house from anywhere.",
		"Yo mama's so tall, she uses two 100-foot ladders as crutches.",
		"Yo mama's so tall, she has to take out the driver's seat of her car and sit in the back to operate the vehicle.",
		"Yo mama's so tall, she makes Shaquille O'Neal look like Gary Coleman.",
		"Yo mama's so tall, she did a push-up and burned her back on the sun.",
		"Yo mama is so short that you can see her feet on her drivers license!",
		"Yo mama is so short that she has to use a ladder to pick up a dime.",
		"Yo mama is so short that she does backflips under the bed.",
		"Yo mama is so short that she models for trophys.",
		"Yo mama is so short that her homies are the Keebler Elfs.",
		"Yo mama is so short that she has to get a running start to get up on the toilet.",
		"Yo mama is so short that when she sneezes, she hits her head on the floor.",
		"Yo mama is so short that she does pull-ups on a staple.",
		"Yo mama is so short that she can do push-ups under the door.",
		"Yo mama is so short that when I was dissin' her she tried to jump kick me in the ankle.",
		"Yo mama is so short that she can limbo under the door.",
		"Yo mama is so short that she uses a condom for a sleeping bag.",
		"Yo mama is so short that she slam-dunks her bus fare.",
		"Yo mama is so short that she has to look up to look down.",
		"Yo mama is so short that she makes Gary Coleman look like Shaquille O'Neal.",
		"Yo mama is so short, you can make a life size sculpture of her using one can of Play-Doh.",
		"Yo mama's so short that when she sat on the curb her feet didn't touch the ground.",
		"Yo mama is so short that she can play handball on the curb.",
		"Yo mama has so much hair on her upper lip that she braids it.",
		"Yo mama is so hairy that Bigfoot wants to take HER picture!",
		"Yo mama is so hairy that she looks like she has Buckwheat in a headlock.",
		"Yo mama is so hairy that you almost died of rugburn at birth!",
		"Yo mama is so hairy that they filmed \"Gorillas in the Mist\" in her shower!",
		"Yo mama is so hairy that if she could fly she'd look like a magic carpet.",
		"Yo mama is so hairy that she looks like Bigfoot in a tank top.",
		"Yo mama is so hairy that she has afros on her nipples.",
		"Yo mama is so hairy that when I took her to a pet store they locked her in a cage.",
		"Yo mama is so hairy that she looks like a Chia pet with a sweater on.",
		"Yo mama is so hairy that Jane Goodall follows her around.",
		"Yo mama is so hairy that the only language she can speak is wookie.",
		"Yo mama is so hairy that she shaves her legs with a weedwacker.",
		"Yo mama is so hairy that if you shaved her legs, you could supply wigs for the entire Hair Club for Men.",
		"Yo mama is so hairy that her armpits look like she has Don King in a headlock.",
		"Yo mama's so hairy that she's got sideburns on her tits.",
		"Yo mama is so hairy that she got a trim and lost 20 pounds.",
		"Yo mama is so hairy that people run up to her and say \"Chewbacca, can I get your autograph?\"",
		"Yo mama is so hairy that she gets mistaken for Chewbacca's cousin.",
		"Yo mama is so hairy that two birds made nests in her armpits and she doesn't even know about it!",
		"Yo mama is so hairy that when she's at a nude beach people think she's wearing a fur coat!",
		"Yo mama is so dirty that that she was banned from a sewage facility because of sanitation concerns.",
		"Yo mama is so dirty that she makes mud look clean.",
		"Yo mama is so dirty that that you can't tell where the dirt stops and she begins.",
		"Yo mama is so dirty that she has to creep up on bathwater.",
		"Yo mama is so dirty that she loses weight in the shower.",
		"Yo mama is so dirty that even Swamp Thing told her to take a shower.",
		"Yo mama is so dirty that the US Government uses her bath water as a chemical weapon.",
		"Yo mama is so dirty that when she tried to take a bath, the water jumped out and said \"I'll wait.\"",
		"Yo mama is so nasty that she has more rappers in her than an iPod.",
		"Yo mama is so nasty that she makes speed stick slow down.",
		"Yo mama is so nasty that she brings crabs to the beach.",
		"Yo mama is so nasty that that pours salt water down her pants to keep her crabs fresh.",
		"Yo mama is so nasty that the fishery pays her to stay away.",
		"Yo mama is so nasty that she only changes her drawers once every 10000 miles.",
		"Yo mama is so nasty that a skunk smelled her ass and passed out.",
		"Yo mama is so nasty that I chatted with her on MSN and she gave me a virus.",
		"Yo mama is so nasty that her tits leak sour milk.",
		"Yo mama is so nasty that she has to use Right Guard and Left Guard.",
		"Yo mama is so nasty that she bit the dog and gave it rabies.",
		"Yo mama is so nasty that she has a sign by her crotch that says: \"Warning: May cause irritation, drowsiness, and a rash or breakouts.\"",
		"Yo mama is so nasty that she's got more clap than an auditorium.",
		"Yo mama is so nasty that she calls Janet \"Miss Jackson.\"",
		"Yo mama is so nasty that she has more crabs then Red Lobster.",
		"Yo mama is so nasty that she made right guard turn left.",
		"Yo mama is so nasty that I when I talked to her on the phone, she gave me an ear infection.",
		"Yo mama is so nasty that next to her a skunk smells sweet.",
		"Yo mama is so nasty that her shit is glad to escape.",
		"Yo mama is so nasty that when you were being delivered, the doctor was wearing the oxygen mask.",
		"Yo mama is so nasty that every time she opens her mouth she's talking shit.",
		"Yo mama is so nasty that even dogs won't sniff her crotch.",
		"Yo mama is so nasty that the only dis I want to give her is a disinfectant.",
		"Yo mama is so nasty that her crabs use her tampon string as a bungee cord.",
		"Yo mama is so greasy that she uses bacon as a band-aid!",
		"Yo mama is so greasy that she sweats Crisco!",
		"Yo mama is so greasy that Texaco buys Oil from her.",
		"Yo mama is so greasy that she sweats butter and syrup and has a full time job at Denny's wiping pancakes across her forehead.",
		"Yo mama is so greasy that her freckles slipped off.",
		"Yo mama is so greasy that if Crisco had a football team, she'd be the mascot.",
		"Yo mama is so greasy that she squeezes Crisco from her hair to bake cookies.",
		"Yo mama is so greasy that she's labeled as an ingredient in Crisco.",
		"Yo mama is so greasy that you could fry a chicken dinner for 12 on her forehead.",
		"Yo mama is so greasy that I buttered my popcorn with her leg hairs.",
		"Yo mama's house is so dirty that roaches ride around on dune buggies!",
		"Yo mama's house is so dirty that she has to wipe her feet before she goes outside.",
		"Yo mama's teeth are so rotten that when she smiles it looks like she has dice in her mouth.",
		"Yo mama's teeth are so yellow that traffic slows down when she smiles!",
		"Yo mama's teeth are so yellow that she spits butter!",
		"Yo mama's so dirty, she fertilizes her lawn by rolling in it!",
		"Yo mama's so dirty, when a seed gets stuck in her ass crack it beings to grow!",
		"Yo mama's so dirty, she jumped in a river and created a mud slide!",
		"Yo mama's so dirty, when the wind blows people yell \"Sand Storm!!!\"",
		"Yo mama's so greasy, on hot days she cooks bacon strips on her ass cheeks!",
		"Yo mama is so fat that she took geometry in high school just cause she heard there was gonna be some pi.",
		"Yo mama is so fat that the ratio of the circumference to her diameter is four.",
		"Yo mama is so fat that her derivative is strictly positive.",
		"Yo mama is like a protractor - she's good at every angle.",
		"Yo mama is so fat that in a love triangle, she'd be the hypotenuse.",
		"Yo mama is so stupid that when I told her \"pi-r-squared\" and she replied no, they are round.",
		"The limit of yo mama's ass goes to infinity.",
		"Yo mama = x/0 for every x in yo mama.",
		"The infinite series of yo mama from 0 to infinity is strictly diverging.",
		"Yo mama is so mean that she has no standard deviation.",
		"Yo mama is so ugly, that Pythagoras wouldn't touch her with a 3-4-5 triangle.",
		"Yo mama is so square that she's got imaginary numbers on her social security card.",
		"Yo mama is such a ho, that she asked all the math majors to to figure out g(f(your mom)) just so they could \"f\" her first.",
		"The volume of yo mama is an improper integral.",
		"The integral of yo mama is fat plus a constant, where the constant is equal to more fat.",
		"Yo mama's muscle-to-fat ratio can only be explained in irrational complex numbers.",
		"The only way to get from point A to point B is around yo mama's fat ass.",
		"Yo mama's so smart, the hardest decision she's ever had to make was which college to accept a scholarship from - Harvard, Yale or Princeton!",
		"Yo mama's so clean, she could bottle her bathwater and sell it at the grocery store alongside Evian, Dasani and FIJI.",
		"Yo mama's so generous that she sponsors children in Africa, Asia AND South America!",
		"Yo mama's so popular that Facebook crashed on her birthday, because too many people posted wishes on her wall.",
		"Yo mama's such a good cook that her vegetable lasagna could be served as the featured item at a Michelin Star restaurant!",
		"Yo momma's so healthy that medical textbooks use her x-rays to demonstrate what perfect bone structure should look like.",
		"Yo mama's breath smells so fresh that Wrigley's could make a chewing gum flavour based on it.",
		"Yo mama's so fit that she could run a marathon, teach a Zumba class AND climb Mount Everest without stopping to catch her breath once.",
		"Yo mama's so fashionable that Gucci, Prada and Fendi call her on a daily basis to get insight into upcoming fashion trends.",
		"Yo mama's aging with such grace and beauty that she could be featured on the cover of Elle magazine.",
		"Yo mama's like a puppy... everybody wants to give her a hug.",
		"Yo mama's so smart that an employee from Wikipedia calls her when they need to verify facts about 18th century political figures",
		"Yo mama's so fat, when she fell I didn't laugh, but the sidewalk cracked up.",
		"Yo mama's so fat, when she skips a meal, the stock market drops.",
		"Yo mama's so fat, it took me two buses and a train to get to her good side.",
		"Yo mama's so fat, when she goes camping, the bears hide their food.",
		"Yo mama's so fat, if she buys a fur coat, a whole species will become extinct.",
		"Yo mama's so fat, she stepped on a scale and it said: \"To be continued.\"",
		"Yo mama's so fat, I swerved to miss her in my car and ran out of gas.",
		"Yo mama's so fat, when she wears high heels, she strikes oil.",
		"Yo mama's so fat, she was overthrown by a small militia group, and now she's known as the Republic of Yo Mama.",
		"Yo mama's so fat, when she sits around the house, she SITS AROUND the house.",
		"Yo mama's so fat, her car has stretch marks.",
		"Yo mama's so fat, her blood type is Ragu.",
		"Yo mama's so fat, if she was a Star Wars character, her name would be Admiral Snackbar.",
		"Yo mama's so fat, she brought a spoon to the Super Bowl."
	]))

    @commands.command(name="randomemote", aliases=["re", "randomcancer_", "randomcancer"])
    async def re(self, ctx: commands.Context):
        if ctx.channel.name == "poal48":
            emt = choice(bot.emts)
            if emt['data']['flags'] == 256: await ctx.send(f"frame145delay007s {emt['name']}")
            else: await ctx.send(f"{emt['name']}")
        if ctx.channel.name == "the_il_":
            emt = choice(bot.emtsil)
            if emt['data']['flags'] == 256: await ctx.send(f"frame145delay007s {emt['name']}")
            else: await ctx.send(f"{emt['name']}")
        if ctx.channel.name == "enihei":
            emt = choice(bot.emtshei)
            if emt['data']['flags'] == 256: await ctx.send(f"frame145delay007s {emt['name']}")
            else: await ctx.send(f"{emt['name']}")
        if ctx.channel.name == "shadowdemonhd_":
            emt = choice(bot.emtsdemon)
            if emt['data']['flags'] == 256: await ctx.send(f"frame145delay007s {emt['name']}")
            else: await ctx.send(f"{emt['name']}")
        if ctx.channel.name == "tatt04ek":
            emt = choice(bot.emts04)
            if emt['data']['flags'] == 256: await ctx.send(f"frame145delay007s {emt['name']}")
            else: await ctx.send(f"{emt['name']}")
        if ctx.channel.name == "alexoff35":
            emt = choice(bot.emtsoff)
            if emt['data']['flags'] == 256: await ctx.send(f"frame145delay007s {emt['name']}")
            else: await ctx.send(f"{emt['name']}")
        if ctx.channel.name == "red3xtop":
            emt = choice(bot.emtsred3x)
            if emt['data']['flags'] == 256: await ctx.send(f"frame145delay007s {emt['name']}")
            else: await ctx.send(f"{emt['name']}")
        if ctx.channel.name == "orlega_":
            emt = choice(bot.emtsorl)
            if emt['data']['flags'] == 256: await ctx.send(f"frame145delay007s {emt['name']}")
            else: await ctx.send(f"{emt['name']}")
        if ctx.channel.name == "wanderning_":
            emt = choice(bot.emtswand)
            if emt['data']['flags'] == 256: await ctx.send(f"frame145delay007s {emt['name']}")
            else: await ctx.send(f"{emt['name']}")
        if ctx.channel.name == "echoinshade":
            emt = choice(bot.emtsecho)
            if emt['data']['flags'] == 256: await ctx.send(f"frame145delay007s {emt['name']}")
            else: await ctx.send(f"{emt['name']}")
        if ctx.channel.name == "erynga":
            emt = choice(bot.emtserynga)
            if emt['data']['flags'] == 256: await ctx.send(f"frame145delay007s {emt['name']}")
            else: await ctx.send(f"{emt['name']}")

    @commands.command(name="updateemotes")
    async def updateemotes(self, ctx: commands.Context):
        if ctx.author.name in self.USERDATA['mods']:
            asd = cdcs.open("temp.emt", 'w', 'utf8')
            asd.write(req.get("https://7tv.io/v3/emote-sets/6301dcecf7723932b45c06b0").text)
            asd.close()
            asd = cdcs.open("temp.emt", 'r', 'utf8')
            self.emts = json.load(asd)
            asd.close()
            os.remove("temp.emt")
            self.emts = self.emts['emotes']
            self.emtsil = req.get("https://7tv.io/v3/emote-sets/62b36e38765d72b656d6e985").json()['emotes']
            self.emtshei = req.get("https://7tv.io/v3/emote-sets/63c43185219a2920cb348329").json()['emotes']
            self.emtsdemon = req.get("https://7tv.io/v3/emote-sets/6330291d9474f0aac65a0488").json()['emotes']
            self.emts04 = req.get("https://7tv.io/v3/emote-sets/6106a52a3ed2ea3f60da4d58").json()['emotes']
            self.emtsoff = req.get("https://7tv.io/v3/emote-sets/6414ce0a220f8400b8783ce6").json()['emotes']
            self.emtsred3x = req.get("https://7tv.io/v3/emote-sets/63191283b2ef04bef5df01a3").json()['emotes']
            self.emtsorl = req.get("https://7tv.io/v3/emote-sets/63e146945d4acdefd44791d5").json()['emotes']
            self.emtswand = req.get("https://7tv.io/v3/emote-sets/631db3cc4f3e0f1fc59fa8d9").json()['emotes']
            self.emtsecho = req.get("https://7tv.io/v3/emote-sets/647ef56b28b72684e122574c").json()['emotes']
            self.emtserynga = req.get("https://7tv.io/v3/emote-sets/64a2c96712c2ceffb1120915").json()['emotes']
            print("\nEmotes loaded!\n")
            resp = req.get("https://7tv.io/v3/emote-sets/61c802080bf6300371940381").json()
            for i in range(len(resp['emotes'])):
                if resp['emotes'][i]['name'] in self.USERDATA['pwemts'].keys(): pass
                else:
                    self.USERDATA['pwemts'][resp['emotes'][i]['name']] = {'id': resp['emotes'][i]['id'], 'used': 0, 'pause': False}
            self.saveUserData()
            print("\nPWGood 7tv emotes loaded!\n")
            await ctx.send("Эмоуты обновлены! Zaebok")

    @commands.command(name="execute", aliases=["exec"])
    async def execute__(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            try:
                content = str0list0split(ctx.message.content, listcut=(0,0)).str
                cnt = ""
                for i in range(len(content)):
                    try:
                        This = content[i]
                        if content[i:i+3] == "=n ":
                            This = "\n"
                            content = content[0:i] + content[i+2:len(content)]
                        cnt += This
                    except IndexError: pass
                content = cnt
                cnt = ""
                for i in range(len(content)):
                    try:
                        This = content[i]
                        if content[i:i+3] == "=t ":
                            This = "    "
                            content = content[0:i] + content[i+2:len(content)]
                        cnt += This
                    except IndexError: pass
                self.write = None
                self.write500 = None
                self.writeIn = None
                exec(cnt)
                if self.write != None: await ctx.send(str(self.write))
                if self.write500!=None:await self.more500send(ctx, str(self.write500))
                if self.writeIn != None:
                    if len(self.writeIn) == 2 and type(self.writeIn) == type([]): await self.get_channel(self.writeIn[0]).send(self.writeIn[1])
            except Exception as e:
                await ctx.send(f"THIS эта ошибка возникла! {e}")


    def preadankthread(self, ctx, i):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.adankthread(ctx, i))
        loop.close()

    async def adankthread(self, ctx, i):
        while True:
            if self.danks[i]['Error'] == '-1':
                break
            elif self.danks[i]['Error'] != '0':
                if self.danks[i]['Error'] == '1':
                    await ctx.send(f"THIS Ошибка питона!: {self.danks[i]['Return']}")
                    return
                if self.danks[i]['Error'] == '2':
                    await ctx.reply("Хуй Пенис, открывать файлы нельзя")
                    return
                if self.danks[i]['Error'] == '3':
                    await ctx.reply("HARAM Error")
                    return
            #print((self.danks[i]['Time'] - dt.datetime.now()).total_seconds())
            if (dt.datetime.now() - self.danks[i]['Time']).total_seconds() >= 30:
                await ctx.reply(f"THIS твоя программа работает слишком долго!")
                self.danks[i]['Thread'].do_run = False
                return
        await ctx.send(str(self.danks[i]['Return']))

    '''@commands.command(name="python", aliases=["pt", "dankdebug"])
    async def dankidebugik(self, ctx: commands.Context):
        try:
            cnt = str0list0split(ctx.message.content)
            cnt.listcut(0, 0)
            content = cnt.str
            if not content:
                await ctx.send("Строка не введена. Доки: (Чувак, ты думаел здесь что то будет Something )")
                return
            cnt = ""
            for i in range(len(content)):
                try:
                    This = content[i]
                    if content[i:i+3] == "=n ":
                        This = "\n"
                        content = content[0:i] + content[i+2:len(content)]
                    cnt += This
                except IndexError: pass
            content = cnt
            cnt = ""
            for i in range(len(content)):
                try:
                    This = content[i]
                    if content[i:i+3] == "=t ":
                        This = "    "
                        content = content[0:i] + content[i+2:len(content)]
                    cnt += This
                except IndexError: pass
            content = cnt
            cnt = ""
            if "botinok_" in content:
                content = ""
                cnt = "raise HARAMERROR"
            if "global" in content:
                content = ""
                cnt = "raise HARAMERROR"
            for i in range(len(content)):
                try:
                    This = content[i]
                    if content[i:i+3] == "=r ":
                        This = f"botinok_.danks[{len(self.danks)}]['Return']="
                        content = content[0:i] + content[i+2:]
                    cnt += This
                except IndexError: pass
            if "open" in cnt: cnt = "raise OPENERROR"
            """content = cnt
            cnt = ""
            for i in range(len(content)):
                try:
                    This = content[i]
                    if content[i:i+4] == "=or """"
            self.danks.append({'Error': '0', 'Return': None, 'Thread': thrd.Thread(target=dankthread, args=(ctx, cnt, len(self.danks), self)), 'PREaThread': thrd.Thread(target=self.preadankthread, args=(ctx, len(self.danks))), 'Time': dt.datetime.now()})
            self.danks[len(self.danks)-1]['Thread'].start()
            self.danks[len(self.danks)-1]['PREaThread'].start()
        except Exception as e: await ctx.send(f"Возникла ошибка с преобразованием говна: {e}")

    @commands.command(name="file")
    async def fileKOROCHEaliasbl(self, ctx: commands.Context):
        cnt = str0list0split(ctx.message.content)
        cnt.listcut(0, 0)
        if cnt.list[0] == "load":
            cnt.listcut(0, 0)
            await self.fileLoad(ctx, cnt.str)
        elif cnt.list[0] == "copy":
            cnt.listcut(0, 0)
            await self.fileCopy(ctx, cnt)
        elif cnt.list[0] == "info":
            cnt.listcut(0, 0)
            await self.fileInfo(ctx, cnt.str)
        elif cnt.list[0] == "remove" or cnt.list[0] == "delete":
            cnt.listcut(0, 0)
            await self.fileRemove(ctx, cnt.str)
        elif cnt.list[0] == "rename":
            cnt.listcut(0, 0)
            await self.fileRename(ctx, cnt)
        else:
            await self.filePlay(ctx, cnt.str)

    async def fileRename(self, ctx, cnt):
        try: self.USERDATA['files'][ctx.author.name][cnt.list[0]]
        except KeyError:
            await ctx.send(f"У тебя нет файла {cnt.list[0]}")
            return
        self.USERDATA['files'][ctx.author.name][cnt.list[1]] = self.USERDATA['files'][ctx.author.name][cnt.list[0]]
        self.USERDATA['files'][ctx.author.name].pop(cnt.list[0])
        self.saveUserData()
        await ctx.send(f"Твой файл {cnt.list[0]} переиминован в {cnt.list[1]}")

    async def fileRemove(self, ctx, cnt):
        try: self.USERDATA['files'][ctx.author.name][cnt]
        except KeyError:
            await ctx.send(f"У тебя нету файла \"{cnt}\"")
            return
        self.USERDATA['files'][ctx.author.name].pop(cnt)
        self.saveUserData()
        await ctx.send(f"Файл \"{cnt}\" успешно удален!")

    async def fileInfo(self, ctx, cnt):
        try: self.USERDATA['files'][ctx.author.name][cnt]
        except KeyError:
            await ctx.send(f"У тебя нет файла {cnt}")
            return
        tf = cdcs.open("temp.file", 'w', 'utf-8')
        tf.write(self.USERDATA['files'][ctx.author.name][cnt]['data'])
        tf.close()
        tf = cdcs.open("temp.file", 'r', 'utf-8')
        resp = req.post("https://gachi.gay/api/upload", files={"file": tf}).json()
        tf.close()
        await ctx.send(f"Файл: {cnt} , Автор: {self.USERDATA['files'][ctx.author.name][cnt]['author']} , Дата: {resp['link']}")

    async def fileLoad(self, ctx, cnt):
        try: self.USERDATA['files'][ctx.author.name]
        except KeyError: self.USERDATA['files'][ctx.author.name] = {}
        asd = req.get(f"{cnt.split()[0].strip()}").text
        cntt = str0list0split(cnt)
        cntt.listcut(0, 0)
        cnt = cntt.str
        self.USERDATA['files'][ctx.auhtor.name][cnt] = {}
        self.USERDATA['files'][ctx.author.name][cnt]['data'] = asd
        self.USERDATA['files'][ctx.author.name][cnt]['author']=ctx.author.name
        self.saveUserData()
        await ctx.send(f"Твой файл сохранен как {cnt}")

    async def fileCopy(self, ctx, cnt):
        tca = cnt.list[0].lower() #to copy author
        cnt.listcut(0, 0)
        cnt = cnt.str
        #try:
        self.USERDATA['files'][tca][cnt]
        #except KeyError:
            #await ctx.send("У данного пользователя нет такого файла! FeelsWeirdMan ")
            #return
        try: self.USERDATA['files'][ctx.author.name]
        except KeyError: self.USERDATA['files'][ctx.author.name] = {}
        self.USERDATA['files'][ctx.author.name][cnt] = {}
        self.USERDATA['files'][ctx.author.name][cnt]['data'] = self.USERDATA['files'][tca][cnt]['data']
        self.USERDATA['files'][ctx.author.name][cnt]['author']= self.USERDATA['files'][tca][cnt]['author']
        self.saveUserData()
        await ctx.send(f"Ты успешно скопировал файл {cnt} у {tca} peepoHappy")

    async def filePlay(self, ctx, cnt):
        try:
            if not cnt:
                await ctx.send("Строка не введена. Доки: (Чувак, ты думаел здесь что то будет Something )")
                return
            try:
                cnt = self.USERDATA['files'][ctx.author.name][cnt]['data']
            except KeyError:
                await ctx.send(f"У тебя не файла {cnt}")
                return
            content = cnt
            cnt = ""
            if "botinok_" in content:
                content = ""
                cnt = "raise HARAMERROR"
            if "global" in content:
                content = ""
                cnt = "raise HARAMERROR"
            for i in range(len(content)):
                try:
                    This = content[i]
                    if content[i:i+3] == "=r ":
                        This = f"botinok_.danks[{len(self.danks)}]['Return']="
                        content = content[0:i] + content[i+2:]
                    cnt += This
                except IndexError: pass
            if "open" in cnt: cnt = "raise OPENERROR"
            """content = cnt
            cnt = ""
            for i in range(len(content)):
                try:
                    This = content[i]
                    if content[i:i+4] == "=or """"
            self.danks.append({'Error': '0', 'Return': None, 'Thread': thrd.Thread(target=dankthread, args=(ctx, cnt, len(self.danks), self)), 'PREaThread': thrd.Thread(target=self.preadankthread, args=(ctx, len(self.danks))), 'Time': dt.datetime.now()})
            self.danks[len(self.danks)-1]['Thread'].start()
            self.danks[len(self.danks)-1]['PREaThread'].start()
        except Exception as e: await ctx.send(f"Возникла ошибка с преобразованием говна: {e}")'''

    @commands.command(name="submassping", aliases=["notifysub", "notify", "сабмасстык", "масстык"])
    async def submassping(self, ctx: commands.Context):
        if ctx.channel.name == "poal48":
            if ctx.author.display_name in self.USERDATA['massping']:
                #await ctx.reply("Ты уже есть в списочке на масс тык! FeelsOkayMan ")
                self.USERDATA['massping'].remove(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Ты отписался от масс тыка Disappointed ")
            else:
                self.USERDATA['massping'].append(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Ты в списочке! DankG ")
        if ctx.channel.name == "the_il_":
            if ctx.author.display_name in self.USERDATA['IL']['massping']:
                #await ctx.reply("Ты уже с списочке на масс тык! FeelsOkayMan ")
                self.USERDATA['IL']['massping'].remove(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Ты отписался от масс тыка Disappointed ")
            else:
                self.USERDATA['IL']['massping'].append(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Записал тебя в списочек на масс тык! PepoG")
        if ctx.channel.name == "enihei":
            if ctx.author.display_name in self.USERDATA['enihei']['massping']:
                #await ctx.reply("Ты уже с списочке на масс тык! Okayge ")
                self.USERDATA['enihei']['massping'].remove(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Ты отписался от масс тыка SAJ ")
            else:
                self.USERDATA['enihei']['massping'].append(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Записал тебя в списочек на масс тык! PepoG ")
        if ctx.channel.name == "shadowdemonhd_":
            if ctx.author.display_name in self.USERDATA['demon']['massping']:
                #await ctx.reply("Ты уже с списочке на масс тык! FeelsOkayMan ")
                self.USERDATA['demon']['massping'].remove(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Ты отписался от масс тыка Monday ")
            else:
                self.USERDATA['demon']['massping'].append(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Записал тебя в списочек на масс тык! PepoG ")
        if ctx.channel.name == "tatt04ek":
            if ctx.author.display_name in self.USERDATA['tatt04ek']['massping']:
                #await ctx.reply("Ты уже с списочке на масс тык! Okayge ")
                self.USERDATA['tatt04ek']['massping'].remove(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Ты отписался от масс тыка SAJ ")
            else:
                self.USERDATA['tatt04ek']['massping'].append(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Записал тебя в списочек на масс тык! yaderka ")
        if ctx.channel.name == "red3xtop":
            if ctx.author.display_name in self.USERDATA['red3x']['massping']:
                #await ctx.reply("Ты уже с списочке на масс тык! peepoKotleta ")
                self.USERDATA['red3x']['massping'].remove(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Ты отписался от масс тыка Disappointed ")
            else:
                self.USERDATA['red3x']['massping'].append(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Записал тебя в списочек на масс тык! essaying ")
        if ctx.channel.name == "orlega_":
            if ctx.author.display_name in self.USERDATA['orlega_']['massping']:
                #await ctx.reply("Ты уже с списочке на масс тык! uuh ")
                self.USERDATA['orlega_']['massping'].remove(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Ты отписался от масс тыка yaderka ")
            else:
                self.USERDATA['orlega_']['massping'].append(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Записал тебя в списочек на масс тык! pwgoodG ")
        if ctx.channel.name == "wanderning_":
            if ctx.author.display_name in self.USERDATA['wanderning_']['massping']:
                #await ctx.reply("Ты уже с списочке на масс тык! uuh ")
                self.USERDATA['wanderning_']['massping'].remove(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Ты отписался от масс тыка uuh ")
            else:
                self.USERDATA['wanderning_']['massping'].append(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Записал тебя в списочек на масс тык! rilobulion ")
        if ctx.channel.name == "echoinshade":
            if ctx.author.display_name in self.USERDATA['echo']['massping']:
                #await ctx.reply("Ты уже с списочке на масс тык! uuh ")
                self.USERDATA['echo']['massping'].remove(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Ты отписался от масс тыка Disappointed ")
            else:
                self.USERDATA['echo']['massping'].append(ctx.author.display_name)
                self.saveUserData()
                await ctx.reply("Записал тебя в списочек на масс тык! catBombing ")

    @commands.command(name="masspingedit")
    async def masspingedit(self, ctx: commands.Context):
        chnl = None
        if ctx.author.name == "poal48" and ctx.channel.name == "poal48":
            cnt = str0list0split(ctx.message.content, listcut=(0, 0))
            if cnt.list[0] == "add":
                self.USERDATA['massping'].append(cnt.list[1])
                self.saveUserData()
                await ctx.reply(f"Добавил {cnt.list[1]} к масс тыку PepoG")
            if cnt.list[0] == "remove":
                try:
                    self.USERDATA['massping'].remove(cnt.list[1])
                    self.saveUserData()
                    await ctx.reply(f"Успешно удалил {cnt.list[1]} из масс тыка yaderka")
                except ValueError: await ctx.reply(f"Не нашел {cnt.list[1]} в списке масс тыка! uuh")
        if (ctx.author.name == "poal48" or ctx.author.name == "the_il_") and ctx.channel.name == "the_il_":
            chnl = "IL"
        if (ctx.author.name == "poal48" or ctx.author.name == "enihei") and ctx.channel.name == "enihei":
            chnl = "enihei"
        if (ctx.author.name == "poal48" or ctx.author.name == "shadowdemonhd_") and ctx.channel.name == "shadowdemonhd_":
            chnl = "demon"
        if (ctx.author.name == "poal48" or ctx.author.name == "tatt04ek") and ctx.channel.name == "tatt04ek":
            chnl = "tatt04ek"
        if (ctx.author.name == "poal48" or ctx.author.name == "red3xtop") and ctx.channel.name == "red3xtop":
            chnl = "red3x"
        if (ctx.author.name == "poal48" or ctx.author.name == "orlega_") and ctx.channel.name == "orlega_":
            chnl = "orlega_"
        if (ctx.author.name == "poal48" or ctx.author.name == "wanderning_") and ctx.channel.name == "wanderning_":
            chnl = "wanderning_"
        if (ctx.author.name == "poal48" or ctx.author.name == "echoinshade") and ctx.channel.name == "echoinshade":
            chnl = "echo"
        if chnl:
            cnt = str0list0split(ctx.message.content, listcut=(0, 0))
            if cnt.list[0] == "add":
                self.USERDATA[chnl]['massping'].append(cnt.list[1])
                self.saveUserData()
                await ctx.reply(f"Добавил {cnt.list[1]} к масс тыку PepoG")
            if cnt.list[0] == "remove":
                try:
                    self.USERDATA[chnl]['massping'].remove(cnt.list[1])
                    self.saveUserData()
                    await ctx.reply(f"Успешно удалил {cnt.list[1]} из масс тыка yaderka")
                except ValueError: await ctx.reply(f"Не нашел {cnt.list[1]} в списке масс тыка! uuh")
            
            

    @commands.command(name="domassping")
    async def domassping(self, ctx: commands.Context):
        if ctx.author.name == "poal48" and ctx.channel.name == "poal48":
            cnt = str0list0split(ctx.message.content)
            cnt.listcut(0, 0)
            massPing = " ".join(self.USERDATA['massping'])
            try:
                await self.more500send(ctx, massPing, start=cnt.list[0], end=cnt.list[1])
            except IndexError:
                await self.more500send(ctx, massPing)
        if (ctx.author.name == "poal48" or ctx.author.name == "the_il_") and ctx.channel.name == "the_il_":
            await self.more500send(ctx, " ".join(self.USERDATA['IL']['massping']), start="ppBounce", end = "ppBounce")
        if (ctx.author.name == "poal48" or ctx.author.name == "enihei") and ctx.channel.name == "enihei":
            await self.more500send(ctx, " ".join(self.USERDATA['enihei']['massping']), start="NOWAY", end = "NOWAY")
        if (ctx.author.name == "poal48" or ctx.author.name == "shadowdemonhd_") and ctx.channel.name == "shadowdemonhd_":
            await self.more500send(ctx, " ".join(self.USERDATA['demon']['massping']), start="NOWAY", end = "NOWAY")
        if (ctx.author.name == "poal48" or ctx.author.name == "tatt04ek") and ctx.channel.name == "tatt04ek":
            await self.more500send(ctx, " ".join(self.USERDATA['tatt04ek']['massping']), start="plink", end = "plonk")
        if (ctx.author.name == "poal48" or ctx.author.name == "red3xtop") and ctx.channel.name == "red3xtop":
            await self.more500send(ctx, " ".join(self.USERDATA['red3x']['massping']), start="cat3", end = "cat3")
        if (ctx.author.name == "poal48" or ctx.author.name == "orlega_") and ctx.channel.name == "orlega_":
            await self.more500send(ctx, " ".join(self.USERDATA['orlega_']['massping']), start="stare", end = "stare")
        if (ctx.author.name == "poal48" or ctx.author.name == "wanderning_") and ctx.channel.name == "wanderning_":
            await self.more500send(ctx, " ".join(self.USERDATA['wanderning_']['massping']), start="Zaebok", end = "Zaebok")
        if (ctx.author.name == "poal48" or ctx.author.name == "echoinshade") and ctx.channel.name == "echoinshade":
            await self.more500send(ctx, " ".join(self.USERDATA['echo']['massping']), start="catBombing", end = "catBombing")

    def saveUserData(self):
        THIS = cdcs.open("USERDATA.data", 'w', 'utf-8')
        json.dump(self.USERDATA, THIS)
        THIS.close()

    @commands.command(name="spauth")
    async def spauth(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            await ctx.send("Проследуй командам в консоли EZ")
            resp = req.get("https://clck.ru/--", params={'url': "https://accounts.spotify.com/authorize?" +  \
                'response_type' + '=' + "code" + "&" \
                "client_id" + '=' + CFG['sp_client_id'] + "&" \
                "scope" + '=' + 'ugc-image-upload user-read-playback-state app-remote-control user-modify-playback-state'\
                    ' playlist-read-private user-follow-modify playlist-read-collaborative user-follow-read'\
                    ' user-read-currently-playing user-read-playback-position user-library-modify'\
                    ' playlist-modify-private playlist-modify-public user-read-email user-top-read '\
                    ' user-read-recently-played user-read-private user-library-read' + "&" \
                "redirect_uri" + '=' + "http://денис.space/" }).text
            print(f"\n\n\nАвторизация Spotify\n{resp}\nКод сюда же\n")
            self.sp_code = input()
            print("\nКод принят, получаю токен...\n")
            resp = req.post("https://accounts.spotify.com/api/token", params={\
                "grant_type": "authorization_code", \
                "code": self.sp_code, \
                "redirect_uri": "http://денис.space/"}, headers={\
                "Authorization": f"Basic {CFG['sp_based']}", \
                "Content-Type": "application/x-www-form-urlencoded"}\
                ).json()
            print(resp)
            self.sp_token = resp['access_token']
            self.sp_refresh = resp['refresh_token']
            print("\nТокен получен!\n")
            try:
                resp = req.get("https://api.spotify.com/v1/me/player", headers={\
                'Authorization': f"Bearer {self.sp_token}", \
                'Content-Type': "application/json"}).json()
                print(f"\nСейчас играет: {resp['item']['name']} - {resp['item']['artists'][0]['name']}\n")
            except Exception: print("\nМузыка не играет!\n")
            thrd.Thread(target=self.spreauth).start()
            print("Конец связи!")
            await asyncio.sleep(2)
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print("\n\n\n\n\n\\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    def spreauth(self, who):
        sleep(3610)
        resp = req.post("https://accounts.spotify.com/api/token", params={\
            'grant_type': "refresh_token",\
            'refresh_token': self.sp_data[who]['refresh']}, headers={\
            'Authorization': f"Basic {CFG['sp_based']}", \
            'Content-Type': "application/x-www-form-urlencoded"}).json()
        self.sp_data[who]['access'] = resp['access_token']
        try: self.sp_refresh[who]['refresh'] = resp['refresh_token']
        except KeyError: print("refresh token get failed, use old refresh token")
        thrd.Thread(target=self.spreauth, args=(who, )).start()

    @commands.command(name="spauthStep2")
    async def spauthStep2(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            resp = req.post("https://accounts.spotify.com/api/token", params={\
                "grant_type": "authorization_code", \
                "code": f"{self.sp_code}", \
                "redirect_uri": "http://денис.space/"}, headers={\
                "Authorization": f"Basic {CFG['sp_based']}", \
                "Content-Type": "application/x-www-form-urlencoded"}\
                ).text
            print(resp)

    @commands.command(name="sptest")
    async def sptest(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            resp = req.get("https://api.spotify.com/v1/me/player", headers={\
                'Authorization': f"Bearer {self.sp_token}", \
                'Content-Type': "application/json"}).json()
            #await self.more500send(ctx, str(resp['item']))
            await ctx.send(resp['item']['artists'][0]['name'])
            await ctx.send(resp['item']['name'])
            await ctx.send(resp['item']['external_urls']['spotify'])

    @commands.command(name="sr", aliases=["songrequest", "ср"])
    async def sr(self, ctx: commands.Context):
        if ctx.channel.name == "poal48" or ctx.channel.name == "enihei" or ctx.channel.name == "tatt04ek" or ctx.channel.name == "shadowdemonhd_" or ctx.channel.name == "orlega_":
            who = ctx.channel.name
            if not self.USERDATA['spotify'][who]['sr']['enabled']:
                await ctx.reply("Сонг реквесты выключены сейчас pwgoodDespair")
                return
            if self.USERDATA['spotify'][who]['sr']['id'] == "None":
                await ctx.reply("Стример не установил плей-лист для сров, скажи ему об этом!")
            self.updateSpotifySongs(who)
            content = str0list0split(ctx.message.content)
            content.listcut(0, 0)
            skipSearch = False
            for i in range(len(content.list)):
                if "youtube.com/watch" in content.list[i] or "youtu.be/" in content.list[i]:
                    #await ctx.reply("Мы пока не принимает ссылки с ютуба, введи название трека или прямую ссылку на \"open.spotify.com/123\"")
                    #return
                    skipSearch = True
                    slResp = req.get("https://api.song.link/v1-alpha.1/links", params={\
                        'url': content.list[i]}).json()
                    try:
                        trackId = slResp['linksByPlatform']['spotify']['nativeAppUriDesktop'].split(':')[2]
                        resp = req.get(f"https://api.spotify.com/v1/tracks/{trackId}", headers={\
                            'Authorization': f"Bearer {self.sp_data[who]['access']}", \
                            'Content-Type': "application/json"}).json()
                        track = resp
                    except KeyError:
                        await ctx.reply(f"Не нашли такую же песню на spotify uuh")
                        return
                if "https://open.spotify.com/track/" in content.list[i]:
                    skipSearch = True
                    trackId = content.list[i].split("https://open.spotify.com/track/")[1]
                    trackId = trackId.split("?si")[0]
                    resp = req.get(f"https://api.spotify.com/v1/tracks/{trackId}", headers={\
                        'Authorization': f"Bearer {self.sp_data[who]['access']}", \
                        'Content-Type': "application/json"}).json()
                    track = resp
            if not skipSearch:
                cnt = content.str
                resp = req.get("https://api.spotify.com/v1/search", params={\
                    'q': cnt, \
                    'type': "track", \
                    'limit': 1}, headers={\
                    'Authorization': f"Bearer {self.sp_data[who]['access']}", \
                    'Content-Type': "application/json"}).json()
                track = resp['tracks']['items'][0]
            ex = ""
            if track['explicit']: ex += f" (Этот трек с пометкой E, будь осторожен {ctx.channel.name} )"
            resp = req.get(f"https://api.spotify.com/v1/playlists/{self.USERDATA['spotify'][who]['sr']['id']}", headers={\
                'Authorization': f"Bearer {self.sp_data[who]['access']}", \
                'Content-Type': "application/json"}).json()
            for i in range(len(resp['tracks']['items'])):
                if track['uri'] == resp['tracks']['items'][i]['track']['uri']:
                    await ctx.reply("Этот трек уже есть в очереди!")
                    return
            pos = resp['tracks']['total']
            resp = req.post(f"https://api.spotify.com/v1/playlists/{self.USERDATA['spotify'][who]['sr']['id']}/tracks", params={\
                'position': pos,\
                'uris': track['uri']}, headers={\
                'Authorization': f"Bearer {self.sp_data[who]['access']}", \
                'Content-Type': "application/json"})
            self.USERDATA['spotify'][who]['sr']['songs'].append({\
                'name': track['name'], 'artist': track['artists'][0]['name'], \
                'uri': track['uri'], 'by': ctx.author.display_name})
            self.saveUserData()
            await ctx.reply(f"Трек {track['name']} - {track['artists'][0]['name']} успешно встал в очередь в позиции {pos+1}, напиши *csr если он неверен!" + ex)

    @commands.command(name="csr")
    async def csr(self, ctx: commands.Context):
        if ctx.channel.name == "poal48" or ctx.channel.name == "enihei" or ctx.channel.name == "tatt04ek" or ctx.channel.name == "shadowdemonhd_" or ctx.channel.name == "orlega_":
            who = ctx.channel.name
            cnsl = "None"
            for i in range(len(self.USERDATA['spotify'][who]['sr']['songs'])):
                if self.USERDATA['spotify'][who]['sr']['songs'][i]['by'] == ctx.author.display_name:
                    cnsl = self.USERDATA['spotify'][who]['sr']['songs'][i]
            if cnsl == "None":
                await ctx.reply("Не нашел ни одного твоего трека в сонг реквестах")
                return
            req.delete(f"https://api.spotify.com/v1/playlists/{self.USERDATA['spotify'][who]['sr']['id']}/tracks", json={\
                       'tracks': [{'uri': cnsl['uri']}]}, headers={\
                        'Authorization': f"Bearer {self.sp_data[who]['access']}", \
                        'Content-Type': "application/json"}).json()
            self.USERDATA['spotify'][who]['sr']['songs'].remove(cnsl)
            await ctx.reply(f"Успешно удалил {cnsl['name']} - {cnsl['artist']} из сонг реквестов")

    @commands.command(name="usr")
    async def updatesr(self, ctx: commands.Context):
        if (ctx.author.name == "poal48") or (ctx.author.name == "enihei" and ctx.channel.name == "enihei") or (ctx.author.name == "tatt04ek" and ctx.channel.name == "tatt04ek") or (ctx.author.name == "shadowdemonhd_" and ctx.channel.name == "shadowdemonhd_") or (ctx.channel.name == "orlega_" and ctx.channel.name == "orlega_"):
            who = ctx.channel.name
            tracks = req.get(f"https://api.spotify.com/v1/playlists/{self.USERDATA['spotify'][who]['sr']['id']}", headers={\
                'Authorization': f"Bearer {self.sp_data[who]['access']}", \
                'Content-Type': "application/json"}).json()['tracks']['items']
            for i in range(len(tracks)):
                try:
                    if tracks[i]['track']['uri'] == self.USERDATA['spotify'][who]['sr']['songs'][i]['uri']:
                        continue
                    else:
                        self.USERDATA['spotify'][who]['sr']['songs'][i] = "D"
                except IndexError: pass
            while "D" in self.USERDATA['spotify'][who]['sr']['songs']: self.USERDATA['spotify'][who]['sr']['songs'].remove("D")
            self.saveUserData()
            await ctx.send("Список сонг реквестов обновлен")

    @commands.command(name="clrsr")
    async def clrsr(self, ctx: commands.Context):
        if (ctx.author.name == "poal48") or (ctx.author.name == "enihei" and ctx.channel.name == "enihei") or (ctx.author.name == "tatt04ek" and ctx.channel.name == "tatt04ek") or (ctx.author.name == "shadowdemonhd_" and ctx.channel.name == "shadowdemonhd_") or (ctx.channel.name == "orlega_" and ctx.channel.name == "orlega_"):
            who = ctx.channel.name
            tracks = req.get(f"https://api.spotify.com/v1/playlists/{self.USERDATA['spotify'][who]['sr']['id']}", headers={\
                'Authorization': f"Bearer {self.sp_data[who]['access']}", \
                'Content-Type': "application/json"}).json()['tracks']['items']
            uris = []
            for i in range(len(tracks)):
                uris.append({'uri': tracks[i]['track']['uri']})
            req.delete(f"https://api.spotify.com/v1/playlists/{self.USERDATA['spotify'][who]['sr']['id']}/tracks", json={\
                       'tracks': tracks}, headers={\
                        'Authorization': f"Bearer {self.sp_data[who]['access']}", \
                        'Content-Type': "application/json"}).json()
            self.USERDATA['spotify'][who]['sr']['songs'] = []
            self.saveUserData()

    @commands.command(name="srturn")
    async def srturn(self, ctx: commands.Context):
        if (ctx.author.name == "poal48") or (ctx.author.name == "enihei" and ctx.channel.name == "enihei") or (ctx.author.name == "tatt04ek" and ctx.channel.name == "tatt04ek") or (ctx.author.name == "shadowdemonhd_" and ctx.channel.name == "shadowdemonhd_") or (ctx.channel.name == "orlega_" and ctx.channel.name == "orlega_"):
            who = ctx.channel.name
            cnt = str0list0split(ctx.message.content, listcut=(0,0)).list[0]
            if cnt != "off" and cnt != "on":
                await ctx.send("Неверное состояние сонг реквестов, только on или off!")
                return
            if cnt == "off":
                self.USERDATA['spotify'][who]['sr']['enabled'] = False
                await ctx.send("Сонг реквесты выключены!")
            if cnt == "on":
                if self.USERDATA['spotify'][who]['sr']['id'] == "None":
                    await ctx.reply("У тебя не установлен плей-лист для сров. Установи его с помощью *srset <Ссылка>")
                    return
                self.USERDATA['spotify'][who]['sr']['enabled'] = True
                await ctx.send("Сонг реквесты включены!")
            self.saveUserData()

    @commands.command(name="srset")
    async def srset(self, ctx: commands.Context):
        if (ctx.author.name == "poal48") or (ctx.author.name == "enihei" and ctx.channel.name == "enihei") or (ctx.author.name == "tatt04ek" and ctx.channel.name == "tatt04ek") or (ctx.author.name == "shadowdemonhd_" and ctx.channel.name == "shadowdemonhd_") or (ctx.channel.name == "orlega_" and ctx.channel.name == "orlega_"):
            who = ctx.channel.name
            cnt = str0list0split(ctx.message.content, listcut=(0, 0)).list[0]
            plstId = cnt.split("https://open.spotify.com/playlist/")[1]
            plstId = plstId.split("?si")[0]
            self.USERDATA['spotify'][who]['sr']['id'] = plstId
            self.saveUserData()
            try:
                resp = req.get(f"https://api.spotify.com/v1/playlists/{self.USERDATA['spotify'][who]['sr']['id']}", headers={\
                'Authorization': f"Bearer {self.sp_data[who]['access']}", \
                'Content-Type': "application/json"}).json()
                await ctx.send(f"Плей-лист для сонг реквестов установлен, его название {resp['name']}")
            except KeyError:
                await ctx.send("Ошибка при получении плей-листа, попробуй снова, хз")
                self.USERDATA['spotify'][who]['sr']['id'] = "None"
                self.saveUserData()

    def updateSpotifySongs(self, who):
        try: nowPlay = req.get("https://api.spotify.com/v1/me/player", headers={\
                        'Authorization': f"Bearer {self.sp_data[who]['access']}", \
                        'Content-Type': "application/json"}).json()['item']['uri']
        except Exception: return
        tracks = []
        for i in range(len(self.USERDATA['spotify'][who]['sr']['songs'])):
            if nowPlay != self.USERDATA['spotify'][who]['sr']['songs'][i]['uri']:
                tracks.append({'uri': self.USERDATA['spotify'][who]['sr']['songs'][i]['uri']})
                self.USERDATA['spotify'][who]['sr']['songs'][i] = "D"
            else:
                break
        if len(tracks) > 0:
            req.delete(f"https://api.spotify.com/v1/playlists/{self.USERDATA['spotify'][who]['sr']['id']}/tracks", json={\
                       'tracks': tracks}, headers={\
                        'Authorization': f"Bearer {self.sp_data[who]['access']}", \
                        'Content-Type': "application/json"}).json()
        while "D" in self.USERDATA['spotify'][who]['sr']['songs']: self.USERDATA['spotify'][who]['sr']['songs'].remove("D")
        self.saveUserData()

    @commands.command(name="song", aliases=["сонг", "песня"])
    async def song(self, ctx: commands.Context):
        if ctx.channel.name == "poal48" or ctx.channel.name == "enihei" or ctx.channel.name == "tatt04ek" or ctx.channel.name == "shadowdemonhd_" or ctx.channel.name == "orlega_":
            who = ctx.channel.name
            if self.USERDATA['spotify'][who]['sr']['enabled']: self.updateSpotifySongs(who)
            try:
                resp = req.get("https://api.spotify.com/v1/me/player", headers={\
                        'Authorization': f"Bearer {self.sp_data[who]['access']}", \
                        'Content-Type': "application/json"}).json()
                slResp = req.get("https://api.song.link/v1-alpha.1/links", params={\
                        'url': resp['item']['external_urls']['spotify']}).json()
                try: _link = f"Ссылка song link: {slResp['pageUrl']}"
                except KeyError: _link = f"Ссылка spotify: {resp['item']['external_urls']['spotify']}"
                await ctx.reply(f"Сейчас играет {resp['item']['name']} - {resp['item']['artists'][0]['name']}. {_link}")
            except Exception as e:
                if type(e) == type(KeyError()):
                    await ctx.reply(f"Стример не авторизован в спотифай, или произошла не привиденная ошибка!")
                else:
                    await ctx.reply("Произошла непридвиденая ошибка или музыка не играет! Попробуй позже!")

    @commands.command(name="songlist", aliases=["сонглист"])
    async def songlist(self, ctx: commands.Context):
        if ctx.channel.name == "poal48" or ctx.channel.name == "enihei" or ctx.channel.name == "tatt04ek" or ctx.channel.name == "shadowdemonhd_" or ctx.channel.name == "orlega_":
            who = ctx.channel.name
            if not self.USERDATA['spotify'][who]['sr']['id']:
                await ctx.send("Стример не установил плей лист для сров")
                return
            self.updateSpotifySongs(who)
            try:
                resp = req.get(f"https://api.spotify.com/v1/playlists/{self.USERDATA['spotify'][who]['sr']['id']}", headers={
                    'Authorization': f"Bearer {self.sp_data[who]['access']}", 
                    'Content-Type': "application/json"}).json()
                queue = []
                for i in range(len(resp['tracks']['items'])):
                    queue.append({'name': resp['tracks']['items'][i]['track']['name'], 
                                   'artist': resp['tracks']['items'][i]['track']['artists'][0]['name']})
                msg = []
                if len(queue) < 6:
                    if len(queue) == 1:
                        msg = False
                    elif len(queue) == 0:
                        await ctx.send("В очереди нет треков")
                        return
                    else:
                        for i in range(1, len(queue)):
                            msg.append(f"{queue[i]['artist']} - {queue[i]['name']}")
                else:
                    for i in range(1, 6):
                        msg.append(f"{queue[i]['artist']} - {queue[i]['name']}")
                if not msg:
                    await ctx.send(f"Сейчас играет: {queue[0]['artist']} - {queue[0]['name']}. В очереди нет треков")
                else:
                    await ctx.send(f"Сейчас играет: {queue[0]['artist']} - {queue[0]['name']}. В очереди: {', '.join(msg)}.")
            except Exception as e:
                if type(e) == type(KeyError()):
                    await ctx.send("Кажется стример не авторизован Spotify, или произошла не придвиденная ошибка")
                else:
                    await ctx.send("Произошла не придвиденная ошибка")

        

    @commands.command(name="spload")
    async def spload(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            self.sp_token = cdcs.open("spsave.token", 'r', 'utf-8').read()
            print("Токен загружен!")

    @commands.command(name="spsave")
    async def spsave(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            tempf = cdcs.open("spsave.token", 'w', 'utf-8')
            tempf.write(self.sp_token)
            tempf.close()
            print("Токен сохранен!")

    @commands.command(name="setmod")
    async def setmod(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            content = str0list0split(ctx.message.content)
            content.listcut(0, 0)
            if content.list[0] == "add":
                content.listcut(0, 0)
                cnt = content.str
                self.USERDATA['mods'].append(cnt.lower())
                self.saveUserData()
                await ctx.send(f"{cnt} добавлен в качестве модератора бота!")
            if content.list[0] == "remove":
                content.listcut(0, 0)
                cnt = content.str
                self.USERDATA['mods'].remove(cnt.lower())
                self.saveUserData()
                await ctx.send(f"{cnt} удален из списка модераторов бота!")

    def modCheck(self, name):
        for i in range(len(self.USERDATA['mods'])):
            if name.lower() == self.USERDATA['mods'][i]:
                return True
        return False

    @commands.command(name="botban")
    async def botban(self, ctx: commands.Context):
        if self.modCheck(ctx.author.name):
            content = str0list0split(ctx.message.content)
            content.listcut(0, 0)
            cnt = content.str
            self.USERDATA['bans'].append(cnt.lower())
            self.saveUserData()
            await ctx.send(f"{cnt} Успешно забанен")
            
    @commands.command(name="botunban")
    async def botunban(self, ctx: commands.Context):
        if self.modCheck(ctx.author.name):
            content = str0list0split(ctx.message.content)
            content.listcut(0, 0)
            cnt = content.str
            self.USERDATA['bans'].remove(cnt.lower())
            self.saveUserData()
            await ctx.send(f"{cnt} Успешно разбанен")

    @commands.command(name="listmods", aliases=["modslist", "mods"])
    async def moooooods(self, ctx: commands.Context):
        mods = "Список модераторов бота MODS : "
        for i in range(len(self.USERDATA['mods'])):
            mods += self.USERDATA['mods'][i]
            mods += "X, "
        await ctx.send(mods)

    @commands.command(name="sup")
    async def sup(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            content = str0list0split(ctx.message.content)
            content.listcut(0,0)
            cnt = content.str
            resp = req.post("https://supinic.com/api/bot/command/run", json={\
                'query': cnt}, headers={\
                'Authorization': f"Basic {CFG['sup_us']}:{CFG['sup']}"}\
                ).json()
            '''resp = req.get("https://supinic.com/api/test/auth",
                headers={
                'Authorization': f"Basic {CFG['sup_us']}:{CFG['sup']}"
                }).json()'''
            '''resp = req.post("https://supinic.com/api/bot/reminder", params={\
                'username': "feelsdyslexiaman",
                'text': "modCheck"}, headers={\
                'Authorization': f"Basic {CFG['sup_us']}:{CFG['sup']}"}).json()'''
            await ctx.send(resp['data']['reply'])

    '''@commands.command(name="title")
    async def title(self, ctx: commands.Context):
        info = await self.fetch_channel("276061388")
        await ctx.send(f"Карент титле: {info.title}")'''

    async def notifer_timer(self):
        while not self.eventctx: pass
        await self.eventctx.send("Канал для ивентового (уведомлялка) устоновлен! pwgoodKlass")
        while True:
            #await asyncio.sleep(10)
            await self.notifer()

    async def notifer(self):
        info = await self.fetch_channel("276061388")
        if self.USERDATA['notify']['poal48']['title'] != info.title:
            self.USERDATA['notify']['poal48']['title'] = info.title
            await self.eventctx.send(f"PagMan НАЗВАНИЕ СТРИМА ИЗМЕНЕНО 👉 {info.title}")

    @commands.command(name="top7tv")
    async def top7tv(self, ctx: commands.Context):
        if self.USERDATA['gcd']['top7tv'] != 0: return
        await ctx.reply("Создаю картинку PauseChamp ✋ ")
        top1 = self.USERDATA['pwemts']
        top2 = {'name': [], 'id': [], 'used': []}
        for i in top1.keys():
            top2['name'].append(i)
            top2['id'].append(top1[i]['id'])
            top2['used'].append(top1[i]['used'])
        df = pd.DataFrame(top2)
        df = df.sort_values(by=['used'], ascending=False)
        top3 = {}
        for i in range(10):
            top3[df['name'][df.index[i]]] = {'id': df['id'][df.index[i]], 'used': df['used'][df.index[i]], 'n': i+1}
        '''top4 = ""
        maxX = 100
        maxY = 0
        alX = 50
        alY = 50
        img = cv.imread("asd_.png")
        cv.putText(img, "Top 7tv emotes in #pwgood !", (alX, alY), cv.FONT_HERSHEY_SIMPLEX, 1.5,(255, 255, 255), 6)
        wht, _ = cv.getTextSize("Top 7tv emotes in #pwgood !", cv.FONT_HERSHEY_SIMPLEX, 1.5, 6)
        wt, ht = wht
        if alX + wt + 50 > maxX: maxX = alX + wt + 50
        alY += ht + 50
        maxY += ht + 50
        for i in top3.keys():
            url_d = f"https://cdn.7tv.app/emote/{top3[i]['id']}/4x.webp"
            try:
                ulr.urlretrieve(url_d, "temp.webp")
                webpmux_getframe("temp.webp", "temp.webp", '1')
                dwebp("temp.webp", "temp.png", '-o')
                _img = cv.imread("temp.png")
            except Exception:
                _img = cv.imread("error_get.png")
            h = _img.shape[0]
            w = _img.shape[1]
            wc = 1
            if w != h:
                if w > h:
                    for j in range(w // h):
                        img[alY:alY+h, alX+(j*h):alX+h+(j*h)] = _img[0:h, j*h:h+(j*h)]
                    wc = w//h
                elif h > w:
                    for j in range(h // w):
                        img[alY+(j*w):alY+w+(j*w), alX:alX+w] = _img[j*w:w+(j*w), 0:w]
            else:
                img[alY:alY+h, alX:alX+w] = _img[0:h, 0:w]
            cv.putText(img, i, (alX+50+(h*wc), alY+((h//3)*2)), cv.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 6)
            wht, _ = cv.getTextSize(i, cv.FONT_HERSHEY_SIMPLEX, 3, 6)
            wt, ht = wht
            cv.putText(img, str(top3[i]['used']), (alX+50+(h*wc)+wt+50, alY+((h//3)*2)), cv.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 6)
            wht_, _ = cv.getTextSize(str(top3[i]['used']), cv.FONT_HERSHEY_SIMPLEX, 3, 6)
            wt_, ht = wht_
            if alX + w + 50 + wt + 50 + wt_ + 50 > maxX: maxX = alX + w + 50 + wt + 50 + wt_ + 50
            alY += h + 50
            maxY += h + 50
        maxY += 50
        img = img[0:maxY, 0:maxX]
        cv.imwrite("tomato.png", img)'''
        bg = Image.open("emts/bg.webp")
        bg = bg.convert("RGBA")
        bgD = ImageDraw.Draw(bg)
        font = ImageFont.truetype("segoeuib.ttf", 80)
        maxX = 0
        maxY = 20
        nowX = 40
        bgD.text((nowX, maxY-20), "Топ 7тв эмоутов пвгуда", (0, 0, 0), font)
        maxY += 80 + 40
        for i in top3.keys():
            url_d = f"https://cdn.7tv.app/emote/{top3[i]['id']}/4x.webp"
            try:
                ulr.urlretrieve(url_d, "emts/temp.webp")
                emt = Image.open("emts/temp.webp")
            except Exception:
                emt = Image.open("emts/error_getting_emote.webp")
            nowX = 40
            bgD.line([(0, maxY-20), (3000, maxY-20)], (175, 175, 175), 6)

            bgD.text((nowX, maxY), str(top3[i]['n']), (0, 0, 0), font)
            nowX += font.getlength(str(top3[i]['n'])) + 40

            bgD.line([(nowX-20, maxY-20), (nowX-20, maxY+emt.size[1]+20)], (175, 175, 175), 6)

            bg.alpha_composite(emt, (int(nowX), int(maxY)))
            nowX += emt.size[0] + 40

            bgD.line([(nowX-20, maxY-20), (nowX-20, maxY+emt.size[1]+20)], (175, 175, 175), 6)

            bgD.text((nowX, maxY), i, (0, 0, 0), font)
            nowX += font.getlength(i) + 40

            bgD.line([(nowX-20, maxY-20), (nowX-20, maxY+emt.size[1]+20)], (175, 175, 175), 6)

            bgD.text((nowX, maxY), str(top3[i]['used']), (0, 0, 0), font)
            nowX += font.getlength(str(top3[i]['used'])) + 40
            maxY += emt.size[1] + 40
            if nowX > maxX: maxX = nowX
        bg = bg.crop((0, 0, maxX, maxY))
        #bg.show()
        bg.save("emts/ready.webp")
        resp = req.post("https://gachi.gay/api/upload", files={'file': open("emts/ready.webp", 'rb')}).json()
        await ctx.reply(f"Топ 7тв эмоутов в чате ПВГуда: {resp['link']} PagMan | Кд - 120сек")
        self.USERDATA['gcd']['top7tv']  = 120
        self.saveUserData()

    @commands.command(name="estat")
    async def estat(self, ctx: commands.Context):
        if ctx.channel.name == "pwgood" or ctx.channel.name == "poal48":
            cnt = str0list0split(ctx.message.content, listcut=(0,0)).list[0]
            try:
                self.USERDATA['pwemts'][cnt]['used']
            except KeyError:
                await ctx.reply("Не нашел такого эмоута в 7tv! 🤨 ")
                return
            top1 = self.USERDATA['pwemts']
            top2 = {'name': [], 'used': []}
            for i in top1.keys():
                top2['name'].append(i)
                top2['used'].append(top1[i]['used'])
            df = pd.DataFrame(top2)
            df = df.sort_values(by=['used'], ascending=False)
            top3 = {}
            for i in range(len(df)):
                top3[df['name'][df.index[i]]] = {'used': df['used'][df.index[i]]}
            a = 1
            for i in top3.keys():
                if cnt == i: break
                a += 1
            pauseText = ""
            if self.USERDATA['pwemts'][cnt]['pause']: pauseText = ", эмоут на паузе"
            await ctx.reply(f"{cnt} used times: {self.USERDATA['pwemts'][cnt]['used']}, место в топе: {a}/{len(self.USERDATA['pwemts'].keys())}{pauseText}")

    @commands.command(name="server", aliases=["сервер"])
    async def server(self, ctx: commands.Context):
        #if ctx.channel.name == "poal48" or ctx.channel.name == "the_il_" or ctx.channel.name == "enihei" or ctx.channel.name == "shadowdemonhd_" or ctx.channel.name == "tatt04ek" or ctx.channel.name == "red3xtop" or ctx.channel.name == "orlega_" or ctx.channel.name == "wanderning_":
            #await ctx.reply("Приватный лицензионый сервер ПепеЛенд: pepeland.net ")
        if ctx.channel.name == "poal48" or ctx.channel.name == "the_il_" or ctx.channel.name == "enihei" or ctx.channel.name == "shadowdemonhd_" or ctx.channel.name == "tatt04ek" or ctx.channel.name == "red3xtop":
            await ctx.reply("Лицензионый сервер пепехаба, проходку можно купить за баллы канала у любого пепехабовца с компаньонкой, IP: pepehub.joinserver.xyz")
            
    @commands.command(name="pepehub", aliases=["pph", "пепехаб", "ппх"])
    async def pepehub(self, ctx: commands.Context):
        if ctx.channel.name == "poal48" or ctx.channel.name == "the_il_" or ctx.channel.name == "enihei" or ctx.channel.name == "shadowdemonhd_" or ctx.channel.name == "tatt04ek" or ctx.channel.name == "red3xtop":
            await ctx.reply("Наше сообщество ребят с Пепеленда, дискорд: http://денис.space/ппх")
            
    def cd_ticker(self):
        sleep(300)
        while True:
            for i in self.USERDATA['gcd'].keys():
                if self.USERDATA['gcd'][i] != 0:
                    self.USERDATA['gcd'][i] -= 1
                    self.saveUserData()
            if self.turningOn: self.turningOn -= 1
            sleep(1)

    @commands.command(name="testLoop")
    async def testLoop(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            for i in self.testDataLoop.keys(): break
            self.loop_ = {'enabled': True, 'i': i, 'type': 'test'}
            await ctx.send("Цикл test начан")
            await ctx.send(f"{i} - {self.testDataLoop[i]}")
            self.testDataLoopCompl = {}

    @commands.command(name="avaGameLoop")
    async def avaGameLoop(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            for i in self.avaGame.keys(): break
            self.loop_ = {'enabled': True, 'i': i, 'type': 'avaGame'}
            await ctx.send("Цикл avaGame начан")
            await ctx.send(f"{i} - {self.avaGame[i]['image']}")
            self.avaGameCompl = {}

    @commands.command(name="originset")
    async def originset(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            self.loop_ = {'enabled': True, 'i': 0, 'type': "origin", 'start': True}
            await ctx.send("Цикл origin начан")

    @commands.command(name="o")
    async def set_loop(self, ctx: commands.Context):
        if ctx.author.name == "poal48" and self.loop_['enabled']:
            if self.loop_['type'] == "origin":
                cnt = str0list0split(ctx.message.content, listcut=(0, 0)).str
                if not self.loop_['start']:
                    self.USERDATA['origins'][self.emts[self.loop_['i']]['name']] = cnt
                    self.saveUserData()
                print(self.loop_['i'])
                try:
                    while self.emts[self.loop_['i']]['name'] in self.USERDATA['origins'].keys():
                        self.loop_['i'] += 1
                except IndexError:
                    await ctx.send("Цикл origin завершен")
                    self.loop_ = {'enabled': False}
                    return
                self.loop_['start'] = False
                await ctx.send(f"Origin for {self.emts[self.loop_['i']]['name']}")

    @commands.command(name="y")
    async def yes_loop(self, ctx: commands.Context):
        if ctx.author.name == "poal48" and self.loop_['enabled']:
            if self.loop_['type'] == "avaGame":
                self.avaGameAdd['compl'][self.loop_['i']] = self.avaGame[self.loop_['i']]
                self.avaGameAdd['ignore'].append(self.loop_['i'])
                agaw = open("avaGameAdd.data", 'w')
                json.dump(self.avaGameAdd, agaw)
                agaw.close()
                g = False
                gg = False
                for i in self.avaGame.keys():
                    if g:
                        gg = True
                        break
                    if i == self.loop_['i']: g = True
                if not gg:
                    self.loop_ = {'enabled': False}
                    await ctx.send("Цикл avaGame завершен")
                    return
                self.loop_['i'] = i
                await ctx.send(f"{i} - {self.avaGame[i]['image']}")
            if self.loop_['type'] == "test":
                self.testDataLoopCompl[self.loop_['i']] = self.testDataLoop[self.loop_['i']]
                g = False
                gg = False
                for i in self.testDataLoop.keys():
                    if g:
                        gg = True
                        break
                    if i == self.loop_['i']: g = True
                if not gg:
                    self.loop_ = {'enabled': False}
                    await ctx.send("Цикл test завершен")
                    return
                self.loop_['i'] = i
                await ctx.send(f"{i} - {self.testDataLoop[i]}")

    @commands.command(name="n")
    async def no_loop(self, ctx: commands.Context):
        if ctx.author.name == "poal48" and self.loop_['enabled']:
            if self.loop_['type'] == "avaGame":
                self.avaGameAdd['ignore'].append(self.loop_['i'])
                agaw = open("avaGameAdd.data", 'w')
                json.dump(self.avaGameAdd, agaw)
                agaw.close()
                g = False
                gg = False
                for i in self.avaGame.keys():
                    if g:
                        gg = True
                        break
                    if i == self.loop_['i']: g = True
                if not gg:
                    self.loop_ = {'enabled': False}
                    await ctx.send("Цикл avaGame завершен")
                    return
                self.loop_['i'] = i
                await ctx.send(f"{i} - {self.avaGame[i]['image']}")
            if self.loop_['type'] == "test":
                g = False
                gg = False
                for i in self.testDataLoop.keys():
                    if g:
                        gg = True
                        break
                    if i == self.loop_['i']: g = True
                if not gg:
                    self.loop_ = {'enabled': False}
                    await ctx.send("Цикл test завершен")
                    return
                self.loop_['i'] = i
                await ctx.send(f"{i} - {self.testDataLoop[i]}")

    @commands.command(name="massping")
    async def massping(self, ctx: commands.Context):
        usersSet = ctx.chatters
        usersSetCopy = usersSet.copy()
        usersList = []
        for i in range(len(usersSet)):
            usersList.append(usersSet.pop())
        users = []
        tUserChan = await ctx.channel.user()
        pu = self.create_user(tUserChan.id, ctx.channel.name)
        #await ctx.send(f"MODS: {await pu.fetch_moderators(CFG['api_token'])}")
        for i in range(len(usersList)):
            tUser = await usersList[i].user()
            users.append(str(tUser.display_name))
        freeWires = cdcs.open("chatters.temp", 'w', 'utf-8')
        freeWires.write("\n".join(users))
        freeWires.close()
        resp = req.post("https://gachi.gay/api/upload", files={'file': cdcs.open("chatters.temp", 'r', 'utf-8')}).json()
        await ctx.send(f"Alright {resp['link']}")

    @commands.command(name="rr")
    async def rr(self, ctx: commands.Context):
        activeChannels = ["poal48", "tatt04ek", "the_il_", "enihei", "alexoff35", "shadowdemonhd_", "red3xtop", "orlega_", "wanderning_", "echoinshade"]
        if ctx.channel.name in activeChannels:
            if randint(0, 1):
                chnlUser = await ctx.channel.user(force=True)
                pu = self.create_user(chnlUser.id, chnlUser.name)
                await ctx.reply("Ты проиграл в русской рулетке pwgood4 ")
                await pu.timeout_user(CFG['api_token_ppSpin'], 841491788, ctx.author.id, 60, "пипо русская рулетка")
            else:
                await ctx.reply("Ты выиграл в русской рулетке pwgood3 ")

    @commands.command(name="7tvEventsRec")
    async def _7tvEventsRec(self, ctx: commands.Context): self.isReconnect7tvEvents = True

    @commands.command(name="help", aliases=["commands", "хелп"])
    async def help(self, ctx: commands.Context):
        if ctx.channel.name == "pwgood": await ctx.reply("Список команд доступен здесь: https://денис.space/ppSpin/команды/pwgood/")
        else: await ctx.reply("Список команд доступен здесь: https://денис.space/ppSpin/команды/")

    @commands.command(name="cmd")
    async def cmd(self, ctx: commands.Context):
        enabled_channels=["poal48", "tatt04ek", "the_il_", "enihei", "shadowdemonhd_", "red3xtop", "erynga", "orlega_", "wanderning_",
                          "echoinshade", "alexoff35"]
        if ctx.channel.name in enabled_channels and (ctx.author.name == "poal48" or ctx.author.name == ctx.channel.name):
            cnt = str0list0split(ctx.message.content, listcut=(0, 0))
            try: cnt.list[0]
            except IndexError:
                await ctx.reply("Не приведена саб команда")
                return
            if cnt.list[0] == "add":
                try: name = cnt.list[1]
                except IndexError:
                    await ctx.reply("Не приведено название команды")
                    return
                if name == "aliases":
                    await ctx.reply("Нельзя назвать команду таким именем")
                    return
                cnt.listcut(0, 1)
                if not cnt.str:
                    await ctx.reply("Не приведен вывод команды")
                    return
                prefix = ['!']
                if "-prefix" in cnt.list:
                    i = cnt.list.index("-prefix")
                    if len(cnt.list)-1 != i:
                        prefix = []
                        for l in range(len(cnt.list[i+1])):
                            prefix.append(cnt.list[i+1][l])
                        cnt.listcut(i, i+1)
                is_reply = False
                if "-reply" in cnt.list:
                    is_reply = True
                    cnt.listcut(cnt.list.index("-reply"), cnt.list.index("-reply"))
                if not cnt.str:
                    await ctx.reply("Не приведен вывод команды")
                    return
                if not ctx.channel.name in self.USERDATA['cmd'].keys():
                    self.USERDATA['cmd'][ctx.channel.name] = {}
                self.USERDATA['cmd'][ctx.channel.name][name] = {"prefix": prefix, "cmd": cnt.str, "is_reply": is_reply, "is_alias": False, "aliases": [], "original_name": None}
                self.saveUserData()
                await ctx.reply(f"Команда {name} добавлена! poal48Arbuz ")
            elif cnt.list[0] == "remove":
                try: name = cnt.list[1]
                except IndexError:
                    await ctx.reply("Не приведено название команды")
                    return
                if not ctx.channel.name in self.USERDATA['cmd'].keys():
                    await ctx.reply("У тебя нет команд")
                    return
                if not name in self.USERDATA['cmd'][ctx.channel.name].keys():
                    await ctx.reply(f"У тебя нет команды {name}")
                    return
                if self.USERDATA['cmd'][ctx.channel.name][name]['is_alias']:
                    await ctx.reply(f"Ты пытаешься удалить алиас, алиасы удаляются с помощью команды *cmd alias remove. (Оригинальное название команды этого алиаса: {self.USERDATA['cmd'][ctx.channel.name][name]['original_name']})")
                    return
                for i in self.USERDATA['cmd'][ctx.channel.name][name]['aliases']:
                    self.USERDATA['cmd'][ctx.channel.name].pop(i)
                self.USERDATA['cmd'][ctx.channel.name].pop(name)
                self.saveUserData() 
                await ctx.reply(f"Команда {name} убрана успешно! poal48Arbuz ")
            elif cnt.list[0] == "edit":
                if not ctx.channel.name in self.USERDATA['cmd'].keys():
                    await ctx.reply("У тебя нет ни одной команды")
                    return
                try: name = cnt.list[1]
                except IndexError:
                    await ctx.reply("Не приведено название команды")
                    return
                if not name in self.USERDATA['cmd'][ctx.channel.name].keys():
                    await ctx.reply("У тебя нет такой команды")
                    return
                cnt.listcut(0, 1)
                if not cnt.str:
                    await ctx.reply("Не приведен вывод команды")
                    return
                if self.USERDATA['cmd'][ctx.channel.name][name]['is_alias']: name = self.USERDATA['cmd'][ctx.channel.name][name]['original_name']
                cmd = self.USERDATA['cmd'][ctx.channel.name][name]
                prefix = cmd['prefix']
                if "-prefix" in cnt.list:
                    i = cnt.list.index("-prefix")
                    if len(cnt.list)-1 != i:
                        prefix = []
                        for l in range(len(cnt.list[i+1])):
                            prefix.append(cnt.list[i+1][l])
                        cnt.listcut(i, i+1)
                is_reply = False
                if "-reply" in cnt.list:
                    is_reply = True
                    cnt.listcut(cnt.list.index("-reply"), cnt.list.index("-reply"))
                if not cnt.str:
                    await ctx.reply("Не приведен вывод команды")
                    return
                for i in self.USERDATA['cmd'][ctx.channel.name][name]['aliases']:
                    alCmd = self.USERDATA['cmd'][ctx.channel.name][i].copy()                    
                    self.USERDATA['cmd'][ctx.channel.name][i] = {"prefix": prefix, "cmd": cnt.str, "is_reply": is_reply, "is_alias": alCmd['is_alias'], "aliases": alCmd['aliases'], "original_name": alCmd['original_name']}
                self.USERDATA['cmd'][ctx.channel.name][name] = {"prefix": prefix, "cmd": cnt.str, "is_reply": is_reply, "is_alias": cmd['is_alias'], "aliases": cmd['aliases'], "original_name": cmd['original_name']}
                self.saveUserData()
                await ctx.reply(f"Команда {name} изменена! poal48Arbuz ")
            elif cnt.list[0] == "alias":
                try: cnt.list[1]
                except IndexError: await ctx.reply("Не хватает саб команд")
                if cnt.list[1] == "add":
                    try: name = cnt.list[2]
                    except IndexError:
                        await ctx.reply("Не привиденно название команды")
                        return
                    try: nameAl = cnt.list[3]
                    except IndexError:
                        await ctx.reply("Не привиденно название алиаса")
                        return
                    cnt.listcut(0, 3)
                    if not name in self.USERDATA['cmd'][ctx.channel.name].keys():
                        await ctx.reply("У тебя нету такой команды poal48Arbuz ")
                        return
                    if self.USERDATA['cmd'][ctx.channel.name][name]['is_alias']: name = self.USERDATA['cmd'][ctx.channel.name][name]['original_name']
                    self.USERDATA['cmd'][ctx.channel.name][nameAl] = self.USERDATA['cmd'][ctx.channel.name][name].copy()
                    self.USERDATA['cmd'][ctx.channel.name][nameAl]['is_alias'] = True
                    self.USERDATA['cmd'][ctx.channel.name][nameAl]['aliases'] = []
                    self.USERDATA['cmd'][ctx.channel.name][nameAl]['original_name'] = name
                    self.USERDATA['cmd'][ctx.channel.name][name]['aliases'].append(nameAl)
                    self.saveUserData()
                    await ctx.reply(f"Алиас {nameAl} создан к команде {name}")
                elif cnt.list[1] == "remove":
                    try: name = cnt.list[2]
                    except IndexError:
                        await ctx.reply("Не привиденно название команды")
                        return
                    cnt.listcut(0, 2)
                    if not name in self.USERDATA['cmd'][ctx.channel.name].keys():
                        await ctx.reply("У тебя нету такой команды poal48Arbuz ")
                        return
                    if not self.USERDATA['cmd'][ctx.channel.name][name]['is_alias']:
                        await ctx.reply("Ты пытаешся удалить не алиас! ")
                        return
                    self.USERDATA['cmd'][ctx.channel.name][self.USERDATA['cmd'][ctx.channel.name][name]['original_name']]['aliases'].remove(name)
                    self.USERDATA['cmd'][ctx.channel.name].pop(name)
                    self.saveUserData()
                    await ctx.reply(f"Алиас {name} удален")


    async def handle_custom_commands(self, msg: tio.Message):
        enabled_channels=["poal48", "tatt04ek", "the_il_", "enihei", "shadowdemonhd_", "red3xtop", "erynga", "orlega_", "wanderning_",
                          "echoinshade", "alexoff35"]
        if not msg.channel.name in enabled_channels: return
        cnt = msg.content
        if len(cnt) == 1: return
        prefix = cnt[0]
        cnt = cnt[1:]
        command = cnt.split()[0]
        try:
            cmd = self.USERDATA['cmd'][msg.channel.name][command]
            if prefix in cmd['prefix']:
                if not cmd['is_reply']: await commands.Context(msg, self).send(cmd['cmd'])
                else: await commands.Context(msg, self).reply(cmd['cmd'])
        except KeyError: pass


    @commands.command(name="announceTo")
    async def announceTo(self, ctx: commands.Context):
        if ctx.author.name == "poal48":
            cnt = str0list0split(ctx.message.content, listcut=(0, 0))
            channels = cnt.list[0].split(',')
            cnt.listcut(0, 0)
            for i in channels:
                await self.get_channel(i).send(cnt.str)
            await ctx.send("Анонс отправлен")
                

    @commands.command(name="хуй")
    async def test(self, ctx: commands.Context):
        pass

async def websocket_handler(ws, bot):
    async for msg in ws:
        if bot.isReconnect7tvEvents:
            bot.isReconnect7tvEvents = False
            await bot.get_channel("poal48").send(f"Реконекшусь ppSpin")
            await ws.close()
            thrd.Thread(target=wb_starter, args=(bot, )).start()
        msg = json.loads(msg)
        if msg['op'] == 1: await bot.get_channel("poal48").send("WebSocket 7tv events подключен! uuh")
        if msg['op'] == 0:
            if msg['d']['body']['id'] == "6301dcecf7723932b45c06b0": #ne pwgood
                if 'pushed' in msg['d']['body'].keys():
                    for i in range(len(msg['d']['body']['pushed'])):
                        emote = msg['d']['body']['pushed'][i]
                        await bot.get_channel("poal48").send(f"[7tv] Эмоут {emote['value']['name']} добавлен")
                elif 'pulled' in msg['d']['body'].keys():
                    for i in range(len(msg['d']['body']['pulled'])):
                        emote = msg['d']['body']['pulled'][i]
                        await bot.get_channel("poal48").send(f"[7tv] Эмоут {emote['old_value']['name']} убран")
                elif 'updated' in msg['d']['body'].keys():
                    for i in range(len(msg['d']['body']['updated'])):
                        emote = msg['d']['body']['updated'][i]
                        await bot.get_channel("poal48").send(f"[7tv] Эмоут {emote['old_value']['name']} переименнован в {emote['value']['name']}")
            if msg['d']['body']['id'] == "61c802080bf6300371940381": #pwgood
                if 'pushed' in msg['d']['body'].keys():
                    for i in range(len(msg['d']['body']['pushed'])):
                        emote = msg['d']['body']['pushed'][i]
                        try:
                            bot.USERDATA['pwemts'][emote['value']['name']]
                            bot.USERDATA['pwemts'][emote['value']['name']]['id'] = emote['value']['id']
                            bot.USERDATA['pwemts'][emote['value']['name']]['pause'] = False
                        except KeyError:
                            bot.USERDATA['pwemts'][emote['value']['name']] = {'id': emote['value']['id'], 'used': 0, 'pause': False}
                        bot.saveUserData()
                        await bot.get_channel("poal48").send(f"[7tv- PWGood ] Эмоут {emote['value']['name']} добавлен (by {msg['d']['body']['actor']['display_name']})")
                elif 'pulled' in msg['d']['body'].keys():
                    for i in range(len(msg['d']['body']['pulled'])):
                        emote = msg['d']['body']['pulled'][i]
                        bot.USERDATA['pwemts'][emote['old_value']['name']]['pause'] = True
                        bot.saveUserData()
                        await bot.get_channel("poal48").send(f"[7tv- PWGood ] Эмоут {emote['old_value']['name']} убран (by {msg['d']['body']['actor']['display_name']})")
                elif 'updated' in msg['d']['body'].keys():
                    for i in range(len(msg['d']['body']['updated'])):
                        emote = msg['d']['body']['updated'][i]
                        bot.USERDATA['pwemts'][emote['value']['name']] = bot.USERDATA['pwemts'][emote['old_value']['name']]
                        bot.USERDATA['pwemts'].pop(emote['old_value']['name'])
                        bot.saveUserData()
                        await bot.get_channel("poal48").send(f"[7tv- PWGood ] Эмоут {emote['old_value']['name']} переименнован в {emote['value']['name']} (by {msg['d']['body']['actor']['display_name']})")
        if msg['op'] == 7:
            await bot.get_channel("poal48").send(f"WebSocket 7tv  events дисконектится, пытаюсь реконектиться ppSpin")
            await ws.close()
            thrd.Thread(target=wb_starter, args=(bot, )).start()
            return

async def websocket_mainloop(bot):
    await asyncio.sleep(10)
    async with wbscks.connect("wss://events.7tv.io/v3") as ws:
        await ws.send('{"op": 35, "d": {"type": "emote_set.update", "condition": {"object_id": "6301dcecf7723932b45c06b0"}}}')
        await ws.send('{"op": 35, "d": {"type": "emote_set.update", "condition": {"object_id": "61c802080bf6300371940381"}}}')
        await websocket_handler(ws, bot)
        

def between_callback(args):
    loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    nest_asyncio.apply(loop)
    #asyncio.run(notifer_timer(args))
    asyncio.run(events(args))
    #loop.run_until_complete(target(args))

def wb_starter(args):
    loop = asyncio.new_event_loop()
    nest_asyncio.apply(loop)
    asyncio.run(websocket_mainloop(args))

async def events(bot):
    while not bot.eventctx: pass
    #await bot.eventctx.send("Канал для ивентового устоновлен! pwgoodKlass")
    print("Канал для ивентового устоновлен! pwgoodKlass")
    events = {'gm': True, 'gn': True, 'emt': True, 'd0': True, 'd2': True, 'd4': True, 'd5': True, 'd6': True}
    while True:
        if dt.datetime.now().hour == 8 and dt.datetime.now().minute == 0 and events['gm']:  
            events['gm'] = False
            events['gn'] = True
            await bot.eventctx.send("Всем утра! GoodMorning")
            await bot.more500send(bot.eventctx, "POAL48", start="GoodMorning", end="GoodMorning")
        if dt.datetime.now().hour == 0 and dt.datetime.now().minute == 0 and events['gn']:
            events['gn'] = False
            events['gm'] = True
            await bot.eventctx.send("Всем спокойной ночи! catSleep")
            if randint(0, 100): await bot.more500send(bot.eventctx, "POAL48", start="catSleep", end="catSleep")
            else:
                bror = []
                for i in range(500):
                    bror.append("The_il_ brorAhuel")
                await bot.more500send(bot.eventctx, " ".join(bror), start="catSleep", end="catSleep", delay=3)
        if dt.datetime.now().hour == 0 and dt.datetime.now().minute == 0 and dt.datetime.now().weekday() == 0 and events['d0']:
            events['d0'] = False
            events['d6'] = True
            pu = bot.create_user(276061388, "poal48")
            await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"Monday !")
        if dt.datetime.now().hour == 0 and dt.datetime.now().minute == 0 and dt.datetime.now().weekday() == 2 and events['d2']:
            events['d2'] = False
            events['d0'] = True
            pu = bot.create_user(276061388, "poal48")
            await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"JABA TeaTime")
        if dt.datetime.now().hour == 0 and dt.datetime.now().minute == 0 and dt.datetime.now().weekday() == 4 and events['d4']:
            events['d4'] = False
            events['d2'] = True
            pu = bot.create_user(276061388, "poal48")
            await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"Friday !")
        if dt.datetime.now().hour == 0 and dt.datetime.now().minute == 0 and dt.datetime.now().weekday() == 5 and events['d5']:
            events['d5'] = False
            events['d4'] = True
            pu = bot.create_user(276061388, "poal48")
            await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"saturday")
        if dt.datetime.now().hour == 0 and dt.datetime.now().minute == 0 and dt.datetime.now().weekday() == 6 and events['d6']:
            events['d6'] = False
            events['d5'] = True
            pu = bot.create_user(276061388, "poal48")
            await pu.chat_announcement(CFG['api_token_ppSpin'], 841491788, f"MondayTomorow ")
        if dt.datetime.now().minute == 0 and events['emt']:
            events['emt'] = False
            if not bot.isLastMsgPpSpin['poal48']:
                emt = choice(bot.emts)
                if emt['data']['flags'] == 256: await bot.eventctx.send(f"frame145delay007s {emt['name']}")
                else: await bot.eventctx.send(f"{emt['name']}")
                bot.isLastMsgPpSpin['poal48'] = True
            if not bot.isLastMsgPpSpin['the_il_']:
                emt = choice(bot.emtsil)
                if emt['data']['flags'] == 256: await bot.get_channel("the_il_").send(f"frame145delay007s {emt['name']}")
                else: await bot.get_channel("the_il_").send(f"{emt['name']}")
                bot.isLastMsgPpSpin['the_il_'] = True
            if not bot.isLastMsgPpSpin['enihei']:
                emt = choice(bot.emtshei)
                if emt['data']['flags'] == 256: await bot.get_channel("enihei").send(f"frame145delay007s {emt['name']}")
                else: await bot.get_channel("enihei").send(f"{emt['name']}")
                bot.isLastMsgPpSpin['enihei'] = True
            if not bot.isLastMsgPpSpin['shadowdemonhd_']:
                emt = choice(bot.emtsdemon)
                if emt['data']['flags'] == 256: await bot.get_channel("shadowdemonhd_").send(f"frame145delay007s {emt['name']}")
                else: await bot.get_channel("shadowdemonhd_").send(f"{emt['name']}")
                bot.isLastMsgPpSpin['shadowdemonhd_'] = True
            if not bot.isLastMsgPpSpin['tatt04ek']:
                emt = choice(bot.emts04)
                if emt['data']['flags'] == 256: await bot.get_channel("tatt04ek").send(f"frame145delay007s {emt['name']}")
                else: await bot.get_channel("tatt04ek").send(f"{emt['name']}")
                bot.isLastMsgPpSpin['tatt04ek'] = True
            await bot.get_channel("alexoff35").send(f"{choice(bot.emtsoff)['name']}")
            await bot.get_channel("erynga").send(f"{choice(bot.emtserynga)['name']}")
            if not bot.isLastMsgPpSpin['red3xtop']:
                emt = choice(bot.emtsred3x)
                if emt['data']['flags'] == 256: await bot.get_channel("red3xtop").send(f"frame145delay007s {emt['name']}")
                else: await bot.get_channel("red3xtop").send(f"{emt['name']}")
                bot.isLastMsgPpSpin['red3xtop'] = True
            if not bot.isLastMsgPpSpin['orlega_']:
                emt = choice(bot.emtsorl)
                if emt['data']['flags'] == 256: await bot.get_channel("orlega_").send(f"frame145delay007s {emt['name']}")
                else: await bot.get_channel("orlega_").send(f"{emt['name']}")
                bot.isLastMsgPpSpin['orlega_'] = True
            if not bot.isLastMsgPpSpin['wanderning_']:
                emt = choice(bot.emtswand)
                if emt['data']['flags'] == 256: await bot.get_channel("wanderning_").send(f"frame145delay007s {emt['name']}")
                else: await bot.get_channel("wanderning_").send(f"{emt['name']}")
                bot.isLastMsgPpSpin['wanderning_'] = True
            if not bot.isLastMsgPpSpin['echoinshade']:
                emt = choice(bot.emtsecho)
                if emt['data']['flags'] == 256: await bot.get_channel("echoinshade").send(f"frame145delay007s {emt['name']}")
                else: await bot.get_channel("echoinshade").send(f"{emt['name']}")
                bot.isLastMsgPpSpin['echoinshade'] = True
        if dt.datetime.now().minute != 0 and not events['emt']:
            events['emt'] = True
        '''if bot.testThat:
            if not bot.isLastMsgPpSpin['poal48']:
                await bot.eventctx.send(f"{choice(bot.emts)['name']}")
                bot.isLastMsgPpSpin['poal48'] = True
            if not bot.isLastMsgPpSpin['the_il_']:
                await bot.get_channel("the_il_").send(f"{choice(bot.emtsil)['name']}")
                bot.isLastMsgPpSpin['the_il_'] = True
            if not bot.isLastMsgPpSpin['enihei']:
                await bot.get_channel("enihei").send(f"{choice(bot.emtshei)['name']}")
                bot.isLastMsgPpSpin['enihei'] = True
            if not bot.isLastMsgPpSpin['shadowdemonhd_']:
                await bot.get_channel("shadowdemonhd_").send(f"{choice(bot.emtsdemon)['name']}")
                bot.isLastMsgPpSpin['shadowdemonhd_'] = True
            if not bot.isLastMsgPpSpin['tatt04ek']:
                await bot.get_channel("tatt04ek").send(f"{choice(bot.emts04)['name']}")
                bot.isLastMsgPpSpin['tatt04ek'] = True
            if not bot.isLastMsgPpSpin['alexoff35']:
                await bot.get_channel("alexoff35").send(f"{choice(bot.emtsoff)['name']}")
                bot.isLastMsgPpSpin['alexoff35'] = True
            if not bot.isLastMsgPpSpin['red3xtop']:
                await bot.get_channel("red3xtop").send(f"{choice(bot.emtsred3x)['name']}")
                bot.isLastMsgPpSpin['red3xtop'] = True
            bot.testThat = False'''

            
bot = Bot()
thrd.Thread(target=between_callback, args=(bot,)).start()
thrd.Thread(target=wb_starter, args=(bot, )).start()
#thrd.Thread(target=between_callback, args=(bot, )).start()
thrd.Thread(target=bot.cd_ticker).start()

bAuth = tb.TeleBot(CFG['telebot_auth'])
bNot = tb.TeleBot(CFG['telebot_notifer'])
bAvg = tb.TeleBot(CFG['telebot_avaGame'])
bSpin = tb.TeleBot(CFG['telebot_ppSpin'])

@bAuth.message_handler(commands=['ping'])
def ping_telebot(msg):
    bAuth.send_message(msg.chat.id, "Плюнк!!")

@bAuth.message_handler(commands=['sppoal48'])
def spauth_telebot_poal48(msg):
    resp = req.get("https://clck.ru/--", params={'url': "https://accounts.spotify.com/authorize?" +  \
                'response_type' + '=' + "code" + "&" \
                "client_id" + '=' + CFG['sp_client_id'] + "&" \
                "scope" + '=' + 'ugc-image-upload user-read-playback-state app-remote-control user-modify-playback-state'\
                    ' playlist-read-private user-follow-modify playlist-read-collaborative user-follow-read'\
                    ' user-read-currently-playing user-read-playback-position user-library-modify'\
                    ' playlist-modify-private playlist-modify-public user-read-email user-top-read '\
                    ' user-read-recently-played user-read-private user-library-read' + "&" \
                "redirect_uri" + '=' + "http://денис.space/echo/code/" }).text
    bAuth.send_message(msg.chat.id, "Авторизация Spotify")
    bAuth.send_message(msg.chat.id, str(resp))
    bAuth.send_message(msg.chat.id, "Код сюда же")
    bAuth.who = "poal48"
    bAuth.register_next_step_handler(msg, spauth_step2)

@bAuth.message_handler(commands=['enihei'])
def spauth_telebot_enihei(msg):
    resp = req.get("https://clck.ru/--", params={'url': "https://accounts.spotify.com/authorize?" +  \
                'response_type' + '=' + "code" + "&" \
                "client_id" + '=' + CFG['sp_client_id'] + "&" \
                "scope" + '=' + 'ugc-image-upload user-read-playback-state app-remote-control user-modify-playback-state'\
                    ' playlist-read-private user-follow-modify playlist-read-collaborative user-follow-read'\
                    ' user-read-currently-playing user-read-playback-position user-library-modify'\
                    ' playlist-modify-private playlist-modify-public user-read-email user-top-read '\
                    ' user-read-recently-played user-read-private user-library-read' + "&" \
                "redirect_uri" + '=' + "http://денис.space/echo/code/" }).text
    bAuth.send_message(msg.chat.id, "Авторизация Spotify")
    bAuth.send_message(msg.chat.id, str(resp))
    bAuth.send_message(msg.chat.id, "Код сюда же")
    bAuth.who = "enihei"
    bAuth.register_next_step_handler(msg, spauth_step2)

@bAuth.message_handler(commands=['tatt04ek'])
def spauth_telebot_tatt04ek(msg):
    resp = req.get("https://clck.ru/--", params={'url': "https://accounts.spotify.com/authorize?" +  \
                'response_type' + '=' + "code" + "&" \
                "client_id" + '=' + CFG['sp_client_id'] + "&" \
                "scope" + '=' + 'ugc-image-upload user-read-playback-state app-remote-control user-modify-playback-state'\
                    ' playlist-read-private user-follow-modify playlist-read-collaborative user-follow-read'\
                    ' user-read-currently-playing user-read-playback-position user-library-modify'\
                    ' playlist-modify-private playlist-modify-public user-read-email user-top-read '\
                    ' user-read-recently-played user-read-private user-library-read' + "&" \
                "redirect_uri" + '=' + "http://денис.space/echo/code/" }).text
    bAuth.send_message(msg.chat.id, "Авторизация Spotify")
    bAuth.send_message(msg.chat.id, str(resp))
    bAuth.send_message(msg.chat.id, "Код сюда же")
    bAuth.who = "tatt04ek"
    bAuth.register_next_step_handler(msg, spauth_step2)

@bAuth.message_handler(commands=['shadowdemonhd_'])
def spauth_telebot_shadowdemonhd_(msg):
    resp = req.get("https://clck.ru/--", params={'url': "https://accounts.spotify.com/authorize?" +  \
                'response_type' + '=' + "code" + "&" \
                "client_id" + '=' + CFG['sp_client_id'] + "&" \
                "scope" + '=' + 'ugc-image-upload user-read-playback-state app-remote-control user-modify-playback-state'\
                    ' playlist-read-private user-follow-modify playlist-read-collaborative user-follow-read'\
                    ' user-read-currently-playing user-read-playback-position user-library-modify'\
                    ' playlist-modify-private playlist-modify-public user-read-email user-top-read '\
                    ' user-read-recently-played user-read-private user-library-read' + "&" \
                "redirect_uri" + '=' + "http://денис.space/echo/code/" }).text
    bAuth.send_message(msg.chat.id, "Авторизация Spotify")
    bAuth.send_message(msg.chat.id, str(resp))
    bAuth.send_message(msg.chat.id, "Код сюда же")
    bAuth.who = "shadowdemonhd_"
    bAuth.register_next_step_handler(msg, spauth_step2)

@bAuth.message_handler(commands=['orlega_'])
def spauth_telebot_shadowdemonhd_(msg):
    resp = req.get("https://clck.ru/--", params={'url': "https://accounts.spotify.com/authorize?" +  \
                'response_type' + '=' + "code" + "&" \
                "client_id" + '=' + CFG['sp_client_id'] + "&" \
                "scope" + '=' + 'ugc-image-upload user-read-playback-state app-remote-control user-modify-playback-state'\
                    ' playlist-read-private user-follow-modify playlist-read-collaborative user-follow-read'\
                    ' user-read-currently-playing user-read-playback-position user-library-modify'\
                    ' playlist-modify-private playlist-modify-public user-read-email user-top-read '\
                    ' user-read-recently-played user-read-private user-library-read' + "&" \
                "redirect_uri" + '=' + "http://денис.space/echo/code/" }).text
    bAuth.send_message(msg.chat.id, "Авторизация Spotify")
    bAuth.send_message(msg.chat.id, str(resp))
    bAuth.send_message(msg.chat.id, "Код сюда же")
    bAuth.who = "orlega_"
    bAuth.register_next_step_handler(msg, spauth_step2)

    
def spauth_step2(msg):
    bAuth.delete_message(msg.chat.id, msg.id)
    bAuth.send_message(msg.chat.id, "Код принят")
    bAuth.send_message(msg.chat.id, "Получаю токен...")
    resp = req.post("https://accounts.spotify.com/api/token", params={\
                "grant_type": "authorization_code", \
                    "code": msg.text, \
                "redirect_uri": "http://денис.space/echo/code/"}, headers={\
                "Authorization": f"Basic {CFG['sp_based']}", \
                "Content-Type": "application/x-www-form-urlencoded"}\
                ).json()
    bot.sp_token = resp['access_token']
    bot.sp_refresh = resp['refresh_token']
    bot.sp_data[bAuth.who] = {'access': resp['access_token'], 'refresh': resp['refresh_token']}
    spdataf = open("spotify.spdata", 'w')
    json.dump(bot.sp_data, spdataf)
    spdataf.close()
    bAuth.send_message(msg.chat.id, "Токен получен")
    try:
        resp = req.get("https://api.spotify.com/v1/me/player", headers={\
        'Authorization': f"Bearer {bot.sp_token}", \
        'Content-Type': "application/json"}).json()
        bAuth.send_message(msg.chat.id, f"\nСейчас играет: {resp['item']['name']} - {resp['item']['artists'][0]['name']}\n")
    except Exception: bAuth.send_message(msg.chat.id, "Музыка не играет!")
    thrd.Thread(target=bot.spreauth, args=(bAuth.who, )).start()
    bAuth.send_message(msg.chat.id, "Готово!!")


@bNot.message_handler(commands=['pingtotwitch'])
def notifer_ping(msg):
    if msg.from_user.username == "POAL48":
        p1 = msg.id
        p2 = bNot.send_message(msg.chat.id, "Пинганул в твич uuh").id
        bot.tgfw = "[]pingtotw[]poal[]"
        #bNot.delete_message(msg.chat.id, p1, timeout=5)
        bNot.delete_message(msg.chat.id, p2, timeout=5)
    #else: bNot.delete_message(msg.chat.id, msg.id)

@bNot.message_handler(commands=['pingtotwitchpw'])
def notifer_ping_pw(msg):
    if msg.from_user.username == "POAL48":
        p1 = msg.id
        p2 = bNot.send_message(msg.chat.id, "Пинганул в твич").id
        bot.tgfw = "[]pingtotw[]pw[]"
        #bNot.delete_message(msg.chat.id, p1)
        bNot.delete_message(msg.chat.id, p2, timeout=9)
    #else: bNot.delete_message(msg.chat.id, msg.id)

'''@bNot.message_handler(content_types=['text'])
def notifer_test(msg):
    if msg.from_user.username == "POAL48":
        bNot.delete_message(msg.chat.id, bNot.send_message(msg.chat.id, "123").id, timeout=10)'''   

@bNot.message_handler(content_types=["animation", "audio", "document", "photo", "sticker", "video", "voice", "video_note", "poll", "text"])
def notifer_message(msg):
    if not msg.sender_chat: return
    if msg.sender_chat.type == "channel" and (msg.sender_chat.username == "" or msg.sender_chat.username == "pwgood"):
        fw = ""
        if msg.text: fw += msg.text
        if msg.caption: 
            fw += ' "'
            fw += msg.caption
            fw += ' "'
        if msg.photo:
            file_i = bNot.get_file(msg.photo[len(msg.photo)-1].file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Фото: {resp['link']} "
        if msg.audio:
            file_i = bNot.get_file(msg.audio.file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Аудио: {resp['link']} "
        if msg.animation:
            file_i = bNot.get_file(msg.animation.file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Анимация: {resp['link']} "
        if msg.video:
            file_i = bNot.get_file(msg.video.file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Видео: {resp['link']} "
        if msg.document:
            file_i = bNot.get_file(msg.document.file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Документ: {resp['link']} "
        if msg.sticker:
            file_i = bNot.get_file(msg.sticker.file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Стикер: {resp['link']} "
        if msg.voice:
            file_i = bNot.get_file(msg.voice.file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Голос: {resp['link']} "
        if msg.video_note:
            file_i = bNot.get_file(msg.video_note.file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Кружочек (хз, наверное): {resp['link']} "
        bot.tgfw += fw

'''@bNot.channel_post_handler(content_types=["animation", "audio", "document", "photo", "sticker", "video", "voice", "video_note", "poll", "text"])
def notifer_post(msg):
    if True:
        fw = ""
        if msg.text: fw += msg.text
        if msg.caption: 
            fw += ' "'
            fw += msg.caption
            fw += ' "'
        if msg.photo:
            file_i = bNot.get_file(msg.photo[len(msg.photo)-1].file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Фото: {resp['link']} "
        if msg.audio:
            file_i = bNot.get_file(msg.audio.file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Аудио: {resp['link']} "
        if msg.animation:
            file_i = bNot.get_file(msg.animation.file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Анимация: {resp['link']} "
        if msg.video:
            file_i = bNot.get_file(msg.video.file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Видео: {resp['link']} "
        if msg.document:
            file_i = bNot.get_file(msg.document.file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Документ: {resp['link']} "
        if msg.sticker:
            file_i = bNot.get_file(msg.sticker.file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Стикер: {resp['link']} "
        if msg.voice:
            file_i = bNot.get_file(msg.voice.file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Голос: {resp['link']} "
        if msg.video_note:
            file_i = bNot.get_file(msg.video_note.file_id)
            file_d = bNot.download_file(file_i.file_path)
            wpt = open("temp.tg", 'wb')
            wpt.write(file_d)
            wpt.close()
            resp = req.post("https://gachi.gay/api/upload", files={'file': open("temp.tg", 'rb')}).json()
            fw += f" Кружочек (хз, наверное): {resp['link']} "
        bot.tgfw += fw'''

bAvg.USERDATA = json.load(open("avgUSERDATA.data", 'r'))

def bAvgSaveUserData():
    that = open("avgUSERDATA.data", 'w')
    json.dump(bAvg.USERDATA, that)
    that.close()

@bAvg.message_handler(commands=['start', 'help'])
def _start(msg):
    bAvg.send_message(msg.chat.id, "Сюда инструкцию")

@bAvg.message_handler(commands=['game'])
def _game(msg):
    try: bAvg.USERDATA['c'][msg.chat.id]['stat']
    except KeyError:
        bAvg.USERDATA['c'][msg.chat.id] = {\
            'stat': {'games': 0, 'wins': 0, 'loses': 0}, \
            'game': {}}
    bAvg.USERDATA['c'][msg.chat.id]['game'] = {'i': 1, 'history': [], 'ra': 0}
    bAvgSaveUserData()
    mark = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text = "Начать игру!", callback_data = f"gamestart")
    mark.add(btn1)
    bAvg.send_message(msg.chat.id, "123", reply_markup=mark)

@bAvg.callback_query_handler(func = lambda call:True)
def __ansfer___(call):
    msg = call.message
    if call.data == "gamestart":
        nicks = []
        for i in bot.avaGameAdd['compl'].keys(): nicks.append(i)
        true = choice(nicks)
        while true in bAvg.USERDATA['c'][msg.chat.id]['game']['history']:
            true = choice(nicks)
        bAvg.USERDATA['c'][msg.chat.id]['game']['r'] = true
        buttons = []
        buttons.append(types.InlineKeyboardButton(text = bot.avaGameAdd['compl'][true]['display'], callback_data = f"game.{true}"))
        for i in range(7):
            false = bAvg.USERDATA['c'][msg.chat.id]['game']['r']
            while false == bAvg.USERDATA['c'][msg.chat.id]['game']['r']:
                false = choice(nicks)
            buttons.append(types.InlineKeyboardButton(text = bot.avaGameAdd['compl'][false]['display'], callback_data = f"game.{false}"))
        shuffle(buttons)
        mark = types.InlineKeyboardMarkup()
        mark.add(buttons[0], buttons[1])
        mark.add(buttons[2], buttons[3])
        mark.add(buttons[4], buttons[5])
        mark.add(buttons[6], buttons[7])
        ulr.urlretrieve(bot.avaGameAdd['compl'][true]['image'], "avaGame.temp.png")
        bAvg.USERDATA['c'][msg.chat.id]['game']['msg'] = bAvg.send_photo(msg.chat.id, open("avaGame.temp.png", 'rb'), f"Раунд {bAvg.USERDATA['c'][msg.chat.id]['game']['i']}/10. Кто это?", reply_markup = mark).id
        bAvg.USERDATA['c'][msg.chat.id]['game']['history'].append(true)
        bAvgSaveUserData()
    if call.data.split('.')[0] == "game":
        last = bAvg.USERDATA['c'][msg.chat.id]['game']
        bAvg.USERDATA['c'][msg.chat.id]['game']['i'] += 1
        if call.data.split('.')[1] == bAvg.USERDATA['c'][msg.chat.id]['game']['r']:
            bAvg.USERDATA['c'][msg.chat.id]['game']['ra'] += 1
            mark = types.InlineKeyboardMarkup()
            mark.add(types.InlineKeyboardButton(f"✅ Верно, {bot.avaGameAdd['compl'][bAvg.USERDATA['c'][msg.chat.id]['game']['r']]['display']}", callback_data='pass'))
            bAvg.edit_message_caption(f"Верно угадано, правильных ответов: {bAvg.USERDATA['c'][msg.chat.id]['game']['ra']}", msg.chat.id, bAvg.USERDATA['c'][msg.chat.id]['game']['msg'], reply_markup=mark)
        else:
            mark = types.InlineKeyboardMarkup()
            mark.add(types.InlineKeyboardButton(f"❌ Неверно, {bot.avaGameAdd['compl'][bAvg.USERDATA['c'][msg.chat.id]['game']['r']]['display']}", callback_data='pass'))
            bAvg.edit_message_caption(f"Неверно угадано, правильных ответов: {bAvg.USERDATA['c'][msg.chat.id]['game']['ra']}", msg.chat.id, bAvg.USERDATA['c'][msg.chat.id]['game']['msg'], reply_markup=mark)
        if bAvg.USERDATA['c'][msg.chat.id]['game']['i'] == 11:
            return
        nicks = []
        for i in bot.avaGameAdd['compl'].keys(): nicks.append(i)
        true = choice(nicks)
        while true in bAvg.USERDATA['c'][msg.chat.id]['game']['history']:
            true = choice(nicks)
        bAvg.USERDATA['c'][msg.chat.id]['game']['r'] = true
        buttons = []
        buttons.append(types.InlineKeyboardButton(text = bot.avaGameAdd['compl'][true]['display'], callback_data = f"game.{true}"))
        for i in range(7):
            false = bAvg.USERDATA['c'][msg.chat.id]['game']['r']
            while false == bAvg.USERDATA['c'][msg.chat.id]['game']['r']:
                false = choice(nicks)
            buttons.append(types.InlineKeyboardButton(text = bot.avaGameAdd['compl'][false]['display'], callback_data = f"game.{false}"))
        shuffle(buttons)
        mark = types.InlineKeyboardMarkup()
        mark.add(buttons[0], buttons[1])
        mark.add(buttons[2], buttons[3])
        mark.add(buttons[4], buttons[5])
        mark.add(buttons[6], buttons[7])
        try:
            ulr.urlretrieve(bot.avaGameAdd['compl'][true]['image'], "avaGame.temp.png")
        except Exception:
            mark = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text = "Продолжить", callback_data = f"gamestart.{last['r']}")
            mark.add(btn)
            bAvg.send_message(msg.chat.id, "Проблема с получением аватарки следующего чаттера, скорее всего он ее поменял. Данные откатаны, нажми на кнопку", reply_markup=mark)
            bAvg.USERDATA['c'][msg.chat.id]['game'] = last
            bot.avaGameAdd['ignore'].remove(true)
            bot.avaGameAdd['compl'].pop(true)
            agaw = open("avaGameAdd.data", 'w')
            json.dump(bot.avaGameAdd, agaw)
            agaw.close()
            bAvgSaveUserData()
            return
        bAvg.USERDATA['c'][msg.chat.id]['game']['msg'] = bAvg.send_photo(msg.chat.id, open("avaGame.temp.png", 'rb'), f"Раунд {bAvg.USERDATA['c'][msg.chat.id]['game']['i']}/10. Кто это?", reply_markup = mark).id
        bAvg.USERDATA['c'][msg.chat.id]['game']['history'].append(true)
        bAvgSaveUserData()


@bSpin.message_handler(commands=['start'])
def bSpinStart(msg):
    bSpin.send_message(msg.chat.id, "Hui")
        

def startBotAvaGame():
    #while True:
    if True:
        #try:
        bAvg.polling(none_stop=False)
        #except Exception as e: print(f"bAvg {type(e)}: {e}")
        
def startBotAuth():
    while True:
        try: bAuth.polling(none_stop=False)
        except Exception as e: print(f"bAuth {type(e)}: {e}")

def startBotNotifer():
    while True:
        try: bNot.polling(none_stop=False)
        except Exception as e: print(f"bNot {type(e)}: {e}")

def startBotSpin():
    while True:
        try: bSpin.polling(none_stop=False)
        except Exception as e: print(f"bSpin {type(e)}: {e}")

thrd.Thread(target=startBotAuth).start()
thrd.Thread(target=startBotNotifer).start()
thrd.Thread(target=startBotAvaGame).start()
thrd.Thread(target=startBotSpin).start()

print("Bot starting...\n")

bot.run()




