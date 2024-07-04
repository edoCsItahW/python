# API Documentation

   * [randomHeader](#randomHeader-randomHeader){.function}
   * [randomProxie](#randomProxie-randomProxie){.function}
   * [responses](#responses-responses){.class}
      * json{.function}
      * text{.function}
      * content{.function}
      * soup{.function}
   * [request](#request-request){.class}
      * Proxietest{.function}
      * getPostinfo{.function}
      * getRuninfo{.function}
      * sessioninfo{.function}
      * getsoup{.function}
      * getXpath{.function}
   * [autoBrowser](#autoBrowser-autoBrowser){.class}
      * runengine{.function}
      * checkweb{.function}
      * getHtml{.function}
      * getSoup{.function}
   * [translate_web](#translate_web-translate_web){.function}
   * [translate_single](#translate_single-translate_single){.function}
   * [translate_mutil](#translate_mutil-translate_mutil){.function}
### randomHeader {#randomHeader}
   > 随机获取请求头.
   * Parameters: 
      * param
         * `havehead` (bool): 是否带有"User-Agent"

        
### randomProxie {#randomProxie}
   > 随机获取代理地址.
   * Parameters: 
      * param
         * `protocol` (str): 协议名称.
      * keyword
         * `strtype` (bool): 是否为字符类,否则为字典.

        
### responses {#responses}
   > 一个数据类.
   
        
   * json 
      
        
   * text 
      
        
   * content 
      
        
   * soup 
      
        
### request {#request}
   > 简化并封装了requests的请求功能.
   
        
   * Proxietest 
      > 对代理池中的所有代理地址进行可用检测.
      * Parameters: 
         * param
            * `allowprint` (bool): 是否允许打印.

        
   * getPostinfo 
      > 获取post请求数据.
      
        
   * getRuninfo 
      > 获取get请求数据.
      
        
   * sessioninfo 
      > 获取会话请求数据.
      
        
   * getsoup 
      > 快捷获取BeautifulSoup类数据.
      
        
   * getXpath 
      > 快速放回Xpath类的数据.
      
        
### autoBrowser {#autoBrowser}
   
        
   * runengine 
      > selenium的driver引擎.
      * Parameters: 
         * param
            * `exepath` (str): 你的浏览器驱动器地址.(初次使用可能会自动下载,但地址需要自己寻找.)
            * `webtype` (str): 浏览器类型.
            * `hearless` (bool): 是否开启无头模式.

        
   * checkweb 
      
        
   * getHtml 
      
        
   * getSoup 
      
        
### translate_web {#translate_web}
   > 使用浏览器的无头模式对输入的文本进行翻译.
   * Parameters: 
      * param
         * `word` (str): 文本.
         * `driver` (Any): driver引擎.
         * `webtype` (str): 浏览器类型.
         * `mutil` (bool): 是否需要获得更多翻译.

        
### translate_single {#translate_single}
   > 使用简单的百度api进行翻译，
   * Parameters: 
      * param
         * `word` (str): 文本.
         * `banKWList` (list): 是否允许结果中出现文本的关联时态.
      * keyword
         * `allowName` (bool): 是否允许结果中出现人名.

        
### translate_mutil {#translate_mutil}
   > 从百度api获取翻译,但appid和appkey需要自行获取.
   * Parameters: 
      * param
         * `word` (str): 文本.
         * `from_lang` (str): 文本的语言
         * `to_lang` (str): 要翻译成的语言
      * keyword
         * `appid` (int): 软件id
         * `appkey` (str): 软件密钥

        
