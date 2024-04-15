# python文件夹

## executableDir
   * 用于存放二进制可执行文件
   1. upload.exe - 用于自动化打包并上传python库至testpypi的工具
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
         <mark>PS.使用前请确保安装了[pdoc](https://pypi.org/project/pdoc3/)和[pandoc](https://pandoc.org/installing.html),如果`-T`为`pyd`时需额外安装[Cython](https://pypi.org/project/Cython/),[pybind11](https://pypi.org/project/pybind11/)和[CMake](https://cmake.org/),并且确保它们已被添加在环境变量中</mark>
      ```DOS
      upload C:\path\to\your\pyFile.py -D=True -I=True -T=normal
      ```
      
      * 打包时如果目标py文件所在路径中存在名为`args.json`,则在打包好无需再编写project.toml文件,其内容应如
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
   1. divination
      * 一个趣味的测算项目
   
   2. englishApp
      * 一个用来背单词的软件

   3. pytorchLearn
      * pytorch学习笔记

   4. taskSorter
      * 定义任务基类

   5. timeAllocation
      * 时间管理器

## pypiOrigin
   * 存放一些提交到[testpypi](https://test.pypi.org/)上的库

   1. ansiDefine
      * 简化使用ANSI转义符的代码编写过程

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
