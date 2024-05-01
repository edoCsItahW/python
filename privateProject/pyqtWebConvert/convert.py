#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/25 上午8:19
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from bs4 import BeautifulSoup, Tag
from cssutils import parseFile
from os import PathLike
from functools import cached_property
from warnings import warn


class htmlParser:
    def __init__(self, htmlPath: str | PathLike[str]):
        """
        parser = htmlParser("./static/html.html")
        print(parser.elements)

        :param htmlPath: html文件路径
        :type htmlPath: str | PathLike[str]
        """
        self._htmlPath = htmlPath

    @property
    def htmlPath(self): return self._htmlPath

    @cached_property
    def soup(self):
        with open(self._htmlPath, 'r', encoding='utf-8') as file:
            return BeautifulSoup(file.read(), "html.parser")

    @cached_property
    def elements(self):
        return list(self.soup.find_all(recursive=True))

    def show(self):
        """
        属性::
            name: 标签的名字，比如 'p', 'div' 等。

            attrs: 一个字典，包含了标签的所有属性。

            string: 如果标签内只有文本内容，则返回这些文本。否则返回None。

            text: 获取标签及其所有子标签的文本内容。

            parent: 标签的父标签。

            next_sibling 和 previous_sibling: 标签的下一个和上一个同级标签。

            next_element 和 previous_element: 无论是否同级，标签的下一个和上一个元素。

            contents 和 children: 标签的直接子元素列表。

            descendants: 标签的所有后代元素生成器。

            prefix: 标签的命名空间前缀，如果没有则为None。

            namespace: 标签的命名空间URL，如果没有则为None。

            sourceline 和 sourcepos: 标签在源文档中的行号和位置。

        方法::
            append(), insert(), extend(): 向标签添加子元素。

            clear() 和 decompose(): 移除标签及其内容。

            replace_with() 和 replace_with_children(): 替换标签。

            unwrap() 和 wrap(): 移除或添加标签的父标签。

            find(), find_all(), find_next(), find_previous() 等: 搜索标签或内容。

            has_attr() 和 get(): 检查标签是否有某个属性，并获取属性的值。

            encode() 和 decode(): 对标签内容进行编码和解码。

            prettify(): 格式化标签内容，使其更易读。

            select() 和 select_one(): 使用CSS选择器来搜索标签。

            is_empty_element(): 检查标签是否为空元素（例如 <br> 或 <img>）。

        :return:
        """
        for element in self.elements:
            print(element)


class cssParser:
    def __init__(self, cssPath: str | PathLike[str]):
        """
        parser = cssParser("./static/css.css")

        for rule in parser.sheet:
            if rule.type == rule.STYLE_RULE:
                print(rule.selectorText)
                for prop in rule.style:
                    print(prop.name, prop.value)

        :param cssPath: css文件路径
        :type cssPath: str | PathLike[str]
        """
        self._cssPath = cssPath

    @property
    def cssPath(self): return self._cssPath

    @cached_property
    def sheet(self):
        return parseFile(self._cssPath)


class tagWarpper:
    def __init__(self, element: Tag):
        self._element = element

    @property
    def element(self): return self._element

    def __repr__(self):
        return f"<{self.element.name}>"


class htmlAst:
    AST = {
        "body": []
    }

    def __init__(self, elements: list[Tag]):
        self._elements = elements

    @property
    def elements(self): return self._elements

    def transform(self):
        self.AST['body'].append(self.toAst(self.elements[0]))

    def toAst(self, element: Tag, *, key='body'):
        return {
            'self': tagWarpper(element),
            'parent': tagWarpper(element.parent),
            'children': [self.toAst(i) for i in element.children if i.name]
        }

    def __call__(self):
        self.transform()
        return self.AST


class qtCovert:
    def __init__(self, htmlAST: dict):
        self._htmlAST = htmlAST

        self.transform()

    @property
    def htmlAST(self):
        return self._htmlAST

    def transform(self, ast: dict | list = None, *, level: int = 0, laskKey: str = None):
        if ast is None: ast = self.htmlAST['body']

        if isinstance(ast, dict):
            for k, v in ast.items():
                print("    " * level + f"{k}:")

                self.transform(v, level=level + 1, laskKey=k)

        elif isinstance(ast, list):
            for d in ast:
                self.transform(d, level=level + 1)

        elif isinstance(ast, tagWarpper):
            print("    " * level + str(ast))

            if laskKey == 'self':

                qtFunc(ast.element.name)

        else:
            warn(f"未知类型{type(ast)}")


class qtFunc:
    AST = {
        'import': {},
        'body':   [],
    }

    def __new__(cls, key: str):
        funcDict = {
            "html": cls.html
        }

        try:
            return funcDict[key]

        except KeyError as e:
            warn(  # 无标签对应方法
                f"没有为标签'<{key}>'定义方法")

            return print

    @classmethod
    def assign(cls, key: str, value: str):
        pass

    @classmethod
    def funcDefine(cls, funcName: str):
        pass

    @classmethod
    def html(cls):
        cls.AST['import']['sys'] = ['argv']
        cls.AST['import']['PyQt6.QtWidgets'] = ['QApplication', 'QMainWindow']
        cls.AST['body'].append()


if __name__ == '__main__':
    ins = htmlAst(htmlParser("./static/html.html").elements)
    qtCovert(ins())
