#coding:utf-8
'''
代理池生成模块，使用新爬虫不需要代理池
'''
import requests
from lxml import etree
import re

url="https://www.xicidaili.com/wn/3"
headers = {  # 设置header头
        "Host": "httpbin.org.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Referer": "https://www.haotxt.com/book/allvisit/0/1/",
        "Cookie": "fikker-nSlQ-2Grw=bshKTixihW2kf7RJ6URQMu0EI3dIvNZs; fikker-nSlQ-2Grw=bshKTixihW2kf7RJ6URQMu0EI3dIvNZs",
    }
response=requests.get(url=url,headers=headers)
data=response.content.decode()
with open("./2.html",'w',encoding='utf-8') as fp:
    fp.writelines(data)
iplist=[]
ips=re.findall(r'<td\sclass="country">.*\s+<td>(.*?)</td>\s+<td>(.*?)</td>',data)
for ip,port in ips:
    iplist.append({"https":ip+':'+port})
print(iplist)
url="https://httpbin.org/ip"
lists=[]
for proxy in iplist:
    for i in range(2):
        try:
            response = requests.get(url=url, headers=headers, proxies=proxy,timeout=15, verify=False)
            if response.status_code==200:
                print(response.content)
                print(proxy)
                lists.append(proxy)
                print("有效")
            else:
                #print(response.text)
                print(proxy)
                print("失效")
        except:
            print(proxy)
            print("失效")
print(lists)
'''
[{'https': '117.88.5.227:3000'}, {'https': '117.88.5.227:3000'}, {'https': '60.191.11.229:3128'}, {'https': '121.33.220.158:808'}, {'https': '115.171.85.114:9000'}, {'https': '218.2.226.42:80'}, {'https': '112.64.233.130:9991'}]
[{'https': '182.109.91.85:4213'}, {'https': '182.109.91.85:4213'}, {'https': '223.242.175.19:4227'}, {'https': '223.242.175.19:4227'}, {'https': '111.75.117.176:4225'}, {'https': '111.75.117.176:4225'}, {'https': '117.91.249.172:4264'}, {'https': '117.91.249.172:4264'}, {'https': '58.243.205.46:4243'}, {'https': '58.243.205.46:4243'}, {'https': '221.10.34.242:4255'}, {'https': '221.10.34.242:4255'}, {'https': '112.85.45.40:4217'}, {'https': '112.85.45.40:4217'}, {'https': '112.85.161.46:4250'}, {'https': '112.85.161.46:4250'}, {'https': '175.154.202.125:4278'}, {'https': '175.154.202.125:4278'}, {'https': '106.111.228.246:4203'}, {'https': '106.111.228.246:4203'}, {'https': '60.188.62.220:4257'}, {'https': '60.188.62.220:4257'}, {'https': '42.54.83.14:4252'}, {'https': '183.146.221.71:4274'}, {'https': '183.146.221.71:4274'}, {'https': '113.78.64.41:4283'}, {'https': '113.78.64.41:4283'}, {'https': '113.78.64.98:4283'}, {'https': '113.78.64.98:4283'}, {'https': '125.109.193.120:4260'}, {'https': '125.109.193.120:4260'}, {'https': '112.84.98.112:4278'}, {'https': '112.84.98.112:4278'}, {'https': '58.252.200.208:4261'}, {'https': '58.252.200.208:4261'}]

'''