from javascript import require, On
from javascript.proxy import Proxy
from functools import cached_property, partial
from typing import Any, Callable
from scatteredFile.argParse import command, interpreter
from scatteredFile.debuger import debuger


mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
viewer = require('prismarine-viewer')


class Bot:
    def __init__(self, botName: str, *, host: str = '127.0.0.1', port: int = 25565):
        self._botName, self._host, self._port = botName, host, port
        self._plugins = {}

        self.bindOn()

    @property
    def botName(self):
        return self._botName

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def plugins(self):
        return self._plugins

    @plugins.setter
    def plugins(self, value):
        self._plugins = value

    @cached_property
    def bot(self):
        return mineflayer.createBot({
            'host':     self.host,
            'port':     self.port,
            'username': self.botName
        })

    def registerPlugins(self, plugin: Any):
        self.bot.loadPlugin(plugin)

    def bindOn(self):
        On(self.bot, 'spawn')(self.handleSpawn)
        On(self.bot, 'message')(self.handleMessage)

    @staticmethod
    def handleSpawn(*args):
        print("spawned")

    @staticmethod
    def handleMessage(*args):
        print("message")


def getStrFromProxy(proxy: Proxy):
    return proxy.valueOf()


class Mineflayer:
    def __init__(self, botName: str, *, host: str = '127.0.0.1', port: int = 25565, autoBind: bool = True, _viewer: bool = True):
        self._botName, self._host, self._port = botName, host, port
        self._auotBind = autoBind
        self.viewer = viewer

        if self._autoBindFlag: self.bindOn()
        if self.viewer: self.createViewer()

    @property
    def botName(self):
        return self._botName

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def _autoBindFlag(self):
        return self._auotBind

    @cached_property
    def bot(self): return mineflayer.createBot({'host': self.host, 'port': self.port, 'username': self.botName})

    def __enter__(self):
        return self.bot

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.bot.end()
        pass

    def bindOn(self, callbackDict: dict[str, Callable] = None):
        if self._autoBindFlag:
            for func in filter(lambda x: x.startswith('handle'), dir(self)):
                On(self.bot, func.replace('handle', '').lower())(getattr(self, func))

        elif callbackDict:
            for event, callback in callbackDict.items():
                On(self.bot, event)(callback)

    def createViewer(self):
        if self.viewer:
            viewer(self.bot, {"port": 3007, "firstPerson": True})

            print(f"viewer开启于'{self.host}:{3007}'")

    @staticmethod
    def handleSpawn(*args):
        print("spawned")

    @staticmethod
    def handleMessage(*args):
        print(getStrFromProxy(args[1]))


# bot = mineflayer.createBot({
#     'host': 'localhost',
#     'port': 25565,
#     'username': 'Bot'
# })
#
# @On(bot, 'spawn')
# def handle(*args):
#     print("I spawned 👋")
#     movements = pathfinder.Movements(bot)
#
#     @On(bot, 'chat')
#     def handleMsg(this, sender, message, *args):
#         print("Got message", sender, message)
#         if sender and (sender != 'bot'):
#             bot.chat('Hi, you said ' + message)
#             if 'come' in message:
#                 player = bot.players[sender]
#                 print("Target", player)
#                 target = player.entity
#                 if not target:
#                     bot.chat("I don't see you !")
#                     return
#
#                 pos = target.position
#                 bot.pathfinder.setMovements(movements)
#                 bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, 1))
#
#
# @On(bot, "end")
# def handle(*args):
#     print("Bot ended!", args)


if __name__ == '__main__':
    # bot = Bot('Bot')
    # bot.registerPlugins(pathfinder.pathfinder)
    # bot.bot.chat("hi")
    parser = interpreter()

    bot = Mineflayer('bot')

    def response(_bot: Mineflayer, *args):
        bot.bot.chat(''.join(args))

    parser.register(partial(response, bot))
