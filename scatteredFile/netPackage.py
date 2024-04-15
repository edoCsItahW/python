#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/12 8:39
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from scapy.all import sniff
from systemTools import instruct
from re import findall
from threading import Thread


class DnsTimeOutError(Exception):
    def __init__(self, *args):
        self.args = args


def getIp(url: str):
    res = instruct(output=False, ignore=True, eliminate="文件名、目录名或卷标语法不正确。")(f"nslookup {url}")
    ip = findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", res)
    try:
        return ip[1]

    except IndexError as e:
        e.add_note(f"ip: {ip}")
        raise e from DnsTimeOutError(res)


def packet_callback(packet):
    print(packet.summary())
    print(packet.show())


if __name__ == '__main__':
    sniff(prn=packet_callback, store=0, count=0, filter=f"host {getIp('yujuo.cn')}")
