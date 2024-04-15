#! /user/bin/python3

#  Copyright (c) 2023-2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/10/21 12:55
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from netTools import request
from conFunc import square
from ansiDefine import ansiManger
from multiprocessing import freeze_support
from asyncio import get_event_loop, gather, new_event_loop
from threading import Lock
from constantPackage.ptioTools.PTIOtools import processDo, threadDo
from os import mkdir, path


class get:
    def __init__(self, dirPath: str, *, name: str = "notName", test: bool = False):
        """
        root/
            1-10/
                1-10.pdf
                1/
                2/

        1.将页数分成几部分

        2.对应每部分页数创建文件夹,如: 1-10

        3.获取图片列表

        4.将一个图片下载至一个
        """
        self.dirPath = dirPath
        self.name = name
        self.test = test
        self.color = ansiManger()

    @staticmethod
    def getIndex(url: str):
        return int(url.split("/")[-1].split(".")[0])

    def begin(self, endNum: int):
        processDo(self.mutilPage, [(l, r) for l, r in square(0, endNum, 14)])

    @staticmethod
    def mkdirN(dirPath: str):
        if not path.exists(dirPath): mkdir(dirPath)

    def mutilPage(self, startPage: int, endPage: int):
        print(f"p -> ({startPage}-{endPage})")

        pageDirPath = path.join(self.dirPath, f"{startPage}-{endPage}")
        self.mkdirN(pageDirPath)

        filePath = path.join(self.dirPath, f"{self.name}{startPage}-{endPage}.md")

        threadDo(self.getPage, [(i, pageDirPath, filePath) for i in range(startPage, endPage + 1)])

    def getPage(self, index: int, pageDirPath: str, filePath: str):
        pagePath = path.join(pageDirPath, str(index))
        self.mkdirN(pagePath)

        while not (urllist := self.getImglist(index)):
            print(self.color.f_otherColor(f"第{index}页失败: 重试.", RGB=self.color.pink))

        lock = Lock()

        self.createLoop(pagePath, urllist, filePath, lock=lock)
        # for url in urllist:
        #     self.beforeGetImg(pagePath, eval(url)["url"], filePath)

    def beforeGetImg(self, imgDirPath: str, url: str, filePath: str, lock: Lock):
        print(f"b -> {url}") if self.test else None

        index = self.getIndex(url)

        imgPath = path.join(imgDirPath, f"{index}.jpg")

        self.downloadImg(imgPath, url)
        self.writeToFile(filePath, imgPath, index=index)

    async def downList(self, imgDirPath: str, urlList: list[str], filePath: str, lock: Lock):
        return gather(*[get_event_loop().run_in_executor(None, self.beforeGetImg, imgDirPath, eval(url)["url"], filePath, lock) for url in urlList])

    def createLoop(self, imgDirPath: str, urlList: list[str], filePath: str, *, lock: Lock):
        loop = new_event_loop()
        loop.run_until_complete(self.downList(imgDirPath, urlList, filePath, lock))

    def downloadImg(self, imgPath: str, url: str):
        print(f"img -> {url}") if self.test else None

        if path.exists(imgPath):
            print(f"success: {url} -> {imgPath}")
            return

        while not (content := request(url).getRuninfo().content):
            print(self.color.f_yellow(f"failed: {url} -> {imgPath}"))

        with open(imgPath, "wb") as file:
            file.write(content)
            print(f"success: {url} -> {imgPath}")

    def getImglist(self, page: int):
        try:
            print(f"page -> {page}") if self.test else None

            soup = request(f"https://cn.czmanga.com/comic/chapter/shenjingbang-manyanxingkong/0_{page}.html").getsoup()

            assert soup, "soup 为空"

            urlList = [element.text for element in soup.find("body").find_all("script")]

            assert urlList, "urlList 为空"

            return urlList

        except SystemError as e:
            print(f"System: {e}")
        except BufferError as b:
            print(f"Buffer: {b}")
        except Exception as exp:
            print(f"Other: {exp}")

    @staticmethod
    def writeToFile(filePath: str, imgPath: str, *, index: int):
        with open(filePath, "a", encoding="utf-8") as file:
            file.write(f"![图{index}]({imgPath})\n\n")


if __name__ == '__main__':
    freeze_support()
    ins = get(r"C:\Users\Lenovo\Desktop\文档集\神精榜", name="神精榜")
    ins.begin(522)

