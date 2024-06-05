#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/5/23 下午4:11
# 当前项目名: Python
# 编码模式: utf-8
# 注释: minecraft-data\index.js
# -------------------------<edocsitahw>----------------------------


def toMajor(mcVersion, preNetty, typeArg):
    parts = mcVersion.split("_")

    _type = typeArg if typeArg else parts[0] if len(parts) == 2 else 'pc'

    version = parts[1] if len(parts) == 2 else mcVersion


def export(mcVersion, preNetty = None):
    preNetty = preNetty if preNetty else False

    mcVersion = str(mcVersion).replace('pe_', 'bedrock_')

    majorVersion = toMajor(mcVersion, preNetty)

