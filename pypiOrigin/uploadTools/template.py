#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/5/11 下午9:32
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
def pyproject(projectName: str, version: str, name: str, email: str, desc: str, moduleName: str, addFile: str):
    return f"""[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{projectName}"
version = "{version}"
authors = [
  {{ name="{name}", email="{email}" }},
]
description = "{desc}"
readme = "README.md"
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

{addFile}

[project.urls]
"Homepage" = "https://github.com/edoCsItahW/python/pypiOrigin/{moduleName}"
"Bug Tracker" = "https://github.com/edoCsItahW/python/issues"
"""


def CMakeLists(cmakeVision: str, projectName: str, pyVersion: str, moduleName: str, addFile: str):
    return f"""cmake_policy(SET CMP0057 NEW)
cmake_minimum_required(VERSION {cmakeVision} FATAL_ERROR)
project({projectName})

find_package(Python {pyVersion} COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)
pybind11_add_module({moduleName} {addFile})
"""


def setup(fileName: str):
    #     return f"""from setuptools import setup, Extension
    # from Cython.Build import cythonize
    #
    # setup(
    #     ext_modules=cythonize("{}", language_level=3),
    # )"""
    return f"""from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("{fileName}")
)"""
