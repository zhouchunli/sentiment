# sentiment
btc sentiment analysis
此处通过简单情感词进行文本舆论分析，专门针对BTC相关的评论进行分词判断，有较高的准确率
另外一种方法是通过机器学习方法，word2vec+svm进行监督学习，此处仅呈现方法流程。
## 1.基本中文语料来源于wiki中文语料，可网上搜索
## 2.通过提取，jieba分词将语料向量化，存储向量模型
## 3.对通过爬虫爬取的tradingview 评论数据进行分词，标注
## 4.根据wiki向量模型获得评论数据向量模型，进行特征选择和降维
## 5.通过svm进行模型训练。
## 6.评估模型
## 7.结果呈现 [BTC众评](http://www.datafarm.top/comments/)
