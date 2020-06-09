#-*- coding:utf-8 -*-
'''
time：2020-4-15
摘要生成算法
通过textRank算法实现摘要的生成
'''
import jieba  #用于摘要样本分词处理
import math
from heapq import nlargest  #寻找最大最小
from itertools import product, count
from gensim.models import Word2Vec
import numpy as np
np.seterr(all='warn')

class specimenHandle():#样本数据处理
    '''
    关于摘要样本的处理，与语料样本存在差异，
    摘要样本是不需要进行标点符号的去停用词等等
    因为这些会在摘要的生成当中产生作用，所以重写样本处理类。
    '''
    def __init__(self,model):
        self.model=model  #加载导入的模型变量
        str = '还'
        if str not in model.wv.index2entity:
            print(True)
        else:
            print(False)

    def cutSentences(self,sentence):  #句子处理
        '''
        对于摘要样本，要对每一个句子进行分词，然后对单个句子进行停用词处理
        判断每一个单词是否在模型当中
        :param sentence:
        :return:
        '''
        punctuation=frozenset(u'。！？')  #根据标点判断一个句子是否结束
        tmpList=[]
        for item in sentence:
            tmpList.append(item)
            if punctuation.__contains__(item):
                yield "".join(tmpList)   #一句话处理结束，将其返回。
                tmpList=[]
        yield "".join(tmpList)

    def stopWord(self):
        '''
        返回停用词，因为摘要样本和训练样本不同，因此停用词处理存在区别
        :return:
        '''
        stopList=[]
        with open("./StopWords.txt",'r',encoding='utf-8') as fp:
            line=fp.readline()
            while line:
                stopList.append(line.strip())
                line=fp.readline()
        return stopList

    def swHandle(self,sents):  #停用词处理
        '''
        对每一句话进行停用词处理
        :param sents:
        :return:
        '''
        stopwords=self.stopWord()
        _sents=[]
        for sentence in sents:
            for word in sentence:
                if word in stopwords:
                    sentence.remove(word)
            if sentence:
                _sents.append(sentence)
        return _sents

    def modelHandle(self,sents):
        '''
        对分词进行模型处理，如果模型中没有这个关键字，
        直接去掉，避免之后摘要分析出错
        :param sents:
        :return:
        '''
        _sents=[]
        for sentence in sents:
            tmpsent=sentence[:]
            for word in tmpsent:
                if word not in self.model.wv.index2entity:
                    sentence.remove(word)
            if sentence:
                _sents.append(sentence)
        return _sents

class textRanks():
    '''
    textRank算法实现类
    '''
    def __init__(self,model):
        self.model=model

    def create_graph(self,word_sent):
        """
        传入句子链表  返回句子之间相似度的图
        :param word_sent:
        :return:
        """
        num = len(word_sent)
        board = [[0.0 for _ in range(num)] for _ in range(num)]

        for i, j in product(range(num), repeat=2):
            if i != j:
                board[i][j] = self.compute_similarity_by_avg(word_sent[i], word_sent[j])
        return board

    def cosine_similarity(self,vec1, vec2):
        '''
        计算两个向量之间的余弦相似度
        :param vec1:
        :param vec2:
        :return:
        '''
        tx = np.array(vec1)
        ty = np.array(vec2)
        cos1 = np.sum(tx * ty)
        cos21 = np.sqrt(sum(tx ** 2))
        cos22 = np.sqrt(sum(ty ** 2))
        cosine_value = cos1 / float(cos21 * cos22)
        return cosine_value

    def compute_similarity_by_avg(self,sents_1, sents_2):
        '''
        对两个句子求平均词向量
        :param sents_1:
        :param sents_2:
        :return:
        '''
        if len(sents_1) == 0 or len(sents_2) == 0:
            return 0.0
        vec1 = self.model[sents_1[0]]
        for word1 in sents_1[1:]:
            vec1 = vec1 + self.model[word1]

        vec2 = self.model[sents_2[0]]
        for word2 in sents_2[1:]:
            vec2 = vec2 + self.model[word2]

        similarity = self.cosine_similarity(vec1 / len(sents_1), vec2 / len(sents_2))
        return similarity

    def calculate_score(self,weight_graph, scores, i):
        """
        计算句子在图中的分数
        :param weight_graph:
        :param scores:
        :param i:
        :return:
        """
        length = len(weight_graph)
        d = 0.85
        added_score = 0.0

        for j in range(length):
            fraction = 0.0
            denominator = 0.0
            # 计算分子
            fraction = weight_graph[j][i] * scores[j]
            # 计算分母
            for k in range(length):
                denominator += weight_graph[j][k]
                if denominator == 0:
                    denominator = 1
            added_score += fraction / denominator
        # 算出最终的分数
        weighted_score = (1 - d) + d * added_score
        return weighted_score

    def weight_sentences_rank(self,weight_graph):
        '''
        输入相似度的图（矩阵)
        返回各个句子的分数
        :param weight_graph:
        :return:
        '''
        # 初始分数设置为0.5
        scores = [0.5 for _ in range(len(weight_graph))]
        old_scores = [0.0 for _ in range(len(weight_graph))]

        # 开始迭代
        while self.different(scores, old_scores):
            for i in range(len(weight_graph)):
                old_scores[i] = scores[i]
            for i in range(len(weight_graph)):
                scores[i] = self.calculate_score(weight_graph, scores, i)
        return scores

    def different(self,scores, old_scores):
        '''
        判断前后分数有无变化
        :param scores:
        :param old_scores:
        :return:
        '''
        flag = False
        for i in range(len(scores)):
            if math.fabs(scores[i] - old_scores[i]) >= 0.0001:
                flag = True
                break
        return flag



if __name__ == '__main__':
    model=Word2Vec.load("./model/result.model")
    specimen=specimenHandle(model=model)
    textRank=textRanks(model=model)
    with open("./specimen/news.txt",'r',encoding='utf-8') as fp:
        text=fp.read().replace('\n','')
        tokens=specimen.cutSentences(text)
        sentences=[]
        sents=[]
        for sent in tokens:
            sentences.append(sent)
            sents.append([word for word in jieba.cut(sent) if word])
        sents=specimen.swHandle(sents)
        sents=specimen.modelHandle(sents)
        print(sents)
        graph=textRank.create_graph(sents)

        scores=textRank.weight_sentences_rank(graph)
        sent_selected=nlargest(2,zip(scores,count()))
        sent_index = []
        for i in range(2):
            sent_index.append(sent_selected[i][1])
        with open(r'./specimen/result1.txt','a',encoding='utf-8') as fp:
            fp.write("".join([sentences[i] for i in sent_index]))
        print("摘要生成完毕！")