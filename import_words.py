import pymysql
import re

db = pymysql.connect(host='localhost',
                     user='root',
                     passwd = "123456",
                     database='dict',
                     charset='utf8')
c = db.cursor()
sql = "insert into words (word,mean) values (%s,%s);"

fd = open('dict.txt','r')

data_list = []
for line in fd:
	tup = re.findall(r'(\w+)\s+(.*)',line)[0]
	data_list.append(tup)



try:
	c.executemany(sql,data_list)
	db.commit()
except Exception:
	db.rollback()
	print("出现异常，内容回滚")

fd.close()
c.close()
db.close()