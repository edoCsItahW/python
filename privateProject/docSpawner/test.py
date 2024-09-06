#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

from ast import parse, NodeVisitor, AST, FunctionDef, Expr, Constant
from pypiOrigin.systemTools.systemTools import jsonOpen
from atexit import register
from re import findall


target = r"E:\codeSpace\codeSet\Python\pypiOrigin\systemTools\systemTools.py"


def decode(data: str) -> dict:
    return {k: k.encode('utf-8').decode('unicode_escape') for k in findall(r'\\u[0-9a-fA-F]{4}', data)}


@register
def dec():
    with open(r"E:\codeSpace\codeSet\Python\privateProject\docSpawner\common.json", "r+", encoding='utf-8') as f:
        d = decode(t := f.read())

        for k, v in d.items():
            t = t.replace(k, v)

        f.seek(0)
        f.write(t)
        f.truncate()


class Visitor(NodeVisitor):
    def generic_visit(self, node: AST):
        super().generic_visit(node)
        if isinstance(node, Expr) and isinstance(node.value, Constant):
            with jsonOpen(r"E:\codeSpace\codeSet\Python\privateProject\docSpawner\common.json", "w", encoding='utf-8') as f:
                d = f.read()
                d.append(node.value.value)
                f.write(d)


if __name__ == '__main__':
    visitor = Visitor()
    with open(target, 'r', encoding='utf-8') as file:
        # print(parse(file.read()))
        visitor.visit(parse(file.read()))

