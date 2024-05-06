#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/5/4 下午1:21
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from os import PathLike
from ast import parse, FunctionDef, ClassDef, AST, Expr, Constant, dump, Module, Assign, AnnAssign, Name, Load, If, Compare
from functools import cached_property, wraps
from astor import to_source
from typing import Any, Callable
from re import findall, sub, DOTALL


class engine:
    def __init__(self, filePath: str | PathLike):
        self._filePath = filePath
        self._comments = {}
        self._typeDict = {
            FunctionDef: 'function',
            ClassDef:    'class',
        }

        self.initAst(self.ast)
        self.ergodicAst(self.ast)

    @property
    def filePath(self) -> str | PathLike:
        return self._filePath

    @cached_property
    def ast(self):
        with open(self.filePath, 'r', encoding='utf-8') as file:
            return parse(file.read())

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, value):
        self._comments = value

    @property
    def typeDict(self):
        return self._typeDict

    def getCommentExp(self, node: FunctionDef | ClassDef, *, commentDict: dict = None):
        exp = [body] if isinstance(body := node.body[0], Expr) else []
        if commentDict is not None:
            try:
                self.setAttr(node, 'comment', body.value.s, commentDict=commentDict)

            except AttributeError:
                pass
        return exp

    def ergodicAst(self, node: AST, *, commentDict: dict = None):
        if commentDict is None: commentDict = self.comments

        if isinstance(node, FunctionDef):
            comDict = self.register(node, commentDict=commentDict)

            if body := list(filter(lambda n: isinstance(n, FunctionDef), node.body)):
                node.body = body
                for n in node.body:
                    self.ergodicAst(n, commentDict=comDict['children'])
            else:
                self.modifiesAst(node, commentDict=commentDict)

        elif isinstance(node, ClassDef):
            comDict = self.register(node, commentDict=commentDict)
            if body := list(filter(lambda n: isinstance(n, FunctionDef), node.body)):

                for n in body:
                    self.ergodicAst(n, commentDict=comDict['children'])

                node.body = self.getCommentExp(node, commentDict=commentDict) + body

        elif hasattr(node, 'body'):
            for n in node.body:
                self.ergodicAst(n, commentDict=commentDict)

    def register(self, node: FunctionDef | ClassDef, *, commentDict: dict):
        commentDict[(node.name, self.typeDict[type(node)])] = comDict = {"comment": None, "children": {}}

        return comDict

    def setAttr(self, node: FunctionDef | ClassDef, attr: str, value: Any, *, commentDict: dict):
        commentDict[(node.name, self.typeDict[type(node)])][attr] = value

    @staticmethod
    def initAst(node: AST):
        if isinstance(node, Module):
            for i, n in enumerate(node.body):

                if isinstance(n, Assign):
                    node.body[i] = AnnAssign(target=n.targets[0], annotation=Name(type(v.value).__name__ if isinstance(v := n.value, Constant) else type(v).__name__.lower(), ctx=Load()), value=None, simple=1)

                elif isinstance(n, If) and isinstance(test := n.test, Compare):
                    if test.left.id == '__name__' and test.comparators[0].value == '__main__':
                        node.body.remove(n)

    def modifiesAst(self, node: FunctionDef, *, commentDict: dict = None):
        node.body = self.getCommentExp(node, commentDict=commentDict) + [Expr(value=Constant(value=Ellipsis))]

    def pyi(self, *, filePath: str | PathLike = None):
        pyi = to_source(self.ast)

        if filePath:
            with open(filePath, 'w', encoding='utf-8') as file:
                file.write(pyi)

        else:
            return pyi


class docParser:
    def __init__(self, commentDict: dict):
        self._commentDict = commentDict
        self._markdown = ""

    @property
    def commentDict(self):
        return self._commentDict

    @property
    def markdown(self):
        return self._markdown

    @markdown.setter
    def markdown(self, value):
        self._markdown = value

    def contents(self):
        self.markdown += "# API Documentation\n\n"

        def execFunc(k: tuple[str, str], v: dict, *, level: int = 0):
            self.markdown += '   ' * level + f"   * {k[0]}{{.{k[1]}}}\n"

        def execCond(k: tuple[str, str], v: dict):
            return not k[0].startswith('_')

        self.recursion(self.commentDict, lambda k, v: v['children'], execFunc=execFunc, execCond=execCond)

    def detail(self):
        def execFunc(k: tuple[str, str], v: dict, *, level: int = 0):
            self.markdown += reTemplate(k, v, level=level).template

        def execCond(k: tuple[str, str], v: dict):
            return not k[0].startswith('_')

        self.recursion(self.commentDict, lambda k, v: v['children'], execFunc=execFunc, execCond=execCond)

    def recursion(self, currentDict: dict, lastFunc: Callable, *, execFunc: Callable = None, execCond: Callable = None, level: int = 0):
        if execCond is None: execCond = lambda k, v: True

        for k, v in currentDict.items():
            if execCond(k, v) and execFunc:
                execFunc(k, v, level=level)

            if lastDict := lastFunc(k, v):
                self.recursion(lastDict, lastFunc=lastFunc, execFunc=execFunc, execCond=execCond, level=level + 1)


def join(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return '无' if res is None else ''.join(res) if isinstance(res, list) else res

    return wrapper


class reTemplate:
    def __init__(self, key: tuple[str, str], value: dict, *, level: int = 0):
        self._key = key
        self._value = value
        self._level = level

    @property
    def funcName(self):
        return self._key[0]

    @property
    def funcType(self):
        return self._key[1]

    @property
    def comment(self):
        return self._value['comment']

    @property
    def level(self):
        return self._level

    @property
    def space(self):
        return " " * 3 * self._level

    @cached_property
    def lineBreak(self):
        return '\n'

    @property
    def template(self):
        return f"""{'###' if self._level == 0 else f'{self.space}*'} {self.funcName}
   {self.space}> {self.description().replace(self.lineBreak, '').strip()}
   {f'{self.lineBreak}{self.space}{example}' if (example := self.example()) else ''}
   {self.space}{self.classTemp if self.funcType == 'class' else self.funcTemp}
   \n"""

    @property
    def classTemp(self):
        return f""""""

    @property
    def funcTemp(self):
        # TODO: 函数注释模板
        return f""""""

    @join
    def description(self, comment: str = None):
        comment = self.comment if comment is None else comment

        if comment is None: return

        try:
            res = (text := sub(r"(?<=\S)\s(?=\S)", '(#s#)', comment).replace(' ', ''))[:text.index('\n\n')].replace('(#s#)', ' ')

            if all(t not in res for t in ['Attributes:', 'Methods:', ':param', ':return', 'Example:', 'example:', ':raises']):
                return res

        except ValueError:
            return comment

    @join
    def example(self, comment: str = None):
        comment = self.comment if comment is None else comment

        if comment is None: return

        if 'example' in comment.lower():
            return findall(r"(?<=Example:|example:)(?::).*?(?=:|$|Attributes|Methods)", comment, DOTALL)


if __name__ == '__main__':
    parser = engine(filePath=r"E:\codeSpace\codeSet\Python\test\annotationTest.py")
    ins = docParser(parser.comments)
    ins.contents()
    ins.detail()
    with open(r"E:\codeSpace\codeSet\Python\test.md", "w", encoding="utf-8") as file:
        file.write(ins.markdown)
