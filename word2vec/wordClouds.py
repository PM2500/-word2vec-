#-*- coding:utf-8 -*-
'''
time：2020-3-25
词云生成程序
调用wordCloud包
用于读取全部语料资料，并生成词云
可以控制词频个数等等
'''
from collections import Counter  #词频计数
from wordcloud import WordCloud, ImageColorGenerator  #词云包
import numpy as np
import matplotlib.pyplot as plt  #可视化
from PIL import Image
from os import listdir
from random import randint
from multiprocessing import Pool
from time import sleep

class wordClouds:
    def __init__(self):
        self.picPath='./img/'  #词云模型照片库
        self.wdPath="./wd/"  #词云存储库
        self.wordResult='./text/'  #分词库
        self.count=500   #词云个数，打印词频最高的前500个
        self.scale=4    # 词云比列放大  数值越大  词云越清晰

    def _getPic(self):  #随机生成词云图片
        pngs=listdir(self.picPath)
        count=pngs.__len__()
        return self.picPath+pngs[randint(0,count-1)]

    def _wdCreate(self,wordDict,path):  #生成词云
        storePath=self.wdPath+path+'.png'
        imgPath=self._getPic()  #get picture path of wordCloud
        img = np.array(Image.open(imgPath))   #open zhe picture
        wc = WordCloud(
            background_color="white", #背景颜色
            mask=img,
            max_words=self.count,  # 显示最大词数
            font_path=r"C:\Windows\Fonts\STXINGKA.TTF",  # 使用字体
            min_font_size=10,
            max_font_size=50,
            scale=self.scale,  # 比列放大  数值越大  词云越清晰
            # width=1680,  #图幅宽度
            # height=1050,
            random_state=50,
            relative_scaling=False,
        ).generate_from_frequencies(wordDict)
        # 绘制文字的颜色以背景图颜色为参考
        image_color = ImageColorGenerator(img)
        # 结合原图色彩
        wc.recolor(color_func=image_color)
        plt.figure()  # 创建图像
        plt.imshow(wc, interpolation="bilinear")
        # 关闭坐标轴
        plt.axis("off")
        plt.show()
        # 保存图片
        wc.to_file(storePath)
        return True

    def wordHandle(self,path):  #分词处理，获取词频最高的词
        print("文件{param}开始处理".format(param=path))
        rePath=self.wordResult+path
        words=[]
        with open(rePath,'r',encoding='utf-8') as fp:
            try:
                for x in fp.readlines():
                    pairs = x.split(' ')
                    for pair in pairs:
                       words.append(pair)
                counts = Counter(words).most_common(self.count)
                attrDict = {}
                for word, frequency in counts:
                    attrDict[word] = frequency  #转换为频率字典

                #生成词云图片
                if self._wdCreate(attrDict,path):
                    print("Success")
            except:
                print("{path}文件存在错误无法生成词云".format_map(path=path))
                pass


if __name__ == '__main__':
    wds=wordClouds()  #创建词云对象
    rePath=wds.wordResult  #获取语料存储地址
    pool = Pool(2)  # 开辟进程池
    files = listdir(rePath)  # 获取全部样本数据
    print("样本目录读完毕，一共{num}个样本语料。".format(num=files.__len__()))
    for fileName in files:
        nextOne = pool.apply_async(wds.wordHandle, args=(fileName,))
        sleep(1)
    pool.close()  # 关闭进程池
    pool.join()  # 阻塞父进程等待全部子进程结束
    sleep(5)
    print("全部词云生成完毕")