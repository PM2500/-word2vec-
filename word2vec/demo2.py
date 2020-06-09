#coding:utf-8
from gensim.models import Word2Vec
model=Word2Vec.load("./model/result.model")
lists=model.wv.index2word    #获得所有的词汇
print(lists)
print(len(lists))
for word in lists:
    print(word,model.wv[word])     #获得词汇及其对应的向量
