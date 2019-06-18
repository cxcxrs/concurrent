
from socket import *
from threading import Thread
import sys

#创建监听套接字
HOST = '127.0.0.1'
PORT = 8888
ADDR = (HOST, PORT)


#处理客户端请求
def handle(c):
    while True:
        data = c.recv(1024)
        if not data:
            break
        print(data.decode())
        c.send(b'OK')
    c.close()


s = socket(AF_INET, SOCK_STREAM)  #tcp套接字
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  #套接字端口立即重用
s.bind(ADDR)
s.listen(3)

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
    t = Thread(target=handle, args=(c,))
    t.setDaemon(True)
    t.start()



























