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
r"""

from ast import parse, NodeVisitor


with open(r'D:\xst_project_202212\codeSet\Python\pypiOrigin\uploadTools\uploadTools.py', "r", encoding='utf-8') as file:
    code = file.read()

for i in parse(code).body:
    print()
import ast


# 定义一个函数访问者，用于访问AST树中的函数定义节点
class FuncVisitor(ast.NodeVisitor):
    # 定义一个空的函数列表，用于存储找到的所有函数
    def __init__(self):
        self.functions = []

    # 当访问到函数定义节点时，将函数名和函数定义添加到函数列表中
    def visit_FunctionDef(self, node):
        func_name = node.name
        func_args = [arg.arg for arg in node.args.args]
        func_defaults = [None] * (len(func_args) - len(node.args.defaults)) + node.args.defaults
        func_code = ast.unparse(node.body).strip()
        self.functions.append({
            'name':     func_name,
            'args':     func_args,
            'defaults': func_defaults,
            'code':     func_code,
        })


# 读取Python代码文件，并解析为AST树
with open(r'D:\xst_project_202212\codeSet\Python\pypiOrigin\uploadTools\uploadTools.py', 'r', encoding="utf-8") as f:
    source_code = f.read()
    tree = ast.parse(source_code)

# 创建函数访问者，用于遍历AST树中的函数定义节点
visitor = FuncVisitor()
visitor.visit(tree)

# 输出找到的所有函数
for func in visitor.functions:
    print(f"Function name: {func['name']}")
    print(f"Function args: {func['args']}")
    print(f"Function defaults: {func['defaults']}")
    print(f"Function code:\n{func['code']}\n")
"""


r"""
将AST转换为json格式字符串
from ast import AST, parse, iter_fields
from json import dumps


def ast_to_dict(node):
    # 递归地将AST节点转换为字典
    if isinstance(node, AST):

        return node.__class__.__name__, {k: ast_to_dict(v) for k, v in iter_fields(node)}

    elif isinstance(node, list):

        return [ast_to_dict(x) for x in node]

    else:

        return node


def python_code_to_json_ast(code):
    # 将Python代码转换为JSON格式的AST
    return dumps(ast_to_dict(parse(code)), indent=2)


# 示例Python代码
with open(r'D:\xst_project_202212\codeSet\Python\pypiOrigin\uploadTools\uploadTools.py', 'r', encoding='utf-8') as file:
    python_code = file.read()

print(json_ast_str := python_code_to_json_ast(python_code))

# 如果需要，你可以将JSON字符串写入文件
with open('ast.json', 'w') as f:
    f.write(json_ast_str)
"""


# from ast import Name, FunctionDef, Module, Assign, Num, Store
# from astor import to_source
#
#
# print(to_source(Module(body=[Assign(targets=[Name(id='a', ctx=Store())], value=Num(n=10))])))

"""
函数定义
import ast
import astor

# 定义一个函数：def my_function(a, b):
func_def = ast.FunctionDef(
    name='my_function',  # 函数名
    args=ast.arguments(
        args=[ast.arg(arg='a', annotation=None), ast.arg(arg='b', annotation=None)],  # 参数列表
        vararg=None,  # 可变位置参数名
        kwonlyargs=[],  # 关键字参数列表
        kw_defaults=[],  # 关键字参数的默认值列表
        kwarg=None,  # 可变关键字参数名
        defaults=[]  # 位置参数的默认值列表
    ),
    body=[  # 函数体
        # 一个条件语句：if a > b:
        ast.If(
            test=ast.Compare(left=ast.Name(id='a', ctx=ast.Load()),  # 条件表达式左操作数
                             ops=[ast.Gt()],  # 比较操作符列表
                             comparators=[ast.Name(id='b', ctx=ast.Load())]  # 条件表达式右操作数列表
                             ),
            body=[  # 真分支
                # 一个打印语句：print("a is greater than b")
                ast.Expr(value=ast.Call(
                    func=ast.Name(id='print', ctx=ast.Load()),  # 函数名
                    args=[ast.Constant(value="a is greater than b")],  # 函数参数列表
                    keywords=[]  # 关键字参数列表
                ))
            ],
            orelse=[]  # 假分支（留空表示没有假分支）
        )
    ],
    decorator_list=[],  # 装饰器列表
    returns=None  # 返回值注解
)

# 创建一个模块，将函数定义作为其子节点
module = ast.Module(body=[func_def])

# 使用astor模块将AST还原为源码
source_code = astor.to_source(module)
print(source_code)"""

"""
# 类定义
import ast
import astor

# 创建一个表示类属性的AST节点
class_attribute = ast.Assign(
    targets=[ast.Name(id='my_attribute', ctx=ast.Store())],
    value=ast.Constant(value=42)
)

# 创建一个表示类方法的AST节点
class_method = ast.FunctionDef(
    name='my_method',
    args=ast.arguments(
        args=[ast.arg(arg='self', annotation=None)],
        vararg=None,
        kwonlyargs=[],
        kw_defaults=[],
        kwarg=None,
        defaults=[]
    ),
    body=[
        ast.Return(value=ast.Num(n=1))
    ],
    decorator_list=[],
    returns=None
)

class_method2 = ast.FunctionDef(
    name='__init__',
    args=ast.arguments(
        args=[ast.arg(arg='self', annotation=None)],
        vararg=None,
        kwonlyargs=[],
        kw_defaults=[],
        kwarg=None,
        defaults=[]
    ),
    body=[
        ast.Return()
    ]
)

# 创建一个类定义AST节点
class_def = ast.ClassDef(
    name='MyClass',
    bases=[ast.Name(id='object', ctx=ast.Load())],  # 基类，这里使用object作为基类
    keywords=[],
    body=[class_attribute, class_method],  # 类体，包含属性和方法
    decorator_list=[]  # 装饰器列表，留空表示没有装饰器
)

# 创建一个模块AST节点，将类定义作为其子节点
module = ast.Module(body=[class_def])

# 使用astor模块将AST还原为源码
source_code = astor.to_source(module)
print(source_code)
# """

import ast
import astor

# 创建 __init__ 方法
init_method = ast.FunctionDef(
    name='__init__',
    args=ast.arguments(
        args=[ast.arg(arg='self', annotation=None), ast.arg(arg='arg', annotation=ast.Name(id='int', ctx=ast.Load()))],
        defaults=[ast.Num(n=1)]
    ),
    body=[
        ast.Assign(
            targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr='arg', ctx=ast.Store())],
            value=ast.Name(id='arg', ctx=ast.Load())
        )
    ],
    decorator_list=[],
    returns=None
)

# 创建 @property 装饰器调用
property_decorator = ast.Call(
    func=ast.Name(id='property', ctx=ast.Load()),
    args=[],
    keywords=[]
)

# 创建 arg 方法，并添加 @property 装饰器
property_arg_method = ast.FunctionDef(
    name='arg',
    args=ast.arguments(
        args=[ast.arg(arg='self', annotation=None)],
        defaults=[]
    ),
    body=[
        ast.Return(value=ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr='arg', ctx=ast.Load()))
    ],
    decorator_list=["property"],  # 直接将装饰器调用添加到 decorator_list
    returns=ast.Name(id='int', ctx=ast.Load())
)

# 创建 @staticmethod 装饰器调用
staticmethod_decorator = ast.Call(
    func=ast.Name(id='staticmethod', ctx=ast.Load()),
    args=[],
    keywords=[]
)

# 创建 func 方法，并添加 @staticmethod 装饰器
staticmethod_func_method = ast.FunctionDef(
    name='func',
    args=ast.arguments(
        args=[ast.arg(arg='cls', annotation=None)],
        defaults=[]
    ),
    body=[
        ast.Expr(value=ast.Call(
            func=ast.Name(id='print', ctx=ast.Load()),
            args=[ast.Constant(value="Hello World!")],
            keywords=[]
        ))
    ],
    decorator_list=["staticmethod"],  # 直接将装饰器调用添加到 decorator_list
    returns=None
)

# 创建类定义，包含上述方法
class_def = ast.ClassDef(
    name='a',
    bases=[],
    keywords=[],
    body=[init_method, property_arg_method, staticmethod_func_method],
    decorator_list=[]
)

# 创建模块定义，包含类定义
module = ast.Module(body=[class_def])

# 将AST转换为源代码
source_code = astor.to_source(module)

# 打印源代码
print(source_code)

exec(source_code)
