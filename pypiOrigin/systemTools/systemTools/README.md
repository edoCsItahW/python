![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAzMCAzMCI+PHBhdGggc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLW1pdGVybGltaXQ9IjEwIiBzdHJva2Utd2lkdGg9IjIiIGQ9Ik00IDdoMjJNNCAxNWgyMk00IDIzaDIyIj48L3BhdGg+PC9zdmc+)

<div>

## API Documentation

-   [FileTree](#FileTree){.function}
-   [PYI_spawnTools](#PYI_spawnTools){.class}
    -   [PYI_spawnTools](#PYI_spawnTools.__init__){.function}
    -   [content](#PYI_spawnTools.content){.variable}
    -   [funcOfClass](#PYI_spawnTools.funcOfClass){.variable}
    -   [findImport](#PYI_spawnTools.findImport){.function}
    -   [rmMagicV](#PYI_spawnTools.rmMagicV){.variable}
    -   [getAllFunc](#PYI_spawnTools.getAllFunc){.function}
    -   [toPYI](#PYI_spawnTools.toPYI){.function}
-   [clearfolder](#clearfolder){.function}
-   [fullpath](#fullpath){.function}
-   [get_function_docs_in_file](#get_function_docs_in_file){.function}
-   [localattr](#localattr){.function}
-   [runInCMD](#runInCMD){.function}
-   [to_EXE](#to_EXE){.function}
-   [updateAllPackage](#updateAllPackage){.function}
-   [varname](#varname){.function}
-   [CMDError](#CMDError){.class}
    -   [CMDError](#CMDError.__init__){.function}
    -   [args](#CMDError.args){.variable}
-   [instruct](#instruct){.class}
    -   [instruct](#instruct.__init__){.function}

[built with [pdoc]{.visually-hidden}![pdoc
logo](data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20role%3D%22img%22%20aria-label%3D%22pdoc%20logo%22%20width%3D%22300%22%20height%3D%22150%22%20viewBox%3D%22-1%200%2060%2030%22%3E%3Ctitle%3Epdoc%3C/title%3E%3Cpath%20d%3D%22M29.621%2021.293c-.011-.273-.214-.475-.511-.481a.5.5%200%200%200-.489.503l-.044%201.393c-.097.551-.695%201.215-1.566%201.704-.577.428-1.306.486-2.193.182-1.426-.617-2.467-1.654-3.304-2.487l-.173-.172a3.43%203.43%200%200%200-.365-.306.49.49%200%200%200-.286-.196c-1.718-1.06-4.931-1.47-7.353.191l-.219.15c-1.707%201.187-3.413%202.131-4.328%201.03-.02-.027-.49-.685-.141-1.763.233-.721.546-2.408.772-4.076.042-.09.067-.187.046-.288.166-1.347.277-2.625.241-3.351%201.378-1.008%202.271-2.586%202.271-4.362%200-.976-.272-1.935-.788-2.774-.057-.094-.122-.18-.184-.268.033-.167.052-.339.052-.516%200-1.477-1.202-2.679-2.679-2.679-.791%200-1.496.352-1.987.9a6.3%206.3%200%200%200-1.001.029c-.492-.564-1.207-.929-2.012-.929-1.477%200-2.679%201.202-2.679%202.679A2.65%202.65%200%200%200%20.97%206.554c-.383.747-.595%201.572-.595%202.41%200%202.311%201.507%204.29%203.635%205.107-.037.699-.147%202.27-.423%203.294l-.137.461c-.622%202.042-2.515%208.257%201.727%2010.643%201.614.908%203.06%201.248%204.317%201.248%202.665%200%204.492-1.524%205.322-2.401%201.476-1.559%202.886-1.854%206.491.82%201.877%201.393%203.514%201.753%204.861%201.068%202.223-1.713%202.811-3.867%203.399-6.374.077-.846.056-1.469.054-1.537zm-4.835%204.313c-.054.305-.156.586-.242.629-.034-.007-.131-.022-.307-.157-.145-.111-.314-.478-.456-.908.221.121.432.25.675.355.115.039.219.051.33.081zm-2.251-1.238c-.05.33-.158.648-.252.694-.022.001-.125-.018-.307-.157-.217-.166-.488-.906-.639-1.573.358.344.754.693%201.198%201.036zm-3.887-2.337c-.006-.116-.018-.231-.041-.342.635.145%201.189.368%201.599.625.097.231.166.481.174.642-.03.049-.055.101-.067.158-.046.013-.128.026-.298.004-.278-.037-.901-.57-1.367-1.087zm-1.127-.497c.116.306.176.625.12.71-.019.014-.117.045-.345.016-.206-.027-.604-.332-.986-.695.41-.051.816-.056%201.211-.031zm-4.535%201.535c.209.22.379.47.358.598-.006.041-.088.138-.351.234-.144.055-.539-.063-.979-.259a11.66%2011.66%200%200%200%20.972-.573zm.983-.664c.359-.237.738-.418%201.126-.554.25.237.479.548.457.694-.006.042-.087.138-.351.235-.174.064-.694-.105-1.232-.375zm-3.381%201.794c-.022.145-.061.29-.149.401-.133.166-.358.248-.69.251h-.002c-.133%200-.306-.26-.45-.621.417.091.854.07%201.291-.031zm-2.066-8.077a4.78%204.78%200%200%201-.775-.584c.172-.115.505-.254.88-.378l-.105.962zm-.331%202.302a10.32%2010.32%200%200%201-.828-.502c.202-.143.576-.328.984-.49l-.156.992zm-.45%202.157l-.701-.403c.214-.115.536-.249.891-.376a11.57%2011.57%200%200%201-.19.779zm-.181%201.716c.064.398.194.702.298.893-.194-.051-.435-.162-.736-.398.061-.119.224-.3.438-.495zM8.87%204.141c0%20.152-.123.276-.276.276s-.275-.124-.275-.276.123-.276.276-.276.275.124.275.276zm-.735-.389a1.15%201.15%200%200%200-.314.783%201.16%201.16%200%200%200%201.162%201.162c.457%200%20.842-.27%201.032-.653.026.117.042.238.042.362a1.68%201.68%200%200%201-1.679%201.679%201.68%201.68%200%200%201-1.679-1.679c0-.843.626-1.535%201.436-1.654zM5.059%205.406A1.68%201.68%200%200%201%203.38%207.085a1.68%201.68%200%200%201-1.679-1.679c0-.037.009-.072.011-.109.21.3.541.508.935.508a1.16%201.16%200%200%200%201.162-1.162%201.14%201.14%200%200%200-.474-.912c.015%200%20.03-.005.045-.005.926.001%201.679.754%201.679%201.68zM3.198%204.141c0%20.152-.123.276-.276.276s-.275-.124-.275-.276.123-.276.276-.276.275.124.275.276zM1.375%208.964c0-.52.103-1.035.288-1.52.466.394%201.06.64%201.717.64%201.144%200%202.116-.725%202.499-1.738.383%201.012%201.355%201.738%202.499%201.738.867%200%201.631-.421%202.121-1.062.307.605.478%201.267.478%201.942%200%202.486-2.153%204.51-4.801%204.51s-4.801-2.023-4.801-4.51zm24.342%2019.349c-.985.498-2.267.168-3.813-.979-3.073-2.281-5.453-3.199-7.813-.705-1.315%201.391-4.163%203.365-8.423.97-3.174-1.786-2.239-6.266-1.261-9.479l.146-.492c.276-1.02.395-2.457.444-3.268a6.11%206.11%200%200%200%201.18.115%206.01%206.01%200%200%200%202.536-.562l-.006.175c-.802.215-1.848.612-2.021%201.25-.079.295.021.601.274.837.219.203.415.364.598.501-.667.304-1.243.698-1.311%201.179-.02.144-.022.507.393.787.213.144.395.26.564.365-1.285.521-1.361.96-1.381%201.126-.018.142-.011.496.427.746l.854.489c-.473.389-.971.914-.999%201.429-.018.278.095.532.316.713.675.556%201.231.721%201.653.721.059%200%20.104-.014.158-.02.207.707.641%201.64%201.513%201.64h.013c.8-.008%201.236-.345%201.462-.626.173-.216.268-.457.325-.692.424.195.93.374%201.372.374.151%200%20.294-.021.423-.068.732-.27.944-.704.993-1.021.009-.061.003-.119.002-.179.266.086.538.147.789.147.15%200%20.294-.021.423-.069.542-.2.797-.489.914-.754.237.147.478.258.704.288.106.014.205.021.296.021.356%200%20.595-.101.767-.229.438.435%201.094.992%201.656%201.067.106.014.205.021.296.021a1.56%201.56%200%200%200%20.323-.035c.17.575.453%201.289.866%201.605.358.273.665.362.914.362a.99.99%200%200%200%20.421-.093%201.03%201.03%200%200%200%20.245-.164c.168.428.39.846.68%201.068.358.273.665.362.913.362a.99.99%200%200%200%20.421-.093c.317-.148.512-.448.639-.762.251.157.495.257.726.257.127%200%20.25-.024.37-.071.427-.17.706-.617.841-1.314.022-.015.047-.022.068-.038.067-.051.133-.104.196-.159-.443%201.486-1.107%202.761-2.086%203.257zM8.66%209.925a.5.5%200%201%200-1%200c0%20.653-.818%201.205-1.787%201.205s-1.787-.552-1.787-1.205a.5.5%200%201%200-1%200c0%201.216%201.25%202.205%202.787%202.205s2.787-.989%202.787-2.205zm4.4%2015.965l-.208.097c-2.661%201.258-4.708%201.436-6.086.527-1.542-1.017-1.88-3.19-1.844-4.198a.4.4%200%200%200-.385-.414c-.242-.029-.406.164-.414.385-.046%201.249.367%203.686%202.202%204.896.708.467%201.547.7%202.51.7%201.248%200%202.706-.392%204.362-1.174l.185-.086a.4.4%200%200%200%20.205-.527c-.089-.204-.326-.291-.527-.206zM9.547%202.292c.093.077.205.114.317.114a.5.5%200%200%200%20.318-.886L8.817.397a.5.5%200%200%200-.703.068.5.5%200%200%200%20.069.703l1.364%201.124zm-7.661-.065c.086%200%20.173-.022.253-.068l1.523-.893a.5.5%200%200%200-.506-.863l-1.523.892a.5.5%200%200%200-.179.685c.094.158.261.247.432.247z%22%20transform%3D%22matrix%28-1%200%200%201%2058%200%29%22%20fill%3D%22%233bb300%22/%3E%3Cpath%20d%3D%22M.3%2021.86V10.18q0-.46.02-.68.04-.22.18-.5.28-.54%201.34-.54%201.06%200%201.42.28.38.26.44.78.76-1.04%202.38-1.04%201.64%200%203.1%201.54%201.46%201.54%201.46%203.58%200%202.04-1.46%203.58-1.44%201.54-3.08%201.54-1.64%200-2.38-.92v4.04q0%20.46-.04.68-.02.22-.18.5-.14.3-.5.42-.36.12-.98.12-.62%200-1-.12-.36-.12-.52-.4-.14-.28-.18-.5-.02-.22-.02-.68zm3.96-9.42q-.46.54-.46%201.18%200%20.64.46%201.18.48.52%201.2.52.74%200%201.24-.52.52-.52.52-1.18%200-.66-.48-1.18-.48-.54-1.26-.54-.76%200-1.22.54zm14.741-8.36q.16-.3.54-.42.38-.12%201-.12.64%200%201.02.12.38.12.52.42.16.3.18.54.04.22.04.68v11.94q0%20.46-.04.7-.02.22-.18.5-.3.54-1.7.54-1.38%200-1.54-.98-.84.96-2.34.96-1.8%200-3.28-1.56-1.48-1.58-1.48-3.66%200-2.1%201.48-3.68%201.5-1.58%203.28-1.58%201.48%200%202.3%201v-4.2q0-.46.02-.68.04-.24.18-.52zm-3.24%2010.86q.52.54%201.26.54.74%200%201.22-.54.5-.54.5-1.18%200-.66-.48-1.22-.46-.56-1.26-.56-.8%200-1.28.56-.48.54-.48%201.2%200%20.66.52%201.2zm7.833-1.2q0-2.4%201.68-3.96%201.68-1.56%203.84-1.56%202.16%200%203.82%201.56%201.66%201.54%201.66%203.94%200%201.66-.86%202.96-.86%201.28-2.1%201.9-1.22.6-2.54.6-1.32%200-2.56-.64-1.24-.66-2.1-1.92-.84-1.28-.84-2.88zm4.18%201.44q.64.48%201.3.48.66%200%201.32-.5.66-.5.66-1.48%200-.98-.62-1.46-.62-.48-1.34-.48-.72%200-1.34.5-.62.5-.62%201.48%200%20.96.64%201.46zm11.412-1.44q0%20.84.56%201.32.56.46%201.18.46.64%200%201.18-.36.56-.38.9-.38.6%200%201.46%201.06.46.58.46%201.04%200%20.76-1.1%201.42-1.14.8-2.8.8-1.86%200-3.58-1.34-.82-.64-1.34-1.7-.52-1.08-.52-2.36%200-1.3.52-2.34.52-1.06%201.34-1.7%201.66-1.32%203.54-1.32.76%200%201.48.22.72.2%201.06.4l.32.2q.36.24.56.38.52.4.52.92%200%20.5-.42%201.14-.72%201.1-1.38%201.1-.38%200-1.08-.44-.36-.34-1.04-.34-.66%200-1.24.48-.58.48-.58%201.34z%22%20fill%3D%22green%22/%3E%3C/svg%3E)](https://pdoc.dev "pdoc: Python API documentation generator"){.attribution}

</div>

::: {.pdoc role="main"}
::: {.section .module-info}
# systemTools.systemTools {#systemtools.systemtools .modulename}

View Source

::: {.pdoc-code .codehilite}
      1#! /user/bin/python3
      2
      3#  Copyright (c) 2023-2024. All rights reserved.
      4#  This source code is licensed under the CC BY-NC-ND
      5#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
      6#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
      7#  purposes is prohibited without the author's permission. If you have any questions or require
      8#  permission, please contact the author: 2207150234@st.sziit.edu.cn
      9
     10# -------------------------<Lenovo>----------------------------
     11# 传建时间: 2023/10/20 22:48
     12# 当前项目名: Python
     13# 编码模式: utf-8
     14# 注释: 
     15# -------------------------<Lenovo>----------------------------
     16from subprocess import PIPE, Popen
     17from traceback import format_exc
     18from warnings import warn
     19from inspect import signature, getmembers, getmodule, stack, isfunction, getdoc, isclass
     20from typing import Literal, Callable, Annotated
     21from pandas import set_option, Series
     22from types import ModuleType
     23from copy import copy
     24from os import listdir, path, remove, rmdir, walk, PathLike
     25from re import findall, sub
     26
     27
     28__version__ = "0.0.9"
     29
     30
     31try:
     32    from ANSIdefine.ansiDefine import ansiManger
     33except Exception:
     34    from ansiDefine.ansiDefine import ansiManger
     35
     36__all__ = [
     37    "FileTree",
     38    "PYI_spawnTools",
     39    "clearfolder",
     40    "fullpath",
     41    "get_function_docs_in_file",
     42    "localattr",
     43    "runInCMD",
     44    "to_EXE",
     45    "updateAllPackage",
     46    "varname",
     47    "CMDError",
     48    "instruct"
     49]
     50
     51color = ansiManger()
     52
     53
     54def clearfolder(folder_path):
     55    """
     56    用于清空文件夹
     57
     58    :param folder_path: 文件夹路径
     59    :type folder_path: str
     60    :return: 操作执行函数不做返回
     61    :retype: None
     62    """
     63    # 遍历文件夹中的所有文件和子文件夹
     64    for filename in listdir(folder_path):
     65        file_path = path.join(folder_path, filename)
     66        # 判断是否为文件
     67        if path.isfile(file_path):
     68            # 删除文件
     69            remove(file_path)
     70        # 判断是否为文件夹
     71        elif path.isdir(file_path):
     72            # 递归清空子文件夹
     73            clearfolder(file_path)
     74            # 删除子文件夹
     75            rmdir(file_path)
     76
     77
     78def FileTree() -> None:
     79    """
     80    打印树状目录
     81    """
     82    inp = int(input('输入模式\n1.打印文件夹和文件\t2.打印文件夹\n:'))
     83    filepath = input('输入文件路径\n(1.默认):')
     84    filepath = 'E:\\数学' if filepath == '1' else filepath
     85
     86    # 定义计算文件夹大小的函数
     87    def get_folder_size(folder_path):
     88        total_size = 0
     89        for dirpath, dirnames, filenames in walk(folder_path):
     90            for f in filenames:
     91                fp = path.join(dirpath, f)
     92                try:
     93                    total_size += path.getsize(fp)
     94                except PermissionError:
     95                    print("Permission denied: ", fp)
     96        return total_size
     97
     98    if inp == 1:
     99
    100        def print_tree(dir_path: str, *, prefix: str = '', folder_level: int = 0) -> None:
    101            files = listdir(dir_path)
    102            folder_level += 1
    103            for i, file in enumerate(sorted(files)):
    104                path_ws = path.join(dir_path, file)
    105                if path.isdir(path_ws):
    106                    folder_size = get_folder_size(path_ws)
    107                    inside = f"{folder_size}Byte" if folder_size <= 1024 else \
    108                        f"{folder_size // 1024}KB" if 1024 < folder_size <= 1024 ** 2 else \
    109                            f"{folder_size // 1024 ** 2}MB" if 1024 ** 2 < folder_size <= 1024 ** 3 else \
    110                                f"{folder_size // 1024 ** 3}G"
    111                    folder_info = f'大小:{inside}({len(listdir(path_ws))}个文件)'
    112                    if i == len(files) - 1:
    113                        print(
    114                            prefix + '└── ' + f'\033[3{folder_level}m{file}\033[0m({folder_level}级文件夹)({folder_info})')
    115                        print_tree(path_ws, prefix=prefix + '    ', folder_level=folder_level)
    116                    else:
    117                        print(
    118                            prefix + '├── ' + f'\033[3{folder_level}m{file}\033[0m({folder_level}级文件夹)({folder_info})')
    119                        print_tree(path_ws, prefix=prefix + '│   ', folder_level=folder_level)
    120                else:
    121                    file_size = path.getsize(path_ws)
    122                    inside = f"{file_size}Byte" if file_size <= 1024 else \
    123                        f"{file_size // 1024}KB" if 1024 < file_size <= 1024 ** 2 else \
    124                            f"{file_size // 1024 ** 2}MB" if 1024 ** 2 < file_size <= 1024 ** 3 else \
    125                                f"{file_size // 1024 ** 3}G"
    126                    file = "".join(file.split(".")[:-1]) + "." + color.f_under_line(file.split(".")[-1],
    127                                                                                    _ANSI=color.b_wide)
    128                    if i == len(files) - 1:
    129                        print(prefix + '└── ' + f'\033[3{folder_level}m{file}\033[0m({inside})')
    130                    else:
    131                        print(prefix + '├── ' + f'\033[3{folder_level}m{file}\033[0m({inside})')
    132
    133        print_tree(filepath)
    134
    135    elif inp == 2:
    136
    137        def print_tree_nf(dir_path, *, prefix = '', folder_level = 0):
    138            files = listdir(dir_path)
    139            folder_level += 1
    140            for i, file in enumerate(sorted(files)):
    141                path_ws = path.join(dir_path, file)
    142
    143                if path.isdir(path_ws):
    144                    folder_size = get_folder_size(path_ws)
    145                    inside = f"{folder_size}Byte" if folder_size <= 1024 else \
    146                        f"{folder_size // 1024}KB" if 1024 < folder_size <= 1024 ** 2 else \
    147                            f"{folder_size // 1024 ** 2}MB" if 1024 ** 2 < folder_size <= 1024 ** 3 else \
    148                                f"{folder_size // 1024 ** 3}G"
    149                    folder_info = f'大小:{inside}({len(listdir(path_ws))}个文件)'
    150                    if i == len(files) - 1:
    151                        print(
    152                            prefix + '└── ' + f'\033[3{folder_level}m{file}\033[0m({folder_level}级文件夹)({folder_info})')
    153                        print_tree_nf(path_ws, prefix=prefix + '    ', folder_level=folder_level)
    154                    else:
    155                        print(
    156                            prefix + '├── ' + f'\033[3{folder_level}m{file}\033[0m({folder_level}级文件夹)({folder_info})')
    157                        print_tree_nf(path_ws, prefix=prefix + '│   ', folder_level=folder_level)
    158
    159        print_tree_nf(filepath)
    160
    161
    162def runInCMD(*args: str, allowRIGHT: bool = True, allowERROR: bool = True, returnR: bool = False, returnE: bool = False,
    163             mod: Literal["utf-8", "gbk", "latin-1"] = "gbk"):
    164    result = ""
    165    for arg in args:
    166        result = Popen(arg, shell=True, stdout=PIPE, stderr=PIPE)
    167
    168    right = result.stdout.read().decode(mod, errors='ignore') if allowRIGHT else None
    169    error = color.f_otherColor(f"提示符回溯:\n\t{result.stderr.read().decode('gbk', errors='ignore')}", r=247, g=84,
    170                               b=100) if allowERROR else None
    171
    172    if allowRIGHT or allowERROR:
    173        print(f"结果:\n{right}\n{error}")
    174
    175    if returnR and returnE:
    176        return right, error
    177    elif returnR:
    178        return right
    179    elif returnE:
    180        return error
    181
    182
    183def varname(variable: object):
    184    module = getmodule(stack()[1][0])
    185    # 找到在跨包级的命名空间里是class_name类的实例
    186    instances = [name for name, obj in getmembers(module) if obj is variable]
    187    return instances[0]
    188
    189
    190def localattr(func: Callable): return list(signature(func).parameters.keys())
    191
    192
    193def fullpath(dirpath: str): return [path.join(dirpath, filename) for filename in listdir(dirpath)]
    194
    195
    196def to_EXE(pyPath: str, mutliPath: list = None, figPath: list[tuple] = None, console: bool = True):
    197    """
    198    如果有多个文件相关联,那么在a的第一个数字中加入文件路径即可.
    199    有静态文件及配置文件则将元组(源路径, 打包后在包中的路径)填入datas数组中即可.
    200    如需关闭控制台在则设置console设置为False
    201    注意:如果该文件或多文件中的主文件运行后不执行任何交换,则不会正确的打包.
    202    pyinstaller --icon=path/to/icon.ico your_script.py
    203    """
    204    from conFunc import waiter
    205    from textTools import isChinese
    206    if any(isChinese(word) for word in pyPath):
    207        raise ValueError("不支持中文文件名")
    208    print("以下是仅是第一次信息,请等待第二次信息,打包过程可能较长.")
    209    res = runInCMD(f"pyi-makespec {pyPath}", returnR=True)
    210    filepath = findall(r"(?<=Wrote\s)[^.]*\.[^.]*", res)[0]
    211    with open(filepath, "r", encoding="utf-8") as file:
    212        text = file.read()
    213    text = text.replace(f"['{pyPath}']".replace("\\", r"\\"), str([pyPath] + mutliPath)) \
    214        if isinstance(mutliPath, list) else text
    215    text = text.replace("datas=[]", f"datas={str(figPath)}") if \
    216        isinstance(figPath, list) and all(isinstance(t, tuple) for t in figPath) else text
    217    text = text.replace("console=True", "console=False") if console is False else text
    218    with open(filepath, "w", encoding="utf-8") as file:
    219        file.write(text)
    220    if input(
    221            f"现在你可以手动运行代码:\n\t{color.f_yellow('pyinstaller')} {filepath}\n这样可以看到具体进程.\n\t需要继续吗(Y:继续,N:停止).").lower() == "y":
    222        print("以下是第二次信息,打包即将开始.")
    223        wait = waiter(20)
    224        wait.begin_wait()
    225        runInCMD(f"pyinstaller {filepath}")
    226        wait.end_wait()
    227    else:
    228        print("已停止.")
    229
    230
    231def updateAllPackage():
    232    packages = runInCMD("pip list", returnR=True)
    233    for package in (l := findall(r"(?<=\s)[a-zA-Z].*?(?=\s)", packages))[l.index("numba"):]:
    234        runInCMD(f"pip install --upgrade {package}")
    235
    236
    237def spawn_package__all__(packageName: Annotated[str, "like constantPackage.con_func"]):
    238    if packageName[-3:] == ".py" and ("\\" in packageName or "/" in packageName):
    239        packageName = ".".join(packageName[:-3].split("\\" if "\\" in packageName else "/"))
    240
    241    tools = PYI_spawnTools(packageName)
    242    content = tools.content
    243
    244    mode = __import__(packageName, fromlist=[""])
    245
    246    impList = sum([i.split(", ") for i in findall(r"(?<=import\s).*", content)], start=[])
    247
    248    # funclist = [_ for _ in dir(mode) if not _.startswith("__")]
    249    text = "__all__ = [\n"
    250
    251    for name, member in filter(lambda x: not x[0].endswith("__"), getmembers(mode)):
    252        if (p := getmodule(member)) is None:
    253            if name not in impList:
    254                text += f"    \"{name}\",\n"
    255        else:
    256            if p.__name__ == packageName:
    257                text += f"    \"{name}\",\n"
    258
    259    print(text[:-2] + "\n]")
    260
    261
    262def get_function_docs_in_file(modeName: str | ModuleType = None, *, otherMagic: bool = False) -> Series | list:
    263    """
    264    这是用来显示func_Define这个python文件里的所有函数和对应的简要提示的.
    265
    266    :param modeName: 模块名或.py文件名.
    267    :type modeName: str
    268    :keyword otherMagic: 是否运行结果中出现未显示定义的魔法变量,如: __str__, ...
    269    :type otherMagic: bool
    270    :return: 将包含函数和简要提示的Series.
    271    :rtype: Series
    272    """
    273    if isinstance(modeName, ModuleType):
    274        modeName = modeName.__name__
    275
    276    if not otherMagic:
    277        tools = PYI_spawnTools(modeName)
    278        logdict, _ = tools.rmMagicV
    279
    280    set_option("display.max_rows", None)
    281    set_option("display.max_columns", None)
    282
    283    # 过滤出所有函数并构造名称和文档字符串的字典
    284    functions_dict = {}
    285    try:
    286        for name, member in globals().items() if modeName is None else getmembers(
    287                mode := __import__(modeName, fromlist=[""])):
    288            if (isfunction(member) or isclass(member)) and getmodule(member).__name__ == modeName:
    289                docs = getdoc(member)  # 文档字符串
    290                # 将函数名称及其文档字符串添加到字典中
    291
    292                functions_dict[f"<{name}>" if isclass(member) else name] = docs.split("\n\n")[0] if docs else \
    293                    f"(这个{'函数' if isfunction(member) else '变量'}没有简要提示.)"
    294
    295                if isclass(member) and getmodule(member).__name__ == modeName:
    296
    297                    for n, m in filter(lambda x: hasattr(member, x[0]), getmembers(getattr(mode, member.__name__))):
    298
    299                        if not otherMagic and name in logdict and n in logdict[name]:
    300                            functions_dict[
    301                                f"{name}.{n}"] = f"(这个{'函数' if isfunction(m) else '变量'}没有简要提示.)" if (
    302                                                                                                                    docs := getdoc(
    303                                                                                                                        m)) is None else \
    304                            docs.split("\n\n")[0]
    305
    306                        if otherMagic:
    307                            functions_dict[
    308                                f"{name}.{n}"] = f"(这个{'函数' if isfunction(m) else '变量'}没有简要提示.)" if (
    309                                                                                                                    docs := getdoc(
    310                                                                                                                        m)) is None else \
    311                            docs.split("\n\n")[0]
    312
    313    except AttributeError:
    314        warn(format_exc(), SyntaxWarning)
    315
    316    return Series(functions_dict)
    317
    318
    319class PYI_spawnTools:
    320    """从.py文件中生成.pyi存根文件"""
    321
    322    def __init__(self, pyFileName: Annotated[str, "like constantPackage.con_func"] | ModuleType, *, autoFile: str = "",
    323                 test: bool = False):
    324        self._test = test
    325
    326        errorList = []
    327
    328        try:
    329            if pyFileName[-3:] == ".py" or "/" in pyFileName or "\\" in pyFileName:
    330                pyFileName = ".".join(pyFileName[:-3].split("/" if "/" in pyFileName else "\\"))
    331
    332            if self._test: print(f"初始文件名: {pyFileName}")
    333
    334            self.dirPath = path.join(autoFile, f"{pyFileName.split('.')[-1]}.pyi") if autoFile is not None else None
    335
    336            if self._test: print(f"目标pyi文件: {self.dirPath}")
    337
    338            self.mode = pyFileName if isinstance(pyFileName, ModuleType) else __import__(pyFileName, fromlist=[""])
    339
    340            if self._test: print(f"实际导入包: {self.mode}")
    341
    342            if self._test: print(f"类列表: {self._classList}")
    343
    344            self.__funcOfClass = {}
    345
    346            for cls in self._classList:
    347                try:
    348                    self.__funcOfClass.update([(cls, dir(getattr(self.mode, cls.split("(")[0])))])
    349                except Exception:
    350                    warn(format_exc(), SyntaxWarning)
    351
    352            # self.__funcOfClass = {cls: dir(getattr(self.mode, cls.split("(")[0])) for cls in self._classList}
    353
    354            if self._test: print(f"包中的类: {self.__funcOfClass}")
    355
    356        except Exception as e:
    357            errorList.append(e)
    358
    359        if errorList: raise ExceptionGroup("初始化错误组: ", errorList)
    360
    361    # 文件中的所有代码内容
    362    @property
    363    def content(self):
    364        with open(self.mode.__file__, "r", encoding="utf-8") as file:
    365            text = file.read()
    366
    367        pset = set()
    368        if "def" not in text:
    369
    370            plist = findall(r"(?<=from\s)(.*?)\simport\s(.*)\b", text)
    371
    372            for p in plist:
    373                pset.add(p[0])
    374
    375            pset.add(self.mode.__file__)
    376
    377            warn(
    378                f"\n文件<{self.mode.__file__}>也许不是源定义文件,你可能需要到以下文件中寻找:\n\t{pset}.")
    379
    380        return text
    381
    382    # 提取出的函数定义列表
    383    @property
    384    def _sentenceList(self):
    385        return [sub(r"/n\s*", " ", word) if "/n" in word else word for word in
    386                findall(r"def\s.*?:(?=/)", self.content.replace("\n", "/n"))]
    387
    388    # 提取出的所有类
    389    @property
    390    def _classList(self):
    391        return list(filter(lambda x: all([i not in x for i in ("{", ",", "}", "/", "\\", ":", "\"")]),
    392                           findall(r"(?<=class\s).*?(?=:)", self.content)))
    393
    394    # 键为类,值为类对应的方法的字典
    395    @property
    396    def funcOfClass(self):
    397        return self.__funcOfClass
    398
    399    @funcOfClass.setter
    400    def funcOfClass(self, value: dict | tuple[str, list]):
    401        if isinstance(value, dict):
    402            self.__funcOfClass = value
    403        elif isinstance(value, tuple):
    404            self.__funcOfClass[value[0]] = value[1]
    405
    406    def _checkSenList(self, sentencelist):
    407        # type: (list) -> tuple[dict, dict]
    408        """
    409        对语句列表进行检查,排除不正确的提取.
    410
    411        @param sentencelist: 语句列表.
    412        @type sentencelist: list
    413        @return: 对每个类的魔术方法的记录字典,以及出现问题的以索引值为键,修正后的列表为值的字典.
    414        @retype: tuple[dict, dict]
    415        """
    416        logdict = {cls: set() for cls in self._classList}
    417
    418        errordict = {}
    419
    420        for i, word in enumerate(sentencelist):
    421            funcName = findall(r"(?<=def\s)\w+?(?=\()", word)
    422
    423            if len(funcName) > 1:
    424                errordict.update([(i, funcName)])
    425            else:
    426                if funcName[0].endswith("__"):
    427                    for key in self._classList:
    428                        if funcName[0] in self.funcOfClass[key]:
    429                            logdict[key].add(funcName[0])
    430
    431        return logdict, errordict
    432
    433    def findImport(self):
    434        return findall(r"from\s.*?import\s.*\b", self.content)
    435
    436    @property
    437    def rmMagicV(self):
    438        senList = copy(self._sentenceList)
    439
    440        logdict, errordict = self._checkSenList(self._sentenceList)
    441
    442        for i in errordict.keys():
    443            senList = senList[:i] + [findall(fr"def\s{errordict[i][idx]}\(.*?\).*?:", w)[0] for idx, w in
    444                                     enumerate([f"def{i}" for i in senList[i].split("def") if i])] + senList[i + 1:]
    445
    446        funcDict = {findall(r"(?<=def\s)\w+?(?=\()", word)[0]: word for word in senList}
    447
    448        for key in self._classList:
    449            self.funcOfClass = (key, [i for i in self.funcOfClass[key] if not i.endswith("__") or i in logdict[key]])
    450
    451        return self.funcOfClass, funcDict
    452
    453    def getAllFunc(self):
    454        s = "\n"
    455
    456        self.funcOfClass, funcDict = self.rmMagicV
    457
    458        finddict = {}
    459
    460        for key in funcDict.keys():
    461            if any((clist := [(i if key in self.funcOfClass[i] else False) for i in self.funcOfClass.keys()])):
    462                finddict.update([(className, f"class {className}:")]) if (className := [i for i in clist if i][
    463                    0]) not in finddict.keys() else None
    464                finddict.update(
    465                    [(key, f"{'' if 'self' in funcDict[key] else f'    @staticmethod{s}'}    {funcDict[key]} ...")])
    466            else:
    467                finddict.update([(key, f"{funcDict[key]} ...")])
    468
    469        return finddict
    470
    471    def toPYI(self, filePath: str = None):
    472        if filePath is None:
    473            filePath = self.dirPath
    474        with open(filePath, "w", encoding="utf-8") as file:
    475            file.write("\n".join(self.findImport()) + "\n" + "\n".join(self.getAllFunc().values()))
    476
    477
    478def docToMd(filePath: str, Class: object) -> None:
    479    from netTools import translate_mutil
    480    """将一个模块中的__doc__转换为文档"""
    481    sy, r, l = "\n", "{", "}"
    482
    483    iters = list(filter(lambda x: not x.endswith("__"), dir(Class)))
    484
    485    with open(filePath, "w", encoding="utf-8") as file:
    486        file.write(f"# {Class.__name__}\n\n")
    487
    488        for title in iters:
    489            file.write(f"## [{title}](#{title}-{title})\n")
    490
    491        for attr in iters:
    492            file.write(
    493                f"\n方法名:\n#### {attr} {r}#{attr}{l}\n:\'{(doc := getattr(Class, attr).__doc__)}\': \n翻译:\'{doc if doc is None else translate_mutil(doc.replace(sy, ''))}\'\n\n")
    494            print(attr)
    495
    496
    497def outputInfo(info: str, *, color: Literal["red", "green", "blue", "yellow"] | str | bool = "green", flag: bool = True):
    498    if not flag: return
    499
    500    colorDict = {
    501        "red": '\033[41m',
    502        "green": '\033[42m',
    503        "yellow": '\033[43m',
    504        "blue": '\033[44m',
    505    }
    506
    507    if isinstance(color, str):
    508        print(f"{colorDict[color] if color in colorDict else color}{info}\033[0m")
    509
    510    elif isinstance(color, bool):
    511        print(f"{colorDict['green']}{info}\033[0m" if color else info)
    512
    513    else:
    514        raise TypeError(
    515            f"关键字参数`color`可以布尔值(bool), ANSI转义符(str)或颜色键,但你的输入'{type(color)}'")
    516
    517
    518class CMDError(Exception):
    519    def __init__(self, *args):
    520        self.args = args
    521
    522
    523class instruct:
    524    """
    525    命令行运行器
    526
    527    使用方法::
    528
    529        >>> ins = instruct(output=True, ignore=False, color=True)
    530        >>> ins("dir")
    531    """
    532    _instance = None
    533
    534    def __new__(cls, *args, **kwargs):
    535
    536        if not cls._instance:
    537            cls._instance = super().__new__(cls)
    538
    539        return cls._instance
    540
    541    def __init__(self, *, output: bool = True, ignore: bool = False, color: bool | Literal["red", "yellow", "green", "blue"] = True, eliminate: str = None):
    542        """
    543        命令行初始器
    544
    545        :keyword output: 是否运行输出结果.
    546        :type output: bool
    547        :keyword ignore: 是否将所有(原本将会抛出错误)错误(Error)降级为警告(Warning)以保证程序不中断.
    548        :type ignore: bool
    549        :keyword color: 档为布尔类型(bool)是决定输出是否带有ANSI色彩,为字符串(str)时决定输出什么颜色.
    550        :type color: bool
    551        :keyword eliminate: 是否排除某些会被误认为错误的无关紧要的警告,例如: '文件名、目录名或卷标语法不正确。'
    552        """
    553        self._flagOutput = output
    554        self._flagIgnore = ignore
    555        self._flagColor = color
    556        self._eleiminate = eliminate
    557
    558    def __call__(self, instruction: str, *, cwd: PathLike | str = None, output: bool = None, encoding: Literal["gbk", "utf-8"] = "gbk", note: str = ""):
    559        """
    560        执行器
    561
    562        :param instruction: 指令
    563        :type instruction: str
    564        :keyword cwd: 设定当前路径或执行路径
    565        :type cwd: str
    566        :keyword allowOUTPUT: 是否允许打印结果
    567        :type allowOUTPUT: bool
    568        :return: cmd执行结果
    569        :rtype: str
    570        """
    571
    572        correct, error = self._execute(instruction, cwd=cwd, encoding=encoding)
    573
    574        tempFunc = lambda x: x.replace("\n", "").replace("\r", "").replace(" ", "")
    575
    576        if self._flagIgnore:
    577
    578            if flag := (self._flagOutput if output is None else output):
    579
    580                outputInfo(f"{cwd if cwd else 'cmd'}>{instruction}", color="green" if self._flagColor else False,
    581                           flag=flag)
    582
    583                print(correct) if correct else None
    584
    585            if self._eleiminate is None or (tempFunc(error) != tempFunc(self._eleiminate)):
    586
    587                warn(
    588                    error + note, SyntaxWarning)
    589
    590            return correct
    591
    592        else:
    593
    594            if self._eleiminate is None or (tempFunc(error) != tempFunc(self._eleiminate)):
    595
    596                raise CMDError(error)
    597
    598            elif tempFunc(error) == tempFunc(self._eleiminate):
    599
    600                warn(
    601                    f"你忽略了错误'{self._eleiminate}',而且没有将错误降级为警告,这导致一个错误被忽略了,带来的后果是返回了None而不是你期望的结果!")
    602
    603    @staticmethod
    604    def _execute(instruction: str, *, cwd: PathLike | str = None, encoding: Literal["gbk", "utf-8"] = "gbk") -> tuple[str, str]:
    605        """
    606        执行器内核
    607
    608        :param instruction: 指令
    609        :type instruction: str
    610        :param cwd: 执行环境路径
    611        :type cwd: PathLike | str
    612        :param encoding: 编码.(防止命令行输出乱码)
    613        :type encoding: str
    614        :return: 一个字典,键'C'对应正确信息,键'E'对应错误消息
    615        :rtype: dict
    616        """
    617        try:
    618
    619            result = Popen(instruction, shell=True, stdout=PIPE, stderr=PIPE, cwd=cwd)
    620
    621            return tuple(getattr(result, i).read().decode(encoding, errors='ignore') for i in ["stdout", "stderr"])
    622
    623        except Exception as err:
    624
    625            err.add_note("命令行执行器内核运行错误")
    626
    627            raise err
    628
    629
    630if __name__ == '__main__':
    631    # executor = instruct(output=True, ignore=True)
    632    # print(executor("nslookup www.baidu.com"))
    633    pass
:::
:::

::: {#FileTree .section}
::: {.attr .function}
[def]{.def} [FileTree]{.name}[([) -\>
[None]{.kc}:]{.return-annotation}]{.signature .pdoc-code .condensed}
View Source
:::

[](#FileTree){.headerlink}

::: {.pdoc-code .codehilite}
     79def FileTree() -> None:
     80    """
     81    打印树状目录
     82    """
     83    inp = int(input('输入模式\n1.打印文件夹和文件\t2.打印文件夹\n:'))
     84    filepath = input('输入文件路径\n(1.默认):')
     85    filepath = 'E:\\数学' if filepath == '1' else filepath
     86
     87    # 定义计算文件夹大小的函数
     88    def get_folder_size(folder_path):
     89        total_size = 0
     90        for dirpath, dirnames, filenames in walk(folder_path):
     91            for f in filenames:
     92                fp = path.join(dirpath, f)
     93                try:
     94                    total_size += path.getsize(fp)
     95                except PermissionError:
     96                    print("Permission denied: ", fp)
     97        return total_size
     98
     99    if inp == 1:
    100
    101        def print_tree(dir_path: str, *, prefix: str = '', folder_level: int = 0) -> None:
    102            files = listdir(dir_path)
    103            folder_level += 1
    104            for i, file in enumerate(sorted(files)):
    105                path_ws = path.join(dir_path, file)
    106                if path.isdir(path_ws):
    107                    folder_size = get_folder_size(path_ws)
    108                    inside = f"{folder_size}Byte" if folder_size <= 1024 else \
    109                        f"{folder_size // 1024}KB" if 1024 < folder_size <= 1024 ** 2 else \
    110                            f"{folder_size // 1024 ** 2}MB" if 1024 ** 2 < folder_size <= 1024 ** 3 else \
    111                                f"{folder_size // 1024 ** 3}G"
    112                    folder_info = f'大小:{inside}({len(listdir(path_ws))}个文件)'
    113                    if i == len(files) - 1:
    114                        print(
    115                            prefix + '└── ' + f'\033[3{folder_level}m{file}\033[0m({folder_level}级文件夹)({folder_info})')
    116                        print_tree(path_ws, prefix=prefix + '    ', folder_level=folder_level)
    117                    else:
    118                        print(
    119                            prefix + '├── ' + f'\033[3{folder_level}m{file}\033[0m({folder_level}级文件夹)({folder_info})')
    120                        print_tree(path_ws, prefix=prefix + '│   ', folder_level=folder_level)
    121                else:
    122                    file_size = path.getsize(path_ws)
    123                    inside = f"{file_size}Byte" if file_size <= 1024 else \
    124                        f"{file_size // 1024}KB" if 1024 < file_size <= 1024 ** 2 else \
    125                            f"{file_size // 1024 ** 2}MB" if 1024 ** 2 < file_size <= 1024 ** 3 else \
    126                                f"{file_size // 1024 ** 3}G"
    127                    file = "".join(file.split(".")[:-1]) + "." + color.f_under_line(file.split(".")[-1],
    128                                                                                    _ANSI=color.b_wide)
    129                    if i == len(files) - 1:
    130                        print(prefix + '└── ' + f'\033[3{folder_level}m{file}\033[0m({inside})')
    131                    else:
    132                        print(prefix + '├── ' + f'\033[3{folder_level}m{file}\033[0m({inside})')
    133
    134        print_tree(filepath)
    135
    136    elif inp == 2:
    137
    138        def print_tree_nf(dir_path, *, prefix = '', folder_level = 0):
    139            files = listdir(dir_path)
    140            folder_level += 1
    141            for i, file in enumerate(sorted(files)):
    142                path_ws = path.join(dir_path, file)
    143
    144                if path.isdir(path_ws):
    145                    folder_size = get_folder_size(path_ws)
    146                    inside = f"{folder_size}Byte" if folder_size <= 1024 else \
    147                        f"{folder_size // 1024}KB" if 1024 < folder_size <= 1024 ** 2 else \
    148                            f"{folder_size // 1024 ** 2}MB" if 1024 ** 2 < folder_size <= 1024 ** 3 else \
    149                                f"{folder_size // 1024 ** 3}G"
    150                    folder_info = f'大小:{inside}({len(listdir(path_ws))}个文件)'
    151                    if i == len(files) - 1:
    152                        print(
    153                            prefix + '└── ' + f'\033[3{folder_level}m{file}\033[0m({folder_level}级文件夹)({folder_info})')
    154                        print_tree_nf(path_ws, prefix=prefix + '    ', folder_level=folder_level)
    155                    else:
    156                        print(
    157                            prefix + '├── ' + f'\033[3{folder_level}m{file}\033[0m({folder_level}级文件夹)({folder_info})')
    158                        print_tree_nf(path_ws, prefix=prefix + '│   ', folder_level=folder_level)
    159
    160        print_tree_nf(filepath)
:::

::: {.docstring}
打印树状目录
:::
:::

::: {#PYI_spawnTools .section}
::: {.attr .class}
[class]{.def} [PYI_spawnTools]{.name}: View Source
:::

[](#PYI_spawnTools){.headerlink}

::: {.pdoc-code .codehilite}
    320class PYI_spawnTools:
    321    """从.py文件中生成.pyi存根文件"""
    322
    323    def __init__(self, pyFileName: Annotated[str, "like constantPackage.con_func"] | ModuleType, *, autoFile: str = "",
    324                 test: bool = False):
    325        self._test = test
    326
    327        errorList = []
    328
    329        try:
    330            if pyFileName[-3:] == ".py" or "/" in pyFileName or "\\" in pyFileName:
    331                pyFileName = ".".join(pyFileName[:-3].split("/" if "/" in pyFileName else "\\"))
    332
    333            if self._test: print(f"初始文件名: {pyFileName}")
    334
    335            self.dirPath = path.join(autoFile, f"{pyFileName.split('.')[-1]}.pyi") if autoFile is not None else None
    336
    337            if self._test: print(f"目标pyi文件: {self.dirPath}")
    338
    339            self.mode = pyFileName if isinstance(pyFileName, ModuleType) else __import__(pyFileName, fromlist=[""])
    340
    341            if self._test: print(f"实际导入包: {self.mode}")
    342
    343            if self._test: print(f"类列表: {self._classList}")
    344
    345            self.__funcOfClass = {}
    346
    347            for cls in self._classList:
    348                try:
    349                    self.__funcOfClass.update([(cls, dir(getattr(self.mode, cls.split("(")[0])))])
    350                except Exception:
    351                    warn(format_exc(), SyntaxWarning)
    352
    353            # self.__funcOfClass = {cls: dir(getattr(self.mode, cls.split("(")[0])) for cls in self._classList}
    354
    355            if self._test: print(f"包中的类: {self.__funcOfClass}")
    356
    357        except Exception as e:
    358            errorList.append(e)
    359
    360        if errorList: raise ExceptionGroup("初始化错误组: ", errorList)
    361
    362    # 文件中的所有代码内容
    363    @property
    364    def content(self):
    365        with open(self.mode.__file__, "r", encoding="utf-8") as file:
    366            text = file.read()
    367
    368        pset = set()
    369        if "def" not in text:
    370
    371            plist = findall(r"(?<=from\s)(.*?)\simport\s(.*)\b", text)
    372
    373            for p in plist:
    374                pset.add(p[0])
    375
    376            pset.add(self.mode.__file__)
    377
    378            warn(
    379                f"\n文件<{self.mode.__file__}>也许不是源定义文件,你可能需要到以下文件中寻找:\n\t{pset}.")
    380
    381        return text
    382
    383    # 提取出的函数定义列表
    384    @property
    385    def _sentenceList(self):
    386        return [sub(r"/n\s*", " ", word) if "/n" in word else word for word in
    387                findall(r"def\s.*?:(?=/)", self.content.replace("\n", "/n"))]
    388
    389    # 提取出的所有类
    390    @property
    391    def _classList(self):
    392        return list(filter(lambda x: all([i not in x for i in ("{", ",", "}", "/", "\\", ":", "\"")]),
    393                           findall(r"(?<=class\s).*?(?=:)", self.content)))
    394
    395    # 键为类,值为类对应的方法的字典
    396    @property
    397    def funcOfClass(self):
    398        return self.__funcOfClass
    399
    400    @funcOfClass.setter
    401    def funcOfClass(self, value: dict | tuple[str, list]):
    402        if isinstance(value, dict):
    403            self.__funcOfClass = value
    404        elif isinstance(value, tuple):
    405            self.__funcOfClass[value[0]] = value[1]
    406
    407    def _checkSenList(self, sentencelist):
    408        # type: (list) -> tuple[dict, dict]
    409        """
    410        对语句列表进行检查,排除不正确的提取.
    411
    412        @param sentencelist: 语句列表.
    413        @type sentencelist: list
    414        @return: 对每个类的魔术方法的记录字典,以及出现问题的以索引值为键,修正后的列表为值的字典.
    415        @retype: tuple[dict, dict]
    416        """
    417        logdict = {cls: set() for cls in self._classList}
    418
    419        errordict = {}
    420
    421        for i, word in enumerate(sentencelist):
    422            funcName = findall(r"(?<=def\s)\w+?(?=\()", word)
    423
    424            if len(funcName) > 1:
    425                errordict.update([(i, funcName)])
    426            else:
    427                if funcName[0].endswith("__"):
    428                    for key in self._classList:
    429                        if funcName[0] in self.funcOfClass[key]:
    430                            logdict[key].add(funcName[0])
    431
    432        return logdict, errordict
    433
    434    def findImport(self):
    435        return findall(r"from\s.*?import\s.*\b", self.content)
    436
    437    @property
    438    def rmMagicV(self):
    439        senList = copy(self._sentenceList)
    440
    441        logdict, errordict = self._checkSenList(self._sentenceList)
    442
    443        for i in errordict.keys():
    444            senList = senList[:i] + [findall(fr"def\s{errordict[i][idx]}\(.*?\).*?:", w)[0] for idx, w in
    445                                     enumerate([f"def{i}" for i in senList[i].split("def") if i])] + senList[i + 1:]
    446
    447        funcDict = {findall(r"(?<=def\s)\w+?(?=\()", word)[0]: word for word in senList}
    448
    449        for key in self._classList:
    450            self.funcOfClass = (key, [i for i in self.funcOfClass[key] if not i.endswith("__") or i in logdict[key]])
    451
    452        return self.funcOfClass, funcDict
    453
    454    def getAllFunc(self):
    455        s = "\n"
    456
    457        self.funcOfClass, funcDict = self.rmMagicV
    458
    459        finddict = {}
    460
    461        for key in funcDict.keys():
    462            if any((clist := [(i if key in self.funcOfClass[i] else False) for i in self.funcOfClass.keys()])):
    463                finddict.update([(className, f"class {className}:")]) if (className := [i for i in clist if i][
    464                    0]) not in finddict.keys() else None
    465                finddict.update(
    466                    [(key, f"{'' if 'self' in funcDict[key] else f'    @staticmethod{s}'}    {funcDict[key]} ...")])
    467            else:
    468                finddict.update([(key, f"{funcDict[key]} ...")])
    469
    470        return finddict
    471
    472    def toPYI(self, filePath: str = None):
    473        if filePath is None:
    474            filePath = self.dirPath
    475        with open(filePath, "w", encoding="utf-8") as file:
    476            file.write("\n".join(self.findImport()) + "\n" + "\n".join(self.getAllFunc().values()))
:::

::: {.docstring}
从.py文件中生成.pyi存根文件
:::

::: {#PYI_spawnTools.__init__ .classattr}
::: {.attr .function}
[PYI_spawnTools]{.name}[([ [pyFileName]{.n}[:]{.p}
[Union]{.n}[\[]{.p}[Annotated]{.n}[\[]{.p}[str]{.nb}[,]{.p} [\'like
constantPackage.con_func\']{.s1}[\],]{.p}
[module]{.n}[\]]{.p},]{.param}[ [\*]{.o},]{.param}[
[autoFile]{.n}[:]{.p} [str]{.nb} [=]{.o} [\'\']{.s1},]{.param}[
[test]{.n}[:]{.p} [bool]{.nb} [=]{.o} [False]{.kc}]{.param})]{.signature
.pdoc-code .multiline} View Source
:::

[](#PYI_spawnTools.__init__){.headerlink}

::: {.pdoc-code .codehilite}
    323    def __init__(self, pyFileName: Annotated[str, "like constantPackage.con_func"] | ModuleType, *, autoFile: str = "",
    324                 test: bool = False):
    325        self._test = test
    326
    327        errorList = []
    328
    329        try:
    330            if pyFileName[-3:] == ".py" or "/" in pyFileName or "\\" in pyFileName:
    331                pyFileName = ".".join(pyFileName[:-3].split("/" if "/" in pyFileName else "\\"))
    332
    333            if self._test: print(f"初始文件名: {pyFileName}")
    334
    335            self.dirPath = path.join(autoFile, f"{pyFileName.split('.')[-1]}.pyi") if autoFile is not None else None
    336
    337            if self._test: print(f"目标pyi文件: {self.dirPath}")
    338
    339            self.mode = pyFileName if isinstance(pyFileName, ModuleType) else __import__(pyFileName, fromlist=[""])
    340
    341            if self._test: print(f"实际导入包: {self.mode}")
    342
    343            if self._test: print(f"类列表: {self._classList}")
    344
    345            self.__funcOfClass = {}
    346
    347            for cls in self._classList:
    348                try:
    349                    self.__funcOfClass.update([(cls, dir(getattr(self.mode, cls.split("(")[0])))])
    350                except Exception:
    351                    warn(format_exc(), SyntaxWarning)
    352
    353            # self.__funcOfClass = {cls: dir(getattr(self.mode, cls.split("(")[0])) for cls in self._classList}
    354
    355            if self._test: print(f"包中的类: {self.__funcOfClass}")
    356
    357        except Exception as e:
    358            errorList.append(e)
    359
    360        if errorList: raise ExceptionGroup("初始化错误组: ", errorList)
:::
:::

::: {#PYI_spawnTools.content .classattr}
::: {.attr .variable}
[content]{.name}
:::

[](#PYI_spawnTools.content){.headerlink}
:::

::: {#PYI_spawnTools.funcOfClass .classattr}
::: {.attr .variable}
[funcOfClass]{.name}
:::

[](#PYI_spawnTools.funcOfClass){.headerlink}
:::

::: {#PYI_spawnTools.findImport .classattr}
::: {.attr .function}
[def]{.def}
[findImport]{.name}[([[self]{.bp}]{.param}[):]{.return-annotation}]{.signature
.pdoc-code .condensed} View Source
:::

[](#PYI_spawnTools.findImport){.headerlink}

::: {.pdoc-code .codehilite}
    434    def findImport(self):
    435        return findall(r"from\s.*?import\s.*\b", self.content)
:::
:::

::: {#PYI_spawnTools.rmMagicV .classattr}
::: {.attr .variable}
[rmMagicV]{.name}
:::

[](#PYI_spawnTools.rmMagicV){.headerlink}
:::

::: {#PYI_spawnTools.getAllFunc .classattr}
::: {.attr .function}
[def]{.def}
[getAllFunc]{.name}[([[self]{.bp}]{.param}[):]{.return-annotation}]{.signature
.pdoc-code .condensed} View Source
:::

[](#PYI_spawnTools.getAllFunc){.headerlink}

::: {.pdoc-code .codehilite}
    454    def getAllFunc(self):
    455        s = "\n"
    456
    457        self.funcOfClass, funcDict = self.rmMagicV
    458
    459        finddict = {}
    460
    461        for key in funcDict.keys():
    462            if any((clist := [(i if key in self.funcOfClass[i] else False) for i in self.funcOfClass.keys()])):
    463                finddict.update([(className, f"class {className}:")]) if (className := [i for i in clist if i][
    464                    0]) not in finddict.keys() else None
    465                finddict.update(
    466                    [(key, f"{'' if 'self' in funcDict[key] else f'    @staticmethod{s}'}    {funcDict[key]} ...")])
    467            else:
    468                finddict.update([(key, f"{funcDict[key]} ...")])
    469
    470        return finddict
:::
:::

::: {#PYI_spawnTools.toPYI .classattr}
::: {.attr .function}
[def]{.def} [toPYI]{.name}[([[self]{.bp},
]{.param}[[filePath]{.n}[:]{.p} [str]{.nb} [=]{.o}
[None]{.kc}]{.param}[):]{.return-annotation}]{.signature .pdoc-code
.condensed} View Source
:::

[](#PYI_spawnTools.toPYI){.headerlink}

::: {.pdoc-code .codehilite}
    472    def toPYI(self, filePath: str = None):
    473        if filePath is None:
    474            filePath = self.dirPath
    475        with open(filePath, "w", encoding="utf-8") as file:
    476            file.write("\n".join(self.findImport()) + "\n" + "\n".join(self.getAllFunc().values()))
:::
:::
:::

::: {#clearfolder .section}
::: {.attr .function}
[def]{.def}
[clearfolder]{.name}[([[folder_path]{.n}]{.param}[):]{.return-annotation}]{.signature
.pdoc-code .condensed} View Source
:::

[](#clearfolder){.headerlink}

::: {.pdoc-code .codehilite}
    55def clearfolder(folder_path):
    56    """
    57    用于清空文件夹
    58
    59    :param folder_path: 文件夹路径
    60    :type folder_path: str
    61    :return: 操作执行函数不做返回
    62    :retype: None
    63    """
    64    # 遍历文件夹中的所有文件和子文件夹
    65    for filename in listdir(folder_path):
    66        file_path = path.join(folder_path, filename)
    67        # 判断是否为文件
    68        if path.isfile(file_path):
    69            # 删除文件
    70            remove(file_path)
    71        # 判断是否为文件夹
    72        elif path.isdir(file_path):
    73            # 递归清空子文件夹
    74            clearfolder(file_path)
    75            # 删除子文件夹
    76            rmdir(file_path)
:::

::: {.docstring}
用于清空文件夹

:param folder_path: 文件夹路径 :type folder_path: str :return:
操作执行函数不做返回 :retype: None
:::
:::

::: {#fullpath .section}
::: {.attr .function}
[def]{.def} [fullpath]{.name}[([[dirpath]{.n}[:]{.p}
[str]{.nb}]{.param}[):]{.return-annotation}]{.signature .pdoc-code
.condensed} View Source
:::

[](#fullpath){.headerlink}

::: {.pdoc-code .codehilite}
    194def fullpath(dirpath: str): return [path.join(dirpath, filename) for filename in listdir(dirpath)]
:::
:::

::: {#get_function_docs_in_file .section}
::: {.attr .function}
[def]{.def} [get_function_docs_in_file]{.name}[([ [modeName]{.n}[:]{.p}
[str]{.nb} [\|]{.o} [module]{.n} [=]{.o} [None]{.kc},]{.param}[
[\*]{.o},]{.param}[ [otherMagic]{.n}[:]{.p} [bool]{.nb} [=]{.o}
[False]{.kc}]{.param}[) -\>
[pandas]{.n}[.]{.o}[core]{.n}[.]{.o}[series]{.n}[.]{.o}[Series]{.n}
[\|]{.o} [list]{.nb}:]{.return-annotation}]{.signature .pdoc-code
.multiline} View Source
:::

[](#get_function_docs_in_file){.headerlink}

::: {.pdoc-code .codehilite}
    263def get_function_docs_in_file(modeName: str | ModuleType = None, *, otherMagic: bool = False) -> Series | list:
    264    """
    265    这是用来显示func_Define这个python文件里的所有函数和对应的简要提示的.
    266
    267    :param modeName: 模块名或.py文件名.
    268    :type modeName: str
    269    :keyword otherMagic: 是否运行结果中出现未显示定义的魔法变量,如: __str__, ...
    270    :type otherMagic: bool
    271    :return: 将包含函数和简要提示的Series.
    272    :rtype: Series
    273    """
    274    if isinstance(modeName, ModuleType):
    275        modeName = modeName.__name__
    276
    277    if not otherMagic:
    278        tools = PYI_spawnTools(modeName)
    279        logdict, _ = tools.rmMagicV
    280
    281    set_option("display.max_rows", None)
    282    set_option("display.max_columns", None)
    283
    284    # 过滤出所有函数并构造名称和文档字符串的字典
    285    functions_dict = {}
    286    try:
    287        for name, member in globals().items() if modeName is None else getmembers(
    288                mode := __import__(modeName, fromlist=[""])):
    289            if (isfunction(member) or isclass(member)) and getmodule(member).__name__ == modeName:
    290                docs = getdoc(member)  # 文档字符串
    291                # 将函数名称及其文档字符串添加到字典中
    292
    293                functions_dict[f"<{name}>" if isclass(member) else name] = docs.split("\n\n")[0] if docs else \
    294                    f"(这个{'函数' if isfunction(member) else '变量'}没有简要提示.)"
    295
    296                if isclass(member) and getmodule(member).__name__ == modeName:
    297
    298                    for n, m in filter(lambda x: hasattr(member, x[0]), getmembers(getattr(mode, member.__name__))):
    299
    300                        if not otherMagic and name in logdict and n in logdict[name]:
    301                            functions_dict[
    302                                f"{name}.{n}"] = f"(这个{'函数' if isfunction(m) else '变量'}没有简要提示.)" if (
    303                                                                                                                    docs := getdoc(
    304                                                                                                                        m)) is None else \
    305                            docs.split("\n\n")[0]
    306
    307                        if otherMagic:
    308                            functions_dict[
    309                                f"{name}.{n}"] = f"(这个{'函数' if isfunction(m) else '变量'}没有简要提示.)" if (
    310                                                                                                                    docs := getdoc(
    311                                                                                                                        m)) is None else \
    312                            docs.split("\n\n")[0]
    313
    314    except AttributeError:
    315        warn(format_exc(), SyntaxWarning)
    316
    317    return Series(functions_dict)
:::

::: {.docstring}
这是用来显示func_Define这个python文件里的所有函数和对应的简要提示的.

:param modeName: 模块名或.py文件名. :type modeName: str :keyword
otherMagic: 是否运行结果中出现未显示定义的魔法变量,如: \_\_str\_\_, \...
:type otherMagic: bool :return: 将包含函数和简要提示的Series. :rtype:
Series
:::
:::

::: {#localattr .section}
::: {.attr .function}
[def]{.def} [localattr]{.name}[([[func]{.n}[:]{.p}
[Callable]{.n}]{.param}[):]{.return-annotation}]{.signature .pdoc-code
.condensed} View Source
:::

[](#localattr){.headerlink}

::: {.pdoc-code .codehilite}
    191def localattr(func: Callable): return list(signature(func).parameters.keys())
:::
:::

::: {#runInCMD .section}
::: {.attr .function}
[def]{.def} [runInCMD]{.name}[([ [\*]{.o}[args]{.n}[:]{.p}
[str]{.nb},]{.param}[ [allowRIGHT]{.n}[:]{.p} [bool]{.nb} [=]{.o}
[True]{.kc},]{.param}[ [allowERROR]{.n}[:]{.p} [bool]{.nb} [=]{.o}
[True]{.kc},]{.param}[ [returnR]{.n}[:]{.p} [bool]{.nb} [=]{.o}
[False]{.kc},]{.param}[ [returnE]{.n}[:]{.p} [bool]{.nb} [=]{.o}
[False]{.kc},]{.param}[ [mod]{.n}[:]{.p}
[Literal]{.n}[\[]{.p}[\'utf-8\']{.s1}[,]{.p} [\'gbk\']{.s1}[,]{.p}
[\'latin-1\']{.s1}[\]]{.p} [=]{.o}
[\'gbk\']{.s1}]{.param}[):]{.return-annotation}]{.signature .pdoc-code
.multiline} View Source
:::

[](#runInCMD){.headerlink}

::: {.pdoc-code .codehilite}
    163def runInCMD(*args: str, allowRIGHT: bool = True, allowERROR: bool = True, returnR: bool = False, returnE: bool = False,
    164             mod: Literal["utf-8", "gbk", "latin-1"] = "gbk"):
    165    result = ""
    166    for arg in args:
    167        result = Popen(arg, shell=True, stdout=PIPE, stderr=PIPE)
    168
    169    right = result.stdout.read().decode(mod, errors='ignore') if allowRIGHT else None
    170    error = color.f_otherColor(f"提示符回溯:\n\t{result.stderr.read().decode('gbk', errors='ignore')}", r=247, g=84,
    171                               b=100) if allowERROR else None
    172
    173    if allowRIGHT or allowERROR:
    174        print(f"结果:\n{right}\n{error}")
    175
    176    if returnR and returnE:
    177        return right, error
    178    elif returnR:
    179        return right
    180    elif returnE:
    181        return error
:::
:::

::: {#to_EXE .section}
::: {.attr .function}
[def]{.def} [to_EXE]{.name}[([ [pyPath]{.n}[:]{.p} [str]{.nb},]{.param}[
[mutliPath]{.n}[:]{.p} [list]{.nb} [=]{.o} [None]{.kc},]{.param}[
[figPath]{.n}[:]{.p} [list]{.nb}[\[]{.p}[tuple]{.nb}[\]]{.p} [=]{.o}
[None]{.kc},]{.param}[ [console]{.n}[:]{.p} [bool]{.nb} [=]{.o}
[True]{.kc}]{.param}[):]{.return-annotation}]{.signature .pdoc-code
.multiline} View Source
:::

[](#to_EXE){.headerlink}

::: {.pdoc-code .codehilite}
    197def to_EXE(pyPath: str, mutliPath: list = None, figPath: list[tuple] = None, console: bool = True):
    198    """
    199    如果有多个文件相关联,那么在a的第一个数字中加入文件路径即可.
    200    有静态文件及配置文件则将元组(源路径, 打包后在包中的路径)填入datas数组中即可.
    201    如需关闭控制台在则设置console设置为False
    202    注意:如果该文件或多文件中的主文件运行后不执行任何交换,则不会正确的打包.
    203    pyinstaller --icon=path/to/icon.ico your_script.py
    204    """
    205    from conFunc import waiter
    206    from textTools import isChinese
    207    if any(isChinese(word) for word in pyPath):
    208        raise ValueError("不支持中文文件名")
    209    print("以下是仅是第一次信息,请等待第二次信息,打包过程可能较长.")
    210    res = runInCMD(f"pyi-makespec {pyPath}", returnR=True)
    211    filepath = findall(r"(?<=Wrote\s)[^.]*\.[^.]*", res)[0]
    212    with open(filepath, "r", encoding="utf-8") as file:
    213        text = file.read()
    214    text = text.replace(f"['{pyPath}']".replace("\\", r"\\"), str([pyPath] + mutliPath)) \
    215        if isinstance(mutliPath, list) else text
    216    text = text.replace("datas=[]", f"datas={str(figPath)}") if \
    217        isinstance(figPath, list) and all(isinstance(t, tuple) for t in figPath) else text
    218    text = text.replace("console=True", "console=False") if console is False else text
    219    with open(filepath, "w", encoding="utf-8") as file:
    220        file.write(text)
    221    if input(
    222            f"现在你可以手动运行代码:\n\t{color.f_yellow('pyinstaller')} {filepath}\n这样可以看到具体进程.\n\t需要继续吗(Y:继续,N:停止).").lower() == "y":
    223        print("以下是第二次信息,打包即将开始.")
    224        wait = waiter(20)
    225        wait.begin_wait()
    226        runInCMD(f"pyinstaller {filepath}")
    227        wait.end_wait()
    228    else:
    229        print("已停止.")
:::

::: {.docstring}
如果有多个文件相关联,那么在a的第一个数字中加入文件路径即可.
有静态文件及配置文件则将元组(源路径,
打包后在包中的路径)填入datas数组中即可.
如需关闭控制台在则设置console设置为False
注意:如果该文件或多文件中的主文件运行后不执行任何交换,则不会正确的打包.
pyinstaller \--icon=path/to/icon.ico your_script.py
:::
:::

::: {#updateAllPackage .section}
::: {.attr .function}
[def]{.def}
[updateAllPackage]{.name}[([):]{.return-annotation}]{.signature
.pdoc-code .condensed} View Source
:::

[](#updateAllPackage){.headerlink}

::: {.pdoc-code .codehilite}
    232def updateAllPackage():
    233    packages = runInCMD("pip list", returnR=True)
    234    for package in (l := findall(r"(?<=\s)[a-zA-Z].*?(?=\s)", packages))[l.index("numba"):]:
    235        runInCMD(f"pip install --upgrade {package}")
:::
:::

::: {#varname .section}
::: {.attr .function}
[def]{.def} [varname]{.name}[([[variable]{.n}[:]{.p}
[object]{.nb}]{.param}[):]{.return-annotation}]{.signature .pdoc-code
.condensed} View Source
:::

[](#varname){.headerlink}

::: {.pdoc-code .codehilite}
    184def varname(variable: object):
    185    module = getmodule(stack()[1][0])
    186    # 找到在跨包级的命名空间里是class_name类的实例
    187    instances = [name for name, obj in getmembers(module) if obj is variable]
    188    return instances[0]
:::
:::

::: {#CMDError .section}
::: {.attr .class}
[class]{.def} [CMDError]{.name}([builtins.Exception]{.base}): View
Source
:::

[](#CMDError){.headerlink}

::: {.pdoc-code .codehilite}
    519class CMDError(Exception):
    520    def __init__(self, *args):
    521        self.args = args
:::

::: {.docstring}
Common base class for all non-exit exceptions.
:::

::: {#CMDError.__init__ .classattr}
::: {.attr .function}
[CMDError]{.name}[([[\*]{.o}[args]{.n}]{.param})]{.signature .pdoc-code
.condensed} View Source
:::

[](#CMDError.__init__){.headerlink}

::: {.pdoc-code .codehilite}
    520    def __init__(self, *args):
    521        self.args = args
:::
:::

::: {#CMDError.args .classattr}
::: {.attr .variable}
[args]{.name}
:::

[](#CMDError.args){.headerlink}
:::

::: {.inherited}
##### Inherited Members

builtins.BaseException
:   with_traceback
:   add_note
:::
:::

::: {#instruct .section}
::: {.attr .class}
[class]{.def} [instruct]{.name}: View Source
:::

[](#instruct){.headerlink}

::: {.pdoc-code .codehilite}
    524class instruct:
    525    """
    526    命令行运行器
    527
    528    使用方法::
    529
    530        >>> ins = instruct(output=True, ignore=False, color=True)
    531        >>> ins("dir")
    532    """
    533    _instance = None
    534
    535    def __new__(cls, *args, **kwargs):
    536
    537        if not cls._instance:
    538            cls._instance = super().__new__(cls)
    539
    540        return cls._instance
    541
    542    def __init__(self, *, output: bool = True, ignore: bool = False, color: bool | Literal["red", "yellow", "green", "blue"] = True, eliminate: str = None):
    543        """
    544        命令行初始器
    545
    546        :keyword output: 是否运行输出结果.
    547        :type output: bool
    548        :keyword ignore: 是否将所有(原本将会抛出错误)错误(Error)降级为警告(Warning)以保证程序不中断.
    549        :type ignore: bool
    550        :keyword color: 档为布尔类型(bool)是决定输出是否带有ANSI色彩,为字符串(str)时决定输出什么颜色.
    551        :type color: bool
    552        :keyword eliminate: 是否排除某些会被误认为错误的无关紧要的警告,例如: '文件名、目录名或卷标语法不正确。'
    553        """
    554        self._flagOutput = output
    555        self._flagIgnore = ignore
    556        self._flagColor = color
    557        self._eleiminate = eliminate
    558
    559    def __call__(self, instruction: str, *, cwd: PathLike | str = None, output: bool = None, encoding: Literal["gbk", "utf-8"] = "gbk", note: str = ""):
    560        """
    561        执行器
    562
    563        :param instruction: 指令
    564        :type instruction: str
    565        :keyword cwd: 设定当前路径或执行路径
    566        :type cwd: str
    567        :keyword allowOUTPUT: 是否允许打印结果
    568        :type allowOUTPUT: bool
    569        :return: cmd执行结果
    570        :rtype: str
    571        """
    572
    573        correct, error = self._execute(instruction, cwd=cwd, encoding=encoding)
    574
    575        tempFunc = lambda x: x.replace("\n", "").replace("\r", "").replace(" ", "")
    576
    577        if self._flagIgnore:
    578
    579            if flag := (self._flagOutput if output is None else output):
    580
    581                outputInfo(f"{cwd if cwd else 'cmd'}>{instruction}", color="green" if self._flagColor else False,
    582                           flag=flag)
    583
    584                print(correct) if correct else None
    585
    586            if self._eleiminate is None or (tempFunc(error) != tempFunc(self._eleiminate)):
    587
    588                warn(
    589                    error + note, SyntaxWarning)
    590
    591            return correct
    592
    593        else:
    594
    595            if self._eleiminate is None or (tempFunc(error) != tempFunc(self._eleiminate)):
    596
    597                raise CMDError(error)
    598
    599            elif tempFunc(error) == tempFunc(self._eleiminate):
    600
    601                warn(
    602                    f"你忽略了错误'{self._eleiminate}',而且没有将错误降级为警告,这导致一个错误被忽略了,带来的后果是返回了None而不是你期望的结果!")
    603
    604    @staticmethod
    605    def _execute(instruction: str, *, cwd: PathLike | str = None, encoding: Literal["gbk", "utf-8"] = "gbk") -> tuple[str, str]:
    606        """
    607        执行器内核
    608
    609        :param instruction: 指令
    610        :type instruction: str
    611        :param cwd: 执行环境路径
    612        :type cwd: PathLike | str
    613        :param encoding: 编码.(防止命令行输出乱码)
    614        :type encoding: str
    615        :return: 一个字典,键'C'对应正确信息,键'E'对应错误消息
    616        :rtype: dict
    617        """
    618        try:
    619
    620            result = Popen(instruction, shell=True, stdout=PIPE, stderr=PIPE, cwd=cwd)
    621
    622            return tuple(getattr(result, i).read().decode(encoding, errors='ignore') for i in ["stdout", "stderr"])
    623
    624        except Exception as err:
    625
    626            err.add_note("命令行执行器内核运行错误")
    627
    628            raise err
:::

::: {.docstring}
命令行运行器

使用方法::

    >>> ins = instruct(output=True, ignore=False, color=True)
    >>> ins("dir")
:::

::: {#instruct.__init__ .classattr}
::: {.attr .function}
[instruct]{.name}[([ [\*]{.o},]{.param}[ [output]{.n}[:]{.p} [bool]{.nb}
[=]{.o} [True]{.kc},]{.param}[ [ignore]{.n}[:]{.p} [bool]{.nb} [=]{.o}
[False]{.kc},]{.param}[ [color]{.n}[:]{.p}
[Union]{.n}[\[]{.p}[bool]{.nb}[,]{.p}
[Literal]{.n}[\[]{.p}[\'red\']{.s1}[,]{.p} [\'yellow\']{.s1}[,]{.p}
[\'green\']{.s1}[,]{.p} [\'blue\']{.s1}[\]\]]{.p} [=]{.o}
[True]{.kc},]{.param}[ [eliminate]{.n}[:]{.p} [str]{.nb} [=]{.o}
[None]{.kc}]{.param})]{.signature .pdoc-code .multiline} View Source
:::

[](#instruct.__init__){.headerlink}

::: {.pdoc-code .codehilite}
    542    def __init__(self, *, output: bool = True, ignore: bool = False, color: bool | Literal["red", "yellow", "green", "blue"] = True, eliminate: str = None):
    543        """
    544        命令行初始器
    545
    546        :keyword output: 是否运行输出结果.
    547        :type output: bool
    548        :keyword ignore: 是否将所有(原本将会抛出错误)错误(Error)降级为警告(Warning)以保证程序不中断.
    549        :type ignore: bool
    550        :keyword color: 档为布尔类型(bool)是决定输出是否带有ANSI色彩,为字符串(str)时决定输出什么颜色.
    551        :type color: bool
    552        :keyword eliminate: 是否排除某些会被误认为错误的无关紧要的警告,例如: '文件名、目录名或卷标语法不正确。'
    553        """
    554        self._flagOutput = output
    555        self._flagIgnore = ignore
    556        self._flagColor = color
    557        self._eleiminate = eliminate
:::

::: {.docstring}
命令行初始器

:keyword output: 是否运行输出结果. :type output: bool :keyword ignore:
是否将所有(原本将会抛出错误)错误(Error)降级为警告(Warning)以保证程序不中断.
:type ignore: bool :keyword color:
档为布尔类型(bool)是决定输出是否带有ANSI色彩,为字符串(str)时决定输出什么颜色.
:type color: bool :keyword eliminate:
是否排除某些会被误认为错误的无关紧要的警告,例如:
\'文件名、目录名或卷标语法不正确。\'
:::
:::
:::
:::
