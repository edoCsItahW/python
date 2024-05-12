#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/5/11 下午5:09
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from socket import AF_INET, SOCK_STREAM, socket
from typing import overload
from win32gui import FindWindow
from win32process import GetWindowThreadProcessId, EnumProcesses, GetModuleFileNameEx
from win32api import OpenProcess
from win32con import PROCESS_QUERY_INFORMATION, PROCESS_VM_READ
from win32file import CloseHandle
from subprocess import run, PIPE
from warnings import warn
from re import findall
from functools import cached_property
from win32com.client import Dispatch
from time import sleep
from atexit import register


class PID:
    @overload
    def __init__(self, handleTitleName: str): ...

    @overload
    def __init__(self, executableName: str): ...

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

    def getPid(self):
        if self.name.endswith('.exe'):
            return self.getPidFromExe()

        return self.getPidFromTitle()

    def getPidFromTitle(self):
        if (hwnd := FindWindow(None, self.name)) != 0:
            _, pid = GetWindowThreadProcessId(hwnd)
            return pid

    def getPidFromExe(self):
        for pid in (handles := EnumProcesses()):
            try:
                if self.name.lower() in GetModuleFileNameEx(handle := OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid), 0).lower():
                    CloseHandle(handle)
                    return pid
            except Exception:
                pass

        warn(
            f"Process {self.name} not found!")

    def getPort(self):
        if (result := run(f'netstat -ano | find "{(p := self.getPid())}"', shell=True, stdout=PIPE, stderr=PIPE, text=True)).returncode != 0:
            warn(
                f"PID为'{p}'的进程: '{self.name}'可能不接入网络或者端口号查找失败!")

        return {r[0] for line in map(str.strip, result.stdout.split('\n')) if (r := findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:(\d+)", line))}

    def reverseFind(self):
        if (result := run(f'tasklist | findstr {(p := self.getPid())}', shell=True, stdout=PIPE, stderr=PIPE, text=True)).returncode != 0:
            warn(
                f"PID为'{p}'的进程: '{self.name}'可能不存在!")

        else:
            print(result.stdout)


class Interacting:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @cached_property
    def socket(self):
        """
        sendall()方法用于发送数据到套接字，recv()方法用于接收数据。
        recv()方法的第二个参数指定了接收数据的最大长度。
        """
        return socket(AF_INET, SOCK_STREAM)

    def __enter__(self):
        self.socket.connect((self.host, self.port))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    def cycleInput(self):
        while (inp := input("请输入指令: ").lower()) != 'exit':
            self.socket.sendall(inp.encode())

            if out := self.socket.recv(1024).decode():
                print(out)


def pragramExit(_socket: socket):
    _socket.sendall("exit".encode())


if __name__ == '__main__':
    Dispatch("WScript.Shell").Run(r"cmd.exe /k python E:\codeSpace\codeSet\Python\server.py")
    sleep(1)
    # pid = PID('edge.exe')
    # print(pid.getPort())
    with Interacting(host='127.0.0.1', port=8081) as s:
        register(lambda: pragramExit(s.socket))
        s.cycleInput()
