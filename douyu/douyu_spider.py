'''
Author: MGod_wu
Date: 2021-02-05 21:59:04
LastEditTime: 2021-02-18 15:23:00
Description: 获取斗鱼所有的直播间数据(包括直播间名，主播名，直播类型，人气值)，
    数据将会以json格式存储到./result/datas.json，模块还会根据爬取到的直播间名和
    直播内容出现的文字频率生成对应的词云图片直播间名,直播内容，当前直播内容的流行程度一览无遗
FilePath: /VScode_Worker/Spider/douyu_spider.py
'''
from proxies import proxies
from analys import analys_of_data
from time import time,sleep,strftime,localtime
from os import mkdir,path
from jsonpath import jsonpath
from json import loads,dumps
from requests import get
from lxml.html import etree
from wordcloud import WordCloud,STOPWORDS
import jieba

# url = 'https://www.douyu.com/gapi/rkc/directory/mixList/0_0/' + '页数'

# url = 'https://www.douyu.com/directory/all'

# 全局变量
font_path = r'C:\Windows\Fonts\STXINGKA.TTF'  # 词云所用字体路径
data_path = r'./result'  # 存储数据的路径
is_show_wc = False # 是否展示词云

# 1,初始化爬虫，创建目录
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}

px = proxies()
if px.result_code:
    print('='*50 +'\n正在使用代理：\n' + px.proxies['http'] + '\n' + px.proxies['https'] + '\n' +'='*50)
else:
    print('='*50 +'\n无法获取到有效代理，转换为无代理模式(无代理模式爬取过程稍慢，请耐心等待)\n' + '='*50)

if not path.exists(data_path):
    mkdir(data_path)
get_date = strftime('[%y%m%d]', localtime(time()))
get_time = strftime('_%H%M%S', localtime(time()))
# 2,获取网页总页数(网页总数是由js动态生成的，无法直接获取)
# page_url = 'https://www.douyu.com/directory/all'
# page_resp = get(url=page_url,headers=headers,proxies=px,timeout=5)
# print(page_resp.text)
# # etr = etree.HTML(page_resp.text)
# # page_num = etr.xpath("//ul[@class='dy-Pagination ListPagination']/li[last()-1]")
# # print(page_num)

# 3，获取每个直播间的内容（包括直播间名，主播名，主播人气，主播分类）
try:
    datas = list()
    start_time = time()
    for num in range(1,400):
        url = 'https://www.douyu.com/gapi/rkc/directory/mixList/0_0/' + str(num)
        print('正在从<' + url + '>获取数据！' + '----当前页:' + str(num))
        try:
            if px.result_code:
                response = get(url,headers=headers,proxies=px.proxies,timeout=5)
            else:
                response = get(url,headers=headers,timeout=5)   # 代理ip太多失效的话，只能选择不用代理
                sleep(1)
        except Exception:
            px.reset()  # 当访问不成功时，重置代理ip
            print('='*50 +'\n代理已失效，成功更换代理：\n' + px.proxies['http'] + '\n' + px.proxies['https'] + '\n' + '='*50)
            response = get(url,headers=headers,proxies=px.proxies,timeout=5)
        json_data = loads(response.text)
        if int(json_data['data']['pgcnt']) < num: # 判断网页是否溢出
            break
        else:
            try:
                sudio_name_list = jsonpath(json_data, '$..rn')  # 直播间名称
                name_list = jsonpath(json_data, '$..nn')    # 主播名
                popularity_list = jsonpath(json_data, '$..ol') # 主播人气值
                type_list = jsonpath(json_data, '$..c2name')    # 分类
                for i in range(len(sudio_name_list)):
                    data = dict()
                    data['sudio_name'] = sudio_name_list[i]
                    data['name'] = name_list[i]
                    data['popularity'] = popularity_list[i]
                    data['type'] = type_list[i]
                    datas.append(data)
                end_time = time()
                print('>>>成功获取到' + str(len(sudio_name_list)) + '条数据，总耗时{' + str(end_time-start_time) + '}s')
            except Exception as err:
                with open('./result/error.log', 'a', encoding='utf-8') as fp:
                    fp.write(f'[{strftime("%y/%m/%d    %H:%M:%S %a", localtime(time()))}]\n发生错误：{err}\n')
                continue

    print('\n\n>>>已从网站上成功获取到了<' + str(len(datas)) + '>位主播信息！总耗时{' + '{:d}'.format(int((end_time-start_time)/60))
                        + 'm' + str((int(end_time-start_time))%60) +'s}')

    # 4，生成词云信息并展示出来
    wc = WordCloud(
        background_color='black',  # 背景设置为黑色
        font_path=font_path,  # 字体
        max_words=300,  # 最大显示的关键词数量
        stopwords=STOPWORDS,  # 使用上面导入停用词表
        max_font_size=300,  # 最大字体
        random_state=30,  # 设置随机状态数，及配色的方案数
        width=1080,
        height=960,  # 如果使用默认图片，则可以设置高
        margin=2,  # 图片属性
        collocations=False,  # 是否包括两个词的搭配
    )
    sudio_str = ''.join(data['sudio_name'].replace('\n','') for data in datas)
    sudio_list = jieba.cut(sudio_str)   # 分解词组
    sudio_name = '/'.join(sudio_list)
    wc.generate(sudio_name) # 生成词云
    wc.to_file(f'{data_path}/sudio.png')
    if is_show_wc:
        sudio_img = wc.to_image()
        sudio_img.show(title='sudio_wordcloud')

    type_name = '/'.join(data['type'].replace('\n','') for data in datas)
    wc.generate(type_name)
    wc.to_file(f'{data_path}/type.png')
    if is_show_wc:
        type_img = wc.to_image()
        type_img.show(title='type_wordcloud')

    # 5，分析数据并生成对应的图表
    analys_of_data(datas=datas)

    # 6，将所有主播信息转换为字典并存储在json文件中
    all_datas = dict()
    all_datas[f'datas{get_time}'] = datas
    with open(f'{data_path}/datas{get_date}.json', 'a') as fp:
        fp.write(dumps(all_datas))

except Exception as err:
    with open('./result/error.log', 'a', encoding='utf-8') as fp:
        fp.write(f'[{strftime("%y/%m/%d    %H:%M:%S %a" , localtime(time()))}]\n发生错误：{err}\n')

