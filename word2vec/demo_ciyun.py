#coding:utf-8
from collections import Counter
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

dm_words_with_attr = []
with open('./result1.txt', 'r',encoding="utf-8") as f:
    try:
        for x in f.readlines():
            pairs = x.split(' ')
            for pair in pairs:
                dm_words_with_attr.append((pair))
    except:
        pass
#print(dm_words_with_attr)
c = Counter(dm_words_with_attr).most_common(650)
#print(c)
attr_dict = {}
for i, j in c:
    attr_dict[i] = j
img = np.array(Image.open(r'./img/17.png'))


wc = WordCloud(
    background_color="white", #背景颜色
    mask=img,
    max_words=650, #显示最大词数
    font_path=r"C:\Windows\Fonts\SIMLI.TTF",  #使用字体
    min_font_size=30,
    max_font_size=80,
    scale=4,        # 比列放大  数值越大  词云越清晰
    # width=1680,  #图幅宽度
    # height=1050,
    random_state=50,
    relative_scaling=False,
    ).generate_from_frequencies(attr_dict)
#image_produce = wc.to_image()
#image_produce.show()

# 绘制文字的颜色以背景图颜色为参考
image_color = ImageColorGenerator(img)
# 好像是结合原图色彩啥的  忘记了。。。。
wc.recolor(color_func=image_color)
plt.figure()        # 创建图像
plt.imshow(wc, interpolation="bilinear")
# 关闭坐标轴
plt.axis("off")
plt.show()
# 保存图片
wc.to_file('./18.jpg')