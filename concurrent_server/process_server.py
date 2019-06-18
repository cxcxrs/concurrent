from socket import *
from multiprocessing import Process
import sys
import signal

#创建监听套接字
HOST = '127.0.0.1'
PORT = 8888
ADDR = ('127.0.0.1', 8888)


#处理客户端请求
def handle(c):
    while True:
        data = c.recv(1024)
        if not data:
            break
        print(data.decode())
        c.send(b'OK')
    c.close()


s = socket()    #tcp套接字
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)   #套接字端口立即重用
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
        sys.exit("服务器退出")
    except Exception as e:
        print(e)
        continue

    #创建线程处理客户端请求
    p = Process(target=handle, args=(c,))
    p.daemon = True
    p.start()

    #无论出错或者父进程都要循环回去接受请求。
    c.close()   #c对于父进程没用



























