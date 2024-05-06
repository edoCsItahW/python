# API Documentation

   * [CMDError](#CMDError-CMDError){.class}
   * [winAuto](#winAuto-winAuto){.class}
      * shell{.function}
      * args{.function}
      * findCmd{.function}
      * getAllTitle{.function}
      * sendInstruct{.function}
      * begin{.function}
   * [cmd](#cmd-cmd){.class}
   * [instruct](#instruct-instruct){.class}
   * [jsonFile](#jsonFile-jsonFile){.class}
      * jsonData{.function}
      * update{.function}
      * read{.function}
      * write{.function}
   * [jsonOpen](#jsonOpen-jsonOpen){.class}
   * [SpawnError](#SpawnError-SpawnError){.class}
   * [outputInfo](#outputInfo-outputInfo){.function}
   * [strToBool](#strToBool-strToBool){.function}
   * [pathTools](#pathTools-pathTools){.class}
      * isFileExist{.function}
      * createIfNotExist{.function}
   * [argSet](#argSet-argSet){.class}
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
   * [errorHandle](#errorHandle-errorHandle){.class}
      * args{.function}
      * logError{.function}
      * raiseErrorGroup{.function}
      * raiseError{.function}
         * rerr{.function}
      * formatFuncInfo{.function}
      * executeWithTry{.function}
   * [actionSet](#actionSet-actionSet){.class}
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
   * [upload](#upload-upload){.class}
      * args{.function}
      * actionSet{.function}
      * tryDec{.function}
      * pyc{.function}
      * pyd{.function}
      * normal{.function}
      * cToPyd{.function}
      * build{.function}
   * [argParser](#argParser-argParser){.function}
### CMDError {#CMDError}
   > CMD错误类
   
        
### winAuto {#winAuto}
   
        
   * shell 
      > 返回WScript.Shell对象
      
        
   * args 
      > 返回指令元组
      
        
   * findCmd 
      > 查找cmd窗口
      
        
   * getAllTitle 
      > 获取所有窗口标题
      
        
   * sendInstruct 
      > 发送指令
      * Parameters: 
         * param
            * `instruct` (str): 指令
         * keyword
            * `waitTime` (int): 等待时间
            * `enter` (bool): 是否自动添加回车符号{ENTER}

        
   * begin 
      > 开始执行
      
        
### cmd {#cmd}
   > 用于弹出cmd窗口并进行按键模拟
   
        
### instruct {#instruct}
   > 命令行运行器
   
        
### jsonFile {#jsonFile}
   > json文件操作类
   
        
   * jsonData 
      > 设置json数据
      * Parameters: 
         * param
            * `value` (dict): 字典(dict)形式的json数据

        
   * update 
      > 更新json数据
      * Parameters: 
         * param
            * `__m` (list[tuple[Any, Any]]): 键值对列表

        
   * read 
      > 读取json数据
      
        
   * write 
      > 写入json数据
      * Parameters: 
         * param
            * `__d` (dict): 字典(dict)形式的json数据,如果为None则使用当前json数据

        
### jsonOpen {#jsonOpen}
   > json文件操作类
   
        
### SpawnError {#SpawnError}
   > 子进程错误类
   
        
### outputInfo {#outputInfo}
   > 输出信息
   * Parameters: 
      * param
         * `info` (str): 信息内容
      * keyword
         * `color` (Literal["red", "green", "blue", "yellow"] | str | bool): 颜色,可以是布尔值(bool),也可以是red, green, blue, yellow中的一个
         * `flag` (bool): 是否输出信息

        
### strToBool {#strToBool}
   > 根据字符串字面意思转换为布尔值
   * Parameters: 
      * param
         * `text` (str): 字符串
      * keyword
         * `default` (bool): 默认值

        
### pathTools {#pathTools}
   > 文件路径工具类
   
        
   * isFileExist 
      > 检测文件是否存在,如果不存在则报错.
      * Parameters: 
         * param
            * `_path` (str | PathLike): 文件路径
         * keyword
            * `kwargs` (Any): {note: 错误原因注解, willDo: [warn, error, stop] 报错方式, fromError: ..., group: 组}

        
   * createIfNotExist 
      > 创建文件夹,如果文件夹不存在则创建,如果存在则不做任何操作.
      * Parameters: 
         * param
            * `_path` (str | PathLike[str]): 文件夹路径

        
### argSet {#argSet}
   > 参数设置和存储类
   * Attributes: 
      * `filePath`: 文件绝对路径.  
      * `rootPath`: 项目根目录路径.  
      * `fileName`: 文件名.  
      * `moduleName`: 模块名.  
      * `dirPath`: 模块目录路径.  
      * `projectPath`: 项目目录路径.  
      * `newPath`: 上传后文件的路径.  
      * `jsonPath`: args.json路径.  
      * `argsDict`: args.json字典.  
      * `separator`: 路径分隔符.  
      * `executor`: 命令行执行器.  
      * `color`: 是否运行输出信息带有色彩.  
      * `flagRestore`: 当出现错误时是否要还原初始状态.  
      * `flagDebug`: 是否开启Debug模式.  
      * `flagAuto`: 是否自动上传.  
      * `flagIncrease`: 是否运行上传完后自动向args.json中更新版本.  
      * `suffix`: 文件后缀.  
      * `pyVersion`: python版本号.  
      * `cmakeVersion`: cmake版本号.  

   * Methods: 
      * `compliantArg`: 路径合规性检查.  

        
   * filePath 
      
        
   * rootPath 
      > 项目根目录路径.
      
        
   * fileName 
      > 文件名.
      
        
   * moduleName 
      > 模块名.
      
        
   * fileSuffix 
      > 文件后缀.
      
        
   * checkSuffix 
      > 检查文件后缀是否合规.
      * Parameters: 
         * param
            * `suffix` (str | list[str]): 文件后缀

        
   * dirPath 
      > 模块目录路径.
      
        
   * projectPath 
      > 项目目录路径.
      
        
   * newPath 
      
        
   * jsonPath 
      > args.json路径.
      
        
   * argsDict 
      > args.json字典.
      
        
   * separator 
      > 路径分隔符.
      
        
   * executor 
      > 命令行执行器.
      
        
   * color 
      > 关键字参数color启用信号.
      
        
   * flagRestore 
      > 关键字参数restore启用信号.
      
        
   * flagDebug 
      > 关键字参数debug启用信号.
      
        
   * flagAuto 
      > 关键字参数auto启用信号.
      
        
   * flagIncrease 
      > 关键字参数increase启用信号.
      
        
   * suffix 
      > 文件后缀.
      
        
   * pyVersion 
      > python版本号.
      
        
   * cmakeVersion 
      > CMake版本号.
      
        
   * compliantArg 
      > 路径合规性检查.
      * Parameters: 
         * param
            * `_path` (str | PathLike[str]): 文件路径
            * `suffix` (str | list[str]): 文件后缀

        
### errorHandle {#errorHandle}
   
        
   * args 
      > 属性存储类
      
        
   * logError 
      > 错误记录.
      * Parameters: 
         * param
            * `error` (Exception): 错误
            * `group` (str): 分至组

        
   * raiseErrorGroup 
      > 引发错误组.
      
        
   * raiseError 
      
        
      * rerr 
         
        
   * formatFuncInfo 
      > 格式化函数信息
      * Parameters: 
         * param
            * `func` (Callable): 函数
            * `line` (int): 行号(一般为currentframe().f_back.f_lineno)

        
   * executeWithTry 
      > 在try-except中执行指令.
      * Parameters: 
         * param
            * `instruction` (str): 指令
         * keyword
            * `cwd` (str | PathLike): 执行指令的目录
            * `note` (str): 指令注解
            * `group` (str): 指令分组
            * `describe` (str): 指令描述
            * `color` (str): 是否允许输出带有颜色,或者指定颜色

        
### actionSet {#actionSet}
   > 操作集合类
   * Attributes: 
      * `args`: 参数设置和存储类.  
      * `eh`: 错误处理类.  
      * `vsList`: 版本号列表.  

   * Methods: 
      * `versionBack`: 版本号回退.  
      * `_jsonIncrease`: 版本号入口函数.  
      * `_kewargs`: 获取关键字参数.  
      * `_warpCmake`: 包装CMakeLists.format函数.  
      * `_vsIncrease`: 版本号自增.  
      * `_vsToList`: 将版本号字符串转换为列表.  
      * `_listToVs`: 将版本号列表转换为字符串.  
      * `_onlyKey`: 对于只有一个键的字典,返回这个键.  
      * `_jsonIncrease`: 版本号入口函数.  
      * `_increase`: 版本号自增主函数.  

        
   * args 
      > 属性存储类
      
        
   * eh 
      > 错误处理类
      
        
   * vsList 
      > 设置版本号列表
      * Parameters: 
         * param
            * `value` (Any):         :return:

        
   * versionBack 
      > 将版本号回退到上一个版本.
      
        
   * spawnPyi 
      > 生成pyi文件.
      
        
   * spawnPyc 
      > 生成pyc文件.
      
        
   * spawnHtml 
      > 生成html文档.
      
        
   * spawnREADME 
      > 生成README.md文件.
      
        
   * spawnLicense 
      > 生成License.txt文件.
      
        
   * spawnManifest 
      
        
   * spawnInit 
      > 生成__init__.py文件.
      
        
   * spawnPyproject 
      > 生成pyproject.toml文件.
      * Parameters: 
         * param
            * `filePath` (str | PathLike[str]): 生成pyproject.toml文件的路径,默认为None

        
   * spawnSetup 
      > 生成setup.py文件.
      
        
   * spawnC 
      > 生成C文件.
      
        
   * spawnPyd 
      > 生成pyd文件, 原文件为C++文件时需要指定cppFile=True, 否则默认为False.
      
        
   * CMakeLists 
      > 生成CMakeLists.txt文件
      * Parameters: 
         * param
            * `fileName` (str): C/Cpp文件名
         * keyword
            * `toPath` (Any): 生成到指定路径,默认为项目路径

        
   * middleDo 
      > 初始化操作.
      
        
   * checkRequestList 
      > 检查预设需求文件结构是否存在.
      * Parameters: 
         * param
            * `requestList` (list): 预设需求文件结构列表.

        
### upload {#upload}
   
        
   * args 
      > 返回参数对象.
      
        
   * actionSet 
      > 返回操作集对象.
      
        
   * tryDec 
      > 在try-except中执行函数,并在出现错误时还原文件.
      * Parameters: 
         * param
            * `func` (Callable): 要执行的函数.
         * keyword
            * `copy` (bool): 是否复制py源文件到指定路径,默认为False

        
   * pyc 
      > pyc文件打包
      
        
   * pyd 
      > pyd文件打包
      
        
   * normal 
      > 普通py文件打包
      
        
   * cToPyd 
      > 将C或Cpp文件转换为pyd文件
      
        
   * build 
      > 根据传入的打包类型,执行相应的最终打包操作.
      * Parameters: 
         * param
            * `Type` (str): 打包类型,可选值: pyc, pyd, normal, cToPyd.(默认值: pyd)

        
### argParser {#argParser}
   > 包装了argparse的命令行参数解析器,用于解析命令行参数。
   
        
