#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/5/23 下午5:28
# 当前项目名: Python
# 编码模式: utf-8
# 注释: minecraft-protocol\src\datatypes\uuid.js
# -------------------------<edocsitahw>----------------------------
from hashlib import md5
from uuid import UUID


def javaUUID(s):
    _hash = md5(s.encode('utf-8')).digest()

    buffer = bytearray(_hash)

    buffer[6] = (buffer[6] & 0x0f) | 0x30
    buffer[8] = (buffer[8] & 0x3f) | 0x80

    return UUID(bytes=buffer)


def nameToMcOfflineUUID(name):
    return str(javaUUID('OfflinePlayer:' + name))


def fromIntArray(arr):
    buf = bytearray(16)

    for idx, num in enumerate(arr):
        buf[idx*4:idx*4+4] = num.to_bytes(4, byteorder='big')

    return buf.hex()

