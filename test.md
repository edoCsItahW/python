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
   > CMD错误类
   
   
   
### winAuto
   > 无
   
   
   
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
   
      
   
   * begin
      > 开始执行
   
      
   
### cmd
   > 用于弹出cmd窗口并进行按键模拟
   
   
   
### instruct
   > 命令行运行器
   
   
   
### jsonFile
   > json文件操作类
   
   
   
   * jsonData
      > 设置json数据
   
      
   
   * update
      > 更新json数据
   
      
   
   * read
      > 读取json数据
   
      
   
   * write
      > 写入json数据
   
      
   
### jsonOpen
   > json文件操作类
   
   
   
### SpawnError
   > 子进程错误类
   
   
   
### outputInfo
   > 输出信息
   
   
   
### strToBool
   > 根据字符串字面意思转换为布尔值
   
   
   
### pathTools
   > 文件路径工具类
   
   
   
   * isFileExist
      > 检测文件是否存在,如果不存在则报错.
   
      
   
   * createIfNotExist
      > 创建文件夹,如果文件夹不存在则创建,如果存在则不做任何操作.
   
      
   
### argSet
   > 参数设置和存储类
   
   
   
   * filePath
      > 文件绝对路径.        :return: 文件绝对路径.        :rtype: str
   
      
   
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
   
      
   
   * dirPath
      > 模块目录路径.
   
      
   
   * projectPath
      > 项目目录路径.
   
      
   
   * newPath
      > 无
   
      
   
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
   
      
   
### errorHandle
   > 无
   
   
   
   * args
      > 属性存储类
   
      
   
   * logError
      > 错误记录.
   
      
   
   * raiseErrorGroup
      > 引发错误组.
   
      
   
   * raiseError
      > 无
   
      
   
      * rerr
         > 无
   
         
   
   * formatFuncInfo
      > 格式化函数信息
   
      
   
   * executeWithTry
      > 在try-except中执行指令.
   
      
   
### actionSet
   > 操作集合类
   
   
   
   * args
      > 属性存储类
   
      
   
   * eh
      > 错误处理类
   
      
   
   * vsList
      > 设置版本号列表
   
      
   
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
      > 无
   
      
   
   * spawnInit
      > 生成__init__.py文件.
   
      
   
   * spawnPyproject
      > 生成pyproject.toml文件.
   
      
   
   * spawnSetup
      > 生成setup.py文件.
   
      
   
   * spawnC
      > 生成C文件.
   
      
   
   * spawnPyd
      > 生成pyd文件, 原文件为C++文件时需要指定cppFile=True, 否则默认为False.
   
      
   
   * CMakeLists
      > 生成CMakeLists.txt文件
   
      
   
   * middleDo
      > 初始化操作.
   
      
   
   * checkRequestList
      > 检查预设需求文件结构是否存在.
   
      
   
### upload
   > 无
   
   
   
   * args
      > 返回参数对象.
   
      
   
   * actionSet
      > 返回操作集对象.
   
      
   
   * tryDec
      > 在try-except中执行函数,并在出现错误时还原文件.
   
      
   
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
   
      
   
### argParser
   > 包装了argparse的命令行参数解析器,用于解析命令行参数。
   
   
   
