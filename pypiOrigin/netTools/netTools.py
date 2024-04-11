#! /user/bin/python3

#  Copyright (c) 2023-2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/10/20 21:09
# 当前项目名: Python
# 编码模式: utf-8
# 注释:
# -------------------------<Lenovo>----------------------------
from selenium.webdriver.chrome.service import Service as CService
from selenium.webdriver.edge.service import Service as EService
from selenium.webdriver.common.by import By
from requests.exceptions import JSONDecodeError
from selenium.webdriver import Chrome, Edge, ChromeOptions, EdgeOptions
from urllib3.exceptions import InsecureRequestWarning
from warnings import catch_warnings, warn
from requests import get, post, session, Response
from urllib3 import disable_warnings
from hashlib import md5
from typing import Literal
from random import randint, choice
from lxml import etree
from time import time, sleep
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

__all__ = [
    "forProxiePool",
    "headerPool",
    "translate_mutil",
    "proxiePool",
    "randomHeader",
    "randomProxie",
    "request",
    "responses",
    "translate_web",
    "translate_single",
    "autoBrowser"
]

headerPool = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.4031 '
    'SLBChan/105',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)'
    ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0)'
    ' Gecko/20100101 Firefox/65.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)'
    ' AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0)'
    ' like Gecko',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X)'
    ' AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/31.0.1650.18 Mobile/11B554a Safari/8536.25',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X)'
    ' AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
    'Mozilla/5.0 (Linux; Android 4.2.1; M040 Build/JOP40D)'
    ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; M351 Build/KTU84P)'
    ' AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30']

proxiePool = [
    "112.51.96.118:9091",
    "61.164.147.242:80",
    "117.71.133.243:8089",
    "114.102.44.137:8089",
    "117.94.123.149:9000",
    "39.96.140.81:8118",
    "117.69.237.152:8089",
    "110.41.141.65:7890",
    "117.69.232.167:8089",
    "123.60.109.71:8090",
    "36.138.56.214:3128",
    "183.236.232.160:8080",
    "8.130.36.245:8080",
    "36.6.144.198:8089",
    "101.200.235.69:9000",
    "49.71.145.218:7788",
    "36.6.144.176:8089",
    "49.71.145.162:7788",
    "49.89.103.4:8089",
    "117.69.232.115:8089",
    "111.16.50.12:9002",
    "47.106.34.103:8089",
    "49.71.141.138:7788",
    "49.70.89.145:8089",
    "61.185.20.125:8000",
    "47.113.219.226:9091",
    "223.215.177.133:8089",
    "183.164.242.255:8089",
    "183.164.242.30:8089",
    "58.246.58.150:9002",
    "60.174.1.248:8089",
    "36.6.145.109:8089",
    "36.6.145.94:8089",
    "36.6.144.29:8089",
    "223.247.46.214:8089",
    "183.164.242.141:8089",
    "49.71.119.150:8089",
    "150.242.249.79:80",
    "49.89.103.222:8089",
    "36.6.144.83:8089",
    "114.231.46.103:8888",
    "124.70.78.157:8000",
    "49.70.89.186:8089",
    "8.134.140.146:9999",
    "47.109.52.147:80",
    "61.133.66.69:9002",
    "120.77.204.175:8092",
    "123.57.78.53:8118",
    "43.142.176.171:8080",
    "36.6.144.131:8089",
    "8.134.139.219:8080",
    "111.40.62.176:9091",
    "8.140.201.125:8080",
    "47.98.167.139:8089",
    "47.111.173.88:8888",
    "112.51.96.118:9091",
    "118.195.242.20:8080",
    "122.9.131.161:3128",
    "8.130.36.245:8080",
    "47.109.56.77:1081",
    "39.175.75.53:30001",
    "120.236.74.210:9002"
]

forProxiePool = [
    "98.170.57.231:4145"
]


def randomHeader(havehead: bool = True) -> dict | str:
    """
    随机获取请求头.

    :param havehead: 是否带有"User-Agent"
    :type havehead: bool
    :return: 含有请求头的字典或信息字符串.
    """
    return {"User-Agent": choice(headerPool)} if havehead else choice(headerPool)


def randomProxie(protocol: str = 'http', *, strtype: bool = False) -> dict | str:
    """
    随机获取代理地址.

    :param protocol: 协议名称.
    :type protocol: str
    :keyword strtype: 是否为字符类,否则为字典.
    :type strtype: bool
    :return: 包含代理地址的字典或数据.
    """
    url = f"{protocol}://{choice(proxiePool)}"
    return url if strtype else {protocol: url}


class responses:
    """
    一个数据类.

    :ivar json(): 返回json数据.
    :ivar text(): 返回文本格式数据.
    :ivar content(): 返回二进制数据.
    :ivar soup(): 返回BeautifulSoup类数据.
    """

    def __init__(self, response: Response, mod: str = "lxml", *, recordurl: str):
        self.response = response
        self.mod = mod
        self.url = recordurl

    @property
    def json(self):
        try:
            return self.response.json()
        except JSONDecodeError:
            warn("无法解析为JSON数据,它可能是一段文本", EncodingWarning)
            return None

    @property
    def text(self):
        return self.response.text

    @property
    def content(self):
        return self.response.content

    @property
    def soup(self):
        with catch_warnings(record=True) as w:
            soup = BeautifulSoup(self.response.content, self.mod)
        if XMLParsedAsHTMLWarning in [warning.category for warning in w]:
            times = 0
            while times <= 3:
                response = request(self.url).getRuninfo()
                with catch_warnings(record=True) as war:
                    soup = BeautifulSoup(response.content, self.mod)
                if XMLParsedAsHTMLWarning in [warning.category for warning in war]:
                    times += 1
                    continue
                else:
                    return soup
        return soup


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

    def __init__(self, url, data: dict = None, *, headers: dict = None, params: dict = None,
                 cookies: dict = None, timeout: int = 3600, proxies: dict = None,
                 verify: bool = False, encoding: str = 'utf8'):
        if proxies is None:
            proxies = randomProxie()
        if headers is None:
            headers = randomHeader()
        self.url = url
        self.data = data
        self.headers = headers
        self.params = params
        self.cookies = cookies
        self.timeout = timeout
        self.proxies = proxies
        self.verify = verify
        self.encoding = encoding
        self.statusCode = None
        disable_warnings(InsecureRequestWarning)

    @classmethod
    def Proxietest(cls, allowprint: bool = False) -> None:
        """
        对代理池中的所有代理地址进行可用检测.

        :param allowprint: 是否允许打印.
        :type allowprint: bool
        :return: 操作执行函数不做返回
        """
        for proxie in proxiePool:
            start = time()
            response = get("https://www.baidu.com/", proxies={'http': f"http://{proxie}"})
            if response.status_code == 200:
                print(f"http://{proxie}->可用(时长:{time() - start})") if allowprint else None
            else:
                raise ConnectionError(f"http://{proxie}->不可用,建议更换.")

    def getPostinfo(self, *, mod: str = "lxml") -> responses:
        """
        获取post请求数据.

        :keyword mod: 解析模式.(默认为lxml)
        :type mod: str
        :return: responses数据类.
        """
        response = post(self.url, self.data, headers=self.headers, proxies=self.proxies,
                        params=self.params, cookies=self.cookies, verify=self.verify,
                        timeout=self.timeout)
        response.encoding = self.encoding
        self.statusCode = response.status_code
        return responses(response, mod, recordurl=self.url)

    def getRuninfo(self, *, mod: str = "lxml", stream: bool = False) -> responses | str:
        """
        获取get请求数据.

        :keyword mod: 解析模式.(默认为lxml)
        :type mod: str
        :return: responses数据类.
        """
        response = get(self.url, params=self.params, headers=self.headers, cookies=self.cookies,
                       timeout=self.timeout, proxies=self.proxies, verify=self.verify, stream=stream)
        response.encoding = self.encoding
        self.statusCode = response.status_code
        res = responses(response, mod, recordurl=self.url)
        if res is None:
            return "<html>" \
                   "<title> None <title>" \
                   "<html>"
        return res

    def sessioninfo(self, *, newurl: str = None, mod: str = "lxml") -> responses:
        """
        获取会话请求数据.

        :keyword newurl: 此时self.url为源地址,newurl为会话地址.
        :type newurl: str
        :keyword mod: 解析模式.(默认为lxml)
        :type mod: str
        :return: responses数据类.
        """
        asession = session()
        asession.post(self.url, data=self.data, params=self.params, headers=self.headers, cookies=self.cookies,
                      timeout=self.timeout, proxies=self.proxies, verify=self.verify)
        response = asession.get(newurl if newurl else self.url, params=self.params, headers=self.headers,
                                cookies=self.cookies, timeout=self.timeout, proxies=self.proxies, verify=self.verify)
        response.encoding = self.encoding
        self.statusCode = response.status_code
        return responses(response, mod, recordurl=self.url)

    def getsoup(self, *, mod: str = "lxml") -> BeautifulSoup:
        """
        快捷获取BeautifulSoup类数据.

        :keyword mod: 解析模式.(默认为lxml)
        :type mod: str
        :return: BeautifulSoup类数据.
        """
        response = self.getRuninfo(mod=mod)
        soup: BeautifulSoup = response.soup
        return soup

    def getXpath(self, *, mod: Literal["HTML", "XML"] = "HTML"):
        """
        快速放回Xpath类的数据.

        :keyword mod: 解析模式.(默认为HTML)
        :type mod: str
        :return: Xpath数据类型.
        """
        response = self.getRuninfo()

        tree = etree.HTML(response.text) if mod == "HTML" else etree.XML(response.text)

        return tree


class autoBrowser:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, engine: Chrome | Edge = None, *, webtype: Literal["edge", "chrome"] = "edge",
                 hearless: bool = False, exepath: str = None):
        self.engine = self.runengine(exepath, webtype=webtype, hearless=hearless) if engine is None else engine

    @property
    def _browerType(self):
        browerDict = {
            "edge":   {
                "driver":  Edge,
                "service": EService,
                "option":  EdgeOptions()
            },
            "chrome": {
                "driver":  Chrome,
                "service": CService,
                "option":  ChromeOptions()
            }
        }
        return browerDict

    def runengine(self, exepath: str = None, *, webtype: Literal["edge", "chrome"] = "edge", hearless: bool = True):
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
        if webtype not in ["edge", "chrome"]: raise ValueError(f"你的输入'{webtype}'不在[\"edge\", \"chrome\"]之中.")

        webDict = self._browerType[webtype]

        service = webDict["service"](executable_path=exepath)
        option = webDict["option"]
        option.add_argument("--headless")

        return webDict["driver"](service=service, options=option if hearless else None)

    def checkweb(self, driver: Chrome | Edge = None, url: str = "https://www.baidu.com"):
        if not driver:
            driver = self.engine
        driver.get(url)

        input("任意键结束:")

        driver.quit()

    def getHtml(self, driver: Chrome | Edge = None, url: str = "https://www.baidu.com", *, getWhenInput: bool = False,
                hearless: bool = False):
        if not driver:
            driver = self.engine

        driver.get(url)

        input("按下任意键捕获当前网页源码:") if getWhenInput else None

        code = driver.page_source

        return code

    @staticmethod
    def getSoup(html: str, *, mode: Literal["lxml", "xml"] = "lxml"):
        return BeautifulSoup(html, mode)


def translate_web(word: str, driver: Chrome | Edge = None, *,
                  webtype: Literal["edge", "chrome"] = "edge", mutil: bool = False) -> str | list:
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
    if driver is None:
        driver = autoBrowser().engine
    driver.get(r"https://fanyi.baidu.com/translate")
    element = driver.find_element(By.ID, "baidu_translate_input")
    element.send_keys(word)
    driver.implicitly_wait(1)
    sleep(1)
    try:
        output = driver.find_elements(By.CLASS_NAME, "keywords-means")[0] if mutil else driver.find_element(
            By.CLASS_NAME,
            "trans-right")
    except IndexError:
        output = driver.find_elements(By.CLASS_NAME, "dict-comment-mean")[0]

    result = output.text.split(";") if mutil else output.text.split("\n")[0] if output else "网络超时"

    driver.quit()
    return result


def translate_single(word: str, *, allowName: bool = False, banKWList: list = None) -> str | list:
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
    if banKWList is None:
        banKWList = ['名词复数', '过去分词']
    return list(filter(
        lambda x: True if allowName else (True if '人名' not in x and all([i not in x for i in banKWList]) else False),
        [list(i.values())[1] for i in
         request("https://fanyi.baidu.com/sug", data={"kw": word}).getPostinfo().json['data']]))


def translate_mutil(word: str, appid: int, appkey: str, *,
                    from_lang: str = "en",
                    to_lang: str = "zh") -> list | str:
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
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    salt = randint(32768, 65536)
    sign = md5((str(appid) + word + str(salt) + appkey).encode("utf-8")).hexdigest()

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'appid': appid,
        'q':     word,
        'from':  from_lang,
        'to':    to_lang,
        'salt':  salt,
        'sign':  sign
    }

    r = post(url, params=payload, headers=headers)
    result = r.json()

    return result["trans_result"][0]["dst"]


if __name__ == '__main__':
    pass
