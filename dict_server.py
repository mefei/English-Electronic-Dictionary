"""
dict 服务端部分
处理请求逻辑

"""
import sys
import signal
from socket import *
from multiprocessing import Process
from operating_database import Database
import time

# 全局变量
ADDR = (('0.0.0.0',18888))


# 处理客户请求
def do_request(c,db):
	db.create_cursor()
	while True:
		data = c.recv(1024).decode()
		# print(data)
		# print(c.getpeername(),':',data)
		if not data or data[0] == 'Q':
			do_quit(c,db)
		elif data[0] == 'R':
			do_register(c,db,data)
		elif data[0] == 'L':
			do_login(c,db,data)
		elif data[0] == 'C':
			check_word(c,db,data)
		elif data[0] == 'G':
			get_history(c,db,data)

# 注册
def do_register(c,db,data):
	tmp = data.split(' ')
	name = tmp[1]
	passwd = tmp[2]
	# print(name,passwd)
	if db.register(name,passwd):
		c.send(b'OK')
	else:
		c.send('注册失败'.encode())

# 登录
def do_login(c,db,data):
	tmp = data.split(' ')
	name = tmp[1]
	passwd = tmp[2]
	if db.login(name, passwd):
		c.send(b'OK')
	else:
		c.send('登录失败'.encode())

# 退出
def do_quit(c):
	c.close()
	sys.exit("客户端退出")

# 处理查找单词
def check_word(c,db,data):
	tmp = data.split(' ')
	name = tmp[1]
	word = tmp[2]

	# 插入历史记录
	db.insert_history(name,word)
	mean = db.query(word)
	if not mean:
		c.send("没有找到该单词".encode())
	else:
		msg = "%s : %s"%(word,mean)
		c.send(msg.encode())

# 获取历史记录
def get_history(c,db,data):
	tmp = data.split(' ')
	name = tmp[1]

	# 获取历史记录
	r = db.history(name)
	# print(r)
	if not r:
		c.send("没有查找记录".encode())
		return
	else:
		c.send(b'OK')
		for i in r:
			msg = "%s %s"%i
			time.sleep(0.1)
			c.send(msg.encode())
		time.sleep(0.1)
		c.send(b'##')


# 网络链接
def main():
	# 创建数据库连接对象
	db = Database()

	# 创建TCP套接字
	s = socket()
	s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	s.bind(ADDR)
	s.listen(5)

	# 处理僵尸进程
	signal.signal(signal.SIGCHLD,signal.SIG_IGN)

	# 等待客户链接
	print("Listen the port 18888")
	while True:
		try:
			c,addr = s.accept()
			print("Connect from",addr)
		except KeyboardInterrupt:
			s.close()
			db.close()
			sys.exit("服务器退出")
		except Exception as e:
			print(e)
			continue

		# 创建子进程
		p = Process(target = do_request,args = (c,db))
		p.start()

if __name__ == '__main__':
    main()