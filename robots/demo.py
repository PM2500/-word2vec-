#coding:utf-8
import requests
from lxml import etree
from concurrent import futures  #导入线程池包
import time
from random import randint


def proxyPool():  # 设置ip代理池
    ipList = [
        {'https': '223.215.177.3:4242'},
        {'https': '163.204.219.215:4242'},
        {'https': '117.88.5.227:3000'},
        {'https': '117.88.5.227:3000'},
        {'https': '60.191.11.229:3128'}
    ]
    length = ipList.__len__()
    rand = randint(0, length)
    proxy = ipList[rand]
    return proxy
def download(params):
    i=params[0]
    url=params[1]
    headers = {  # 设置header头
        "Host": "www.xsbiquge.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Referer": "https://www.xsbiquge.com/0_36/",
        "Cookie": "fikker-nSlQ-2Grw=bshKTixihW2kf7RJ6URQMu0EI3dIvNZs; fikker-nSlQ-2Grw=bshKTixihW2kf7RJ6URQMu0EI3dIvNZs",
    }
    proxy=proxyPool()
    print(url)
    response=requests.get(url=url, headers=headers,timeout=25)
    data=response.content
    #print(data)
    html = etree.HTML(data)
    contents = html.xpath('//div[@id="content"]/text()')
    #print(contents)
    with open('./text/剑王朝.txt','a',encoding='utf-8') as fp:
        fp.writelines('第{param}章\n'.format(param=i))
        for content in contents:
            content=content.replace('\xa0','')
            content=content.replace('\n','')
            content=content.replace('\r','')
            fp.writelines(content+'\n')
        fp.writelines('\n\n\n\n\n')
    print("第{param}章下载完成".format(param=i))


headers={  #设置header头
            "Host": "www.xsbiquge.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Referer": "https://www.haotxt.com/book/allvisit/0/1/",
            "Cookie":"fikker-nSlQ-2Grw=bshKTixihW2kf7RJ6URQMu0EI3dIvNZs; fikker-nSlQ-2Grw=bshKTixihW2kf7RJ6URQMu0EI3dIvNZs",
        }
url="https://www.xsbiquge.com/75_75921/"
response=requests.get(url=url,headers=headers,timeout=15)
data=response.content.decode('utf-8')
#print(data)
html=etree.HTML(data)
urls=html.xpath("//dd/a/@href")
lenth=urls.__len__()
mapList = []
tmp = 0
for i in range(0, lenth):
    url = "https://www.xsbiquge.com" + urls[i]  #需要对url进行拼接得到最终的url
    if i == lenth - 1:
        mapList.append((i,url))
        tmp = 8
    if tmp >= 8:
        tmp = 1  # 计数器归零
        executor = futures.ThreadPoolExecutor(max_workers=mapList.__len__())  # 建立20个线程下载图片
        result_list = executor.map(download, mapList)
        #for result in result_list:
            #print(result)
        mapList.clear()
        print("一轮下载完成，休眠5秒")
        time.sleep(3)
    else:
        mapList.append((i,url))
        tmp = tmp + 1