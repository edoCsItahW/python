#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/25 上午10:33
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
# from ast import parse, NodeVisitor
#
#
# with open(r'D:\xst_project_202212\codeSet\Python\pypiOrigin\uploadTools\uploadTools.py', "r", encoding='utf-8') as file:
#     code = file.read()
#
# for i in parse(code).body:
#     print()
# import ast
#
#
# # 定义一个函数访问者，用于访问AST树中的函数定义节点
# class FuncVisitor(ast.NodeVisitor):
#     # 定义一个空的函数列表，用于存储找到的所有函数
#     def __init__(self):
#         self.functions = []
#
#     # 当访问到函数定义节点时，将函数名和函数定义添加到函数列表中
#     def visit_FunctionDef(self, node):
#         func_name = node.name
#         func_args = [arg.arg for arg in node.args.args]
#         func_defaults = [None] * (len(func_args) - len(node.args.defaults)) + node.args.defaults
#         func_code = ast.unparse(node.body).strip()
#         self.functions.append({
#             'name':     func_name,
#             'args':     func_args,
#             'defaults': func_defaults,
#             'code':     func_code,
#         })
#
#
# # 读取Python代码文件，并解析为AST树
# with open(r'D:\xst_project_202212\codeSet\Python\pypiOrigin\uploadTools\uploadTools.py', 'r', encoding="utf-8") as f:
#     source_code = f.read()
#     tree = ast.parse(source_code)
#
# # 创建函数访问者，用于遍历AST树中的函数定义节点
# visitor = FuncVisitor()
# visitor.visit(tree)
#
# # 输出找到的所有函数
# for func in visitor.functions:
#     print(f"Function name: {func['name']}")
#     print(f"Function args: {func['args']}")
#     print(f"Function defaults: {func['defaults']}")
#     print(f"Function code:\n{func['code']}\n")
import ast
import json


def ast_to_dict(node):
    """递归地将AST节点转换为字典"""
    if isinstance(node, ast.AST):
        fields = [(a, ast_to_dict(b)) for a, b in ast.iter_fields(node)]
        return node.__class__.__name__, dict(fields)
    elif isinstance(node, list):
        return [ast_to_dict(x) for x in node]
    else:
        return node


def python_code_to_json_ast(code):
    """将Python代码转换为JSON格式的AST"""
    # 解析Python代码为AST
    parsed_ast = ast.parse(code)

    # 将AST转换为字典
    ast_dict = ast_to_dict(parsed_ast)

    # 将字典转换为JSON字符串
    json_ast = json.dumps(ast_dict, indent=2)

    return json_ast


# 示例Python代码
with open(r'D:\xst_project_202212\codeSet\Python\pypiOrigin\uploadTools\uploadTools.py', 'r', encoding='utf-8') as file:
    python_code = file.read()

# 生成JSON格式的AST
json_ast_str = python_code_to_json_ast(python_code)
print(json_ast_str)

# 如果需要，你可以将JSON字符串写入文件
with open('ast.json', 'w') as f:
    f.write(json_ast_str)
