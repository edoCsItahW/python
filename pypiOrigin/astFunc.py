#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/29 下午8:40
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
"""
-- ASDL's 4 builtin types are:
-- identifier, int, string, constant

module Python
{
    mod = Module(stmt* body, type_ignore* type_ignores)
        | Interactive(stmt* body)
        | Expression(expr body)
        | FunctionType(expr* argtypes, expr returns)

    stmt = FunctionDef(identifier name, arguments args,
                       stmt* body, expr* decorator_list, expr? returns,
                       string? type_comment, type_param* type_params)
          | AsyncFunctionDef(identifier name, arguments args,
                             stmt* body, expr* decorator_list, expr? returns,
                             string? type_comment, type_param* type_params)

          | ClassDef(identifier name,
             expr* bases,
             keyword* keywords,
             stmt* body,
             expr* decorator_list,
             type_param* type_params)
          | Return(expr? value)

          | Delete(expr* targets)
          | Assign(expr* targets, expr value, string? type_comment)
          | TypeAlias(expr name, type_param* type_params, expr value)
          | AugAssign(expr target, operator op, expr value)
          -- 'simple' indicates that we annotate simple name without parens
          | AnnAssign(expr target, expr annotation, expr? value, int simple)

          -- use 'orelse' because else is a keyword in target languages
          | For(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)
          | AsyncFor(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)
          | While(expr test, stmt* body, stmt* orelse)
          | If(expr test, stmt* body, stmt* orelse)
          | With(withitem* items, stmt* body, string? type_comment)
          | AsyncWith(withitem* items, stmt* body, string? type_comment)

          | Match(expr subject, match_case* cases)

          | Raise(expr? exc, expr? cause)
          | Try(stmt* body, excepthandler* handlers, stmt* orelse, stmt* finalbody)
          | TryStar(stmt* body, excepthandler* handlers, stmt* orelse, stmt* finalbody)
          | Assert(expr test, expr? msg)

          | Import(alias* names)
          | ImportFrom(identifier? module, alias* names, int? level)

          | Global(identifier* names)
          | Nonlocal(identifier* names)
          | Expr(expr value)
          | Pass | Break | Continue

          -- col_offset is the byte offset in the utf8 string the parser uses
          attributes (int lineno, int col_offset, int? end_lineno, int? end_col_offset)

          -- BoolOp() can use left & right?
    expr = BoolOp(boolop op, expr* values)
         | NamedExpr(expr target, expr value)
         | BinOp(expr left, operator op, expr right)
         | UnaryOp(unaryop op, expr operand)
         | Lambda(arguments args, expr body)
         | IfExp(expr test, expr body, expr orelse)
         | Dict(expr* keys, expr* values)
         | Set(expr* elts)
         | ListComp(expr elt, comprehension* generators)
         | SetComp(expr elt, comprehension* generators)
         | DictComp(expr key, expr value, comprehension* generators)
         | GeneratorExp(expr elt, comprehension* generators)
         -- the grammar constrains where yield expressions can occur
         | Await(expr value)
         | Yield(expr? value)
         | YieldFrom(expr value)
         -- need sequences for compare to distinguish between
         -- x < 4 < 3 and (x < 4) < 3
         | Compare(expr left, cmpop* ops, expr* comparators)
         | Call(expr func, expr* args, keyword* keywords)
         | FormattedValue(expr value, int conversion, expr? format_spec)
         | JoinedStr(expr* values)
         | Constant(constant value, string? kind)

         -- the following expression can appear in assignment context
         | Attribute(expr value, identifier attr, expr_context ctx)
         | Subscript(expr value, expr slice, expr_context ctx)
         | Starred(expr value, expr_context ctx)
         | Name(identifier id, expr_context ctx)
         | List(expr* elts, expr_context ctx)
         | Tuple(expr* elts, expr_context ctx)

         -- can appear only in Subscript
         | Slice(expr? lower, expr? upper, expr? step)

          -- col_offset is the byte offset in the utf8 string the parser uses
          attributes (int lineno, int col_offset, int? end_lineno, int? end_col_offset)

    expr_context = Load | Store | Del

    boolop = And | Or

    operator = Add | Sub | Mult | MatMult | Div | Mod | Pow | LShift
                 | RShift | BitOr | BitXor | BitAnd | FloorDiv

    unaryop = Invert | Not | UAdd | USub

    cmpop = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn

    comprehension = (expr target, expr iter, expr* ifs, int is_async)

    excepthandler = ExceptHandler(expr? type, identifier? name, stmt* body)
                    attributes (int lineno, int col_offset, int? end_lineno, int? end_col_offset)

    arguments = (arg* posonlyargs, arg* args, arg? vararg, arg* kwonlyargs,
                 expr* kw_defaults, arg? kwarg, expr* defaults)

    arg = (identifier arg, expr? annotation, string? type_comment)
           attributes (int lineno, int col_offset, int? end_lineno, int? end_col_offset)

    -- keyword arguments supplied to call (NULL identifier for **kwargs)
    keyword = (identifier? arg, expr value)
               attributes (int lineno, int col_offset, int? end_lineno, int? end_col_offset)

    -- import name with optional 'as' alias.
    alias = (identifier name, identifier? asname)
             attributes (int lineno, int col_offset, int? end_lineno, int? end_col_offset)

    withitem = (expr context_expr, expr? optional_vars)

    match_case = (pattern pattern, expr? guard, stmt* body)

    pattern = MatchValue(expr value)
            | MatchSingleton(constant value)
            | MatchSequence(pattern* patterns)
            | MatchMapping(expr* keys, pattern* patterns, identifier? rest)
            | MatchClass(expr cls, pattern* patterns, identifier* kwd_attrs, pattern* kwd_patterns)

            | MatchStar(identifier? name)
            -- The optional "rest" MatchMapping parameter handles capturing extra mapping keys

            | MatchAs(pattern? pattern, identifier? name)
            | MatchOr(pattern* patterns)

             attributes (int lineno, int col_offset, int end_lineno, int end_col_offset)

    type_ignore = TypeIgnore(int lineno, string tag)

    type_param = TypeVar(identifier name, expr? bound)
               | ParamSpec(identifier name)
               | TypeVarTuple(identifier name)
               attributes (int lineno, int col_offset, int end_lineno, int end_col_offset)
}
"""
# code = """
# def func(arg):
#     print(f'{arg}')
# """
#
# exec(compile(code, '', 'exec'))
#
# func("a")  # type: ignore
from ast import FunctionDef, Assign, Attribute, Name, Num, Call, Expr, Constant, Load, Store, If, Module, arguments, Return, parse, dump, ClassDef
from astor import to_source
from typing import Any


class astFunc:
    @staticmethod
    def showFrame(testCode: str, *, returnCode: bool = False):
        print(dump(ast := parse(testCode)))

        if returnCode:
            print(to_source(ast))

    @staticmethod
    def FuncDef(name: str, args: list | arguments | Any = None, body: list = None, decorators: list = None, returns: Any = None):
        """
        Example::

            def func(arg: int, *, kwarg: str = 'default', none = None, ):
                return arg

            FunctionDef(
                name='func',
                args=arguments(
                    posonlyargs=[],
                    args=[
                        arg(
                            arg='arg',
                            annotation=Name(id='int', ctx=Load()),
                        )
                    ],
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[]),
                    body=[
                        Return(value=Name(id='arg', ctx=Load()))
                    ],
                    decorator_list=[]
                )


        :param name: 函数名
        :param args: 参数列表
        :param body: 函数体
        :param decorators: 装饰器列表
        :param returns: 返回值
        :return: FunctionDef
        """

        args = [] if args is None else args
        body = [] if body is None else body
        decorators = [] if decorators is None else decorators

        return FunctionDef(
            name=name,
            args=args,
            body=body,
            decorator_list=decorators,
            returns=returns,
        )

    @staticmethod
    def ClassDef(name: str, bases: list = None, keywords: list = None, body: list = None, decorators: list = None, type_params: list = None):
        """
        Example::

             class MyClass(object):
                 def __init__(self, arg: int):
                     self.arg = arg

             ClassDef(
                 name='MyClass',
                 bases=[Name(id='object', ctx=Load())],
                 keywords=[],
                 body=[
                     FunctionDef(
                         name='__init__',
                         args=arguments(
                             posonlyargs=[],
                             args=[
                                 arg(
                                     arg='self',
                                     annotation=None,
                                 ),
                                 arg(
                                     arg='arg',
                                     annotation=Name(id='int', ctx=Load()),
                                 )
                             ],
                             kwonlyargs=[],
                             kw_defaults=[],
                             defaults=[]),
                         body=[
                             Assign(
                                 targets=[
                                     Attribute(
                                         value=Name(id='self', ctx=Load()),
                                         attr='arg',
                                         ctx=Store(),
                                     )
                                 ],
                                 value=Name(id='arg', ctx=Load()),
                                 type_comment=None
                             )
                         ],
                         decorator_list=[]
                     )
                 ],
                 decorator_list=[],
                 type_params=[]

        :param name: 类名
        :param bases: 基类列表
        :param keywords: 关键字参数列表
        :param body: 类体
        :param decorators: 装饰器列表
        :param type_params: 类型参数列表
        :return: ClassDef
        """
        bases = [] if bases is None else bases
        keywords = [] if keywords is None else keywords
        body = [] if body is None else body
        decorators = [] if decorators is None else decorators
        type_params = [] if type_params is None else type_params

        return ClassDef(
            name=name,
            bases=bases,
            keywords=keywords,
            body=body,
            decorator_list=decorators,
            type_params=type_params,
        )


if __name__ == '__main__':
    testCode = """def func(arg: int):
        return arg
    """
    astFunc.showFrame(testCode, returnCode=True)
