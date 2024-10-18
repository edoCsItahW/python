#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# ! /user/bin/python3

"""
file: lexer.py
author: edocsitahw
date: 2024/10/16 下午9:00
encoding: utf-8
command:
"""
from enum import IntEnum
from typing import Iterator, Optional
from abc import ABC, abstractmethod
from warnings import warn


class TokenType(IntEnum):
    INDEX = 1
    LETTER = 2
    DOT = 3
    CONTENT = 4
    NEWLINE = 5
    END = 6
    INVALID = 7


class Token:
    def __init__(self, _type: TokenType, _pos: tuple[int, int], _value: Optional[str] = None) -> None:
        self.type = _type
        self.pos = _pos
        self.value = _value

    def __str__(self) -> str:
        return f"Token<{self.pos[0]}:{self.pos[1]}>({self.type.name}, '{self.value}')"


class Lexer:
    def __init__(self, _text: str) -> None:
        self.text = _text
        self._pos = 0
        self._line = 1
        self._col = 1

    def __iter__(self) -> Iterator[Token]:
        return self

    def __next__(self) -> Token:
        self.skip()
        if self._pos >= len(self.text):
            raise StopIteration

        match c := self.text[self._pos]:
            case '\n':
                self._pos += 1
                self._line += 1
                self._col = 1
                return Token(TokenType.NEWLINE, (self._line, self._col))
            case '.' | '、':
                self._pos += 1
                self._col += 1
                return Token(TokenType.DOT, (self._line, self._col))
            case c if c.isdigit() or c in "一二三四五六七八九十":
                return self.extractIndex()
            case c if c in "ABCD":
                return self.extractLetter()
            case _:
                return self.extractContent()

    def skip(self) -> None:
        while self._pos < len(self.text) and self.text[self._pos].isspace() and self.text[self._pos] != '\n':
            self._pos += 1
            self._col += 1

    def extractIndex(self) -> Token:
        idx, curr = "", (self._line, self._col)
        while self._pos < len(self.text) and self.text[self._pos].isdigit() or self.text[self._pos] in "一二三四五六七八九十":
            idx += self.text[self._pos]
            self._pos += 1
            self._col += 1
        return Token(TokenType.INDEX, curr, idx)

    def extractLetter(self):
        _ = self.text[self._pos]
        self._pos += 1
        return Token(TokenType.LETTER, (self._line, self._col), _)

    def extractContent(self):
        content, curr = "", (self._line, self._col)
        while self._pos < len(self.text) and self.text[self._pos] != '\n':
            content += self.text[self._pos]
            self._pos += 1
            self._col += 1
        return Token(TokenType.CONTENT, curr, content)


class AST(ABC):
    @abstractmethod
    def __str__(self) -> str: pass


class Content(AST):
    def __init__(self, _value: str) -> None:
        self.value = _value

    def __str__(self) -> str:
        return self.value


class Option(AST):
    def __init__(self, _letter: Token, _content: Content) -> None:
        self.letter = _letter
        self.content = _content

    def __str__(self) -> str:
        return f"\n{self.letter.value}.{self.content.value}"


class Question(AST):
    def __init__(self, index: Token, content: Content) -> None:
        self.index = index
        self.content = content

    def __str__(self) -> str:
        return f"{self.index.value}.{self.content.value}"


class Block(AST):
    def __init__(self, question: Question, options: list[Option]) -> None:
        self.question = question
        self.options = options

    def __str__(self) -> str:
        return f"{self.question}{''.join(map(str, self.options))}"


class Paper(AST):
    def __init__(self, _blocks: list[Block]) -> None:
        self.blocks = _blocks

    def __str__(self) -> str:
        l = '\n'
        return f"{l.join(map(str, self.blocks))}"


class Parser:
    @property
    def curr(self) -> Token:
        return self._tokens[self._pos]

    @property
    def end(self) -> bool:
        return self._pos >= len(self._tokens) or self.curr.type == TokenType.END

    def __init__(self, _tokens: list[Token]):
        self._tokens = _tokens
        self._pos = 0
        self._idx = 0

    def consume(self, _type: TokenType, _value: Optional[Token] = None) -> Token:
        _value = _value or self.curr
        if _value.type == _type:
            self._pos += 1
            return _value
        else:
            raise SyntaxError(  # 语法错误
                f"Expected {_type.name}, got {self.curr.type.name} at {self.curr.pos}")

    def parse(self) -> Paper:
        blocks = []
        while not self.end:
            blocks.append(self.parseBlock())
        return Paper(blocks)

    def parseBlock(self) -> Block:
        question = self.parseQuestion()
        options = []
        while not self.end and self.curr.type == TokenType.NEWLINE and self._tokens[self._pos+1].type == TokenType.LETTER:
            options.append(self.parseOption())
        return Block(question, options)

    def parseQuestion(self) -> Question:
        if self.curr.type == TokenType.NEWLINE:
            self.consume(TokenType.NEWLINE)
        try:
            idx = self.consume(TokenType.INDEX)
            if idx.value.isdigit():
                self._idx = int(idx.value)
        except SyntaxError:
            idx = Token(TokenType.INDEX, (0, 0), str(self._idx + 1))
        if self.curr.type == TokenType.DOT:
            self.consume(TokenType.DOT)
        return Question(idx, self.parseContent())

    def parseOption(self) -> Option:
        self.consume(TokenType.NEWLINE)
        letter = self.consume(TokenType.LETTER)
        if self.curr.type == TokenType.DOT:
            self.consume(TokenType.DOT)
        content = self.parseContent()
        if not content.value:
            warn(  # 选项缺失警告
                f"Empty option content at {self.curr.pos} idx {self._idx} option {letter.value}", SyntaxWarning)
        return Option(letter, content)

    def parseContent(self) -> Content:
        content = ""
        while not self.end and self.curr.type != TokenType.NEWLINE:
            content += self.curr.value
            self._pos += 1
        return Content(content)


class Formatter:
    def __init__(self, _paper: Paper) -> None:
        self.paper = _paper

    @staticmethod
    def format(_block: Block):
        return {
            'Content': _block.question.content.value,
            'Options': {k: "" for k in 'ABCD'} | {opt.letter.value: opt.content.value for opt in _block.options},
            'QuesType': "null",
            'MultiLine': "null",
            'Answer': ''
        }

    def show(self):
        for block in self.paper.blocks:
            print(self.format(block))


if __name__ == '__main__':
    from re import findall

    with open(r"C:\Users\Lenovo\Desktop\test.txt", 'r', encoding='gbk') as file:
        text = file.read()
        try:
            # for block in Parser(list(Lexer(text))).parse().blocks:
            #     print(block)
            Formatter(Parser(list(Lexer(text))).parse()).show()
        except SyntaxError as e:
            line = findall(r"\d+", str(e))[0]
            cont = text.split('\n')[int(line)-1]
            print(f"content: {cont}")
            raise e

