import pygamescreens as pgs
import asyncio
import websockets as wbs
import json
import threading as th
from pytube import YouTube, exceptions
import subprocess as subp
import cv2 as cv
import urllib.request as ulr
import webbrowser
import os
import pathlib
import datetime as dt
import tkinter.messagebox as msgb

#if 1:
try:   
    Buttons = []
    class Button(): #Класс кнопки
        def __init__(self, x, y, width, height, root, buttonText='Button', onclickFunction=None, onePress=False, hWWW = 1.1, **kwargs): #Инициализация
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.onclickFunction = onclickFunction
            self.onePress = onePress
            self.hWWW = hWWW
            self.root = root
            try: self.textSize = kwargs['textSize']
            except KeyError: self.textSize = 20
            pgs.pg.alreadyPressed = False

            self.fillColors = {
                'normal': '#afafaf',
                'hover': '#858585',
                'pressed': '#757575',
            }

            self.buttonSurface = pgs.pg.Surface((self.width, self.height))
            self.buttonRect = pgs.pg.Rect(self.x, self.y, self.width, self.height)

            font = pgs.pg.font.SysFont('Arial', self.textSize)
            self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

            self.st = False

            Buttons.append(self)

        def process(self): #Функция рендера кнопки, используется каждый кадр
            if self.st:
                mousePos = pgs.pg.mouse.get_pos()
                self.buttonSurface.fill(self.fillColors['normal'])
                if self.buttonRect.collidepoint(mousePos):
                    self.buttonSurface.fill(self.fillColors['hover'])
                    if pgs.pg.mouse.get_pressed(num_buttons=3)[0]:
                        self.buttonSurface.fill(self.fillColors['pressed'])
                        if self.onePress:
                            self.onclickFunction()
                        elif not pgs.pg.alreadyPressed:
                            self.onclickFunction()
                            pgs.pg.alreadyPressed = True
                    else:
                        pgs.pg.alreadyPressed = False

                self.buttonSurface.blit(self.buttonSurf, [
                    self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
                    self.buttonRect.height/self.hWWW - self.buttonSurf.get_rect().height/self.hWWW
                ])
                self.root.blit(self.buttonSurface, self.buttonRect)

        def hide(self): self.st = False #Выключает рендер кнопки
        def show(self): self.st = True #Включает рендер кнопки

    def addText(sfont, text, color, x, y, root): #Вспомогательная функция рендера любого текста
        rend = sfont.render(text, True, color)
        root.blit(rend, (x-(sfont.size(text)[0]/2), y-(sfont.size(text)[1]/2)))

    def addTextLeft(sfont, text, color, x, y, root): #Вспомогательная функция рендера любого текста
        rend = sfont.render(text, True, color)
        root.blit(rend, (x, y))

    Inputs = []
    class InputBox:
        def __init__(self, x, y, w, h, root, text="", fn=None):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.rect = pgs.pg.Rect(x, y, w, h)
            self.INACTIVE = pgs.pg.Color(175, 175, 175)
            self.ACTIVE = pgs.pg.Color(128, 128, 128)
            self.color = self.INACTIVE
            self.text = text
            self.start_text = text
            self.isFirstTouch = True
            self.root = root
            self.fn = fn
            self.active = True
            self.isShow = False
            addText(pgs.pg.font.SysFont("Arial", 20), self.text, (0, 0, 0), x+w//2, y+h//2, root)
            Inputs.append(self)

        def mouseDown(self, root, event):
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.ACTIVE
                if self.isFirstTouch:
                    self.text = ""
                    self.isFirstTouch = False
            else:
                self.active = False
                self.color = self.INACTIVE
                if self.text == "":
                    self.text = self.start_text
                    self.isFirstTouch = True
            
        def keyDown(self, root, event):
            if self.active:
                if event.key == pgs.pg.K_RETURN:
                    if self.fn:
                        self.fn()
                elif event.key == pgs.pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

        def update(self):
            if self.isShow:
                pgs.pg.draw.rect(self.root, self.color, self.rect)
                addText(pgs.pg.font.SysFont("Arial", 20), self.text, (0, 0, 0), self.x+self.w//2, self.y+self.h//2, self.root)

        def hide(self):
            self.isShow = False
        def show(self):
            self.isShow = True
        def toggle(self):
            self.isShow = not self.isShow

    class Player:
        def __init__(self):
            self.is_play = False
            self.is_pause = False
            self.playing = None
            self.shift = 0.0
        def togglePlay(self):
            log(f"in Player togglePlay: togglePlay задействовена, выясняю ситуацию")
            if not self.is_play:
                log("in Player togglePlay: похоже, ничего не играло, включаю следующий трек")
                song = None
                for i in g.songs:
                    if i.status == "ready":
                        song = i
                        break
                if not song:
                    return
                self.playing = song
                pgs.pg.mixer.music.load(f"{g.PATH}cache/{song.id}.mp3")
                pgs.pg.mixer.music.play()
                self.is_play = True
                self.shift = 0.0
                log(f"in Player togglePlay: трек {self.playing.id} - {self.playing.title} играет!")
            elif not self.is_pause and self.is_play:
                pgs.pg.mixer.music.pause()
                self.is_pause = True
                log(f"in Player togglePlay: поставил воспроизведение на паузу. Трек: {self.playing.id} - {self.playing.title}")
            elif self.is_pause and self.is_play:
                pgs.pg.mixer.music.unpause()
                self.is_pause = False
                log(f"in Player togglePlay: снял воспроизведение С паузы. Трек: {self.playing.id} - {self.playing.title}")
        def run(self):
            if True:
                if self.is_play:  
                    if not self.is_pause:
                        if not pgs.pg.mixer.music.get_busy():
                            log(f"in Player run: обнаружил конец песни, включаю следующую")
                            index = g.songs.index(self.playing)
                            self.playing.status = "played"
                            g.songs[index] = self.playing
                            self.is_play = False
                            pgs.pg.mixer.music.unload()
                            th.Thread(target=self.playing.delete()).start()
                            log(f"in Player run: песня отгружена, и готова к удалению")
                            while not pgs.pg.mixer.music.get_busy(): self.togglePlay()
                            log(f"in Player run: следующая песня играет")
        def back(self):
            log("in Player back: получил back, проверяю наличие музыки")
            if pgs.pg.mixer.music.get_busy() or (not pgs.pg.mixer.music.get_busy() and self.is_pause):
                pos = pgs.pg.mixer.music.get_pos() / 1000 + self.shift
                pos -= 10.0
                self.shift -= 10.0
                if pos < 0:
                    self.shift += pos * -1
                    pos = 0.0
                length = pgs.pg.mixer.Sound(f"{g.PATH}cache/{self.playing.id}.mp3").get_length()
                if pos > length: pos = length
                pgs.pg.mixer.music.set_pos(pos)
                log(f"in Player back: отматал песню. get_pos: {pgs.pg.mixer.music.get_pos()}, pos: {pos}, shift: {self.shift}")
        def forw(self):
            log("in Player forw: получил forw, проверяю наличие музыки")
            if pgs.pg.mixer.music.get_busy() or (not pgs.pg.mixer.music.get_busy() and self.is_pause):
                pos = pgs.pg.mixer.music.get_pos() / 1000 + self.shift
                pos += 10.0
                self.shift += 10.0
                if pos < 0:
                    self.shift += pos * -1
                    pos = 0.0
                length = pgs.pg.mixer.Sound(f"{g.PATH}cache/{self.playing.id}.mp3").get_length()
                if pos > length: pos = length
                pgs.pg.mixer.music.set_pos(pos)
                log(f"in Player forw: отматал песню. get_pos: {pgs.pg.mixer.music.get_pos()}, pos: {pos}, shift: {self.shift}")
        def skip(self):
            pgs.pg.mixer.music.pause()
            log(f"in Player skip: поставил на паузу без тега, трек будет пропущен")


    class Song:
        def __init__(self, _id, title, author, by, status):
            self.id = _id
            self.title = title
            self.author = author
            self.by = by
            self.status = status
        def download(self):
            downloader(self)
        def delete(self):
            deleter(self)

    #class App: CLUELESS
    #    def __init__(self):
    #        pass


    class Globals:
        def __init__(self):
            self.err = "Unknown Error"
            self.data = []
            self.auth = None
            self.send = None
            self.recv = None
            self.answ = None
            self.ws = None
            self.songs = []
            self.player = None
            self.PATH = "cache"
            self.savedAuth = {"name": "", "pass": ""}
            #log("in Globals __init__: глобалы успешно созданы")


    songStructure = {
        "id": "YouTube Video Id - Будет использоваться также в названиях файлов",
        "title": "Название видео",
        "author": "Автор видео",
        "by": "Автор сра",
        "status": "added или not_dwd или ready или played или deleted - added только добавлен, not_dwd - скачивается, ready - скачан и готов, played - проиграна, deleted - призвана удалится со стороны бота"
    }

    g = Globals()

    def log(tolog: str) -> None:
        logfile = open(g.PATH + "logs.txt", 'a')
        logfile.write("\n" + dt.datetime.now().strftime("%H:%M:%S : ") + tolog)
        logfile.close()

    VERSION = "B1.0"

    @pgs.onStart()
    def on_start(root):
        log(f"in on_start: PyGame начал своё существование, инициализируюсь")
        g.root = root
        pgs.pg.display.set_caption("ppSpin Song Requests Client")
        textNameInput = "Имя"
        textPassInput = "Пин-код"
        if g.savedAuth['name']:  textNameInput = g.savedAuth['name']
        if g.savedAuth['pass']: textPassInput = g.savedAuth['pass']
        g.nameInput = InputBox(200, 50, 430, 30, root, textNameInput, check_pswd)
        g.passInput = InputBox(200, 130, 430, 30, root, textPassInput, check_pswd)
        g.cnctBtn = Button(282, 210, 265, 30, root, "Подключиться", check_pswd)
        g.playBtn = Button(830-50-50, 580-30-50, 50, 50, root, "Play", toggle_play)
        g.openBtn = Button(830-50-50-30-50, 580-30-50, 50, 50, root, "Open", open_song)
        g.backBtn = Button(830-50-50-30-50-30-50-30-50, 580-30-50, 50, 50, root, "Back", back_song)
        g.forwBtn = Button(830-50-50-30-50-30-50, 580-30-50, 50, 50, root, "Forw", forw_song)
        g.skipBtn = Button(830-50-50-30-50-30-50-30-50-30-50, 580-30-50, 50, 50, root, "Skip", skip_song)
        pgs.setScreen("start")
        log("in on_start: инициализация успешна")

    @pgs.subEvent(pgs.pg.KEYDOWN, pgs.pg.K_LEFT)
    def k_back_song(root, event):
        if g.player:
            log("in k_back_song: клавиша LEFT нажата, передаюсь в Player.back()")
            g.player.back()

    @pgs.subEvent(pgs.pg.KEYDOWN, pgs.pg.K_RIGHT)
    def k_forw_song(root, event):
        if g.player:
            log("in k_forw_song: клавиша RIGHT нажата, передаюсь в Player.forw()")
            g.player.forw()

    @pgs.subEvent(pgs.pg.KEYDOWN, pgs.pg.K_ESCAPE)
    def k_skip_song(root, event):
        if g.player:
            log("in k_skip_song: клавиша ESCAPE нажата, передаюсь в Player.skip()")
            g.player.skip()

    def back_song():
        if g.player:
            log("in back_song: back_song задайственена, передаюсь в Player.back()")
            g.player.back()

    def forw_song():
        if g.player:
            log("in forw_song: forw_song задайственена, передаюсь в Player.forw()")
            g.player.forw()

    def skip_song():
        if g.player:
            log("in skip_song: skip_song задайственена, передаюсь в Player.skip()")
            g.player.skip()  

    @pgs.onUpdate()
    def on_update(root):
        for i in Buttons:
            i.process()
        for i in Inputs:
            i.update()

    @pgs.onScreenChange()
    def on_screen_change(root):
        log(f"in on_screen_change: экран поменялся на {pgs.pgsGlobals.screen}")
        for i in Buttons:
            i.hide()
        for i in Inputs:
            i.hide()

    @pgs.addScreen("start")
    def sc_start(root: pgs.pg.display):
        root.fill((50, 50, 50))
        g.nameInput.show()
        g.passInput.show()
        g.cnctBtn.show()

    def check_pswd():
        g.auth = {"name": g.nameInput.text, "pass": g.passInput.text}
        log(f"in check_pswd: отправляю на проверку ник и пароль: {g.nameInput.text} - {g.passInput.text}")
        sets = open(g.PATH + "settings.json", 'w')
        json.dump({
            "name": g.nameInput.text,
            "pass": g.passInput.text
        }, sets)
        sets.close()
        log(f"in check_pswd: ник и пароль сохранены в память, переключаю экран на loading")
        pgs.setScreen("loading")

    @pgs.addScreen("loading")
    def sc_loading(root: pgs.pg.display):
        root.fill((50, 50, 50))
        addText(pgs.pg.font.SysFont("Arial", 50), "Connecting to ws...", (255, 255, 255), 415, 250, root)

    def srsongadd(data):
        log(f"in srsongadd: получил запрос на добавление песни {data['data']['vid_id']} от {data['data']['by']}")
        try:
            vid = YouTube(f"https://youtu.be/{data['data']['vid_id']}")
            '''song = {
                "id": data['data']['vid_id'],
                "title": vid.title,
                "author": vid.author,
                "by": data['data']['by'],
                "status": "added",
                "isReadyChecked": False
            }'''
            song = Song(data['data']['vid_id'], vid.title, vid.author, data['data']['by'], "added")
            g.songs.append(song)
            answ("sr.song.add", "ok", "song added", 6900)
            th.Thread(target=song.download()).start()
            log(f"in srsongadd: песня {data['data']['vid_id']} - {vid.title} успешно добавлена в глобальный список песен, отправляю код 6900")
        except Exception as e:
            answ("sr.song.add", "err", "Unknown", 6969)
            log(f"in srsongadd: при добавлени песни {data['data']['vid_id']} произошла неожиданная ошибка {e} - {type(e)}, отправляю код 6969")

    def srsongremove(data):
        log(f"in srsongremove: получил запрос на удаление песни {data['data']['vid_id']}, удаляю...")
        for i in range(len(g.songs)):
            if g.songs[i].id == data['data']['vid_id']:
                g.songs[i].status = "deleted"
                g.songs[i].delete()
        answ("sr.song.remove", "ok", "song removed", 6900)
        log(f"in srsongremove: песня {data['data']['vid_id']} удалена, отвечаю")

    def servping(data):
        log("in servping: получил serv.ping, отвечаю")
        answ("serv.ping", "ok", "Pong!", 6900)

    def servcheckver(data):
        log(f"in servcheckver: отвечаю на чек версии, версия: {VERSION}")
        g.answ = {"op": "serv.check_ver_answer", "data": {"ver": VERSION}}

    def answ(op, status, info, code):
        log(f"in answ: отвечаю: op: {op}, status: {status}, info: {info}, code: {code}")
        g.answ = {"op": "serv.answer", "data": {"op": op, "status": status, "info": info, "code": str(code)}}

    @pgs.subEvent(pgs.pg.KEYDOWN, pgs.pg.K_SPACE)
    def k_space(root, event):
        log("in k_space: пробел нажат, проверяю существование Player'a")
        if g.player:
            log("in k_space: Player существует, передаюсь в Player.togglePlay")
            g.player.togglePlay()

    def toggle_play():
        if g.player:
            log("in toggle_play: toggle play заюзана, передаюсь в Player.togglePlay")
            g.player.togglePlay()

    def deleteSong(vid_id):
        pass

    def open_song():
        if g.player:
            log("in open_song: начинаю открывать сонг, проверяю наличие играющей песни")
            if g.player.playing:
                webbrowser.open(f"https://youtu.be/{g.player.playing.id}", 2)
                log(f"in open_song: песня играла, ссылка открыта. {g.player.playing.id} - {g.player.playing.title}")

    @pgs.subEvent(pgs.pg.MOUSEBUTTONDOWN)
    def mouseDownTipo(root, event):
        log("in mouseDownTipo: мышь нажата")
        if g.player:
            rect = pgs.pg.Rect(820, 0, 20, 580)
            log("in mouseDownTipo: проверяю на попадание в хитбокс линии громоксти")
            if rect.collidepoint(event.pos):
                pgs.pg.mixer.music.set_volume(event.pos[1] / 580)
                log(f"in mouseDownTipo: мышь попала в хитбокс громкости, теперь громкость равна: {round(event.pos[1] / 580, 3)} ({event.pos[1]})")

    @pgs.subEvent(pgs.pg.MOUSEWHEEL)
    def mouseWheel(root, event):
        log("in mouseWheel: движение колесиком мыши")
        if g.player:
            vol = pgs.pg.mixer.music.get_volume()
            vol += (event.y * 0.025)
            if vol < 0: vol = 0
            elif vol > 1: vol = 1
            log(f"in mouseWheel: громкость изменена на {event.y * 0.025}, теперь равна {vol}")
            pgs.pg.mixer.music.set_volume(vol)

    @pgs.addScreen("main")
    def sc_main(root: pgs.pg.display):
        root.fill((100, 100, 100))
        g.playBtn.show()
        g.openBtn.show()
        g.backBtn.show()
        g.forwBtn.show()
        g.skipBtn.show()
        g.player.run()
        vol_cord = int(pgs.pg.mixer.music.get_volume() * 580)
        pgs.pg.draw.line(root, (255, 255, 255), (820, 0), (820, 580), 20)
        pgs.pg.draw.line(root, (100, 255, 100), (820, 0), (820, vol_cord), 20)
        ny = 30
        for i in g.songs:
            x = 20
            if i.status == "ready":
                thumb_surf = pgs.pg.image.load(f"{g.PATH}cache/{i.id}.png")
                root.blit(thumb_surf, (x, ny))
                x += thumb_surf.get_width() + 10
            addTextLeft(pgs.pg.font.SysFont("Segoe UI Bold", 20), i.title, (0, 0, 0), x, ny, g.root)
            ny += 20 + 10
            addTextLeft(pgs.pg.font.SysFont("Segoe UI Bold", 16), i.author, (0, 0, 0), x, ny, g.root)
            ny += 16 + 10
            addTextLeft(pgs.pg.font.SysFont("Segoe UI Bold", 16), i.by, (0, 0, 0), x, ny, g.root)
            ny += 16 + 20

    @pgs.addScreen("error")
    def sc_error(root: pgs.pg.display):
        root.fill((50, 50, 50))
        addText(pgs.pg.font.SysFont("Arial", 10), f"Error: {g.err}", (255, 255, 255), 315, 180, root)

    @pgs.subEvent(pgs.pg.MOUSEBUTTONDOWN)
    def mouseDown(root, event):
        log("in mouseDown: прожал MOUSEDOWN для всех Inputs")
        for i in Inputs:
            i.mouseDown(root, event)

    @pgs.subEvent(pgs.pg.KEYDOWN)
    def keyDown(root, event):
        log("in keyDown: прожал KEYDOWN для всех Input")
        for i in Inputs:
            i.keyDown(root, event)

    def downloader(song: Song):
        log("in downloader: downloader открыт")
        #while 1:
        if 1:
            #for i in range(len(g.songs)):
            if 1:
                try:
                    #if g.songs[i]['status'] == "added":
                    if 1:
                        index = g.songs.index(song)
                        log(f"in downloader: найдена песня для скачивания: {song.id} - {song.title}")
                        song.status = "not_dwd"
                        try: vid = YouTube(f"https://youtu.be/{song.id}")
                        except exceptions.AgeRestrictedError as e:
                            log(f"in downloader: произошла AgeRestictedError при скачивании {song.id} - {song.title}")
                            song.status = "played"
                            return
                        except exceptions.VideoUnavailable as e:
                            log(f"in downloader: произошла VideoUnavailable при скачивании {song.id} - {song.title}")
                            song.status = "played"
                            return
                        try:
                            stream = vid.streams.filter(file_extension="webm", only_audio=True)[0]
                            stream.download(g.PATH+"cache/", song.id+".webm")
                        except exceptions.AgeRestrictedError as e:
                            log(f"in downloader: произошла AgeRestictedError при скачивании {song.id} - {song.title}")
                            song.status = "played"
                            return
                        except exceptions.VideoUnavailable as e:
                            log(f"in downloader: произошла VideoUnavailable при скачивании {song.id} - {song.title}")
                            song.status = "played"
                            return
                        log(f"in downloader: .webm песни {song.id} - {song.title} упешно скачан")
                        subp.run(f"ffmpeg -i {g.PATH}cache/{song.id}.webm {g.PATH}cache/{song.id}.mp3 -y", shell = True)
                        log(f"in downloader: .wemp -> .mp3 сконвертировалось успешно для песни {song.id} - {song.title}")
                        ulr.urlretrieve(vid.thumbnail_url, f"{g.PATH}cache/{song.id}.jpg")
                        log(f"in downloader: обложка .jpg упешно скачна для песни {song.id} - {song.title}")
                        frame = cv.imread(f"{g.PATH}cache/{song.id}.jpg")
                        ys, xs, _ = frame.shape
                        yr = 75
                        xr = xs // (ys // yr)
                        frame = cv.resize(frame, (xr, yr))
                        cv.imwrite(f"{g.PATH}cache/{song.id}.png", frame)
                        log(f"in downloader: обложка успешно ресайзнута в .png для песни {song.id} - {song.title}")
                        song.status = "ready"
                        print(f"Song {song.title} ready")
                        g.songs[index] = song
                        log(f"in downloader: Песня {song.id} - {song.title} готова! ")
                except IndexError: pass


    def deleter(song: Song):
        log("in deleter: deleter запущен")
        #while 1:
        if 1:
            #for i in range(len(g.songs)):
            if 1:
                '''if g.songs[i]['status'] == "ready" and not g.songs[i]['isReadyChecked']:
                    log(f"in deleter: найдена готовая песня {g.songs[i]['id']} - {g.songs[i]['title']}, удаляю остатки")
                    try:
                        os.remove(f"{g.PATH}cache/{g.songs[i]['id']}.webm")
                        log(f"in deleter: удалил {g.songs[i]['id']}.webm ({g.songs[i]['title']})")
                    except Exception as e: log(f"in deleter: не смог удалить {g.songs[i]['id']}.webm ({g.songs[i]['title']}) из-за {e} - {type(e)}")
                    try:
                        os.remove(f"{g.PATH}cache/{g.songs[i]['id']}.jpg")
                        log(f"in deleter: удалил {g.songs[i]['id']}.jpg ({g.songs[i]['title']})")
                    except Exception as e: log(f"in deleter: не смог удалить {g.songs[i]['id']}.jpg ({g.songs[i]['title']}) из-за {e} - {type(e)}")
                    g.songs[i]['isReadyChecked'] = True'''
                #if g.songs[i]['status'] == "played" or g.songs[i]['status'] == "deleted":
                if 1:
                    index = g.songs.index(song)
                    try:
                        os.remove(f"{g.PATH}cache/{song.id}.webm")
                    except Exception: pass
                    try:
                        os.remove(f"{g.PATH}cache/{song.id}.jpg")
                    except Exception: pass
                    try:
                        os.remove(f"{g.PATH}cache/{song.id}.mp3")
                        log(f"in deleter: удалил {song.id}.mp3 ({song.title})")
                    except Exception as e: log(f"in deleter: не смог удалить {song.id}.mp3 ({song.title}) из-за {e} - {type(e)}")
                    try:
                        os.remove(f"{g.PATH}cache/{song.id}.png")
                        log(f"in deleter: удалил {song.id}.png ({song.title})")
                    except Exception as e: log(f"in deleter: не смог удалить {song.id}.png ({song.title}) из-за {e} - {type(e)}")
                    if song.status == "played": g.answ = {"op": "sr.song.remove", "data": {"vid_id": song.id}}
                    log(f"in deleter: Песня {song.id} - {song.title} удалена")
                    g.songs[index] = song
                    g.songs.remove(song)

    def start():
        log("Основной поток экрана....")
        pgs.simpleStartLoop(60, 830, 580)

    async def ws_handler_sender():
        log("in async ws_handler_sender: открыт, жду появления ws в глобале")
        while not g.ws: pass
        log("in async ws_handler_sender: ws получен, начинаю отправлять сообщения")
        try:
            while 1:
                if g.send:
                    await g.ws.send(json.dumps(g.send))
                    g.send = None
                    g.recv = json.loads(await g.ws.recv())
                if g.answ:
                    log("in async ws_handler_sender: новый answer получен, отправляю его")
                    await g.ws.send(json.dumps(g.answ))
                    g.answ = None
        finally:
            log("in async ws_handler_sender: подключение закрыто LULVV")

    async def ws_handler(ws):
        try:
            log("in async ws_handler: подключился, жду превественное сообщение")
            async with asyncio.timeout(30):
                hi = json.loads(await ws.recv())
        except TimeoutError:
            g.err = "Timeout: прошел тайм оут подключения, но сервер ничего не отправил"
            log("in async ws_handler: тайм оут подключения прошел, переключаюсь на экран error")
            pgs.setScreen("error")
            return
        if hi['code'] == "6900":
            await ws.send(json.dumps({
                "nick": g.auth['name'],
                "pass": g.auth['pass'],
                "data": {}
            }))
            log("in async ws_handler: отправил данные для аутификации, жду подтверждение")
            data = json.loads(await ws.recv())
            if data['code'] == "6900":
                g.ws = ws
                g.player = Player()
                pgs.setScreen("main")
                log("in async ws_handler: код 6900 после аутификации, запустил плеер и переключил экран на main, запускаю ожидание сообщений")
                async for msg in ws:
                    g.data.append(json.loads(msg))
                    log("in async ws_handler: получено новое сообщение")
                    ops = {
                        "sr.song.add": srsongadd,
                        "sr.song.remove":srsongremove,
                        "serv.ping": servping,
                        "serv.check_ver": servcheckver
                    }
                    data = json.loads(msg)
                    if data['op'] in ops.keys():
                        log(f"in async ws_handler: операция сообщения известна: {data['op']}")
                        th.Thread(target=ops[data['op']], args=(data, )).start()
            elif data['code'] == "6904":
                g.err = "Nick not found: введенный ник не существует в базе данных"
                log("in async ws_handler: при аутификации возник код ошибки 6904, ник не найден в базе данных, переключаюсь на экран error")
                pgs.setScreen("error")
                return
            elif data['code'] == "6905":
                g.err = "incorrect password: введенный пин-код неверный"
                log("in async ws_handler: при аутификации возник код ошибки 6905, пин-код неверный, переключаюсь на экран error")
                pgs.setScreen("error")
                return

    async def start_ws():
        log("async start_ws открыт, жду аутефикации")
        while not g.auth: pass
        HOSTNAME = "ws://localhost:6969"
        log(f"in asnyc start_ws: Аутификация завершена, пытаюсь подключится к {HOSTNAME}")
        async with wbs.connect(HOSTNAME) as ws:
            log(f"in async start_ws: веб сокет подключен, перехожу в хандлер функцию")
            await ws_handler(ws)

    def start_ws_sender_handler():
        loop = asyncio.new_event_loop()
        loop.run_until_complete(ws_handler_sender())
        loop.run_forever()

    def start_ws_sync():
        loop = asyncio.new_event_loop()
        loop.run_until_complete(start_ws())
        loop.run_forever()

    def pre_start_operations():
        username = str(pathlib.Path.home())
        username = username.split("\\")[len(username.split("\\"))-1]
        g.PATH = f"C:/Users/{username}/ppSpinSrClient/"
        if not os.path.exists(g.PATH):
            os.mkdir(os.path.join(f"C:\\Users\\{username}", "ppSpinSrClient"))
        if not os.path.exists(g.PATH+"settings.json"):
            sets = open(g.PATH + "settings.json", 'w')
            json.dump({
                "name": "",
                "pass": ""
            }, sets)
            sets.close()
        log1 = open(g.PATH + "logs.txt", 'w')
        log1.close()
        log("logs.txt очищен")
        g.savedAuth = json.load(open(g.PATH + "settings.json", 'r'))
        log("pre работы завершены успешно")
        

    if __name__ == "__main__":
        pre_start_operations()
        th.Thread(target=start_ws_sender_handler).start()
        th.Thread(target=start_ws_sync).start()
        start()

except Exception as e:
    msgb.showerror("Ошибка!", f"Произошел сбой в работе программы: {e}. Дополнительная информация в логах")
    logf = open(g.PATH + "logs.txt", 'a')
    logf.write("\n" + dt.datetime.now().strftime("%H:%M:%S: ") + "Произошла ошибка\n")
    logf.write(str(e) + "\n")
    logf.write(str(type(e)) + "\n")
    logf.write(str(e.args) + "\n")
    logf.close()
    pgs.pg.quit()
    exit()
    