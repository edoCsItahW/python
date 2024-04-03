#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/8/6 16:42
# 当前项目名: Python
# 包名: 
# -------------------------<Lenovo>----------------------------
from sympy.parsing.latex.errors import LaTeXParsingError
from sympy.parsing.latex import parse_latex
from warnings import warn
from hashlib import md5
from random import choice, randint
from os import mkdir, path

__all__ = [
    "markdown"
]


class markdown:
    def __init__(self, filepath: str, rootpath: str = r"C:\Users\Lenovo\Desktop\文档集", textpath: str = r"\md文本",
                 picpath: str = r"\md图", latex: bool = False):
        None if filepath.endswith(".md") else warn(f"{filepath}可能不是一个MarkDown文件")
        self.filepath = filepath
        self.rootpath = rootpath
        self.picpath = rootpath + picpath
        self.textpath = rootpath + textpath
        self.latex = latex
        self.dirpath = rf"{self.picpath}\{self.dirname()}"
        self.latters = "abcdefghijklmnopqrstuvwxyz"
        self.checkfile()

    def dirname(self):
        return self.filepath.split("\\")[-1].split(".")[0]

    def checkfile(self):
        if not path.exists(self.dirpath):
            mkdir(self.dirpath)
        with open(self.filepath, "w", encoding="utf-8") as file:
            file.close()

    def randname(self):
        return choice(list(self.latters)) + \
            str(randint(0, 10)) + \
            choice(list(self.latters.upper()))

    @staticmethod
    def download(url: str) -> bytes:
        from netTools import request
        response = request(url).getRuninfo()
        try:
            return response.content
        except AttributeError:
            warn(f"没能下载到网址<{url}>的内容,请确定它的类型.")

    @staticmethod
    def haxtext(text: str):
        hx = md5()
        hx.update(text.encode("utf-8"))
        return hx.hexdigest()

    def img(self, text, name: str = None, picword: str = "图"):
        name = name if name else self.randname()
        imgpath = rf"{self.dirpath}\{self.haxtext(name)}.png"
        with open(imgpath, "wb") as pic:
            pic.write(text)
        self.text(f"![{picword}]({imgpath})")

    def text(self, text: str):
        with open(self.filepath, "a", encoding="utf-8") as md:
            md.write(f"\n{text}\n")

    def latextext(self, text):
        if self.latex:
            globals()['errimg'] = None
            try:
                normaltxt = parse_latex(text)
            except LaTeXParsingError as err1:
                globals()['errimg'] = err1
                while True:
                    newtext = input(f"存在语法错误:\n\t'{globals()['errimg']}'\n请重新输入:")
                    try:
                        normaltxt = parse_latex(newtext)
                    except LaTeXParsingError as err2:
                        globals()['errimg'] = err2
                        continue
                    else:
                        break
            self.text(f"$$\n% {normaltxt}\n{text}\n$$")
        else:
            self.text(f"$$\n{text}\n$$")


if __name__ == '__main__':
    painter = markdown(r"C:\Users\Lenovo\Desktop\罗尔中值定理.md")
    painter.latextext(r"f'’(\xi)+af'(\xi)+bf(\xi)=0")
