# -*-coding:utf-8 -*-
'''
time：2020-3-10
novel类主要用于爬取小说，作为w2v的训练语料，爬取网站：https://www.xsbiquge.com
爬取方式采用多进程爬取小说，多线程下载小说内容
'''
from multiprocessing import Process,Pool  #导入多进程包
from concurrent import futures  #导入线程池包
from time import sleep,time
from lxml import etree  #标签解析
import requests
import os
class novel:
    def __init__(self):
        self.range=100
        self.start=80
        self.thread=9  #下载时开辟的线程数
        self.headers={  #设置header头
            "Host": "www.xsbiquge.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Referer": "https://www.xsbiquge.com/75_75921/",
            "Cookie":"fikker-nSlQ-2Grw=bshKTixihW2kf7RJ6URQMu0EI3dIvNZs; fikker-nSlQ-2Grw=bshKTixihW2kf7RJ6URQMu0EI3dIvNZs",
        }

    def proxyPool(self):#设置ip代理池   如果存在IP限制，可以通过随机代理的方式进行bypass
        ipList=[
            {'https': '117.88.5.227:3000'},
            {'https': '117.88.5.227:3000'},
            {'https': '60.191.11.229:3128'},
            {'https': '121.33.220.158:808'},
            {'https': '115.171.85.114:9000'},
            {'https': '218.2.226.42:80'},
            {'https': '112.64.233.130:9991'}
        ]
        length=ipList.__len__()
        from random import randint
        rand=randint(0,length)
        proxy=ipList[rand]
        return proxy

    def getNovel(self):  #获取可爬取小说列表
        url="https://www.xsbiquge.com/0_{param}/"
        count=0  #循环计数器
        tmpList=[]  #临时存储小说链接和名字
        for i in range(self.start,self.range):
            finalUrl=url.format(param=str(i))
            try:
                response=requests.get(url=finalUrl,headers=self.headers,timeout=5)  #设置超时时间为5秒
                data=response.content.decode('utf-8')
                if response.status_code==200:
                    html = etree.HTML(data)
                    #novelUrl = html.xpath("//tr/td[1]/a/@href")  #获取链接
                    novelName=html.xpath("//h1/text()")  #获取名字
                    tmpList.append((finalUrl,novelName[0]))  #合并两个列表，拼接成数据组
                else:
                    if count < 3:  # 如果请求出错，重新进行三次请求
                        i = i - 1
                        continue
                    else:
                        count = 0
                        continue
            except:
                if count<3:  #如果请求出错，重新进行三次请求
                    i=i-1
                    continue
                else:
                    count=0
                    continue
        print("小说url与名称全部获取完毕，共%d本小说"% tmpList.__len__())
        return tmpList

    def getChapterUrl(self,param):   #获取章节信息
        print(param)
        url=param[0]  #获取url
        name=param[1] #获取小说名
        self.headers['Referer']=url  #设置请求头的Referer
        ###创建文本存储###
        path = r"./text/" + name + ".txt"  #设置存储路径
        if os.path.exists(path):
            os.remove(path)
            print("将自动创建文件")
        else:
            pass
        ##################
        try:
            response=requests.get(url=url,headers=self.headers,timeout=5)  #发送请求获取全部章节页面
            data = response.content.decode('utf-8')
            html = etree.HTML(data)
            urls = html.xpath("//dd/a/@href")   #xpath解析获取全部章节url
            lenth = urls.__len__()  #长度
            mapList = []
            tmp = 0
            for i in range(0, lenth):
                url = "https://www.xsbiquge.com" + urls[i]  #需要对url进行拼接得到最终的url
                if i == lenth - 1:
                    mapList.append((i,url,path))
                    tmp = self.thread
                if tmp >= self.thread:
                    tmp = 1  # 计数器归零
                    executor = futures.ThreadPoolExecutor(max_workers=mapList.__len__())  # 建立个线程下载小说
                    result_list = executor.map(self.getNovelContent, mapList)
                    mapList.clear()
                    print("小说{name}一轮章节下载完成，休眠5秒".format(name=name))
                    sleep(5)
                else:
                    mapList.append((i,url,path))
                    tmp = tmp + 1
            return True
        except:
            return False

    def getNovelContent(self,params):  #下载小说具体内容
        i = params[0]
        url = params[1]
        path=params[2]
        try:
            response = requests.get(url=url, headers=self.headers,timeout=15, verify=False)
            data=response.content
            html = etree.HTML(data)
            contents = html.xpath('//div[@id="content"]/text()')
            with open(path, 'a', encoding='utf-8') as fp:
                fp.writelines('第{param}章\n'.format(param=i))
                for content in contents:
                    content = content.replace('\xa0', '')
                    content = content.replace('\n', '')
                    content = content.replace('\r', '')
                    fp.writelines(content + '\n')
                fp.writelines('\n\n\n\n\n')
            print("第{param}章下载完成".format(param=i))
        except:
            return False

if __name__ == '__main__':
    novels=novel()
    #########首先获取要下载的小说链接和名称#############
    hrefs=novels.getNovel()
    print("3秒后开始下载小说")
    sleep(3)
    print("下载开始")
    print("=" * 40)
    #length = hrefs.__len__()
    ###################################################
    ##############多进程获取全部章节####################
    pool=Pool(2)  #开辟进程池
    for href in hrefs:
        nextOne=pool.apply_async(novels.getChapterUrl, args=(href,))
        sleep(1)
    pool.close() #关闭进程池
    pool.join()  #阻塞父进程，等待全部子进程结束
    sleep(5)
    print("全部下载完成")
    '''
    try:
        for i in range(0, length,2):
            if hrefs.__len__()>2:
                param1=hrefs.pop()
                param2=hrefs.pop()
                first = Process(target=novels.getChapterUrl, args=(param1,))
                second=Process(target=novels.getChapterUrl,args=(param2,))
                first.start()
                second.start()
                first.join()
                second.join()
                first.close()
                second.close()
            else:
                print("列表为空")
                pass
    except:
        print("列表为空")
        pass
    ###################################################
    print("全部下载完成")
    '''