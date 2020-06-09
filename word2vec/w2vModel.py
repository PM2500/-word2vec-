#-*- coding:utf-8 -*-
'''
time：2020-4-10
word2vec模型训练类
用于将下载的语料导入word2vec进行模型训练
并且最后导出训练模型用于下一步摘要分析
'''
from gensim.models import word2vec
import os,logging
logging.basicConfig(format='%(acstime)s : %(levelname)s : %(message)s',level=logging.INFO)

class w2vModel():
    def __init__(self):
        #初始化训练模型的相关变量
        self.path="./result1.txt"    #分词语料存储位置
        self.modelPath="./model/result.model"   #模型存储位置
        self.modelPathBin="./model/result.bin"   #模型存储位置
        self.size=500          #词向量维度，默认值100，与语料大小有关，语料越大维度建议加大
        self.window=5          #上下文距离
        self.sg=0              #训练模型算法，0表示CBOW模型，1则是Skip-Gram模型
        self.hs=1               #word2vec两个解法的选择,0是Negative Sampling，1的话并且负采样个数negative大于0,则是Hierarchical Softmax
        self.negative=10        #即使用Negative Sampling时负采样的个数
        self.cbow_mean=0
        self.min_count=25      #计算词向量的最小词频,可以起到语料清洗的作用
        self.iter=10            #随机梯度下降法中迭代的最大次数，默认是5。对于大语料，可以增大这个值

    def _getSentences(self,path):  #训练语料获取类
        sentences=word2vec.LineSentence(path)
        return sentences


    def _modelTrain(self):   #模型训练类
        sentence=self._getSentences(self.path)
        models=word2vec.Word2Vec(
            size=self.size,
            window=self.window,
            sg=self.sg,
            hs=self.hs,
            negative=self.negative,
            min_count=self.min_count,
            iter=self.iter,
            workers=os.cpu_count()
        )
        models.build_vocab(sentence)
        models.train(sentences=sentence,total_examples=models.corpus_count,epochs=models.iter)
        models.save(self.modelPath)
        models.wv.save_word2vec_format(self.modelPathBin,binary=True)

    def start(self):
        self._modelTrain()

class textHandle():
    def __init__(self):
        self.path="./text/"
        self.storePath='./result1.txt'  #语料存储位置

    def dataHandle(self):
        fp=open(self.storePath,'a+',encoding='utf-8')
        files = os.listdir(self.path)  # 获取全部样本数据
        print("样本目录读完毕，一共{num}个样本语料。".format(num=files.__len__()))
        for fileName in files:
            filePath = self.path + fileName
            with open(filePath,'r',encoding='utf-8') as f:
                lines=f.readline()
                while lines:
                    if lines.strip('\n'):
                        fp.writelines(lines)
                    else:
                        pass
                    lines = f.readline()
            print(fileName+"写入语料文本")
        return True

if __name__ == '__main__':
    handles=textHandle()
    if handles.dataHandle():
        print("全部语料写入完毕，开始模型训练")
        w2vmodel = w2vModel()  # 实例化训练类
        w2vmodel.start()