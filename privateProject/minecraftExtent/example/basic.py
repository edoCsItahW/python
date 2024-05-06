from javascript import require, On
from functools import cached_property
from typing import Any


mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')


class Bot:
    def __init__(self, botName: str, *, host: str = '127.0.0.1', port: int = 25565):
        self._botName, self._host, self._port = botName, host, port
        self._plugins = {}

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

    @On(bot, 'spawn')
    def handleSpawn(self, *args):
        print("spawned")

    @On(bot, 'message')
    def handleMessage(self, *args):
        print(args)

# @On(bot, 'spawn')
# def handle(*args):
#     print("I spawned 👋")
#     movements = pathfinder.Movements(bot)
#
#     @On(bot, 'chat')
#     def handleMsg(this, sender, message, *args):
#         print("Got message", sender, message)
#         if sender and (sender != BOT_USERNAME):
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
#                 bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, RANGE_GOAL))
#
#
# @On(bot, "end")
# def handle(*args):
#     print("Bot ended!", args)


if __name__ == '__main__':
    bot = Bot('Bot')
    bot.registerPlugins(pathfinder.pathfinder)
    bot.bot
