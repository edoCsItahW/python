#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

class TokenType:
    INDEX: int
    LETTER: int
    CONTENT: int
    NEWLINE: int
    DOT: int
    END: int
    INVALID: int

tokenTypeNames: str

class Token:
    type: TokenType
    pos: int
    value: str
    def __init__(self, type: TokenType, pos: int, value: str): ...

    def __repr__(self) -> str: ...

class Lexer:
    def __init__(self, text: str): ...

    def __next__(self) -> Token: ...

    @staticmethod
    def tokenize(text: str) -> list[Token]: ...

class Content:
    value: str
    def __init__(self, value: str): ...

class Option:
    letter: Token
    dot: Token
    content: Content
    def __init__(self, letter: Token, dot: Token, content: Content): ...

class Question:
    index: Token
    dot: Token
    content: Content

    def __init__(self, index: Token, dot: Token, content: Content): ...

class Block:
    question: Question
    options: list[Option]
    def __init__(self, question: Question, options: list[Option]): ...

class Parer:
    blocks: list[Block]
    def __init__(self, blocks: list[Block]): ...

class Parser:
    def __init__(self, tokens: list[Token]): ...

    def parse(self) -> Parer: ...

class ParserError(Exception):
    def what(self) -> str: ...
