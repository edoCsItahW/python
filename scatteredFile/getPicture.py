#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/21 下午3:33
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
# begin https://kkjio.top/album/detail/8/
# end https://kkjio.top/album/detail/1274/
# begin https://luozu.fj.cn/4285/  # 非顺序页

from selenium.webdriver.chrome.service import Service as CService
from selenium.webdriver.edge.service import Service as EService
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, Edge, ChromeOptions, EdgeOptions
from typing import Literal


# bro = autoBrowser(exepath=r"D:\xst_project_202212\selenium\msedgedriver.exe", webtype='edge')
#
# # 启动浏览器并打开网页
# driver = bro.engine
# driver.get("https://cn.bing.com/images/search?q=%E6%B0%B4%E6%9E%9C")
#
# input("任意键继续")
#
# # 找到图片元素
# img_element = driver.find_elements(By.TAG_NAME, "img")[0]
#
# print(img_element)
#
# # 创建一个ActionChains对象
# action_chains = ActionChains(driver)
#
# # 移动到图片元素上并右键点击
# action_chains.move_to_element(img_element).context_click().perform()
#
# # 这里你可以尝试发送按键事件，但这通常不会触发浏览器的右键菜单选项
# # 因为这需要更复杂的操作系统级别的交互
# action_chains.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()  # 这只是一个示例，实际上不会工作
#
# # 关闭浏览器
# driver.quit()
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
