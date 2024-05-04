# API Documentation

   * CMDError{.class}
   * winAuto{.class}
      * shell{.function}
      * args{.function}
      * findCmd{.function}
      * getAllTitle{.function}
      * sendInstruct{.function}
      * begin{.function}
   * cmd{.class}
   * instruct{.class}
   * jsonFile{.class}
      * jsonData{.function}
      * update{.function}
      * read{.function}
      * write{.function}
   * jsonOpen{.class}
   * SpawnError{.class}
   * outputInfo{.function}
   * strToBool{.function}
   * pathTools{.class}
      * isFileExist{.function}
      * createIfNotExist{.function}
   * argSet{.class}
      * filePath{.function}
      * rootPath{.function}
      * fileName{.function}
      * moduleName{.function}
      * fileSuffix{.function}
      * checkSuffix{.function}
      * dirPath{.function}
      * projectPath{.function}
      * newPath{.function}
      * jsonPath{.function}
      * argsDict{.function}
      * separator{.function}
      * executor{.function}
      * color{.function}
      * flagRestore{.function}
      * flagDebug{.function}
      * flagAuto{.function}
      * flagIncrease{.function}
      * suffix{.function}
      * pyVersion{.function}
      * cmakeVersion{.function}
      * compliantArg{.function}
   * errorHandle{.class}
      * args{.function}
      * logError{.function}
      * raiseErrorGroup{.function}
      * raiseError{.function}
         * rerr{.function}
      * formatFuncInfo{.function}
      * executeWithTry{.function}
   * actionSet{.class}
      * args{.function}
      * eh{.function}
      * vsList{.function}
      * versionBack{.function}
      * spawnPyi{.function}
      * spawnPyc{.function}
      * spawnHtml{.function}
      * spawnREADME{.function}
      * spawnLicense{.function}
      * spawnManifest{.function}
      * spawnInit{.function}
      * spawnPyproject{.function}
      * spawnSetup{.function}
      * spawnC{.function}
      * spawnPyd{.function}
      * CMakeLists{.function}
      * middleDo{.function}
      * checkRequestList{.function}
   * upload{.class}
      * args{.function}
      * actionSet{.function}
      * tryDec{.function}
      * pyc{.function}
      * pyd{.function}
      * normal{.function}
      * cToPyd{.function}
      * build{.function}
   * argParser{.function}
### CMDError
   > description: 
   
   CMD错误类

   
   
### winAuto
   > description: 
   
   无
   
   
   * shell
      > description: 
   
      返回WScript.Shell对象
:return:WScript.Shell对象

   
   
   * args
      > description: 
   
      返回指令元组
:return:指令元组

   
   
   * findCmd
      > description: 
   
      查找cmd窗口
:keywordkeyword:查找关键字
:typekeyword:str
:return:cmd窗口句柄
:rtype:int

   
   
   * getAllTitle
      > description: 
   
      获取所有窗口标题
:return:所有窗口标题列表

   
   
   * sendInstruct
      > description: 
   
      发送指令
:paraminstruct:指令
:typeinstruct:str
:keywordwaitTime:等待时间
:typewaitTime:int
:keywordenter:是否自动添加回车符号{ENTER}
:typeenter:bool

   
   
   * begin
      > description: 
   
      开始执行

   
   
### cmd
   > description: 
   
   用于弹出cmd窗口并进行按键模拟

   
   
### instruct
   > description: 
   
   命令行运行器
使用方法::
>>>ins=instruct(output=True,ignore=False,color=True)
>>>ins("dir")

   
   
### jsonFile
   > description: 
   
   json文件操作类

   
   
   * jsonData
      > description: 
   
      设置json数据
:paramvalue:字典(dict)形式的json数据
:typevalue:dict
:raiseTypeError:输入类型错误

   
   
   * update
      > description: 
   
      更新json数据
:param__m:键值对列表
:type__m:list[tuple[Any,Any]]
:raiseValueError:参数形式错误

   
   
   * read
      > description: 
   
      读取json数据
:return:返回字典(dict)形式的json数据

   
   
   * write
      > description: 
   
      写入json数据
:param__d:字典(dict)形式的json数据,如果为None则使用当前json数据
:type__d:dict

   
   
### jsonOpen
   > description: 
   
   json文件操作类

   
   
### SpawnError
   > description: 
   
   子进程错误类

   
   
### outputInfo
   > description: 
   
   输出信息
:paraminfo:信息内容
:typeinfo:str
:keywordcolor:颜色,可以是布尔值(bool),也可以是red,green,blue,yellow中的一个
:typecolor:Literal["red","green","blue","yellow"]|str|bool
:keywordflag:是否输出信息
:typeflag:bool

   
   
### strToBool
   > description: 
   
   根据字符串字面意思转换为布尔值
:paramtext:字符串
:typetext:str
:keyworddefault:默认值
:typedefault:bool
:return:布尔值
:rtype:bool

   
   
### pathTools
   > description: 
   
   文件路径工具类

   
   
   * isFileExist
      > description: 
   
      检测文件是否存在,如果不存在则报错.
:param_path:文件路径
:type_path:str|PathLike
:keywordkwargs:{note:错误原因注解,willDo:[warn,error,stop]报错方式,fromError:...,group:组}
:typekwargs:Any
:return:文件是否存在
:rtype:bool
:raiseFileNotFoundError:如果文件不存在.

   
   
   * createIfNotExist
      > description: 
   
      创建文件夹,如果文件夹不存在则创建,如果存在则不做任何操作.
:param_path:文件夹路径
:type_path:str|PathLike[str]

   
   
### argSet
   > description: 
   
   None
   
   
   * filePath
      > description: 
   
      文件绝对路径.
:return:文件绝对路径.
:rtype:str

   
   
   * rootPath
      > description: 
   
      项目根目录路径.
:return:项目根目录路径.
:rtype:PathLike[str]

   
   
   * fileName
      > description: 
   
      文件名.
:return:文件名
:rtype:str

   
   
   * moduleName
      > description: 
   
      模块名.
:return:模块名
:rtype:str

   
   
   * fileSuffix
      > description: 
   
      文件后缀.
:return:文件后缀
:rtype:str

   
   
   * checkSuffix
      > description: 
   
      检查文件后缀是否合规.
:paramsuffix:文件后缀
:typesuffix:str|list[str]
:return:是否合规
:rtype:bool
:raiseNotImplementedError:类型不支持.

   
   
   * dirPath
      > description: 
   
      模块目录路径.
:return:模块目录路径
:rtype:str
:raiseRuntimeError:当文件后缀为c或cpp时,会抛出此错误.

   
   
   * projectPath
      > description: 
   
      项目目录路径.
:return:项目目录路径
:rtype:PathLike[str]|str
:raiseRuntimeError:当文件后缀为c或cpp时,会抛出此错误.

   
   
   * newPath
      > description: 
   
      无
   
   
   * jsonPath
      > description: 
   
      args.json路径.
:return:args.json路径
:rtype:str|None

   
   
   * argsDict
      > description: 
   
      args.json字典.
:return:args.json字典
:rtype:dict[str,Any]

   
   
   * separator
      > description: 
   
      路径分隔符.
:return:路径分隔符
:rtype:str

   
   
   * executor
      > description: 
   
      命令行执行器.
:return:命令行执行器
:rtype:instruct

   
   
   * color
      > description: 
   
      关键字参数color启用信号.
:return:启用信号
:rtype:bool

   
   
   * flagRestore
      > description: 
   
      关键字参数restore启用信号.
:return:启用信号
:rtype:bool

   
   
   * flagDebug
      > description: 
   
      关键字参数debug启用信号.
:return:启用信号
:rtype:bool

   
   
   * flagAuto
      > description: 
   
      关键字参数auto启用信号.
:return:启用信号
:rtype:bool

   
   
   * flagIncrease
      > description: 
   
      关键字参数increase启用信号.
:return:启用信号
:rtype:bool

   
   
   * suffix
      > description: 
   
      文件后缀.
:return:文件后缀
:rtype:str

   
   
   * pyVersion
      > description: 
   
      python版本号.
:return:python版本号
:rtype:str

   
   
   * cmakeVersion
      > description: 
   
      CMake版本号.
:return:CMake版本号
:rtype:str

   
   
   * compliantArg
      > description: 
   
      路径合规性检查.
:param_path:文件路径
:type_path:str|PathLike[str]
:paramsuffix:文件后缀
:typesuffix:str|list[str]
:raiseValueError:后缀不合规.

   
   
### errorHandle
   > description: 
   
   无
   
   
   * args
      > description: 
   
      属性存储类
:return:属性存储类
:rtype:argSet

   
   
   * logError
      > description: 
   
      错误记录.
:paramerror:错误
:typeerror:Exception
:paramgroup:分至组
:typegroup:str

   
   
   * raiseErrorGroup
      > description: 
   
      引发错误组.

   
   
   * raiseError
      > description: 
   
      无
   
   
      * rerr
         > description: 
   
         无
   
   
   * formatFuncInfo
      > description: 
   
      格式化函数信息
:paramfunc:函数
:typefunc:Callable
:paramline:行号(一般为currentframe().f_back.f_lineno)
:typeline:int
:return:格式化后的函数信息
:rtype:str

   
   
   * executeWithTry
      > description: 
   
      在try-except中执行指令.
:paraminstruction:指令
:typeinstruction:str
:keywordcwd:执行指令的目录
:typecwd:str|PathLike
:keywordnote:指令注解
:typenote:str
:keywordgroup:指令分组
:typegroup:str
:keyworddescribe:指令描述
:typedescribe:str
:keywordcolor:是否允许输出带有颜色,或者指定颜色
:typecolor:str

   
   
### actionSet
   > description: 
   
   操作集合类
Attributes:
:ivarargs:参数设置和存储类.
:ivareh:错误处理类.
:ivarvsList:版本号列表.
Methods:
:meth:`versionBack`:版本号回退.
:meth:`_jsonIncrease`:版本号入口函数.
:meth:`_kewargs`:获取关键字参数.
:meth:`_warpCmake`:包装CMakeLists.format函数.
:meth:`_vsIncrease`:版本号自增.
:meth:`_vsToList`:将版本号字符串转换为列表.
:meth:`_listToVs`:将版本号列表转换为字符串.
:meth:`_onlyKey`:对于只有一个键的字典,返回这个键.
:meth:`_jsonIncrease`:版本号入口函数.
:meth:`_increase`:版本号自增主函数.
:meth:`spawnPyi`:生成pyi文件.
:meth:`spawnPyc`:生成pyc文件.
:meth:`spawnHtml`:生成html文件.
:meth:`spawnReadme`:生成readme文件.
:meth:`spawnSetup`:生成setup.py文件.
:meth:`spawnInit`:生成__init__.py文件.
:meth:`cmakeLists`:生成CMakeLists.txt文件.
:meth:`spawnPyproject`:生成pyproject.toml文件.
:meth:`spawnManifest`:生成MANIFEST.in文件.
:meth:`spawnLicense`:生成LICENSE文件.
:meth:`spawnC`:生成c文件.
:meth:`spawnPyd`:生成pyd文件.
:meth:`middleDo`:初始化操作.
:meth:`checkRequestList`:检查是否与预设文件结构相同.

   
   
   * args
      > description: 
   
      属性存储类
:return:属性存储类
:rtype:argSet

   
   
   * eh
      > description: 
   
      错误处理类
:return:错误处理类
:rtype:errorHandle

   
   
   * vsList
      > description: 
   
      设置版本号列表
:paramvalue:
:return:

   
   
   * versionBack
      > description: 
   
      将版本号回退到上一个版本.

   
   
   * spawnPyi
      > description: 
   
      生成pyi文件.
过程::
1.生成stub文件:stubgen{fileName}
2.移除缓存文件:rd/s/q__pycache__
3.移动pyi文件:moveout/{moduleName}/{moduleName}.pyi{projectPath}
4.删除out文件夹:rd/s/qout
:return:生成的pyi文件路径
:rtype:str

   
   
   * spawnPyc
      > description: 
   
      生成pyc文件.
过程::
1.编译py文件:python-mpy_compile{fileName}
2.移动pyc文件:move__pycache__/{fileName}.pyc{projectPath}
3.删除缓存文件:rd/s/q__pycache__
4.重命名pyc文件:ren{fileName}.pyc{fileName}.cpython-39.pyc
:return:生成的pyc文件路径
:rtype:str

   
   
   * spawnHtml
      > description: 
   
      生成html文档.
过程::
1.生成html文档:pdoc-d=markdown--output{dirPath}{filePath}
2.移除index.html和search.js文件
:return:生成的html文档路径
:rtype:str

   
   
   * spawnREADME
      > description: 
   
      生成README.md文件.
过程::
1.生成html文档:self.spawnHtml()
2.转换html为markdown:pandoc-fhtml-tmarkdown{htmlPath}-o{readmePath}
3.删除html文件:del{htmlPath}
:return:生成的README.md文件路径
:rtype:str

   
   
   * spawnLicense
      > description: 
   
      生成License.txt文件.

   
   
   * spawnManifest
      > description: 
   
      无
   
   
   * spawnInit
      > description: 
   
      生成__init__.py文件.

   
   
   * spawnPyproject
      > description: 
   
      生成pyproject.toml文件.
:paramfilePath:生成pyproject.toml文件的路径,默认为None
:typefilePath:str|PathLike[str]

   
   
   * spawnSetup
      > description: 
   
      生成setup.py文件.

   
   
   * spawnC
      > description: 
   
      生成C文件.
过程::
1.使用setuptools将py文件编译为C文件:pythonsetup.pybuild_ext--inplace
:return:生成的C文件路径
:rtype:str

   
   
   * spawnPyd
      > description: 
   
      生成pyd文件,原文件为C++文件时需要指定cppFile=True,否则默认为False.
过程::
1.执行cmakepybind11build
2.重命名C文件为Cpp文件(如果cppFile=True则不执行这一步)
3.执行cmakebuild
4.重命名生成的pyd文件
5.移除残留build文件夹
:keywordtoPath:生成到指定路径,默认为项目路径
:typetoPath:str|PathLike[str]
:keywordcppFile:原文件是否为C++文件,默认为False
:typecppFile:bool
:return:生成的pyd文件路径
:rtype:str|PathLike[str]

   
   
   * CMakeLists
      > description: 
   
      生成CMakeLists.txt文件
:paramfileName:C/Cpp文件名
:typefileName:str
:keywordtoPath:生成到指定路径,默认为项目路径

   
   
   * middleDo
      > description: 
   
      初始化操作.
:keywordcopy:是否复制py源文件到指定路径,默认为False
:typecopy:bool

   
   
   * checkRequestList
      > description: 
   
      检查预设需求文件结构是否存在.
:paramrequestList:预设需求文件结构列表.
:typerequestList:list

   
   
### upload
   > description: 
   
   无
   
   
   * args
      > description: 
   
      返回参数对象.
:return:参数对象.
:rtype:argSet

   
   
   * actionSet
      > description: 
   
      返回操作集对象.
:return:操作集对象.
:rtype:actionSet

   
   
   * tryDec
      > description: 
   
      在try-except中执行函数,并在出现错误时还原文件.
:paramfunc:要执行的函数.
:typefunc:Callable
:keywordcopy:是否复制py源文件到指定路径,默认为False
:typecopy:bool

   
   
   * pyc
      > description: 
   
      pyc文件打包
   
   
   * pyd
      > description: 
   
      pyd文件打包
   
   
   * normal
      > description: 
   
      普通py文件打包
   
   
   * cToPyd
      > description: 
   
      将C或Cpp文件转换为pyd文件
   
   
   * build
      > description: 
   
      根据传入的打包类型,执行相应的最终打包操作.
:paramType:打包类型,可选值:pyc,pyd,normal,cToPyd.(默认值:pyd)
:typeType:str

   
   
### argParser
   > description: 
   
   包装了argparse的命令行参数解析器,用于解析命令行参数。
:return:一个包含命令行参数的对象。
:rtype:Namespace

   
   
