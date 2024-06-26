#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/5/2 下午4:55
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from typing import Callable, Literal, Self
from functools import cached_property
from os import path, PathLike
from ast import parse, iter_child_nodes, dump, AST, ClassDef, Expr, FunctionDef
from re import findall, DOTALL, RegexFlag, Pattern
from warnings import warn
from pypiOrigin.conFunc.confunc import GsingleDispatch, singleDispatchMethod


class docSpawner:
    def __init__(self, filePath: str | PathLike[str]):
        self._filePath = filePath
        self._commonRules = []
        self._classRules = []
        self.funcRules = []
        self.result = []

        self.ruleInit()

    @property
    def filePath(self):
        return self._filePath

    @property
    def commonRules(self):
        return self._commonRules

    @commonRules.setter
    def commonRules(self, value):
        self._commonRules = value

    @property
    def classRules(self):
        return self._classRules

    @classRules.setter
    def classRules(self, value):
        self._classRules = value

    @property
    def funcRules(self):
        return self._funcRules

    @funcRules.setter
    def funcRules(self, value):
        self._funcRules = value

    @cached_property
    def ast(self):
        with open(self.filePath, "r", encoding="utf-8") as file:
            return parse(file.read())

    def parseAST(self):
        for node in iter_child_nodes(self.ast):
            self.getDoc(node)

    def getDoc(self, node: AST):
        if isinstance(node, dict):
            for value in node.values():
                self.getDoc(value)

        elif isinstance(node, list):
            for item in node:
                self.getDoc(item)

        elif isinstance(node, (ClassDef, FunctionDef)):
            self.getNodeDoc(node)

        elif hasattr(node, "body"):
            for n in node.body:
                self.getDoc(n)

        else:
            pass
            # warn(
            #     f"不支持的节点类型: '{node.__class__.__name__}'")

    def getNodeDoc(self, astNode: ClassDef | FunctionDef, *, replace: bool = True):
        if hasattr(exp := astNode.body[0], "value") and isinstance(exp, Expr):
            if not (comment := exp.value.s):
                return
        else:
            return

        fields = {}

        res = None
        for rule in self.commonRules:
            res = rule(comment, fields)

            if replace and res: comment.replace("".join(res), "")

        if isinstance(astNode, ClassDef):
            for rule in self.classRules:
                res = rule(comment, fields)

                if replace and res: comment.replace("".join(res[0]), "")

        elif isinstance(astNode, FunctionDef):
            for rule in self.funcRules:
                res = rule(comment, fields)

                if replace and res: comment.replace("".join(res[0]), "")

        else:
            warn(
                f"不支持的节点类型: {astNode.__class__.__name__}")

        self.result.append(res)

    @staticmethod
    def middleware(reExp: Pattern, comment: str, fields: dict, field: str, *, flags: RegexFlag = 0, condition: Callable = None):
        if condition is None or condition(comment) and field not in fields:
            fields[field] = res = findall(reExp, comment, flags)

            if not res:
                warn(
                    f"正则表达式: `{reExp}`对于注释: '{comment}'没有匹配到任何东西!")
                    # "正则表达式: `{reExp}`对于注释: '{}'没有匹配到任何东西!".format(comment.replace('\n', '\\n'), reExp=reExp))

            return res
        return False

    def register(self, rule: Literal["common", "class", "func"] = "common", reExp: Pattern | str = None, field: str = None, *, flags: RegexFlag = 0, condition: Callable = None):
        match rule:
            case "common":
                self.commonRules.append(lambda comment, fields: self.middleware(reExp, comment, fields, field, flags=flags, condition=condition))
            case "class":
                self.classRules.append(lambda comment, fields: self.middleware(reExp, comment, fields, field, flags=flags, condition=condition))
            case "func":
                self.funcRules.append(lambda comment, fields: self.middleware(reExp, comment, fields, field, flags=flags, condition=condition))
            case _:
                raise NotImplementedError(
                    f"不支持的规则类型: {rule}")

    def ruleInit(self):
        self.register("common", r".*", "description", condition=lambda comment: '\n' not in comment)
        self.register("common", r"(?:\n?)\S+(?:\n?)", "description", condition=lambda comment: not len(findall(r"\n\s+\n", comment)))
        self.register("common", r"(?:\n?)\S+(?:\n?\s+\n)", "description")
        self.register("common", r"(?<=Example:|example:)(?::).*?(?=:|$|Attributes|Methods)", "example", flags=DOTALL, condition=lambda comment: any([f in comment for f in ["Example", "example"]]))
        self.register("class", r"(?<=Example:|example:)(?::).*?(?=:|$|Attributes|Methods)", "attributes", flags=DOTALL, condition=lambda comment: "Attributes" in comment)
        self.register("class", r"(?<=Methods:)(?::)(?:\n).*(?=$)", "methods", flags=DOTALL, condition=lambda comment: "Methods" in comment)
        self.register("func", r":(param|type|keyword|raise)(.*)(?=$)", "param", flags=DOTALL)


if __name__ == '__main__':
    # anlysisFile(r"E:\codeSpace\codeSet\Python\pypiOrigin\uploadTools\uploadTools.py")
    # getDoc(testFunc)
    # print(dump(parse('def func():\n    """\n    This is a class.\n"""\n    pass'), indent=4))
    ins = docSpawner(r"E:\codeSpace\codeSet\Python\pypiOrigin\uploadTools\uploadTools.py")
    ins.getDoc(ins.ast)
    print(ins.result)
