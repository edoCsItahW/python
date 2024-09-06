#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

from selenium.webdriver import Chrome, Edge
from requests import Response
from typing import Literal
from bs4 import BeautifulSoup
__all__: list
headerPool: list
proxiePool: list
forProxiePool: list


def randomHeader(havehead: bool=True) ->(dict | str):
    """
    随机获取请求头.

    :param havehead: 是否带有"User-Agent"
    :type havehead: bool
    :return: 含有请求头的字典或信息字符串.
    """
    ...


def randomProxie(protocol: str='http', *, strtype: bool=False) ->(dict | str):
    """
    随机获取代理地址.

    :param protocol: 协议名称.
    :type protocol: str
    :keyword strtype: 是否为字符类,否则为字典.
    :type strtype: bool
    :return: 包含代理地址的字典或数据.
    """
    ...


class responses:
    """
    一个数据类.

    :ivar json(): 返回json数据.
    :ivar text(): 返回文本格式数据.
    :ivar content(): 返回二进制数据.
    :ivar soup(): 返回BeautifulSoup类数据.
    """

    def __init__(self, response: Response, mod: str='lxml', *, recordurl: str):
        ...

    @property
    def json(self):
        ...

    @property
    def text(self):
        ...

    @property
    def content(self):
        ...

    @property
    def soup(self):
        ...


class request:
    """
    简化并封装了requests的请求功能.

    :ivar url: 请求地址.
    :ivar data: post请求的参数.
    :ivar headers: 请求头.(默认随机.)
    :ivar params: 带参url字典.
    :ivar cookies: cookies.
    :ivar timeout: 超时时长.
    :ivar proxies: 代理地址.(默认随机.)
    :ivar verify: 是否启用安全检查.
    :ivar encoding: 编码模式.
    :ivar Proxietest(): 对代理池中的所有代理地址进行可用检测.
    :ivar getPostinfo(): 获取post请求数据.
    :ivar getRuninfo(): 获取get请求数据.
    :ivar sessioninfo(): 获取会话请求数据.
    :ivar getsoup(): 快捷获取BeautifulSoup类数据.
    :ivar getXpath(): 快速获取Xpath数据.
    """

    def __init__(self, url, data: dict=None, *, headers: dict=None, params:
        dict=None, cookies: dict=None, timeout: int=3600, proxies: dict=
        None, verify: bool=False, encoding: str='utf8'):
        ...

    @classmethod
    def Proxietest(cls, allowprint: bool=False) ->None:
        """
        对代理池中的所有代理地址进行可用检测.

        :param allowprint: 是否允许打印.
        :type allowprint: bool
        :return: 操作执行函数不做返回
        """
        ...

    def getPostinfo(self, *, mod: str='lxml') ->responses:
        """
        获取post请求数据.

        :keyword mod: 解析模式.(默认为lxml)
        :type mod: str
        :return: responses数据类.
        """
        ...

    def getRuninfo(self, *, mod: str='lxml', stream: bool=False) ->(responses |
        str):
        """
        获取get请求数据.

        :keyword mod: 解析模式.(默认为lxml)
        :type mod: str
        :return: responses数据类.
        """
        ...

    def sessioninfo(self, *, newurl: str=None, mod: str='lxml') ->responses:
        """
        获取会话请求数据.

        :keyword newurl: 此时self.url为源地址,newurl为会话地址.
        :type newurl: str
        :keyword mod: 解析模式.(默认为lxml)
        :type mod: str
        :return: responses数据类.
        """
        ...

    def getsoup(self, *, mod: str='lxml') ->BeautifulSoup:
        """
        快捷获取BeautifulSoup类数据.

        :keyword mod: 解析模式.(默认为lxml)
        :type mod: str
        :return: BeautifulSoup类数据.
        """
        ...

    def getXpath(self, *, mod: Literal['HTML', 'XML']='HTML'):
        """
        快速放回Xpath类的数据.

        :keyword mod: 解析模式.(默认为HTML)
        :type mod: str
        :return: Xpath数据类型.
        """
        ...


class autoBrowser:

    def __new__(cls, *args, **kwargs):
        ...

    def __init__(self, engine: (Chrome | Edge)=None, *, webtype: Literal[
        'edge', 'chrome']='edge', hearless: bool=False, exepath: str=None):
        ...

    @property
    def _browerType(self):
        ...

    def runengine(self, exepath: str=None, *, webtype: Literal['edge',
        'chrome']='edge', hearless: bool=True):
        """
        selenium的driver引擎.

        :param exepath: 你的浏览器驱动器地址.(初次使用可能会自动下载,但地址需要自己寻找.)
        :type exepath: str
        :param webtype: 浏览器类型.
        :type webtype: str
        :param hearless: 是否开启无头模式.
        :type hearless: bool
        :return: driver引擎.
        """
        ...

    def checkweb(self, driver: (Chrome | Edge)=None, url: str=
        'https://www.baidu.com'):
        ...

    def getHtml(self, driver: (Chrome | Edge)=None, url: str=
        'https://www.baidu.com', *, getWhenInput: bool=False, hearless:
        bool=False):
        ...

    @staticmethod
    def getSoup(html: str, *, mode: Literal['lxml', 'xml']='lxml'):
        ...


def translate_web(word: str, driver: (Chrome | Edge)=None, *, webtype:
    Literal['edge', 'chrome']='edge', mutil: bool=False) ->(str | list):
    """
    使用浏览器的无头模式对输入的文本进行翻译.

    :param word: 文本.
    :type word: str
    :param driver: driver引擎.
    :param webtype: 浏览器类型.
    :type webtype: str
    :param mutil: 是否需要获得更多翻译.
    :type mutil: bool
    :return: 翻译所得的列表或文本数据.
    """
    ...


def translate_single(word: str, *, allowName: bool=False, banKWList: list=None
    ) ->(str | list):
    """
    使用简单的百度api进行翻译，

    :param word: 文本.
    :type word: str
    :keyword allowName: 是否允许结果中出现人名.
    :type allowName: bool
    :param banKWList: 是否允许结果中出现文本的关联时态.
    :type banKWList: list
    :return: 翻译后的数据.
    """
    ...


def translate_mutil(word: str, appid: int, appkey: str, *, from_lang: str=
    'en', to_lang: str='zh') ->(list | str):
    """
    从百度api获取翻译,但appid和appkey需要自行获取.

    :param word: 文本.
    :type word: str
    :keyword appid: 软件id
    :type appid: int
    :keyword appkey: 软件密钥
    :type appkey: str
    :param from_lang: 文本的语言
    :type from_lang: str
    :param to_lang: 要翻译成的语言
    :type to_lang: str
    :return: 翻译后的数据.
    """
    ...
