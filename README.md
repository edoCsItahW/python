# python文件夹

## executableDir
   * 用于存放二进制可执行文件
   1. upload.exe - 用于自动化打包并上传python库至[testpypi](https://test.pypi.org/)的工具
      <mark>使用方法</mark>
      
      * 检查环境变量
      ```DOS
      upload --help
      ```
      
      * 如果没有找到指令，那请将所在路径添加到环境变量
      ```DOS
      set PATH "%PATH%;C:\path\to\uploadDir"
      ```
      
      * 如果找到指令,你可以参考其中的参数,其中基本的操作指令
         <mark>PS.如果`-T`参数为`pyd`时需额外安装[pybind11](https://pypi.org/project/pybind11/)和[CMake](https://cmake.org/),并且确保它们已被添加在环境变量中</mark>
      ```DOS
      upload C:\path\to\your\pyFile.py -D=True -I=True -T=normal
      ```
      
      * 打包时如果目标py文件所在路径中存在名为`args.json`,则在打包好无需再编写project.toml文件,其内容应型如
      ```json
      {
          "increase": true,  // 是否在每次打包成功时自动提升版本
          "proName": null,  // 项目名,null时则自动填充你的py文件的名称
          "version": "0.0.0",  // 项目版本
          "name": "",  // 作者姓名
          "email": "",  // 作者邮箱
          "desc": "",  // 该库的简单描述
          "moduleName": null,  // github上的索引,null时则自动填充你的py文件的名称
          "uploadLog": [  // 自动生成的打包记录,false表示打包失败
            {
              "[2024-04-12 17:36:29]": {
                "0.0.14": true
              }
            }
          ]
        }
      ```

## privateProject
   * 存放一些py小项目
   1. docSpawner --- 2024.5
      通过AST实现的注释到文档生成工具,包括`.pyi`存根文件生成,markdown格式文档生成
   
   2. englishApp  --- 2023.8
      一个用来背单词的软件
   
   3. mcProtocol --- 2024.6
      通过**Minecraft**特定的_TCP_规则解析和构造并发送包以完成服务器从握手至交互的过程
      
   4. p2p --- 2024.9
      python实现**P2P**

   5. pytorchLearn --- 2023.8
       pytorch学习笔记
       
   6. responsive --- 2024.8
      python仿写**Vue3**的响应式原理及功能


## pypiOrigin
   * 存放一些提交到[testpypi](https://test.pypi.org/)上的库

   1. ansiDefine
      * 简化使用_ANSII_转义符的使用

   2. conFunc
      * '常用'方法合集

   3. figureTools
      * 包含一些操作图像和包装了matplotlib的方法

   4. logTools
      * 对py标准库logging进行包装

   5. MachineLearningTools
      * 机器学习集合

   6. markDownTools
      * 一些基于markdown语法的转换函数

   7. netTools
      * 包装了网络请求的方法

   8. ptioTools
      * 尝试包装线程,进程相关方法

   9. spiderTools
      * 一些有用的爬虫便捷方法

   10. sqlTools
       * 简化了mysql的语法和pymysql的操作,模拟了mysql的输入和输出
      
   11. systemTools
       * 一些对python系统和pc的操作

   12. textTools
       * 一些有意思的字符画和str类处理方法

   13. uploadTools
       * upload.exe打包前的源代码

## scatteredFile
   * 一些零散的单文件项目
