'''
Author: MGod-wu
Date: 2021-02-05 15:57:57
Description: 获取代理ip，防止使用本地ip爬虫过度而被官方封禁
(但免费的代理ip是真滴不好用啊！！！)
'''
from PIL import Image
from requests import get
from lxml.html import etree
from io import BytesIO
import pytesseract


# 米扑代理获取免费ip的url，当url失效时，请尝试更换url
url = 'https://proxy.mimvp.com/freesecret?proxy=in_hp&sort=&page=1'
# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}


class proxies(object):
    def __init__(self):
        self.url = url
        self.headers = headers
        self.result_code = 0
        self.proxies = dict()
        self.init_proxies()
    
    def init_proxies(self):
        try:
            # 1,获取网页源码
            response = get(url, headers=headers, timeout=10)
            # 2，解析源码，获取到 代理ip，端口图片url
            etr = etree.HTML(response.text)
            ip_list = etr.cssselect('tbody .free-proxylist-tbl-proxy-ip')
            img_list = etr.cssselect('.free-proxylist-tbl-proxy-port>img')
            for ip,img in zip(ip_list,img_list):
                img_url = 'https://proxy.mimvp.com' + img.attrib['src']
                port_str = self.get_img_str(img_url=img_url)
                # 'http': 'http://220.186.160.157:29389'
                self.proxies['http'] = 'http://' + ip.text + ':' + port_str
                # 'https': 'https://220.186.160.157:29389'
                self.proxies['https'] = 'https://' + ip.text + ':' + port_str
                try:
                    # 简单判断代理是否可用
                    print('正在尝试代理--',self.proxies)
                    get('https://www.baidu.com', proxies=self.proxies)
                    self.result_code = 1
                    break
                except Exception:
                    self.proxies = dict()
                    continue
        except Exception:
            self.result_code = 0
    
    # Image库+pytesserat库识别图片端口，获取到文本端口号
    def get_img_str(self, img_url):
        img = Image.open(BytesIO(get(img_url).content))     # 直接通过requests库获取到图片的二进制文件，从而读取
        return pytesseract.image_to_string(image=img).strip().strip(',')    # 对识别出来的字符串进行格式化

    # 重置代理池
    def reset(self):
        try:
            # 1,获取网页源码
            response = get(url, headers=headers, timeout=10)
            # 2，解析源码，获取到 代理ip，端口图片url
            etr = etree.HTML(response.text)
            ip_list = etr.cssselect('tbody .free-proxylist-tbl-proxy-ip')
            img_list = etr.cssselect('.free-proxylist-tbl-proxy-port>img')
            for ip,img in zip(ip_list,img_list):
                ip_str = ip.text
                img_url = 'https://proxy.mimvp.com' + img.attrib['src']
                port_str = self.get_img_str(img_url=img_url)
                # 'http': 'http://220.186.160.157:29389'
                self.proxies['http'] = 'http://' + ip_str + ':' + port_str
                # 'https': 'https://220.186.160.157:29389'
                self.proxies['https'] = 'https://' + ip_str + ':' + port_str
                try:
                    # 简单判断代理是否可用
                    get('https://www.baidu.com', proxies=self.proxies)
                    self.result_code = 1
                    break
                except Exception:
                    continue
        except Exception:
            self.result_code = 0

