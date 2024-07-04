#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/6/29 下午3:02
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from flask import Flask, render_template, request, jsonify
from typing import Any
from questionType import Choice, ChoiceMulti, Judge, QuestionPool
from pandas import DataFrame, read_csv

app = Flask(__name__, static_folder=r".\static", template_folder=r".\template")


def standardizeResponse(data: Any):
    return jsonify({"code": 200, "msg": "ok", "data": data})


@app.route("/", methods=["GET", "POST"])
def root():
    return render_template(r"index.html")


@app.route("/api", methods=["POST"])
def api():
    requestData = request.json

    if requestData == "types":
        return standardizeResponse({"choice": "单选题", "choiceMulti": "多选题", "judge": "判断题"})

    elif requestData == "choice":
        df = read_csv(r"E:\codeSpace\codeSet\Python\privateProject\exam\static\csv\单选题.csv", encoding="gbk")
        return standardizeResponse(list(QuestionPool(df, Type=Choice)))
        # return standardizeResponse([{"id": 1, "question": "请跳过!", "option": {"A": "答案是C", "B": "", "C": "", "D": ""}, "answer": "C"}])

    elif requestData == "choiceMulti":
        df = read_csv(r"E:\codeSpace\codeSet\Python\privateProject\exam\static\csv\多项选择题.csv", encoding="gbk")
        return standardizeResponse(list(QuestionPool(df, Type=ChoiceMulti)))

    elif requestData == "judge":
        df = read_csv(r"E:\codeSpace\codeSet\Python\privateProject\exam\static\csv\判断题.csv", encoding="gbk")
        return standardizeResponse(list(QuestionPool(df, Type=Judge)))

    elif isinstance(requestData, dict):
        key, obj, _type = requestData["key"], requestData["obj"], requestData["type"]

        if _type == "choice":
            return standardizeResponse({"result": key == obj["answer"], "answer": [obj["answer"]]})
        elif _type == "choiceMulti":
            return standardizeResponse({"result": all(k in key for k in obj["answer"]), "answer": obj["answer"]})
        elif _type == "judge":
            return standardizeResponse({"result": key == obj["answer"], "answer": [obj["answer"]]})


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

