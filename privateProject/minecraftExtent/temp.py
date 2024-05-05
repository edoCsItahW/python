#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/5/4 下午11:24
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from time import sleep
from mcpi.minecraft import Minecraft
from mcrcon import MCRcon
from functools import cached_property
from mcpi.block import WOOD, STONE, AIR, WATER, Block
from numpy import arange
from typing import Callable, Literal
from math import ceil, sqrt
from functools import partial
from threading import Thread
from queue import Queue
from warnings import warn
from traceback import format_exc
from multiprocessing import Process


class MC:
    def __init__(self, *, address: str = "127.0.0.1", port: int = 4711, wait: int = 5):
        print('开始测试!')
        sleep(wait)
        self._address = address
        self._port = port
        self._message = set()
        self.messageQueue = Queue()
        self.flagDict = {}

    @property
    def mc(self):
        return Minecraft.create(address=self._address, port=self._port)

    @property
    def playerPos(self):
        return self.mc.player.getPos()

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def funcDict(self):
        return {
            "pos": lambda: self.postToChat(f"当前位置: {[round(i, 2) for i in self.playerPos]}"),
            "warkInEmpty": lambda: self.setKeyAndStart(self.warkInEmpty, self.flagDict, 'warkInEmpty'),
        }

    @staticmethod
    def setKeyAndStart(func: Callable, flagDict: dict, key: str, *, mode: Literal['thread', 'process'] = 'thread'):
        print(f"开始启动功能: '{key}'")
        flagDict[key] = True
        thead = (Thread if mode == 'thread' else Process)(target=func, args=(flagDict, key))
        thead.start()

    def postToChat(self, message: str):
        self.mc.postToChat(message)

    def messageLestener(self):
        while True:
            for chat in self.mc.events.pollChatPosts():
                self.message.add(chat.message)
                sleep(0.1)

            if self.message:
                self.messageQueue.put(self.message.pop())

    def handleMessage(self):
        while True:
            if not self.messageQueue.empty():
                self.instructionParser(self.messageQueue.get())

    def instructionParser(self, instruction: str):
        if instruction.startswith('#'):
            insList = instruction[1:].split(' ')

            kwargs = None

            for i, arg in enumerate(insList):
                if arg.startswith('--'):
                    kwargs = insList.pop(i)

            if len(insList) == 1:
                try:
                    self.funcDict[insList[0]]()
                except KeyError:
                    try:
                        self.setKeyAndStart(attr := getattr(self, insList[0]), self.flagDict, attr.__name__, mode='process' if kwargs == "--p" else 'thread')
                    except AttributeError as e:
                        self.postToChat(f"未知指令: {insList[0]}")
                        warn(format_exc(), SyntaxWarning)
                    else:
                        self.postToChat(f"已启动功能: {attr.__name__}")

            elif len(insList) == 2:
                if insList[0] == 'cancel':
                    if insList[1] in self.funcDict:
                        self.flagDict[insList[1]] = False
                    else:
                        self.postToChat(f"未知功能: '{insList[1]}'")

    def multThread(self):
        thread1 = Thread(target=self.messageLestener)
        thread2 = Thread(target=self.messageLestener)
        thread3 = Thread(target=self.handleMessage)

        thread1.start()
        sleep(0.05)
        thread2.start()
        thread3.start()

    def warkInEmpty(self, flagDict: dict, key: str):
        def _expand(_x: int | float, _z: int | float, arg: int | float):
            r"""
            在极坐标中的目视方向向量本来 x^2 + y^2 + z^2 = 1,
            但我们只需要计算水平方向朝向向量即可, 那么 x^2 + z^2 肯定是小于1的,
            这样会导致在你不抬头至水平时,即x,z很小时计算出来的方块增量就小于1, 这样
            就不会放置方块.
            所以需要扩展数值.

            原本:
                x^2 + y^2 + z^2 = 1

            扩展:
                ax^2 + bz^2 = 1
                \frac{a}{b} = \frac{x}{z}
                a = \frac{xb}{z}
                ...

                a = \sqrt{\frac{x}{x^2 + z^2}}
                b = \sqrt{\frac{z}{x^2 + z^2}}

            :param _x: 向量的x轴范数
            :param _z: 向量的z轴范数
            :param arg: 谁的增量x(a), z(b)
            :return: 扩展后的新权重a或b
            """
            return sqrt(abs(arg / (_x ** 2 + _z ** 2)))

        while flagDict[key]:
            x, y, z = self.mc.player.getDirection()
            px, py, pz = self.playerPos

            expand = partial(_expand, x, z)

            coordinate = (px + x * expand(x), py - 1, pz + z * expand(z))

            if self.mc.getBlock(*coordinate) in [AIR.id, WATER.id]:
                self.mc.setBlock(*coordinate, STONE.id)


class RCON:
    """
    /gamemode 0 ：生存。

    /gamemode 1 ：创造。

    /gamemode 2 ：冒险。

    /gamemode 3 ：旁观。

    /kill ：自杀。

    /kill 玩家名 ：把某某玩家杀死。

    /time set day ：白天。

    /time set night ：夜晚。

    /achievement 获得　　/移除玩家的成就。

    /ban 添加一个玩家到黑名单中。

    /ban-ip 添加一个IP地址到黑名单中。

    /banlist 显示黑名单。

    /blockdata 修改一个方块的数据标签。

    /clear 从玩家的物品栏清除物品。

    /clone 将方块从一个位置复制到另一位置。

    /debug 开始或终止一个 debugging session。

    /defaultgamemode 设定默认的游戏模式。

    /deop 撤销一位玩家的管理员身份。

    /difficulty 设定难度。

    /effect 添加或移除状态效果。

    /enchant 附魔一个玩家的物品。

    /entitydata 修改实体的数据标签。

    /execute 执行另一条命令。

    /fill 用一种特定方块填充一块区域。

    /gamemode 设定一位玩家的游戏模式。

    /gamerule 设定或查询一个游戏规则值。

    /give 给予一位玩家一个物品。

    /help 提供命令的帮助。

    /kick 将一位玩家踢出服务器。

    /kill 杀死实体（玩家、生物、物品等）。

    /list 列出在服务器上的玩家。

    /me 显示一条关于你自己的信息。

    /op 给予一位玩家管理员身份。

    /pardon 从黑名单移除项目。

    /particle 制造颗粒效果。

    /playsound 播放一个音效。

    /publish 对局域网开放单人世界。

    /replaceitem 替换物品栏中的物品。

    /save-all 将服务器保存至硬盘中。

    /save-off 禁用服务器自动保存。

    /save-on 启用服务器自动保存。

    /say 向多名玩家显示一条信息。

    /scoreboard 管理对象、玩家和队伍。

    /seed 显示世界种子。

    /setblock 将一个方块变更至另一个方块。

    /setidletimeout 设定踢出挂机玩家的时间。

    /setworldspawn 设定出生点。

    /spawnpoint 设定一位玩家的出生点。

    /spreadplayers 将实体传送至随机位置。

    /stats 通过命令的返回改变记分板对象。

    /stop 停止服务器。

    /summon 生成一个实体。

    /tell 向其他玩家显示一条私人信息。

    /tellraw 向玩家显示一条JSON信息。

    /testfor 计算匹配特定条件的实体数。

    /testforblock 探测一个方块是否在一个位置。

    /testforblocks 探测两块区域内的方块是否匹配。

    /time 改变或查询世界的游戏时间。

    /title 管理屏幕标题。

    /toggledownfall 切换天气。

    /tp 传送实体。

    /trigger 设定触发装置的激活。

    /weather 设定天气。

    /whitelist 管理服务器白名单。

    /worldborder 管理世界边界。

    /xp 增加或移除玩家的经验值。

    /achievement give *获得所有的成就
    """

    def __init__(self, *, address: str = "127.0.0.1", port: int = 25575, wait: int = 5):
        print('开始测试!')
        sleep(wait)
        self._address = address
        self._port = port
        self._rcon = MCRcon(self._address, 'password', self._port)

    @cached_property
    def rcon(self):
        return self._rcon

    def __enter__(self):
        self.rcon.connect()
        return self

    def send(self, instruction: str, *, output: bool = False):
        if output: print(f'发送指令: {instruction}')
        return self.rcon.command(instruction)

    def continuousInput(self):
        closeFlag = True
        while closeFlag:
            if (ins := input('Minecraft RCON> /')).lower() != 'exit':
                print(self.send(ins))
            else:
                print('退出程序')
                closeFlag = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rcon.disconnect()


if __name__ == '__main__':
    # mc = MC(wait=0)
    # mc.multThread()
    # mc.warkInEmpty({'flag': True}, 'flag')
    with RCON(wait=0) as r:
        # print(r.send('title @a title {\"text\":\"Hello, world!\"}', output=True))
        r.continuousInput()

