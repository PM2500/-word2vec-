#coding:utf-8
'''
time：2020-3-20
分词处理程序
对爬取的语料进行数据清洗与分词处理
之后可以用于词云生成和语料训练
'''
import re,os
import jieba  #结巴分词包
from multiprocessing import Pool,Manager
from time import sleep
class dataClean():
    def __init__(self):
        self.flag=1   #定义用于不同语料的存储
        # step 1 读取停用词
        self.stop_words = []
        with open('./StopWords.txt', encoding='utf-8') as f:
            line = f.readline()
            while line:
                self.stop_words.append(line[:-1])
                line = f.readline()
        self.stop_words=list(set(self.stop_words))
        print('停用词读取完毕，共{n}个单词'.format(n=len(self.stop_words)))

    def setFlag(self,flag):
        self.flag=flag   #为flag赋值

    def _jiebaHandle(self,lines):  #结巴分词处理
        jieba.load_userdict("./newWords.txt")
        if lines.__len__():
            tmpList=jieba.lcut(lines,cut_all=False)  #精确模式进行分词,返回列表格式
            if tmpList.__len__():
                return tmpList
            else:
                return None
        else:
            return None

    def reHandle(self,lines):  #正则表达式处理
        lines=re.sub(r'\\u.{4}','',lines.__repr__())  #用于去除乱码，通过获取原始编码，去除乱码部分
        lines=re.sub('第\d*章','\n',lines)  #去掉章节头部
        lines=re.sub('ps.*','\n',lines,flags=re.IGNORECASE) #匹配末尾的提示
        lines=re.sub('\s*','',lines)  #去特殊字符
        lines=re.sub('\.',"",lines)   #去掉.
        lines=re.sub('[a-z0-9A-Z]','',lines,flags=re.IGNORECASE)   #匹配字母数字下划线
        lines=re.sub('[_]','',lines,flags=re.IGNORECASE)   #匹配字母数字下划线
        return lines

    def stopWords(self,lines,storePath):  #停用词处理
        if lines.__len__():
            wordsList=self._jiebaHandle(lines)  #利用结巴分词返回分词结果
            rawList=[]
            for word in wordsList:
                if word not in self.stop_words:
                    rawList.append(word)
                else:
                    pass
            wordsList.clear()
            with open(storePath,'a',encoding='utf-8') as fp:
                for word in rawList:
                    fp.writelines(word+' ')
                fp.writelines('\n')
            print(".",end='')
            return True
        else:
            return None
    def start(self,path):
        #需要处理一下路径，提取文件名用于保存数据清洗结果
        names=path.split('/')
        name=names[-1:][0].split('.')[0]
        if self.flag:
            storePath="./text/"+name+"_result.txt"  #模型训练语料存储
        else:
            storePath="./specimen/"+name+"_result.txt" #摘要样本语料存储位置
        print(storePath)
        if os.path.exists(storePath):
            os.remove(storePath)
            print("将自动创建文件")
        else:
            pass
        with open(path,'r',encoding='utf-8') as fp:
           lines=fp.readline()
           while lines:
               lines=self.reHandle(lines)
               lines=self.stopWords(lines,storePath)
               if lines==True:
                   lines=fp.readline()
               else:
                   lines=fp.readline()

if __name__ == '__main__':#使用多进程方式进行语料处理，但是由于分词之间需要具有逻辑关系，因此需要控制推进顺序，不方便采用多线程方式
    path=r'../robots/text/'  #定义样本语料目录
    pool=Pool(2)   #开辟进程池
    data=dataClean()   #初始化数据清洗类
    files=os.listdir(path)  #获取全部样本数据
    print("样本目录读完毕，一共{num}个样本语料。".format(num=files.__len__()))
    for fileName in files:
        filePath=path+fileName
        #print("\n文件{param}开始数据清洗".format(param=fileName))
        nextOne=pool.apply_async(data.start,args=(filePath,))
        sleep(1)
    pool.close()  #关闭进程池
    pool.join()  #阻塞父进程等待全部子进程结束
    sleep(5)
    print("全部语料清洗完毕")