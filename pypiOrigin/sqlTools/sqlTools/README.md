# API Documentation

   * [Result](#Result-Result){.class}
   * [Type](#Type-Type){.class}
   * [CanBeStr](#CanBeStr-CanBeStr){.class}
   * [ArgumentError](#ArgumentError-ArgumentError){.class}
   * [feasibleTest](#feasibleTest-feasibleTest){.function}
   * [stderr](#stderr-stderr){.function}
   * [stdout](#stdout-stdout){.function}
   * [Feedback](#Feedback-Feedback){.class}
      * normal{.function}
      * query{.function}
      * empty{.function}
      * alter{.function}
      * useDb{.function}
   * [result](#result-result){.function}
      * getfunc{.function}
         * warp{.function}
   * [remap](#remap-remap){.function}
   * [execute](#execute-execute){.function}
   * [Field](#Field-Field){.class}
      * value{.function}
      * result{.function}
      * related{.function}
   * [Base](#Base-Base){.class}
   * [DB](#DB-DB){.class}
   * [Database](#Database-Database){.class}
      * show{.function}
      * use{.function}
      * create{.function}
      * drop{.function}
   * [py2sql](#py2sql-py2sql){.function}
   * [TB](#TB-TB){.class}
   * [Table](#Table-Table){.class}
      * content{.function}
      * table{.function}
      * show{.function}
      * describe{.function}
      * create{.function}
      * drop{.function}
      * insert{.function}
      * select{.function}
      * update{.function}
      * alter{.function}
      * delete{.function}
      * toDataFrame{.function}
      * toCSV{.function}
      * fromCSV{.function}
   * [MySQL](#MySQL-MySQL){.class}
      * db{.function}
      * tb{.function}
      * database{.function}
      * table{.function}
### Result {#Result}
   
        
### Type {#Type}
   
        
### CanBeStr {#CanBeStr}
   
        
### ArgumentError {#ArgumentError}
   
        
### feasibleTest {#feasibleTest}
   > 先行测试,检查mysql是否安装以及服务是否启动.
   
        
### stderr {#stderr}
   > 错误着色
   
        
### stdout {#stdout}
   > 输出信息
   * Parameters: 
      * param
         * `msg` (Any): 输出信息
         * `allow` (Any): 是否允许输出
      * keyword
         * `kwargs` (Any): 其他print函数参数

        
### Feedback {#Feedback}
   > 反馈类,用于处理mysql的反馈信息.
   
        
   * normal 
      > 输出表类型信息.
      * Parameters: 
         * param
            * `rowcount` (Any): 行数
         * keyword
            * `spendtime` (Any): 耗时

        
   * query 
      > 输出查询信息.
      
        
   * empty 
      > 输出空结果信息.
      
        
   * alter 
      > 输出修改信息.
      
        
   * useDb 
      > 输出切换数据库信息.
      
        
### result {#result}
   
        
   * getfunc 
      
        
      * warp 
         > :raise RuntimeError: 结果处理失败
         
        
### remap {#remap}
   > 格式化字符串,生成sql语句.
   * Parameters: 
      * param
         * `_format` (Any): 格式化字符串
         * `mapping` (Any): 映射字典
      * keyword
         * `kwargs` (Any): 特化参数

        
### execute {#execute}
   > 执行sql语句.
   * Parameters: 
      * param
         * `conn` (Any): sql连接对象
         * `cur` (Any): sql游标对象
         * `res` (Any): 结果字典
         * `cmd` (Any): sql语句
      * keyword
         * `allow` (Any): 是否允许输出

        
### Field {#Field}
   > 字段类,通过仿位掩码类,实现自动处理.
   * Example: 

        >>> # Usage
   
        
   * value 
      > 处理多个来源的输入
      
        
   * result 
      > 获取处理结果
      
        
   * related 
      > 关联字段
      
        
### Base {#Base}
   > 实现单例模式,并提供属性.
   
        
### DB {#DB}
   
        
### Database {#Database}
   
        
   * show 
      > 显示数据库列表
      
        
   * use 
      > 切换数据库
      
        
   * create 
      > 创建数据库
      * Parameters: 
         * param
            * `dbName` (Any): 数据库名
         * keyword
            * `cfg` (Any): 数据库配置
            * `autoUse` (Any): 是否自动切换到新创建的数据库

        
   * drop 
      > 删除数据库
      * Parameters: 
         * param
            * `dbName` (Any): 数据库名
         * keyword
            * `cfg` (Any): 数据库配置

        
### py2sql {#py2sql}
   > 将python数据格式转换为sql数据格式.
   * Parameters: 
      * param
         * `data` (Any): python数据

        
### TB {#TB}
   
        
### Table {#Table}
   > 表操作类.
   
        
   * content 
      
        
   * table 
      
        
   * show 
      
        
   * describe 
      
        
   * create 
      > 创建表
   * Example: 
   
            >>> # Usage
      * Parameters: 
         * param
            * `tbName` (Any): 表名
         * keyword
            * `cfg` (Any): 表配置
            * `autoUse` (Any): 是否自动切换到新创建的表

        
   * drop 
      
        
   * insert 
      
        
   * select 
      
        
   * update 
      
        
   * alter 
      
        
   * delete 
      
        
   * toDataFrame 
      
        
   * toCSV 
      
        
   * fromCSV 
      
        
### MySQL {#MySQL}
   > MySQL操作类.
   * Example: 

        >>> # Usage
   
        
   * db 
      
        
   * tb 
      
        
   * database 
      
        
   * table 
      
        
