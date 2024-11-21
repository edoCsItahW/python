#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/9/29 下午1:30
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from os import getcwd, path, PathLike, rename as osrename, listdir
from typing import overload, Callable, Awaitable, Literal
from asyncio import run, get_running_loop, AbstractEventLoop, new_event_loop, gather, Task
from aiofiles import open as aioopen
from datetime import datetime
from debuger import Dbg, DbgOpt
from atexit import register
from inspect import currentframe as cf
from argparse import ArgumentParser, Namespace
from warnings import warn
from subprocess import PIPE, Popen

mainTs = """import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router/router'

const app = createApp(App).use(createPinia()).use(router).mount('#app')
"""


appVue = f"""<!--
  - Copyright (c) 2024. All rights reserved.
  - This source code is licensed under the CC BY-NC-SA
  - (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
  - This software is protected by copyright law. Reproduction, distribution, or use for commercial
  - purposes is prohibited without the author's permission. If you have any questions or require
  - permission, please contact the author: 2207150234@st.sziit.edu.cn
  -->
<script lang="ts">
/**
 * @file App.vue
 * @author edocsitahw
 * @version 1.1
 * @date {datetime.now():%Y/%m/%d %H:%M:%S}
 * @description
 * */
import {{ defineComponent }} from "vue";
import router from "@/router/router";

onload = () => {{
    router.push("/");
}}

export default defineComponent({{
    name: "App"
}});
</script>

<template>
    <router-view></router-view>
</template>

<style lang="sass">
</style>"""


routerTs = """import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: []
})

export default router"""


storeTs = """import { defineStore } from 'pinia'

export const Store_ = defineStore('store', {
  state() {
      return {}
  },
  getters: {},
  actions: {}
})"""


viteConfigTs = """import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import { viteMockServe } from "vite-plugin-mock";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";

// https://vitejs.dev/config/
export default defineConfig({
    esbuild: {
        target: "es2020"
    },
    css: {
        preprocessorOptions: {
            sass: {
                api: 'modern-compiler'
            }
        }
    },
    plugins: [
        vue({
            script: {
                babelParserPlugins: ["decoratorAutoAccessors"]
            }
        }),
        vueDevTools(),
        viteMockServe({
            mockPath: "./src/mock",
        }),
    ],
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
        },
    },
    assetsInclude: ["**/*.svg"],
    server: {
        host: "0.0.0.0",
        port: 7265,
        open: true
    }
});"""


mockTs = """/*
 - Copyright (c) 2024. All rights reserved.
 - This source code is licensed under the CC BY-NC-SA
 - (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
 - This software is protected by copyright law. Reproduction, distribution, or use for commercial
 - purposes is prohibited without the author's permission. If you have any questions or require
 - permission, please contact the author: 2207150234@st.sziit.edu.cn
 */
import { createProdMockServer } from "vite-plugin-mock/client";
import MockMethod from "./api";

export function setupProdMockServer() {
    createProdMockServer([...MockMethod]);
}"""


apiTs = """export default [
    {
        url: '/api',
        method: 'POST',
        response: {
            code: 200,
            msg: 'ok',
            data: 'Hello, World!'
        }
    }
]"""


tsconfigJson = """{
    "files": [],
    "references": [
        {
            "path": "./tsconfig.node.json"
        },
        {
            "path": "./tsconfig.app.json"
        },
        {
            "path": "./tsconfig.vitest.json"
        }
    ],
    "include": ["./src/components/*.vue", "./src/components/**/*.vue", "./src/*.d.ts", "./src/**/*.ts"],
    "exclude": ["node_modules", "dist"],
    "compilerOptions": {
        "module": "ESNext",
        "declaration": true,
        "emitDeclarationOnly": true,
        "outDir": "./dist",
        "target": "esnext",
        "moduleResolution": "node",
        "baseUrl": "./",
        "paths": {
            "@/*": ["./src/*"]
        }
    }
}"""


indexHtml = lambda title: f"""<!--
  ~ Copyright (c) 2024. All rights reserved.
  ~ This source code is licensed under the CC BY-NC-SA
  ~ (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
  ~ This software is protected by copyright law. Reproduction, distribution, or use for commercial
  ~ purposes is prohibited without the author's permission. If you have any questions or require
  ~ permission, please contact the author: 2207150234@st.sziit.edu.cn
  -->
<!doctype html>
<html lang="zh-Hans">
    <head>
        <meta charset="UTF-8" />
        <link rel="icon" href="/favicon.ico" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{title}</title>
    </head>
    <body>
        <div id="app"></div>
        <script type="module" src="./src/main.ts"></script>
    </body>
</html>"""


prettierCfg = """{
  "$schema": "https://json.schemastore.org/prettierrc",
  "experimentalTernaries": true,  
  "printWidth": 200,  
  "tabWidth": 4,  
  "useTabs": false,  
  "semi": true,  
  "singleQuote": false,  
  "quoteProps": "as-needed",  
  "jsxSingleQuote": false,  
  "trailingComma": "none",  
  "bracketSpacing": true,  
  "bracketSameLine": false,  
  "arrowParens": "avoid",  
  "rangeStart": 0,  
  "proseWrap": "preserve",  
  "htmlWhitespaceSensitivity": "ignore",
  "vueIndentScriptAndStyle": false,  
  "endOfLine": "lf",  
  "embeddedLanguageFormatting": "auto",
  "singleAttributePerLine": false,
  "plugins": []
}"""


class CMDError(Exception):
    def __init__(self, *args):
        self.args = args


def outputInfo(info: str, *, color: Literal["red", "green", "blue", "yellow"] | str | bool = "green",
               flag: bool = True):
    if not flag: return

    colorDict = {
        "red":    '\033[41m',
        "green":  '\033[42m',
        "yellow": '\033[43m',
        "blue":   '\033[44m',
    }

    if isinstance(color, str):
        print(f"{colorDict[color] if color in colorDict else color}{info}\033[0m")

    elif isinstance(color, bool):
        print(f"{colorDict['green']}{info}\033[0m" if color else info)

    else:
        raise TypeError(
            f"关键字参数`color`可以布尔值(bool), ANSI转义符(str)或颜色键,但你的输入'{type(color)}'")


class instruct:
    """
    命令行运行器

    使用方法::

        >>> ins = instruct(output=True, ignore=False, color=True)
        >>> ins("dir")
    """
    _instance = None

    def __new__(cls, *args, **kwargs):

        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, *, output: bool = True, ignore: bool = False,
                 color: bool | Literal["red", "yellow", "green", "blue"] = True, eliminate: str = None):
        """
        命令行初始器

        :keyword output: 是否运行输出结果.
        :type output: bool
        :keyword ignore: 是否将所有(原本将会抛出的)错误(Error)降级为警告(Warning)以保证程序不中断.
        :type ignore: bool
        :keyword color: 为布尔类型(bool)时决定输出是否带有ANSI色彩,为字符串(str)时决定输出什么颜色.
        :type color: bool
        :keyword eliminate: 是否排除某些会被误认为错误的无关紧要的警告,例如: '文件名、目录名或卷标语法不正确。'
        """
        self._flagOutput = output
        self._flagIgnore = ignore
        self._flagColor = color
        self._eleiminate = eliminate

    def __call__(self, instruction: str, *, cwd: PathLike | str = None, output: bool = None,
                 encoding: Literal["gbk", "utf-8"] = "gbk", note: str = ""):
        """
        执行器

        :param instruction: 指令
        :type instruction: str
        :keyword cwd: 设定当前路径或执行路径
        :type cwd: str
        :keyword allowOUTPUT: 是否允许打印结果
        :type allowOUTPUT: bool
        :return: cmd执行结果
        :rtype: str
        """

        correct, error = self._execute(instruction, cwd=cwd, encoding=encoding)

        tempFunc = lambda x: x.replace("\n", "").replace("\r", "").replace(" ", "")

        if self._flagIgnore:

            if flag := (self._flagOutput if output is None else output):
                outputInfo(f"{cwd if cwd else 'cmd'}>{instruction}", color="green" if self._flagColor else False,
                           flag=flag)

                print(correct) if correct else None

            if self._eleiminate is None or (tempFunc(error) != tempFunc(self._eleiminate)):
                warn(
                    error + note, SyntaxWarning)

            return correct

        else:

            if self._eleiminate is None or (tempFunc(error) != tempFunc(self._eleiminate)):

                raise CMDError(error)

            elif tempFunc(error) == tempFunc(self._eleiminate):

                warn(
                    f"你忽略了错误'{self._eleiminate}',而且没有将错误降级为警告,这导致一个错误被忽略了,带来的后果是返回了None而不是你期望的结果!")

    @staticmethod
    def _execute(instruction: str, *, cwd: PathLike | str = None, encoding: Literal["gbk", "utf-8"] = "gbk") -> tuple[
        str, str]:
        """
        执行器内核

        :param instruction: 指令
        :type instruction: str
        :param cwd: 执行环境路径
        :type cwd: PathLike | str
        :param encoding: 编码.(防止命令行输出乱码)
        :type encoding: str
        :return: 一个字典,键'C'对应正确信息,键'E'对应错误消息
        :rtype: dict
        """
        try:

            result = Popen(instruction, shell=True, stdout=PIPE, stderr=PIPE, cwd=cwd)

            return tuple(getattr(result, i).read().decode(encoding, errors='ignore') for i in ["stdout", "stderr"])

        except Exception as err:

            err.add_note("命令行执行器内核运行错误")

            raise err


executor = instruct(ignore=True)


class Context:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, projPath: str):
        if path.isabs(projPath): self.projRoot = projPath  # 绝对路径
        else: self.projRoot = path.abspath(projPath)  # 相对路径
        self.projName = path.basename(self.projRoot)  # 项目名称
        if path.exists(self.projRoot):
            if not path.isdir(self.projRoot):
                raise TypeError(  # 路径错误
                    f"'{projPath}' should be the root directory of a project, not any other path!")
        else:
            raise NotADirectoryError(  # 路径不存在
                f"'{projPath}' is not a valid directory, please check it!")

    async def root(self, _path: PathLike[str] | str):
        return path.join(self.projRoot, _path)


@Dbg(DbgOpt.RAISE, group="check")
def existsCheck(_path: PathLike[str] | str) -> str:
    """
    检查路径是否存在,并且返回一个有效且绝对的路径

    :param _path: 路径
    :return: 有效且绝对的路径
    :raise FileNotFoundError: 文件不存在
    """
    if not path.exists(_path := path.abspath(_path)):
        raise FileNotFoundError(  # 文件不存在
            f"'{_path}' is not a valid file or directory, please check it!")
    return _path


@Dbg(group="operate", note=f"Error occurre when delete line {cf().f_lineno} in <{cf().f_code.co_name}>")
async def delete(_path: PathLike[str] | str, *, pattern: str = None):
    """
    对路径进行删除,无论其是文件还是目录

    :param _path: 路径
    :raise FileNotFoundError: 文件不存在
    """
    _path = existsCheck(_path)
    if pattern:
        for file in listdir(_path):
            if pattern.replace("*", "") in file:
                await delete(path.join(_path, file))
    else:
        executor(f"rd /s /q {_path}" if path.isdir(_path) else f"del /f {_path}", cwd=path.dirname(_path))


@Dbg(group="operate", note=f"Error occurre when modify line {cf().f_lineno} in <{cf().f_code.co_name}>")
async def modify(_path: PathLike[str] | str, content: str, *, handle: Callable[[str], str] = None, **kwargs):
    """
    对文件进行内容修改

    :param _path: 文件路径
    :param content: 新的内容
    :keyword handle: 内容处理函数,将原内容作为参数,返回处理后的内容
    :param kwargs: 其他参数,如encoding,errors等
    :raise FileNotFoundError: 文件不存在
    """
    _path = existsCheck(_path)
    async with aioopen(_path, 'r+' if handle else 'w', **kwargs) as file:
        content = handle(await file.read()) if handle else content
        await file.seek(0)
        await file.write(content)
        await file.truncate()


@Dbg(group="operate", note=f"Error occurre when create line {cf().f_lineno} in <{cf().f_code.co_name}>")
async def create(_path: PathLike[str] | str, content: str = None, **kwargs):
    """
    对路径进行创建,无论其是文件还是目录

    :param _path: 路径
    :param content: 内容
    :keyword kwargs: 其他参数,如encoding,errors等
    """
    if "." in path.basename(_path):  # 文件
        async with aioopen(_path, 'w', **kwargs) as file:
            if content:
                await file.write(content)
    else:  # 目录
        executor(f"mkdir {path.basename(_path)}", cwd=path.dirname(_path))


@Dbg(group="operate", note=f"Error occurre when rename line {cf().f_lineno} in <{cf().f_code.co_name}>")
async def rename(_path: PathLike[str] | str, newName: str, **kwargs):
    _path = existsCheck(_path)
    osrename(_path, path.join(path.dirname(_path), newName))


class Loop:
    def __init__(self, loop: AbstractEventLoop = None):
        try:
            self._loop = loop or get_running_loop()
        except RuntimeError:
            self._loop = new_event_loop()
        self._tasks = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await gather(*self._tasks)

    def addTask(self, task: Callable[..., Awaitable[None]], *args, condition: Callable[[], bool] = None, **kwargs):
        if condition and not condition(): return

        self._tasks.append(self._loop.create_task(task(*args, **kwargs)))


@register
def exitHandler():
    if Dbg.errorLog:
        Dbg.raiseErrorGroup()


async def main(_args: Namespace):
    """
    1. 删除.vscode文件夹
    2. 删除README.md文件
    3. 删除src中的views文件夹
    4. 删除src/assets中的base.css文件
    5. 删除src/assets中的main.css文件
    6. 移除src/main.ts对main.css的引用
    7. 清除App.vue中的多余内容
    8. 更名router的index.ts为router.ts
    9. 修改router/router.ts的内容
    10. 修改src/main.ts对router的引用
    11. 移除src/components的vue和icons文件夹
    12. 更名stores中的counter.ts为stores.ts
    13. 修改stores/stores.ts内容
    14. 安装vite-plugin-mock
    15. 修改vite.config.ts内容
    16. 新建文件夹src/mock
    17. 新建文件src/mock/mock.ts
    18. 修改src/mock/mock.ts内容
    19. 新建文件src/mock/api.ts
    20. 修改src/mock/api.ts内容
    21. 修改tsconfig.json
    (可选) 添加文件openAPI.json
    22. 修改index.html
    (可选) 为vite.config.ts添加server选项
    """
    context = Context(_args.projPath)
    async with Loop() as loop:
        executor("pnpm i --save-dev vite-plugin-mock@latest", cwd=context.projRoot)
        executor("pnpm i --save-dev sass@latest", cwd=context.projRoot)

        loop.addTask(delete, await context.root(".vscode"))  # 删除.vscode文件夹
        loop.addTask(delete, await context.root("README.md"))  # 删除README.md文件
        loop.addTask(delete, await context.root("src/views"))  # 删除src中的views文件夹
        loop.addTask(delete, await context.root("src/assets/base.css"))  # 删除src/assets中的base.css文件
        loop.addTask(delete, await context.root("src/assets/main.css"))  # 删除src/assets中的main.css文件
        loop.addTask(modify, await context.root("src/main.ts"), mainTs)  # 修改src/main.ts
        loop.addTask(modify, await context.root("src/App.vue"), appVue)  # 清除App.vue中的多余内容
        loop.addTask(rename, await context.root("src/router/index.ts"), "router.ts")  # 更名router的index.ts为router.ts
        loop.addTask(modify, await context.root("src/router/router.ts"), routerTs)  # 修改router/router.ts的内容
        loop.addTask(delete, await context.root("src/components"), pattern="*.vue")  # 移除src/components的vue文件
        loop.addTask(delete, await context.root("src/components/icons"))  # 移除src/components/icons文件夹
        loop.addTask(rename, await context.root("src/stores/counter.ts"), "stores.ts")  # 更名stores中的counter.ts为stores.ts
        loop.addTask(modify, await context.root("src/stores/stores.ts"), storeTs)  # 修改stores/stores.ts内容
        loop.addTask(modify, await context.root("vite.config.ts"), viteConfigTs)  # 修改vite.config.ts内容
        loop.addTask(create, await context.root("src/mock"))  # 新建文件夹src/mock

        async def mockCallback():
            await gather(
                create(await context.root("src/mock/mock.ts"), mockTs),   # 新建文件src/mock/mock.ts
                create(await context.root("src/mock/api.ts"), apiTs)   # 新建文件src/mock/api.ts
            )
        await loop._loop.create_task(mockCallback())
        loop.addTask(modify, await context.root("tsconfig.json"), tsconfigJson)  # 修改tsconfig.json
        loop.addTask(modify, await context.root("index.html"), indexHtml(context.projName))  # 修改index.html

        def hasPrettier():
            return path.exists(path.join(context.projRoot, ".prettierrc.json"))

        loop.addTask(modify, await context.root(".prettierrc.json"), prettierCfg, condition=hasPrettier)


def parseArgs():
    parser = ArgumentParser(description="初始化Vue项目")
    parser.add_argument("-p", dest="projPath", type=str, help="项目路径", default=getcwd())
    return parser.parse_args()


if __name__ == '__main__':
    args = parseArgs()
    run(main(args))
    pass
