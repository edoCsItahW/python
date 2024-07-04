#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/6/11 上午11:42
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from abc import ABC, abstractmethod
from typing import Literal, Any
from warnings import warn
from struct import pack
from hashlib import md5
from uuid import UUID
from scatteredFile.debuger import debuger


__all__ = [
    'ignoreList',
    'IGNORE_WARNINGS',
    'Basetype',
    'Boolean',
    'Byte',
    'UByte',
    'Short',
    'UShort',
    'VarInt',
    'String',
    'Uuid',
    'Long'
]


ignoreList = [
    'IGNORE_WARNINGS',
    'ignoreList',
    'baseType',
]


IGNORE_WARNINGS = False


def negativeIntToByte(num: int) -> bytes:
    """
    将负整数转换为字节

    :param num: 负整数
    :type num: int
    :return: 字节
    """
    assert -128 <= num < 0, f"num {num} is not a negative byte"

    complement = (256 + num) & 0xff

    return complement.to_bytes(1, byteorder='big')


class Basetype(ABC):
    def __init__(self, data: int | bytes):
        self._data = data

    @property
    def byte(self) -> bytes:
        """
        如果数据是字节，则返回字节，否则返回数据转换为字节

        :return: 字节
        """
        if not isinstance(self._data, bytes):

            if not IGNORE_WARNINGS:
                warn(
                    f"automatic conversion of {type(self._data).__name__} to bytes")

            return bytes(self._data)

        return self._data

    @property
    def integer(self) -> int:
        """
        如果数据是整数，则返回整数，否则返回字节转换为整数

        :return: 整数
        """
        if isinstance(self._data, bytes):
            return int.from_bytes(self._data, byteorder='big')

        if not IGNORE_WARNINGS:
            warn(
                f"automatic conversion of {type(self._data).__name__} to int")

        return int(self._data)

    @staticmethod
    def checkRange(value: int | bytes, minValue: int, maxValue: int, *, mode: Literal['error', 'warn']) -> None:
        """
        检查值是否在该类型运行的范围内

        :param value: 值
        :type value: int | bytes
        :param minValue: 最小值
        :type minValue: int
        :param maxValue: 最大值
        :type maxValue: int
        :raise ValueError: 值不在范围内或最小值大于最大值
        """
        if minValue > maxValue:
            raise ValueError(
                f"minValue {minValue} is greater than maxValue {maxValue}")

        if isinstance(value, bytes):
            value = int.from_bytes(value, byteorder='big')

        if value < minValue or value > maxValue:

            if mode == 'warn':
                warn(
                    f'value {value} is out of range {minValue}-{maxValue}')

            else:
                raise ValueError(
                    f'value {value} is out of range {minValue}-{maxValue}')

    @staticmethod
    def bytesToInt(value: bytes, *, mode: Literal['big', 'little'] = 'big') -> int:
        """
        将字节转换为整数

        :param value: 字节
        :type value: bytes
        :param mode: 字节序，big或little
        :type mode: str
        :return: 整数
        """
        if isinstance(value, bytes):
            return int.from_bytes(value, byteorder=mode)

        Basetype._confromWithWarn(value, bytes)

    @staticmethod
    def intToBytes(value: int, *, mode: Literal['big', 'little'] = 'big') -> bytes:
        """
        将整数转换为字节

        :param value: 整数
        :type value: int
        :param mode: 字节序，big或little
        :type mode: str
        :return: 字节
        """
        if isinstance(value, int):
            return pack('>B' if mode == 'big' else '<B')

        Basetype._confromWithWarn(value, int)

    @staticmethod
    def _confromWithWarn(data: Any, targetType: type, *, info: str = None) -> Any:
        info = info or f"automatic conversion of {type(data).__name__} to {targetType.__name__} for '{data}'!"

        if not IGNORE_WARNINGS:
            warn(
                info)

        return targetType(data)


class Boolean(Basetype):
    name = 'Boolean'

    def __init__(self, data: bool | bytes):
        self.checkRange(data, 0, 1, mode='warn')

        self._data = data

    @property
    def byte(self):
        if isinstance(self._data, bool):

            return bytes([int(self._data)])

        return self._data

    @property
    def bool(self):
        if isinstance(self._data, bytes):

            return bool(self.bytesToInt(self._data))


class Byte(bytes, Basetype):
    name = 'Byte'

    def __init__(self, data: int | bytes):
        self._data = data


class UByte(bytes, Basetype):
    name = 'UByte'

    def __init__(self, data: int | bytes):
        self.checkRange(data, 0, 255, mode='error')
        self._data = data


class Short(Basetype):
    name = 'Short'

    def __init__(self, data: int | bytes):
        self.checkRange(data, -32768, 32767, mode='error')
        self._data = data

    @property
    def byte(self):
        if isinstance(self._data, int):
            return pack('>h', self._data)

        self._confromWithWarn(self._data, bytes)


class UShort(Short):
    name = 'UShort'

    def __init__(self, data: int | bytes):
        self.checkRange(data, 0, 65535, mode='error')
        self._data = data


class VarInt(Basetype):
    name = 'VarInt'
    SEGMENT_BITS = 0x7F
    CONTINUE_BIT = 0x80

    def __init__(self, data: int | bytes):
        self.checkRange(data, -2147483648, 2147483647, mode='error')
        self._data = data

    @classmethod
    def intToVarint(cls, value: int):
        varint = bytearray()

        while True:

            if (value & ~cls.SEGMENT_BITS) == 0:
                varint.append(value)
                return varint

            varint.append((value & cls.SEGMENT_BITS) | cls.CONTINUE_BIT)

            value >>= 7

    @classmethod
    def varintToInt(cls, varint: bytes):
        result = 0
        shift = 0

        for byte in varint:
            # 清除继续位并左移结果以容纳新的7位
            result |= (byte & cls.SEGMENT_BITS) << shift
            if not (byte & cls.CONTINUE_BIT):
                return result

            shift += 7

        raise ValueError(
            f"Invaild varint encoding: {varint}!")

    @property
    def byte(self):
        if isinstance(self._data, int):
            return self.intToVarint(self._data) if self._data >= 0 else negativeIntToByte(self._data)

        return bytes(self._data)

    @property
    def integer(self):
        if isinstance(self._data, bytes):
            return self.varintToInt(self._data)

        self._confromWithWarn(self._data, int)


class String(Basetype):
    name = 'String'

    def __init__(self, data: bytes | str, *, length: int = None):
        self._data = data
        self._length = length

    @property
    def length(self):
        return self._length

    @property
    def byte(self):
        if isinstance(self._data, str):

            self._length = len(self._data)

            return bytes(VarInt.intToVarint(self._length) + self._data.encode('utf-8'))

        self._confromWithWarn(self._data, bytes)

    @property
    def string(self):
        if isinstance(self._data, bytes):
            return self._autoStr(self._data)

        self._confromWithWarn(self._data, str)

    def _autoStr(self, data: bytes):
        total = 0

        for i, v in enumerate(data):

            total += v

            if total == self._length or total == (l := len(data[i+1:])):
                return data[i+1:].decode('utf-8')

            elif total > l:
                break

        return data.decode('utf-8')


class Uuid(Basetype):
    name = 'Uuid'

    def __init__(self, data: bytes | str, *, offline: bool = True):
        self._data = data
        self._offline = offline

    @staticmethod
    def javaUUID(s):
        _hash = md5(s.encode('utf-8')).digest()

        buffer = bytearray(_hash)

        buffer[6] = (buffer[6] & 0x0f) | 0x30
        buffer[8] = (buffer[8] & 0x3f) | 0x80

        return UUID(bytes=bytes(buffer)).bytes

    @property
    def byte(self) -> bytes:
        return self.javaUUID(("OfflinePlayer:" if self._offline else '') + self._data)


class Long(Basetype):
    name = 'Long'

    def __init__(self, data: bytes | int, *, offline: bool = True):
        self.checkRange(data, -9223372036854775808, 9223372036854775807, mode='error')
        self._data = data

    @property
    def byte(self) -> bytes:
        if isinstance(self._data, int):
            return self._data.to_bytes(8, byteorder='big', signed=True)

        return self._confromWithWarn(self._data, bytes)

    @property
    def integer(self):
        if isinstance(self._data, bytes):
            return int.from_bytes(self._data, byteorder='big', signed=True)

        return self._confromWithWarn(self._data, int)


if __name__ == '__main__':
    pass
