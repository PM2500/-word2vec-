# -*-coding:utf-8 -*-
'''
time：2020-3-10
novel类主要用于爬取小说，作为w2v的训练语料，爬取网站：https://www.haotxt.com/book/allvisit/0/1/
爬取方式采用多进程爬取小说，多线程下载小说内容
爬取本站小说存在反扒措施，需要使用代理ip进行反扒绕过
'''
from multiprocessing import Process  #导入多进程包
from concurrent import futures  #导入线程池包
from time import sleep,time
from lxml import etree  #标签解析
import requests
import os
class novel:
    def __init__(self):
        self.range=2   #小说爬取的页数，一页存在30本小说
        self.headers={  #设置header头
            "Host": "www.haotxt.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Referer": "https://www.haotxt.com/book/allvisit/0/1/",
            "Cookie":"fikker-nSlQ-2Grw=bshKTixihW2kf7RJ6URQMu0EI3dIvNZs; fikker-nSlQ-2Grw=bshKTixihW2kf7RJ6URQMu0EI3dIvNZs",
        }

    def proxyPool(self):#设置ip代理池
        ipList=[
            {'https': '117.88.5.227:3000'},
            {'https': '117.88.5.227:3000'},
            {'https': '60.191.11.229:3128'},
            {'https': '121.33.220.158:808'},
            {'https': '115.171.85.114:9000'},
            {'https': '218.2.226.42:80'},
            {'https': '112.64.233.130:9991'},
            {'https': '182.18.13.149:53281'},
            {'https': '182.18.13.149:53281'},
            {'https': '210.5.10.87:53281'},
            {'https': '117.88.176.5:3000'},
            {'https': '117.88.176.5:3000'},
            {'https': '117.88.176.186:3000'},
            {'https': '117.88.176.186:3000'},
            {'https': '203.110.164.139:52144'},
            {'https': '203.110.164.139:52144'},
        ]
        length=ipList.__len__()
        from random import randint
        rand=randint(0,length)
        proxy=ipList[rand]
        return proxy

    def getNovel(self):  #获取可爬取小说列表
        url="https://www.haotxt.com/book/allvisit/0/"
        count=0  #循环计数器
        tmpList=[]  #临时存储小说链接和名字
        for i in range(1,self.range):
            finalUrl=url+str(i)+'/'  #拼接url
            try:
                response=requests.get(url=finalUrl,headers=self.headers,timeout=5)  #设置超时时间为5秒
                data=response.content.decode('gbk')
                if response.status_code==200:
                    html = etree.HTML(data)
                    novelUrl = html.xpath("//tr/td[1]/a/@href")  #获取链接
                    novelName=html.xpath("//tr/td[1]/a/text()")  #获取名字
                    tmpList.append(list(zip(novelUrl,novelName)))  #合并两个列表，拼接成数据组
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
        hrefs=[]
        for tmp in tmpList:
            hrefs.extend(tmp)  #重新整理，将全部小说链接放进list当中
        print("小说url与名称全部获取完毕，共%d本小说"% hrefs.__len__())
        return hrefs

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
            data = response.content.decode('gbk')
            html = etree.HTML(data)
            urls = html.xpath("//td[@class='ccss']/a/@href")   #xpath解析获取全部章节url
            lenth = urls.__len__()  #长度
            mapList = []
            tmp = 0
            for i in range(0, lenth):
                url = "https://www.haotxt.com" + urls[i]  #需要对url进行拼接得到最终的url
                if i == lenth - 1:
                    mapList.append((i,url,path))
                    tmp = 3
                if tmp >= 3:
                    tmp = 1  # 计数器归零
                    executor = futures.ThreadPoolExecutor(max_workers=mapList.__len__())  # 建立20个线程下载小说
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
        #try:
        proxy=self.proxyPool()
        response = requests.get(url=url, headers=self.headers,proxies=proxy,timeout=5,verify=False)
        print(response)
        data = response.content.decode('gbk')
        print(data)
        html = etree.HTML(data)
        contents = html.xpath('//div[@id="content"]/text()')
        with open(path, 'a', encoding='gbk') as fp:
            fp.writelines('第{param}章\n'.format(param=i))
            for content in contents:
                content = content.replace('\xa0', '')
                content = content.replace('\n', '')
                content = content.replace('\r', '')
                fp.writelines(content + '\n')
            fp.writelines('\n\n\n\n\n')
        print("第{param}章下载完成".format(param=i))
       # except:
           # return False

if __name__ == '__main__':
    novels=novel()
    #########首先获取要下载的小说链接和名称#############
    hrefs=novels.getNovel()
    print("3秒后开始下载小说")
    sleep(3)
    print("下载开始")
    print("=" * 40)
    length = hrefs.__len__()
    ###################################################
    ##############多进程获取全部章节####################
    cpu_count = os.cpu_count()  # 用于设置进程池大小
    for i in range(0, length,2):
        try:
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
        except:
            pass
    ###################################################
    print("全部下载完成")