"""
fork_server  基于fork搭建基础网络并发模型
重点代码

思路分析：
１．每当有一个客户端就创建一个新的进程作为客户端处理进程
２．客户端如果结束，对应进程应该销毁。
"""

from socket import *
import os
import signal

#创建监听套接字
HOST = '127.0.0.1'
PORT = 8888
ADDR = ('127.0.0.1', 8888)


#客户端服务函数
def handle(c):
    while True:
        data = c.recv(1024)
        if not data:
            break
        print(data.decode())
        c.send(b'OK')
    c.close()


s = socket()   #tcp套接字
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  #套接字端口立即重用
s.bind(ADDR)
s.listen(3)

#处理僵尸进程
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

print("Listen the port %d..." % PORT)

#循环等待客户端连接
while True:
    try:
        c, addr = s.accept()
    except KeyboardInterrupt:
        os._exit(0)
    except Exception as e:
        print(e)
        continue

    #创建子进程处理这个客户端（多进程<->处理多个客户端）
    pid = os.fork()
    if pid == 0:  #处理客户端请求
        s.close()    #s对于子进程没用
        handle(c)
        os._exit(0)  #handle处理完客户端请求，子进程也退出。

    #无论出错或者父进程都要循环回去接受请求。
    c.close()   #c对于父进程没用



























