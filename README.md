<!--
 * @Author: your name
 * @Date: 2021-02-07 19:37:16
 * @LastEditTime: 2021-02-07 21:35:54
 * @LastEditors: your name
 * @Description: In User Settings Edit
 * @FilePath: /VScode_Worker/Spider/Data-Viual/README.md
-->
## 数据分析参考小案例

> 自学数据分析可视化，开源小案例

目前已完成：
- [数据分析参考小案例](#数据分析参考小案例)
  - [斗鱼直播人气分析](#斗鱼直播人气分析)
    - [成品展示](#成品展示)





------
### 斗鱼直播人气分析

所用到的第三方库：

- `jieba`：优秀的中文语句断句开源库
- `requests`: 史上最好用的爬虫包
- `lxml`：网页解析利器
- `jsonpath`: 用于解析json数据
- `wordcloud`：优秀的词云开源库
- `pyecharts`：百度史上最良心的数据可视化开源库
- `PIL`：python最常用的图像处理库
- `pytesseract`：好用的OCR开源库

资源：`./douyu_simple`

- `proxies.py`：获取代理ip，防止使用本地ip爬虫过度而被官方封禁(但免费的代理ip是真滴不好用啊！！！)
- `analys.py`: 数据分析及可视化，可生成[前25位人气主播分析网页](#前25位)，[直播类型平均人气值排名网页](#平均)，[主播人气值与数量关系网页](#人气值&数量)，生成的网页数据均在`./result`目录下
- `douyu_spider,py`(main): 获取斗鱼所有的直播间数据(包括直播间名，主播名，直播类型，人气值)，数据将会以json格式存储到`./result/datas.json`，模块还会根据爬取到的[直播间名](#词云1),[直播内容](#词云2)和直播内容出现的文字频率生成对应的词云图片，当前流行的直播内容一览无遗

#### 成品展示

- [<img id="前25位" src="https://i.loli.net/2021/02/07/LvMhUFnRac5uy7Z.png">](#)
------
- [<img id="平均" src="https://i.loli.net/2021/02/07/Ht5FEPeiGmjJfd3.png">](#-1)
------
- [<img id="人气值&数量" src="https://i.loli.net/2021/02/07/kSDwoLu1biOmBcT.png">](#-2)
------
- [<img src="https://i.loli.net/2021/02/07/7xzRkDehQMACtWS.png">](#-3)
------
- [<img id="词云1" src="https://i.loli.net/2021/02/07/1n7VusyJO2Gjg3r.png">](#-4)
-------
- [<img id="词云2" src="https://i.loli.net/2021/02/07/s6dU3jTCyRY4Dfc.png">](#-4)

