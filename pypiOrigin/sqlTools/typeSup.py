#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/9/13 上午10:30
# 当前项目名: ansiDefine.py
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
__all__ = [
    "Result",
    "Type",
    "CanBeStr",
    "ArgumentError",
    "FlagOrStr"
]

from typing import TypedDict, Protocol, Optional, Any
from enum import Enum


class Result(TypedDict):
    result: tuple[tuple[Any, ...], ...]
    header: list[str] | tuple
    rowcount: int
    spendtime: Optional[float]


class Type(Enum):
    VARCHAR = "varchar"
    INT = "int"
    CHAR = "char"
    DATE = "date"
    FLOAT = "float"
    TIME = "time"
    BOOLEAN = "boolean"


FlagOrStr = Optional[bool | str | None]


class CanBeStr(Protocol):
    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...


class ArgumentError(Exception):
    def __init__(self, *args):
        super().__init__(*args or ("Invalid arguments",))
