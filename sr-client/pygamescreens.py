import pygame as pg

class PgsNone: pass

class PgsGlobals:
    def __init__(self):
        self.screens = {}
        self.screen = PgsNone()
        self.root = PgsNone()
        self.events = []
        self.thatEvents = {}

class PyGameScreensException(Exception): pass

pgsGlobals = PgsGlobals()

def addScreen(name=None):
    def addScreenstep(fn):
        if type(name) == type(None):
            raise PyGameScreensException("Screen should have a name!")
        pgsGlobals.screens[name] = {'call': fn}
    return addScreenstep

def subEvent(evtype=None, key=None):
    def subEventstep(fn):
        if type(evtype) == type(None):
            raise PyGameScreensException("No event provided")
        pgsGlobals.events.append({'event': evtype, 'key': key, 'call': fn})
    return subEventstep

def onStart():
    def onStartstep(fn):
        pgsGlobals.thatEvents['start'] = fn
    return onStartstep

def onUpdate():
    def onUpdatestep(fn):
        pgsGlobals.thatEvents['update'] = fn
    return onUpdatestep

def onScreenChange():
    def onScreenChangestep(fn):
        pgsGlobals.thatEvents['screenChange'] = fn
    return onScreenChangestep

def setScreen(screenName: str):
    if not screenName in pgsGlobals.screens.keys():
        raise PyGameScreensException("Screen did not found")
    pgsGlobals.screen = screenName
    if "screenChange" in pgsGlobals.thatEvents.keys():
        if not type(pgsGlobals.root) == type(PgsNone()):
            pgsGlobals.thatEvents['screenChange'](pgsGlobals.root)

def simpleStartLoop(fps: int, width: int, height: int, *args, **kwargs):
    pg.init()
    pgsGlobals.root = pg.display.set_mode((width, height), *args)
    fpsClock = pg.time.Clock()
    state = True
    if 'start' in pgsGlobals.thatEvents.keys():
        pgsGlobals.thatEvents['start'](pgsGlobals.root)
    while state:
        for e in pg.event.get():
            for i in range(len(pgsGlobals.events)):
                if e.type == pgsGlobals.events[i]['event']:
                    if pgsGlobals.events[i]['key']:
                        if e.key:
                            if e.key == pgsGlobals.events[i]['key']: pgsGlobals.events[i]['call'](pgsGlobals.root, e)
                    else: pgsGlobals.events[i]['call'](pgsGlobals.root, e)
            if e.type == pg.QUIT:
                state = False
                break
        if type(pgsGlobals.screen) == type(PgsNone()):
            continue

        if not pgsGlobals.screen in pgsGlobals.screens.keys():
            raise PyGameScreensException("Screen name did not found")

        pgsGlobals.screens[pgsGlobals.screen]['call'](pgsGlobals.root)

        if "update" in pgsGlobals.thatEvents.keys():
            pgsGlobals.thatEvents['update'](pgsGlobals.root)
        
        pg.display.flip()
        fpsClock.tick(fps)
    pg.quit()
