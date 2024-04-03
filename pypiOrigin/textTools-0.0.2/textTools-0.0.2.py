#! /user/bin/python3

#  Copyright (c) 2023-2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/10/20 22:11
# 当前项目名: Python
# 编码模式: utf-8
# 注释:
# -------------------------<Lenovo>----------------------------
"""
定义文字处理功能的模块.
"""
from functools import reduce
from warnings import warn
from tkinter import Label, W, TOP, X, Frame, Entry, StringVar, Radiobutton, LEFT, Text, BOTH, Listbox, IntVar, \
    Checkbutton, END, TclError, Tk
from typing import Annotated, Literal
from math import floor, ceil
from os import listdir, path

import re

__all__ = [
    "DRAGON",
    "END",
    "FUNNY",
    "FUNNYDOG",
    "KEYBOARD",
    "NEVERBUG",
    "ReDemo",
    "WESDRAGON",
    "ZHIHU",
    "dirtoEN",
    "doForAllFile",
    "filetoEN",
    "getWidth",
    "isChinese",
    "issymbol",
    "repath",
    "retest",
    "toEnglish"
]

FUNNY = r"""
          .,,       .,:;;iiiiiiiii;;:,,.     .,,                   
           rGB##HS,.;iirrrrriiiiiiiiiirrrrri;,s&##MAS,                
          r5s;:r3AH5iiiii;;;;;;;;;;;;;;;;iiirXHGSsiih1,               
             .;i;;s91;;;;;;::::::::::::;;;;iS5;;;ii:                  
           :rsriii;;r::::::::::::::::::::::;;,;;iiirsi,               
        .,iri;;::::;;;;;;::,,,,,,,,,,,,,..,,;;;;;;;;iiri,,.           
     ,9BM&,            .,:;;:,,,,,,,,,,,hXA8:            ..,,,.       
    ,;&@@#r:;;;;;::::,,.   ,r,,,,,,,,,,iA@@@s,,:::;;;::,,.   .;.      
     :ih1iii;;;;;::::;;;;;;;:,,,,,,,,,,;i55r;;;;;;;;;iiirrrr,..       
    .ir;;iiiiiiiiii;;;;::::::,,,,,,,:::::,,:;;;iiiiiiiiiiiiri         
    iriiiiiiiiiiiiiiii;;;::::::::::::::::;;;iiiiiiiiiiiiiiiir;        
   ,riii;;;;;;;;;;;;;:::::::::::::::::::::::;;;;;;;;;;;;;;iiir.       
   iri;;;::::,,,,,,,,,,:::::::::::::::::::::::::,::,,::::;;iir:       
  .rii;;::::,,,,,,,,,,,,:::::::::::::::::,,,,,,,,,,,,,::::;;iri       
  ,rii;;;::,,,,,,,,,,,,,:::::::::::,:::::,,,,,,,,,,,,,:::;;;iir.      
  ,rii;;i::,,,,,,,,,,,,,:::::::::::::::::,,,,,,,,,,,,,,::i;;iir.      
  ,rii;;r::,,,,,,,,,,,,,:,:::::,:,:::::::,,,,,,,,,,,,,::;r;;iir.      
  .rii;;rr,:,,,,,,,,,,,,,,:::::::::::::::,,,,,,,,,,,,,:,si;;iri       
   ;rii;:1i,,,,,,,,,,,,,,,,,,:::::::::,,,,,,,,,,,,,,,:,ss:;iir:       
   .rii;;;5r,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,sh:;;iri        
    ;rii;:;51,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.:hh:;;iir,        
     irii;::hSr,.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.,sSs:;;iir:         
      irii;;:iSSs:.,,,,,,,,,,,,,,,,,,,,,,,,,,,..:135;:;;iir:          
       ;rii;;:,r535r:...,,,,,,,,,,,,,,,,,,..,;sS35i,;;iirr:           
        :rrii;;:,;1S3Shs;:,............,:is533Ss:,;;;iiri,            
         .;rrii;;;:,;rhS393S55hh11hh5S3393Shr:,:;;;iirr:              
           .;rriii;;;::,:;is1h555555h1si;:,::;;;iirri:.               
             .:irrrii;;;;;:::,,,,,,,,:::;;;;iiirrr;,                  
                .:irrrriiiiii;;;;;;;;iiiiiirrrr;,.                    
                   .,:;iirrrrrrrrrrrrrrrrri;:.                        
                         ..,:::;;;;:::,,.                              
"""

FUNNYDOG = r"""
           .,:,,,                                        .::,,,::.          
         .::::,,;;,                                  .,;;:,,....:i:         
         :i,.::::,;i:.      ....,,:::::::::,....   .;i:,.  ......;i.        
         :;..:::;::::i;,,:::;:,,,,,,,,,,..,.,,:::iri:. .,:irsr:,.;i.        
         ;;..,::::;;;;ri,,,.                    ..,,:;s1s1ssrr;,.;r,        
         :;. ,::;ii;:,     . ...................     .;iirri;;;,,;i,        
         ,i. .;ri:.   ... ............................  .,,:;:,,,;i:        
         :s,.;r:... ....................................... .::;::s;        
         ,1r::. .............,,,.,,:,,........................,;iir;        
         ,s;...........     ..::.,;:,,.          ...............,;1s        
        :i,..,.              .,:,,::,.          .......... .......;1,       
       ir,....:rrssr;:,       ,,.,::.     .r5S9989398G95hr;. ....,.:s,      
      ;r,..,s9855513XHAG3i   .,,,,,,,.  ,S931,.,,.;s;s&BHHA8s.,..,..:r:     
     :r;..rGGh,  :SAG;;G@BS:.,,,,,,,,,.r83:      hHH1sXMBHHHM3..,,,,.ir.    
    ,si,.1GS,   sBMAAX&MBMB5,,,,,,:,,.:&8       3@HXHBMBHBBH#X,.,,,,,,rr    
    ;1:,,SH:   .A@&&B#&8H#BS,,,,,,,,,.,5XS,     3@MHABM&59M#As..,,,,:,is,   
   .rr,,,;9&1   hBHHBB&8AMGr,,,,,,,,,,,:h&&9s;   r9&BMHBHMB9:  . .,,,,;ri.  
   :1:....:5&XSi;r8BMBHHA9r:,......,,,,:ii19GG88899XHHH&GSr.      ...,:rs.  
   ;s.     .:sS8G8GG889hi.        ....,,:;:,.:irssrriii:,.        ...,,i1,  
   ;1,         ..,....,,isssi;,        .,,.                      ....,.i1,  
   ;h:               i9HHBMBBHAX9:         .                     ...,,,rs,  
   ,1i..            :A#MBBBBMHB##s                             ....,,,;si.  
   .r1,..        ,..;3BMBBBHBB#Bh.     ..                    ....,,,,,i1;   
    :h;..       .,..;,1XBMMMMBXs,.,, .. :: ,.               ....,,,,,,ss.   
     ih: ..    .;;;, ;;:s58A3i,..    ,. ,.:,,.             ...,,,,,:,s1,    
     .s1,....   .,;sh,  ,iSAXs;.    ,.  ,,.i85            ...,,,,,,:i1;     
      .rh: ...     rXG9XBBM#M#MHAX3hss13&&HHXr         .....,,,,,,,ih;      
       .s5: .....    i598X&&A&AAAAAA&XG851r:       ........,,,,:,,sh;       
       . ihr, ...  .         ..                    ........,,,,,;11:.       
          ,s1i. ...  ..,,,..,,,.,,.,,.,..       ........,,.,,.;s5i.         
           .:s1r,......................       ..............;shs,           
           . .:shr:.  ....                 ..............,ishs.             
               .,issr;,... ...........................,is1s;.               
                  .,is1si;:,....................,:;ir1sr;,                  
                     ..:isssssrrii;::::::;;iirsssssr;:..                    
                          .,::iiirsssssssssrri;;:.   
"""

KEYBOARD = r"""
 ┌───┐   ┌───┬───┬───┬───┐ ┌───┬───┬───┬───┐ ┌───┬───┬───┬───┐ ┌───┬───┬───┐
 │Esc│   │ F1│ F2│ F3│ F4│ │ F5│ F6│ F7│ F8│ │ F9│F10│F11│F12│ │P/S│S L│P/B│  ┌┐    ┌┐    ┌┐
 └───┘   └───┴───┴───┴───┘ └───┴───┴───┴───┘ └───┴───┴───┴───┘ └───┴───┴───┘  └┘    └┘    └┘
 ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───────┐ ┌───┬───┬───┐ ┌───┬───┬───┬───┐
 │~ `│! 1│@ 2│# 3│$ 4│% 5│^ 6│& 7│* 8│( 9│) 0│_ -│+ =│ BacSp │ │Ins│Hom│PUp│ │N L│ / │ * │ - │
 ├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─────┤ ├───┼───┼───┤ ├───┼───┼───┼───┤
 │ Tab │ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │{ [│} ]│ | \ │ │Del│End│PDn│ │ 7 │ 8 │ 9 │   │
 ├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─────┤ └───┴───┴───┘ ├───┼───┼───┤ + │
 │ Caps │ A │ S │ D │ F │ G │ H │ J │ K │ L │: ;│" '│ Enter  │               │ 4 │ 5 │ 6 │   │
 ├──────┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴────────┤     ┌───┐     ├───┼───┼───┼───┤
 │ Shift  │ Z │ X │ C │ V │ B │ N │ M │< ,│> .│? /│  Shift   │     │ ↑ │     │ 1 │ 2 │ 3 │   │
 ├─────┬──┴─┬─┴──┬┴───┴───┴───┴───┴───┴──┬┴───┼───┴┬────┬────┤ ┌───┼───┼───┐ ├───┴───┼───┤ E││
 │ Ctrl│ Win│Alt │         Space         │ Alt│ Win│ Fn │Ctrl│ │ ← │ ↓ │ → │ │   0   │ . │←─┘│
 └─────┴────┴────┴───────────────────────┴────┴────┴────┴────┘ └───┴───┴───┘ └───────┴───┴───┘
"""

ZHIHU = r"""
          _____                    _____                    _____                    _____          
         /\    \                  /\    \                  /\    \                  /\    \         
        /::\____\                /::\    \                /::\    \                /::\    \        
       /:::/    /                \:::\    \              /::::\    \              /::::\    \       
      /:::/    /                  \:::\    \            /::::::\    \            /::::::\    \      
     /:::/    /                    \:::\    \          /:::/\:::\    \          /:::/\:::\    \     
    /:::/____/                      \:::\    \        /:::/__\:::\    \        /:::/__\:::\    \    
   /::::\    \                      /::::\    \      /::::\   \:::\    \      /::::\   \:::\    \   
  /::::::\    \   _____    ____    /::::::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \  
 /:::/\:::\    \ /\    \  /\   \  /:::/\:::\    \  /:::/\:::\   \:::\____\  /:::/\:::\   \:::\    \
/:::/  \:::\    /::\____\/::\   \/:::/  \:::\____\/:::/  \:::\   \:::|    |/:::/__\:::\   \:::\____\
\::/    \:::\  /:::/    /\:::\  /:::/    \::/    /\::/   |::::\  /:::|____|\:::\   \:::\   \::/    /
 \/____/ \:::\/:::/    /  \:::\/:::/    / \/____/  \/____|:::::\/:::/    /  \:::\   \:::\   \/____/
          \::::::/    /    \::::::/    /                 |:::::::::/    /    \:::\   \:::\    \     
           \::::/    /      \::::/____/                  |::|\::::/    /      \:::\   \:::\____\    
           /:::/    /        \:::\    \                  |::| \::/____/        \:::\   \::/    /    
          /:::/    /          \:::\    \                 |::|  ~|               \:::\   \/____/     
         /:::/    /            \:::\    \                |::|   |                \:::\    \         
        /:::/    /              \:::\____\               \::|   |                 \:::\____\        
        \::/    /                \::/    /                \:|   |                  \::/    /        
         \/____/                  \/____/                  \|___|                   \/____/         
"""

NEVERBUG = r"""
                           _ooOoo_
                          o8888888o
                          88" . "88
                          (| -_- |)
                          O\  =  /O
                       ____/`---'\____
                     .'  \\|     |//  `.
                    /  \\|||  :  |||//  \
                   /  _||||| -卍- |||||-  \
                   |   | \\\  -  /// |   |
                   | \_|  ''\---/''  |   |
                   \  .-\__  `-`  ___/-. /
                 ___`. .'  /--.--\  `. . __
              ."" '<  `.___\_<|>_/___.'  >'"".
             | | :  `- \`.;`\ _ /`;.`/ - ` : | |
             \  \ `-.   \_ __\ /__ _/   .-` /  /
        ======`-.____`-.___\_____/___.-`____.-'======
                           `=---='
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    佛祖保佑       永无BUG
        佛曰:
                  写字楼里写字间,写字间里程序员;
                  程序人员写程序,又拿程序换酒钱.
                  酒醒只在网上坐,酒醉还来网下眠;
                  酒醉酒醒日复日,网上网下年复年.
                  但愿老死电脑间,不愿鞠躬老板前;
                  奔驰宝马贵者趣,公交自行程序员.
                  别人笑我忒疯癫,我笑自己命太贱;
                  不见满街漂亮妹,哪个归得程序员?
"""

DRAGON = r"""
                                      00                         
                                    000                          
                                 0000                            
                               0000                              
                             000000                              
                           000000    000  000000000000000        
                  000000000000000000000000000000000              
                0   0000000000000000000000000000                 
                       000000000000000000000000000000000         
                   0000000000000000000000000000000               
                  000   00000000000000000000000000000            
               00000  00000000000  0000000000000000000           
              000000000000000 00    0000000000000  00000         
          000000000000000000   0     0000000000000   0000        
        0000000000000000000         000000000000000    000       
       00000000                     0000000000000000     00      
        00000                     000000000000000000             
          0                   00000000000000000000000            
                0000000000000000000000000000000000000            
                  0000000000000000000000000000  00000            
              000000000000000000000000000000    00000            
           00000000000000000000000000000000      0000            
         0000000000000000000000000000000         0000            
       0000000000000000000000000000000           0000            
      0000000000000000000   000000               000             
     0000000000000000                            00              
    000000000000000                 00                           
   000000000000000                     0000                      
   0000000000 000                        00000                   
  00000000000  00                          0000000               
  000000000000   0            000     0000   0000000             
  0000000000000                 000     00000000000000           
  0000000000000000              000000000000000000000000         
  00 00000000000000000         000000000000000000000000000       
   00  000000000000         0000000000000000   000000000000      
    0  0000000000000000000000000000000000           00000000     
       000000000000000000000000000000000              0000000    
       00000 000000000000000000  00000000   0          000000    
        000     0000000000000     0000000000           0  0000   
       000        000 000000000     00000                 0000   
       000               0000000       00000000            000   
        00                   000000                         000  
         0                     0000                        00    
                               000                       00      
                                00                      00       
                                 00                              
                                  0
"""

WESDRAGON = r"""
                                                   __----~~~~~~~~~~~------___
                                  .  .   ~~//====......          __--~ ~~
                  -.            \_|//     |||\\  ~~~~~~::::... /~
               ___-==_       _-~o~  \/    |||  \\            _/~~-
       __---~~~.==~||\=_    -_--~/_-~|-   |\\   \\        _/~
   _-~~     .=~    |  \\-_    '-~7  /-   /  ||    \      /
 .~       .~       |   \\ -_    /  /-   /   ||      \   /
/  ____  /         |     \\ ~-_/  /|- _/   .||       \ /
|~~    ~~|--~~~~--_ \     ~==-/   | \~--===~~        .\
         '         ~-|      /|    |-~\~~       __--~~
                     |-~~-_/ |    |   ~\_   _-~            /\
                          /  \     \__   \/~                \__
                      _--~ _/ | .-~~____--~-/                  ~~==.
                     ((->/~   '.|||' -_|    ~~-/ ,              . _||
                                -_     ~\      ~~---l__i__i__i--~~_/
                                _-~-__   ~)  \--______________--~~
                              //.-~~~-~_--~- |-------~~~~~~~~
                                     //.-~~~--\
"""


class ReDemo:
    """
    正则表达式的测试软件.(python官网实例)

    """
    def __init__(self, master):
        self.master = master

        self.promptdisplay = Label(self.master, anchor=W,
                                   text="输入Perl样式的正则表达式:")
        self.promptdisplay.pack(side=TOP, fill=X)

        self.regexdisplay = Entry(self.master)
        self.regexdisplay.pack(fill=X)
        self.regexdisplay.focus_set()

        self.addoptions()

        self.statusdisplay = Label(self.master, text="", anchor=W)
        self.statusdisplay.pack(side=TOP, fill=X)

        self.labeldisplay = Label(self.master, anchor=W,
                                  text="输入要搜索的文本:")
        self.labeldisplay.pack(fill=X)
        self.labeldisplay.pack(fill=X)

        self.showframe = Frame(master)
        self.showframe.pack(fill=X, anchor=W)

        self.showvar = StringVar(master)
        self.showvar.set("第一个")

        self.showfirstradio = Radiobutton(self.showframe,
                                          text="突出显示第一个匹配",
                                          variable=self.showvar,
                                          value="第一个",
                                          command=self.recompile)
        self.showfirstradio.pack(side=LEFT)

        self.showallradio = Radiobutton(self.showframe,
                                        text="突出显示所有匹配项",
                                        variable=self.showvar,
                                        value="所有",
                                        command=self.recompile)
        self.showallradio.pack(side=LEFT)

        self.stringdisplay = Text(self.master, width=60, height=4)
        self.stringdisplay.pack(fill=BOTH, expand=1)
        self.stringdisplay.tag_configure("hit", background="yellow")

        self.grouplabel = Label(self.master, text="组:", anchor=W)
        self.grouplabel.pack(fill=X)

        self.grouplist = Listbox(self.master)
        self.grouplist.pack(expand=1, fill=BOTH)

        self.regexdisplay.bind('<Key>', self.recompile)
        self.stringdisplay.bind('<Key>', self.reevaluate)

        self.compiled = None
        self.recompile()

        btags = self.regexdisplay.bindtags()
        self.regexdisplay.bindtags(btags[1:] + btags[:1])

        btags = self.stringdisplay.bindtags()
        self.stringdisplay.bindtags(btags[1:] + btags[:1])

    def addoptions(self):
        self.frames = []
        self.boxes = []
        self.vars = []
        for name in (
                dic := {'IGNORECASE': "忽略大小写", 'MULTILINE': "多行模式", 'DOTALL': "匹配所有",
                        'VERBOSE': "忽略空白"}):
            if len(self.boxes) % 3 == 0:
                frame = Frame(self.master)
                frame.pack(fill=X)
                self.frames.append(frame)
            val = getattr(re, name).value
            var = IntVar()
            box = Checkbutton(frame,
                              variable=var, text=dic[name],
                              offvalue=0, onvalue=val,
                              command=self.recompile)
            box.pack(side=LEFT)
            self.boxes.append(box)
            self.vars.append(var)

    def getflags(self):
        flags = 0
        for var in self.vars:
            flags |= var.get()
        return flags

    def recompile(self, event=None):
        try:
            self.compiled = re.compile(self.regexdisplay.get(),
                                       self.getflags())
            bg = self.promptdisplay['background']
            self.statusdisplay.config(text="", background=bg)
        except re.error as msg:
            self.compiled = None
            self.statusdisplay.config(
                text=f"re.error: {str(msg)}",
                background="red")
        self.reevaluate()

    def reevaluate(self, event=None):
        try:
            self.stringdisplay.tag_remove("hit", "1.0", END)
        except TclError:
            pass
        try:
            self.stringdisplay.tag_remove("hit0", "1.0", END)
        except TclError:
            pass
        self.grouplist.delete(0, END)
        if not self.compiled:
            return
        self.stringdisplay.tag_configure("hit", background="yellow")
        self.stringdisplay.tag_configure("hit0", background="orange")
        text = self.stringdisplay.get("1.0", END)
        last = 0
        nmatches = 0
        while last <= len(text):
            m = self.compiled.search(text, last)
            if m is None:
                break
            first, last = m.span()
            if last == first:
                last = first + 1
                tag = "hit0"
            else:
                tag = "hit"
            pfirst = f"1.0 + {first} chars"
            plast = f"1.0 + {last} chars"
            self.stringdisplay.tag_add(tag, pfirst, plast)
            if nmatches == 0:
                self.stringdisplay.yview_pickplace(pfirst)
                groups = list(m.groups())
                groups.insert(0, m.group())
                for i in range(len(groups)):
                    g = f"{i}: {groups[i]}"
                    self.grouplist.insert(END, g)
            nmatches += 1
            if self.showvar.get() == "第一个":
                break

        if nmatches == 0:
            self.statusdisplay.config(text="(没有目标)",
                                      background="yellow")
        else:
            self.statusdisplay.config(text="")


def retest():
    """re程序引擎(入口函数)"""
    root = Tk()
    demo = ReDemo(root)
    root.protocol('WM_DELETE_WINDOW', root.quit)
    root.mainloop()


def issymbol(text: str, *, toEng: bool = True) -> bool:
    """
    判断不定长字符是否为或全为符号.

    :param text: 测试文本.
    :type text: str
    :param toEng: 是否半角化
    :type toEng: bool
    :return: 检测的布尔值.
    """
    return all([True if (toEnglish(str(word)) if toEng else str(word)) in r"-+*/=!@#$%^&()<>?.,;:{}[\]_~`|" else False for word in text])


def isChinese(word: str) -> bool:
    """
    判断不定长字符是否为或全为中文字符.

    :param word: 测试文本.
    :type word: str
    :return: 检测的布尔值.
    """

    def checku(a_word: str):
        try:
            return True if 0x4e00 <= ord(a_word) <= 0x9fff else False
        except TypeError:
            warn(f"无法判断字符-> {word} <-")

    typedict = {"D": 0, "S": 0, "E": 0, "C": 0, "O": 0}

    if isinstance(word, str):
        for w in toEnglish(word):
            w: str
            if w.isdigit():
                typedict["D"] += 1
            elif issymbol(w):
                typedict["S"] += 1
            elif w.isalpha():
                if checku(w):
                    typedict["C"] += 1
                else:
                    typedict["E"] += 1
            else:
                typedict["O"] += 1

        if typedict["C"] > typedict["E"]:
            return True
        else:
            return False

    else:
        warn(f"无法判断字符-> {word} <-")


def repath(filepath: str) -> str:
    """
    用于在 **windows** 系统中强行合法化文件名称.

    :param filepath: 文件路径.
    :type filepath: str
    :return: 处理后的文本.
    """
    return filepath \
        .replace("\\", "") \
        .replace("/", "") \
        .replace(":", "") \
        .replace("*", "") \
        .replace("?", "") \
        .replace('"', "") \
        .replace("<", "") \
        .replace(">", "") \
        .replace("|", "")


def toEnglish(aimstr: str, *, wrapindex: int = None, allowwrap: bool = False) -> str:
    """
    半角符号转换.

    :param aimstr: 需要转换的字符串.
    :type aimstr: str
    :param wrapindex: 一行多少字符串时换行(默认:None #即不换行)
    :type wrapindex: int
    :param allowwrap: 是否允许去掉换行符.(默认False不允许)
    :type allowwrap: bool
    :return: 转换后的字符串.
    """
    finstr = aimstr.replace('，', ',') \
        .replace('。', '.') \
        .replace('；', ';') \
        .replace('、', ',') \
        .replace('“', '"') \
        .replace('”', '"') \
        .replace('‘', "'") \
        .replace('（', '(') \
        .replace('）', ')') \
        .replace('：', ':') \
        .replace('？', '?') \
        .replace("【", "[") \
        .replace("】", "]") \
        .replace("｛", "{") \
        .replace("｝", "}")
    finstr = finstr.replace("\n", '') if allowwrap else finstr
    return ''.join([f"{v}\n" if (i + 1) % wrapindex == 0 else v for i, v in enumerate(finstr)]) if wrapindex else finstr


def filetoEN(path: Annotated[str, "指定目标路径"]) -> None:
    """
    将文件进行半角转换.

    :param path: 目标文件完整路径.
    :type path: str
    :return: 操作执行函数不做返回.
    """

    from conFunc import supcount

    with open(path, 'r', encoding='utf-8') as file:
        filestr = file.read()
        man = reduce(lambda x, y: x + y, supcount(filestr,
                                                  "，", "。", "：", "；", "、", "“", "”", "‘", "（", "）", "？").values())
        filestr = toEnglish(filestr)
        file.close()
    with open(path, 'w', encoding='utf-8') as file:
        file.write(filestr)
        file.close()
        filename = path.split('\\')[-1]
        print(f"<{filename}>转换成功,共{man}个字符被转换.")


def doForAllFile(path: str, _: list = []) -> ...:
    """
    为文件夹中的所有文件进行半角转换.

    :param path: 文件夹路径.
    :type path: str
    :param _: 记录参数 **(非用户参数!)**
    :type _: list
    :return: 操作执行函数不做返回.
    """
    for child in listdir(path):
        child_path = path.join(path, child)
        if path.isdir(child_path):
            doForAllFile(child_path, _)
        else:
            _.append(child_path)
    return _


def dirtoEN(dirpath: str, *, aimpix: Annotated[str, "指定文件后缀名"] = ".txt", allin: bool = False) -> None:
    """
    对目标目录中的目标后缀文件进行半角符号转换.

    :param dirpath: 目标路劲(如C:\\path\to\\dir)
    :type dirpath: str
    :param aimpix: 目标文件类型后缀(默认:".txt")
    :type aimpix: str
    :param allin: 是否递归至所有子文件夹.(默认:False)
    :type allin: bool
    :return: 操作执行函数,不做返回.
    """
    if allin:
        dir = doForAllFile(dirpath)
        for n in dir[:5]:
            print(n)
        print(f"......\n")
        if input(rf"以上等{len(dir) - 5}个文件都将被装换,你确定继续吗\n\t'Y'确定,'N'停止\n:"):
            for file in dir:
                filetoEN(file)
    else:
        dirlist = list(filter(lambda x: True if aimpix in x else False, listdir(dirpath)))
        for i, v in enumerate(dirlist):
            print(i, v)
        agreement = input(f"以上{aimpix}后缀文件将会被转换,您确定继续吗\n\t'Y'确定,'N'停止\n:")
        if agreement == "Y" or agreement == "y":
            for file in dirlist:
                filetoEN(path.join(dirpath, file))
        else:
            print("转换停止")


def getWidth(_chr: str, *, formatWay: Literal["U", "F", "A", "B"] = "A") -> int:
    """
    获取字符的实际宽度.

    :param _chr: 目标字符.
    :type _chr: str
    :param formatWay: 最后长度取整方法,U:向上取整,F:向下取整,A:自动判断,B:反向自动判断.
    :type formatWay: str
    :return: 字符的宽度
    :raise ValueError: 如果输入的选项不在["U", "F", "A", "B"]之中将抛出ValueError错误.
    """

    _chr = str(_chr)

    isint = lambda x: True if isinstance(x, int) or str(x).split(".")[-1] == "0" else False
    width = 0
    for char in _chr:
        if isChinese(char):
            width += 1.6
        else:
            width += 1
    if formatWay == "U":
        return ceil(width)
    elif formatWay == "F":
        return floor(width)
    elif formatWay == "A":
        if isint(width):
            return int(width)
        else:
            if int(str(width)[-1]) > 5: return ceil(width)
            else: return floor(width)
    elif formatWay == "B":
        if isint(width):
            return int(width)
        else:
            if int(str(width)[-1]) > 5: return floor(width)
            else: return ceil(width)
    else:
        raise ValueError(f"'{formatWay}' is not in ["U", "F"]")


if __name__ == '__main__':
    pass

