#  Copyright (c) 2023-2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/8/8 13:23
# 当前项目名: Python
# 包名: 
# -------------------------<Lenovo>----------------------------
from logTools import ignoreErrorAndWarning
from netTools import request
from ptioTools import parallel
from markDownTools import markdown
from bs4.element import Tag
from lxml.etree import _Element
from functools import partial
from typing import Callable, Literal, Annotated, Sequence
from lxml import etree
from bs4 import BeautifulSoup
from inspect import isfunction, ismethod, isbuiltin, isclass

__all__ = [
    "checktag",
    "deepfind",
    "zhihu",
    "supFetch"
]


def deepfind(element: _Element, *, times: int = 0):
    taglist = []
    # if isinstance(element, _Element):

    elemlist = element.iter() if times == 0 else element.getchildren()

    for deepelem in elemlist:

        if len(deepelem):
            taglist.append(deepelem)

            if len(deepelem.getchildren()):
                taglist += deepfind(deepelem, times=times + 1)

    return taglist


class checktag:
    _instance = None

    def __new__(cls, *args):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, element: _Element | Tag = None):
        self.element = element

    def is_title(self, element: _Element | Tag = None, *, func: Callable = None):

        if element is None:
            element = self.element

        if isinstance(element, _Element):
            if element.tag == "title":
                return func(element) if func else element
        elif isinstance(element, Tag):
            if element.name == "title":
                return func(element) if func else element

    def is_img(self, element: _Element | Tag = None, *, func: Callable = None):

        if element is None:
            element = self.element

        if isinstance(element, _Element):
            if element.tag == "img":
                return func(element) if func else element
        elif isinstance(element, Tag):
            if element.name == "img":
                return func(element) if func else element

    def is_h(self, element: _Element | Tag = None, *, func: Callable = None,
             tagH: Literal["h1", "h2", "h3", "h4", "h5", "h6"] = None):

        if element is None:
            element = self.element

        tag = element.tag
        if tag in [f"h{i}" for i in range(1, 7)]:
            if func:
                if tagH and tag == tagH:
                    func(element)
                else:
                    func(element)
            return func(element) if func else element

    def is_script(self, element: _Element | Tag = None, *, func: Callable = None):

        if element is None:
            element = self.element

        if isinstance(element, _Element):
            if element.tag == "script":
                return func(element) if func else element
        elif isinstance(element, Tag):
            if element.name == "script":
                return func(element) if func else element

    def is_p(self, element: _Element | Tag = None, *, func: Callable = None):

        if element is None:
            element = self.element

        if isinstance(element, _Element):
            if element.tag == "p":
                return func(element) if func else element
        elif isinstance(element, Tag):
            if element.name == "p":
                return func(element) if func else element

    def is_b(self, element: _Element | Tag = None, *, func: Callable = None):

        if element is None:
            element = self.element

        if isinstance(element, _Element):
            if element.tag == "b":
                return func(element) if func else element
        elif isinstance(element, Tag):
            if element.name == "b":
                return func(element) if func else element

    def is_li(self, element: _Element | Tag = None, *, func: Callable = None):

        if element is None:
            element = self.element

        if isinstance(element, _Element):
            if element.tag == "li":
                return func(element) if func else element
        elif isinstance(element, Tag):
            if element.name == "li":
                return func(element) if func else element

    def is_a(self, element: _Element | Tag = None, *, func: Callable = None):

        if element is None:
            element = self.element

        if isinstance(element, _Element):
            if element.tag == "a":
                return func(element) if func else element
        elif isinstance(element, Tag):
            if element.name == "a":
                return func(element) if func else element

    def is_span(self, element: _Element | Tag = None, *, func: Callable = None):

        if element is None:
            element = self.element

        if isinstance(element, _Element):
            if element.tag == "span":
                return func(element) if func else element
        elif isinstance(element, Tag):
            if element.name == "span":
                return func(element) if func else element

    def is_div(self, element: _Element | Tag = None, *, func: Callable = None):

        if element is None:
            element = self.element

        if isinstance(element, _Element):
            if element.tag == "div":
                return func(element) if func else element
        elif isinstance(element, Tag):
            if element.name == "div":
                return func(element) if func else element

    def is_othertag(self, tag: str, element: _Element | Tag = None, *, func: Callable = None):

        if element is None:
            element = self.element

        if isinstance(element, _Element):
            if element.tag == tag:
                return func(element) if func else element
        elif isinstance(element, Tag):
            if element.name == tag:
                return func(element) if func else element

    def classIs(self, key: str, element: _Element | Tag = None, *, func: Callable = None):

        if element is None:
            element = self.element

        if isinstance(element, _Element):
            if "class" in (attr := element.attrib) and attr["class"] == key:
                return func(element) if func else attr
        elif isinstance(element, Tag):
            if "class" in (attr := element.attrs) and attr["class"] == key:
                return func(element) if func else attr

    def keyInDict(self, key: str, element: _Element | Tag = None, *, func: Callable = None):

        if element is None:
            element = self.element

        if isinstance(element, _Element):
            if key in (attr := element.attrib):
                return func(element) if func else attr
        elif isinstance(element, Tag):
            if key in (attr := element.attrs):
                return func(element) if func else attr

    def wordInKey(self, word_key: tuple[str, str], element: _Element | Tag = None, *, func: Callable = None):

        if element is None:
            element = self.element

        word, key = word_key
        if isinstance(element, _Element):
            if key in (attr := element.attrib)[word]:
                return func(element) if func else attr
        elif isinstance(element, Tag):
            if key in (attr := element.attrs)[word]:
                return func(element) if func else attr

    @staticmethod
    def findAllInSoup(soup: BeautifulSoup, tag: str, *,
                      classis=None, idis: str = None, keyindict: str = None,
                      wordinkey: Annotated[tuple[str, str], "word in dict[key]"] = None, getkey: str = None, test: bool = False):

        Classis = lambda elem: ("class" in elem.attrs and elem.attrs["class"] == classis) if classis else True
        Idis = lambda elem: ("id" in elem.attrs and elem.attrs["id"] == idis) if idis else True
        Keyindict = lambda elem: (keyindict in elem.attrs) if keyindict else True
        Wordinkey = lambda elem: (
                wordinkey[1] in elem.attrs and wordinkey[0] in elem.attrs[wordinkey[1]]) if wordinkey else True

        if test:
            for element in soup.find("body").find_all(recursive=True):
                print(f"tag: {element.name}\n"
                      f"attrs: {element.attrs}\n"
                      f"text: {element.text}\n"
                      f"self: {element}\n\n")

        for element in soup.find("body").find_all(tag):
            if Classis(element) and Idis(element) and Keyindict(element) and Wordinkey(element):
                yield element.attrs[getkey] if getkey else element

    @staticmethod
    def findAllInSoups(soup: BeautifulSoup, **kwargs: Annotated[dict[str], {"classis": None, "idis": None, "keyindict": None, "wordinkey": None, "getkey": None}]):

        keylist = ["classis", "idis", "keyindict", "wordinkey", "getkey"]

        for k, v in kwargs.items():
            if isinstance(v, dict):
                for key, value in v.items():
                    if key in keylist:
                        if key == "wordinkey" and not isinstance(value, tuple):
                            raise ValueError(f"在键:'{k}'的值'{v}'中,键'{key}'的值应为元组,而不是'{value}'")
                    else:
                        raise ValueError(f"键:'{k}'的值'{v}'中有一个非法键'{key}'")
            else:
                raise ValueError(f"键:'{k}'的值不应为'{v}',而应为字典.")

        def classis(elem: Tag, *, Classis: str = None):
            return ("class" in elem.attrs and elem.attrs["class"] == Classis) if Classis else True

        def idis(elem: Tag, *, Idis: str = None):
            return ("id" in elem.attrs and elem.attrs["id"] == Idis) if Idis else True

        def keyindict(elem: Tag, *, Keyindict: str = None):
            return (keyindict in elem.attrs) if Keyindict else True

        def wordinkey(elem: Tag, *, Wordinkey: tuple[str, str] = None):
            return (Wordinkey[1] in elem.attrs and Wordinkey[0] in elem.attrs[Wordinkey[1]]) if Wordinkey else True

        logdict = {k: [] for k in kwargs.keys()}

        if soup is None:
            raise ConnectionError(f"参数'soup'的值为空,请检测连接是否正确.")

        for k, v in kwargs.items():
            vdict = {k: None for k in keylist}
            for key, value in v.items():
                vdict[key] = value
            kwargs[k] = vdict

        for element in soup.find_all(recursive=True):
            element: Tag
            if (tag := element.name) in kwargs.keys():
                if classis(element, Classis=kwargs[tag]["classis"]) and idis(element,
                                                                             Idis=kwargs[tag]["idis"]) and keyindict(
                    element, Keyindict=kwargs[tag]["keyindict"]) and wordinkey(element,
                                                                               Wordinkey=kwargs[tag]["wordinkey"]):
                    logdict[tag].append(element.attrs[getkey] if (getkey := kwargs[tag]["getkey"]) else element)

        return logdict


class zhihu:
    def __init__(self, url: str, painter: markdown = None):
        self.url = url
        self.response = request(url).getRuninfo()
        self.tree = etree.HTML(self.response.text)
        self.titlelist = [f"h{i}" for i in range(1, 7)]
        self.painter = painter

    @staticmethod
    def is_figcaption(element):
        if element.tag == "figcaption":
            text = element.text
            if text:
                # print(text)
                return text

    @staticmethod
    def other(element):
        text = element.text
        if text:
            from ANSIdefine import ansiManger
            print(ansiManger().f_green(text))

    def titledo(self, element: _Element | Tag):
        text = element.text
        if text:
            self.painter.text(text) if self.painter else print(text)

    @ignoreErrorAndWarning(WarningType=(FutureWarning,))
    def imgdo(self, elemlist, element: _Element | Tag):
        dic = element.attrib
        if 'src' in dic:
            if dic['src'].endswith("b.jpg") or dic['src'].endswith("w.webp"):
                textlist = []
                for elem in elemlist:
                    if n := checktag.is_othertag("figcaption", elem):
                        textlist.append(n.text)
                text = textlist[0] if textlist else "无"
                if self.painter:
                    res = self.painter.download(dic['src'])
                    name = text if text else dic['src']
                    self.painter.img(res, dic['src'], name if text else "图")
                else:
                    print(dic['src'], f"注释:{text}")
            elif "alt" in dic and "class" in dic and dic["class"] == "css-1phd9a0":
                if "source" in dic['src']:
                    self.painter.img(self.painter.download(dic['src']), picword="开头图") if self.painter else print(
                        dic['src'])
        return dic['src']

    def hdo(self, element: _Element | Tag):
        tag = element.tag
        if tag in self.titlelist:
            text = element.text
            if text:
                self.painter.text(f'{"#" * (self.titlelist.index(tag) + 1)} {text}') if self.painter else print(text)
            return text

    def pdo(self, element: _Element | Tag):
        text = element.text
        if text:
            self.painter.text(text) if self.painter else print(text)
        return text

    def bdo(self, element: _Element | Tag):
        text = element.text
        if text:
            self.painter.text(text) if self.painter else print(text)
        return text

    def lido(self, element: _Element | Tag):
        text = element.text
        if text:
            self.painter.text(text) if self.painter else print(text)
        return text

    def ado(self, element: _Element | Tag):
        dic = element.attrib
        if "target" in dic and dic["target"] == "_blank" and dic['class'] == 'LinkCard new':
            if "data-text" in dic:
                text: str = dic["data-text"].replace("kaysen：", "")
            else:
                text = "链接"
            self.painter.text(f"[{text}]({dic['href']})") if self.painter else print(dic['href'])
            return dic['href']

    def latexdo(self, element: _Element | Tag):
        dic = element.attrib
        if "class" in dic and dic['class'] == "ztext-math":
            text = dic["data-tex"]
            self.painter.latextext(text) if self.painter else print(text)
            return dic['data-tex']

    def beginget(self, check: bool = False):
        elemlist = list(self.tree.iter())
        for i, element in enumerate(elemlist):
            figindex = elemlist[i + 1: i + 3] if i < (len(elemlist) - 3) else None
            if not (checktag.is_title(element, func=self.titledo) or
                    checktag.is_img(element, func=partial(self.imgdo, figindex)) or
                    checktag.is_h(element, func=self.hdo) or
                    checktag.is_p(element, func=self.pdo) or
                    checktag.is_b(element, func=self.bdo) or
                    checktag.is_li(element, func=self.lido) or
                    checktag.is_a(element, func=self.ado) or
                    checktag.is_span(element, func=self.latexdo)):
                self.other(element) if check else None


class supFetch:
    def __init__(self, url: str | Literal["like https://www.baidu.com/page=REPLACE"], *, firstUrl: str = None, Range: int | tuple[Literal["like '' there is ok"] | str | int, int] = None, rooturl: str = None, test: bool = False):
        self._url = url
        self._rooturl = rooturl
        self._ins = parallel(test=test)
        self._ran = Range
        self._firstUrl = firstUrl
        self._pageFunc = None
        self.replaceWord = "REPLACE"
        self.pageArgs, self.pageKwargs = None, None

    @property
    def url(self):
        if "REPLACE" not in self._url:
            raise ValueError("如果需要获取多个页面的数据,则url应将页数位置的字符串替换为REPLACE")
        return self._url

    @property
    def rooturl(self): return "//".join([i for i in self.url.split("/") if i][:2]) if self._rooturl is None else self._rooturl

    @property
    def pageFunc(self):
        # if self._pageFunc is None:
        #     return partial(print, "AUTO")
        return self._pageFunc

    @pageFunc.setter
    def pageFunc(self, value: Callable):
        if not (isfunction(value) or isbuiltin(value) or isclass(value) or ismethod(value)):
            raise ValueError("只允许为函数地址.")
        self._pageFunc = value

    def getPage(self, url: str):
        soup = request(url).getsoup()

        if self.pageFunc is None:
            res = checktag.findAllInSoup(soup, *self.pageArgs, **self.pageKwargs)
        else:
            res = self.pageFunc(soup)

    def spawnPageUrlList(self):
        if isinstance(self._ran, tuple):
            if isinstance(self._ran[0], int):
                return [self.url.replace(self.replaceWord, str(i)) for i in range(self._ran[0], self._ran[1])]
            else:
                return [self.url.replace(self.replaceWord, self._ran[0]) if self._firstUrl is None else self._firstUrl] + [self.url.replace("REPLACE", str(i)) for i in range(2, self._ran[1])]
        return [self.url.replace(self.replaceWord, str(i)) for i in range(self._ran)]

    def begin(self, __I: Sequence = None):

        if __I is None:
            __I = self.spawnPageUrlList()

        self._ins.processDo(self.getPage, __I)


if __name__ == '__main__':
    pass
