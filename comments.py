import jieba
import sys
import time
import re
from dingtalkchatbot.chatbot import DingtalkChatbot

webhook = 'https://oapi.dingtalk.com/robot/send?access_token='
xiaoding = DingtalkChatbot(webhook)
 
jieba.load_userdict("/www/wwwroot/website/quant/comments/remark/dict.txt")

def positivelist():
    positivewords = [line.strip() for line in open('/www/wwwroot/website/quant/comments/remark/positive.txt',encoding='UTF-8').readlines()]
    return positivewords
def negtivelist():
    negtivewords = [line.strip() for line in open('/www/wwwroot/website/quant/comments/remark/negtive.txt',encoding='UTF-8').readlines()]
    return negtivewords
def nowordslist():
    nowords = [line.strip() for line in open('/www/wwwroot/website/quant/comments/remark/nowords.txt',encoding='UTF-8').readlines()]
    return nowords
def stopwordslist():
    stopwords = [line.strip() for line in open('/www/wwwroot/website/quant/comments/remark/stop_words.txt',encoding='UTF-8').readlines()]
    return stopwords

nowordslist = nowordslist()
positivelist = positivelist()
negtivelist = negtivelist()
stopwords = stopwordslist()


import pymysql
 
conn = pymysql.connect (
    host='localhost',
    port=3306,
    user='',
    password='',
    database='',
    charset='utf8'
)
# 获取一个光标
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 返回字典数据类型
 
# 定义将要执行的sql语句
sql = 'select id,title from tvdata where titlescore = 0 order by id desc limit 3000;'
# 拼接并执行sql语句
cursor.execute(sql)
 
# 取到查询结果 
ret = cursor.fetchmany(3000)  # 取三条 

if ret:
    for i in ret:
        sentence = (i['title']).replace('|','')
        bigword = []
        #sentence = str(sys.argv[1]).strip()
       	sentenceList = (re.findall(r"[\w’]+", sentence))
       	motion = 0
       	print(sentenceList)
       	for fenju in sentenceList:
       		if fenju:
		        sentence_depart = jieba.cut(fenju.strip(), cut_all=False)
		        outstr = []
		        # 去停用词
		        senti = 0
		        psenti = 0
		        nsenti = 0
		        noflag = 0
		        sentiflag = ''; 
		        for word in sentence_depart:
		            if word not in stopwords:
		                if word != '\t' and word != ' ':
		                    outstr.append(word) 
		                    bigword.append(word)
		            if word in nowordslist:
		                noflag = noflag + 1

		            if word in positivelist:
		                psenti = 1
		                senti = 1
		            if word in negtivelist:
		                senti = -1;
		                psenti = -1; 
		        if senti == 1:
		            if (-1)**noflag == 1:
		                sentiflag = 1
		            else:
		                sentiflag = -1
		        if senti == -1:
		            if (-1)**noflag == 1:
		                sentiflag = -1
		            else:
		                sentiflag = 1
		        if senti == 0:
		            sentiflag = 0
		        motion += sentiflag
	        	print(sentiflag)
        if motion>0:
        	motion = 1
        if motion < 0:
        	motion = -1
        if motion == 0:
        	motion = 2
        sql = "update tvdata set titlescore=%s where id=%s;"
        # 拼接并执行SQL语句
        cursor.execute(sql, [motion, i['id']])
         
        # 涉及写操作注意要提交
        conn.commit()
 
 
import datetime
now_time=datetime.datetime.now()
last24hour = ((now_time+datetime.timedelta(hours=-6)).strftime("%Y-%m-%d %H:%M:%S"))

# 定义将要执行的sql语句
sql = 'select sum(titlescore) as score,count(1) as count from tvdata where titlescore <> 2 and pub_date > %s'
# 拼接并执行sql语句
cursor.execute(sql,[last24hour])
 
# 取到查询结果 
ret = cursor.fetchone()   

f = open('/www/wwwroot/website/quant/comments/remark/tt.txt','r')
macdtr = f.read()
f.close()

if macdtr:
    macdtr = int(macdtr)
else:
    macdtr = 0

t = round(time.time())

if ((ret['score']>2) or (ret['score']< -2))  and (t - macdtr > 4*3600):
	xiaoding.send_text(msg='交易信号：评论 \n得分：'+str(ret['score'])+'\n评论数：'+str(ret['count'])+'\n http://www.datafarm.top/comments', is_at_all=False,at_mobiles=[18221556502])
	f = open('/www/wwwroot/website/quant/comments/remark/tt.txt','w')
	f.write(str(t))
	f.close()
cursor.close()
conn.close()







