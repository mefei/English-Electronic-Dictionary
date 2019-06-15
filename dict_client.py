"""
dict 客户端
发起请求，展示结果

"""

from socket import *
from getpass import getpass
import sys


ADDR = (('127.0.0.1',18888))
s = socket()

# 注册
def do_register():
	while True:
		name = input("User:")
		passwd = input("Password:")
		passwd1 = input("Again:")
		# passwd = getpass()
		# passwd1 = getpass()
		if (' ' in name) or (' ' in passwd):
			print("用户名或密码不能有空格")
			continue
		if passwd != passwd1:
			print("两次密码输入不一致")
			continue

		msg = "R %s %s"%(name,passwd)

		# 发送请求
		s.send(msg.encode())
		data = s.recv(1024).decode()
		print(data)
		if data == 'OK':
			print("注册成功")
			login(name)
		else:
			print("注册失败")
		return
# 登录
def do_login():
	while True:
		name = input("User:")
		passwd = input("Password:")
		msg = "L %s %s"%(name,passwd)
		s.send(msg.encode())
		data = s.recv(1024).decode()
		if data == "OK":
			print("登录成功")
			login(name)
		else:
			print("登录失败")
		return

# 注册成功或登录后页面
def login(name):
	while True:
		print("==========Query==========")
		print("1.查单词  2.历史记录  3.注销")
		print("=========================")
		cmd = input("请输入选项：")
		if cmd == '1':
			check_word(name)
		elif cmd == '2':
			get_history(name)
		elif cmd == '3':
			return
		else:
			print("输入有误，请重新输入")

# 查单词
def check_word(name):
	while True:
		word = input("Word:")
		if word == '##':
			break
		msg = "C %s %s" % (name,word)
		s.send(msg.encode())
		data = s.recv(1024).decode()
		print(data)

# 获取历史记录
def get_history(name):
	msg = "G %s" % name
	s.send(msg.encode())
	data = s.recv(128).decode()
	if data == 'OK':
		while True:
			data = s.recv(4096).decode()
			if data == '##':
				break
			print(data)
	else:
		print(data)

# 退出
def do_quit():
	msg = "Q"
	s.send(msg.encode())
	s.close()
	sys.exit("退出服务")

# 网络链接
def main():
	s.connect(ADDR)
	while True:
		print("=======Welcome======")
		print("1.注册  2.登录  3.退出")
		print("====================")
		cmd = input("请输入选项：")
		if cmd == '1':
			do_register()
		elif cmd == '2':
			do_login()
		elif cmd == '3':
			do_quit()
			return
		else:
			print("输入有误，请重新输入")


if __name__ == '__main__':
    main()