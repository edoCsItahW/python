#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/5/2 下午7:21
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from re import findall, DOTALL
from typing import Literal


annotation1 = """This is a test annotation."""

# 换行注释
annotation2 = """
    This is a multiline test annotation.
    """

# 换行头注释
annotation3 = """
    This is a multiline test annotation.
    This is the second line of the annotation.
    """

# 典型类注释
classAnnotation1 = """
    This is header of this test annotation.
    
    Attributes:
        :ivar arg1: explaintion of arg1
        :ivar arg2: explaintion of arg2
    
    Methods::
        :meth:`method1`: explains method1
        
        :meth:`method2`: explains method2
    """

# 包含示例的类注释
classAnnotation4 = """
This is a test annotation.

Example::

    >>> print("Hello, world!")
    Hello, world!

Attributes:
    :ivar arg1: explaintion of arg1
    :ivar arg2: explaintion of arg2

Methods::
    :meth:`method1`: explains method1
    
    :meth:`method2`: explains method2
"""

# 简化类注释
classAnnotation2 = """
    This is header of this test annotation.
    
    Attributes:
        :ivar arg1: explaintion of arg1
        :ivar arg2: explaintion of arg2
    
    Methods::
        method1: explains method1
        
        method2: explains method2
    """

# 无头类注释
classAnnotation3 = """
    Attributes:
        :ivar arg1: explaintion of arg1
        :ivar arg2: explaintion of arg2
    
    Methods::
        method1: explains method1
        
        method2: explains method2
    """

# 典型函数注释
defAnnotation1 = """
    This is header of this test annotation.
    
    :param arg1: explaintion of arg1
    :type arg1: str
    :param arg2: explaintion of arg2
    :type arg2: int
    :keyword arg3: explaintion of arg3
    :type arg3: bool
    :return: explaintion of return value
    :rtype: str
    :raises TypeError: explaintion of type error
    """

# 包含代码示例的函数注释
defAnnotation2 = """
    This is header of this test annotation.
    
    Example::
    
        >>> print("Hello, world!")
        Hello, world!
    
    :param arg1: explaintion of arg1
    :type arg1: str
    :param arg2: explaintion of arg2
    :type arg2: int
    """

# 无头函数注释
defAnnotation3 = """
    :param arg1: explaintion of arg1
    :type arg1: str
    """


def anlyzeAnnotation(comment: str, *, mode: Literal["class", "func"] = "func"):
    # print(findall(r"(?:.?).*?\.(?:.?)", comment))
    # ^(?:.+\n)*?\r?\n?$

    if "example:" in comment.lower():
        print(findall(r"(?<=Example:|example:)(?::).*?(?=:|$|Attributes|Methods)", comment, DOTALL))

    match mode:
        case "class":
            if "Attributes:" in comment:
                print(findall(r"(?<=Attributes:)(?:\n).*?(?:\n.*?\n)", comment))

            if "Methods:" in comment:
                print(findall(r"(?<=Methods:)(?::)(?:\n).*(?=$)", comment, DOTALL))

        case "func":
            print(findall(r":(param|type|keyword|raise)(.*)(?=$)", comment, DOTALL))


if __name__ == '__main__':
    commentDict = {
        "common": annotation1,
        "multiline": annotation2,
        "multilineHead": annotation3,
        "typicalClass": classAnnotation1,
        "codeExampleClass": classAnnotation4,
        "simplifiedClass": classAnnotation2,
        "noHeaderClass": classAnnotation3,
        "typicalFunc": defAnnotation1,
        "codeExampleFunc": defAnnotation2,
        "noHeaderFunc": defAnnotation3,
    }

    for name, comment in commentDict.items():
        print(f"{name}:\n")

        anlyzeAnnotation(comment, mode="func")
        print("\n")
    # print(classAnnotation1.replace("\n", "|"))

