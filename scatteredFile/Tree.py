#  Copyright (c) 2023-2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/10/14 14:33
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 尝试定义一个二叉树/多叉树类
# -------------------------<Lenovo>----------------------------
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import final


@dataclass
class node:
    """节点类"""
    _nodes: int = 2

    def __init__(self, values: ... = None):
        self._values = values
        self._index = None
        self._lastNodes = None

    def __getitem__(self, index):
        print("__getitem__")
        return self._lastNodes[index]

    # def __setitem__(self, index, value):
    #     self._lastNodes[index] = value

    @property
    def nodes(self): return self._nodes

    @nodes.setter
    def nodes(self, value: int):
        if not isinstance(value, int):
            raise ValueError("nodes只接受int类型参数.")
        elif value <= 1:
            raise ValueError("节点数不能小于1")
        else: self._nodes = value

    @property
    def values(self): return self._values

    @property
    def lastNodes(self):
        if self._lastNodes is None:
            self._lastNodes = [None] * self.nodes

        return self._lastNodes

    @lastNodes.setter
    def lastNodes(self, value): raise


@dataclass
class Tree(ABC):
    """
    树基类

    """
    def __init__(self):
        """
        Todo:
            1. 可以接受的可以被树化的参数
            2. 树之间的连接关系
            3. 节点的附加标签
            4. 节点的增删改查
            5. 树的输出方式
        """
        self._root = ()

    @property
    @abstractmethod
    def root(self):
        pass

    @final
    @root.setter
    def root(self, value):
        pass

    @final
    @root.deleter
    def root(self):
        pass


if __name__ == '__main__':
    ins = node(1)
    ins.lastNodes[0] = 1
    print(ins.lastNodes)
    pass
