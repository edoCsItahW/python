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
from functools import cached_property, wraps
from argparse import ArgumentParser, Namespace
from warnings import warn
from typing import Any, Callable, Literal
from astor import to_source
from copy import deepcopy
from ast import parse, FunctionDef, ClassDef, AST, Expr, Constant, dump, Module, Assign, AnnAssign, Name, Load, If, Compare, ImportFrom, NodeVisitor
from re import findall, sub, DOTALL
from os import PathLike, path


class engine:
    def __init__(self, filePath: str | PathLike):
        self._filePath = filePath

        if not path.isabs(self._filePath): raise ValueError(
            f'文件路径必须为绝对路径!')

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

    @cached_property
    def codeWithoutImport(self):
        for node in (ast := deepcopy(self.ast)).body:
            if isinstance(node, ImportFrom):
                ast.body.remove(node)
        return ast

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

    def checkUse(self, name: str):
        v = visitor(name)

        v.visit(self.codeWithoutImport)

        return v.exit

    def removeUnuse(self):
        for node in self.ast.body:
            if isinstance(node, ImportFrom):
                node.names = [i for i in node.names if self.checkUse(i.name)]

        self.ast.body = [i for i in self.ast.body if not isinstance(i, ImportFrom) or i.names]

    def pyi(self, *, filePath: str | PathLike = None):
        self.removeUnuse()

        pyi = to_source(self.ast)

        if filePath:
            with open(filePath, 'w', encoding='utf-8') as file:
                file.write(pyi)

        else:
            return pyi


class visitor(NodeVisitor):
    def __init__(self, name: str = None):
        self._name = name
        self.exit = False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def visit_FunctionDef(self, node):
        if node.name == self.name:
            self.exit = True

        self.generic_visit(node)

    def visit_ClassDef(self, node):
        if node.name == self.name:
            self.exit = True

        self.generic_visit(node)

    def visit_Name(self, node):
        if node.id == self.name:
            self.exit = True

        self.generic_visit(node)


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
            self.markdown += '   ' * level + f"   * {'' if level else '['}{k[0]}{'' if level else ']'}{'' if level else f'(#{k[0]}-{k[0]})'}{{.{k[1]}}}\n"

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

    def toMarkdown(self, filePath: str | PathLike[str]):
        self.contents()
        self.detail()

        with open(filePath, "w", encoding="utf-8") as file:
            file.write(self.markdown)


def join(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        res = '无' if res is None or not res else ''.join(res) if isinstance(res, list) else res
        return res[int(res.startswith(":")):]

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
        return f"""{f'{self.space}*' if self._level else '###'} {self.funcName} {'' if self._level else f'{{#{self.funcName}}}'}{f'{self.lineBreak}   {self.space}> {des.replace(self.lineBreak, "").strip()}' if (des := self.description()) != '无' else ''}{f'{self.lineBreak}   * Example: {"" if ">>>" in example else "```python"}{self.lineBreak}{self.space}{example}{"" if ">>>" in example else "```"}' if (example := self.example()) != '无' else ''}{f'{self.lineBreak}   {self.space}{res}' if len(res := (self.classTemp if self.funcType == "class" else self.funcTemp)) else ''}\n"""

    @property
    def classTemp(self):
        return f"""{f'* Attributes: {self.lineBreak}{attr}' if (attr := self.Attributes()) != '无' else ''}{f'{self.lineBreak}   * Methods: {self.lineBreak}{meth}' if (meth := self.Methods()) != '无' else ''}
        """

    @property
    def funcTemp(self):
        return f"""{f'* Parameters: {self.lineBreak}{param}' if (param := self.param()) != '无' else ''}
        """

    @join
    def description(self, comment: str = None):
        comment = self.comment if comment is None else comment

        checkRes = lambda res: all(t not in res for t in ['Attributes:', 'Methods:', ':param', ':return', 'Example:', 'example:', ':raises', ":type"])

        if comment is None: return

        try:
            res = (text := sub(r"(?<=\S)\s(?=\S)", '(#s#)', comment).replace(' ', ''))[:text.index('\n\n')].replace('(#s#)', ' ')

        except ValueError:
            if checkRes(comment): return comment

        else:
            if checkRes(res): return res

    @join
    def example(self, comment: str = None):
        comment = self.comment if comment is None else comment

        if comment is None: return

        if 'example:' in comment.lower():
            return findall(r"(?<=Example:|example:)(?::).*?(?=:|$|Attributes|Methods)", comment, DOTALL)

    @join
    def Attributes(self, comment: str = None):
        comment = self.comment if comment is None else comment

        if comment is None: return

        string = ''

        if 'attributes:' in comment.lower():
            if res := findall(r"(?<=Attributes:).*?(?=$|Methods)", comment, DOTALL):

                for v, d in findall(r"(?<=:ivar\s)(.*?)(?::\s)(.*?)(?=\n|$)", res[0], DOTALL):

                    string += f"{self.space}      * `{v}`: {d}  \n"

        return string

    @join
    def Methods(self, comment: str = None):
        comment = self.comment if comment is None else comment

        if comment is None: return

        string = ''

        if 'methods:' in comment.lower():
            if res := findall(r"(?<=Methods:)(?::?).*?(?=$)", comment, DOTALL):

                for f, d in findall(r"(?<=:meth:`)(\w+)(?:`:\s)(.*?)(?=$|\n)", res[0], DOTALL):

                    string += f"{self.space}      * `{f}`: {d}  \n"

        return string

    @join
    def param(self, comment: str = None):
        attrDict = {
            'param': {},
            'keyword': {},
            'raises': {}
        }

        comment = self.comment if comment is None else comment

        if comment is None: return

        if ':param' in comment.lower():
            if res := findall(r":(param|type|keyword|raises)(.*)(?=$)", comment, DOTALL):
                res = ':' + ''.join(res[0])

                for k in attrDict.keys():
                    for n, d in findall(rf"(?<={k}\s)(.*?)(?::\s)(.*?)(?=\n|$)", res, DOTALL):
                        attrDict[k][n] = d if k == 'raises' else (d, t[0] if (t := findall(rf"(?<=type\s)(?:{n}:\s)(.*?)(?=\n|$)", res, DOTALL)) else 'Any')

        res = ''

        for k, v in attrDict.items():
            if v: res += f"{self.space}      * {k}\n"

            for p, t in v.items():
                res += f"{self.space}         * `{p}`{f' ({t[1]})' if isinstance(t, tuple) else ''}: {t[0] if isinstance(t, tuple) else t}\n"

        return res


def handlePath(filePath: str | PathLike[str], *, default: str | PathLike[str], suffix: Literal['pyi', 'md']):
    moduleName, defSuffix = path.splitext(path.basename(default))

    if defSuffix != '.py':
        raise ValueError(
            f"文件后缀必须为.py!")

    if "." in filePath:
        _, orgSuffix = path.splitext(path.basename(filePath))
        if orgSuffix != f".{suffix}":
            raise ValueError(
                f"文件后缀必须为.{suffix}!")
        return filePath

    elif path.isdir(filePath) or filePath == '.':
        return path.join(filePath, f"{moduleName}.{suffix}")

    else:
        raise ValueError(
            f"文件路径不合法!")


def argParser() -> Namespace:
    """
    包装了argparse的命令行参数解析器,用于解析命令行参数。

    :return: 一个包含命令行参数的对象。
    :rtype: Namespace
    """

    parser = ArgumentParser(prog="pyi,markdown文档生成工具", description="一个用于从py文件生产pyi,markdown文档的生成工具.", epilog="None")
    parser.add_argument("file", help="你需要转换的python文件的绝对路径。")
    parser.add_argument("toPath", default=".", help="生成文档的路径。(默认值: 当前路径)")
    parser.add_argument("-t", "--type", default="markdown", choices=["markdown", "pyi"], help="生成文档的类型。(默认值: markdown)")
    return parser.parse_args()


if __name__ == '__main__':
    # test = True
    test = False
    # pyinstaller -F spawner.py -n spawnTools -i E:\codeSpace\codeSet\Python\pypiOrigin\uploadTools\upload_1.ico

    if test:
        warn(
            f"正在运行测试版!")

        ins = docParser((eng := engine(filePath=r"E:\codeSpace\codeSet\Python\pypiOrigin\netTools\netTools.py")).comments)
        # ins.contents()
        # ins.detail()
        # with open(r"E:\codeSpace\codeSet\Python\test.md", "w", encoding="utf-8") as file:
        #     file.write(ins.markdown)
        # eng.pyi(filePath=r"E:\codeSpace\codeSet\Python\test.pyi")
        toPath = handlePath(r"E:\codeSpace\codeSet\Python\README.md", default=r"E:\codeSpace\codeSet\Python\pypiOrigin\netTools\netTools.py", suffix='md')
        ins.toMarkdown(toPath)
    else:
        args = argParser()
        ins = docParser((eng := engine(filePath=args.file)).comments)

        toPath = handlePath(args.toPath, default=args.file, suffix='md' if (t := args.type) == 'markdown' else 'pyi')

        match args.type:
            case 'markdown':
                ins.toMarkdown(toPath)
            case 'pyi':
                eng.pyi(filePath=toPath)
