#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

class Node:
    def __init__(self): ...

    @property
    def data(self): ...

    @property
    def head(self): ...

def createNode(data: int): ...

def append(head, data: int): ...

def printList(node): ...
