"""
ftp客户端
"""
from socket import *
import sys
import time


HOST = '0.0.0.0'
PORT = 8080
ADDR = (HOST, PORT)


#客户端功能处理类
class FTPClient:
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b'L')   #发送请求
        #等待回复
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            #一次接受文件列表字符串
            data = self.sockfd.recv(4096)
            print(data.decode())
        else:
            print(data)

    def do_get(self, filename):
        #发送请求
        self.sockfd.send(('G '+filename).encode())
        #等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            fd = open(filename, 'wb')
            #接受文件
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                else:
                    fd.write(data)
            fd.close()
        else:
            print(data)

    def do_put(self, filename):
        try:
            f = open(filename, 'rb')
        except Exception:
            print("该文件不存在")
            return
        #获取文件名
        filename = filename.split('/')[-1]
        #发送请求
        self.sockfd.send(('P '+filename).encode())
        #等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b'##')   #结束发送
                    break
                self.sockfd.send(data)
            f.close()
        else:
            print(data)

#我的方法
    # def do_put(self, rout, filename):
    #     try:
    #         fd = open(rout, 'rb')
    #     except Exception:
    #         print("文件不存在！")
    #         return
    #     else:
    #         self.sockfd.send(('P '+filename).encode())
    #         time.sleep(0.1)
    #     #文件发送
    #     while True:
    #         data = fd.read(1024)
    #         if not data:
    #             time.sleep(0.1)
    #             self.sockfd.send(b'##')
    #             break
    #         self.sockfd.send(data)
    #     # print(self.sockfd.recv(1024).decode())   #接受服务端的报错信息

    def do_quit(self):
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit("感谢使用！")


def main():
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print(e)
        return

    ftp = FTPClient(sockfd)  #实例化对象

    #循环发送请求
    while True:
        print("\n=========命令选项===========")
        print("*******    list      *******")
        print("*******    get file  *******")
        print("*******    put file  *******")
        print("*******    quit      *******")
        print("=============================")

        cmd = input("输入命令：")

        # sockfd.send(cmd.encode())
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd[:3] == 'get':
            filename = cmd.strip().split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:3] == 'put':
            filename = cmd.strip().split(' ')[-1]
            ftp.do_put("/home/tarena/Secondclass/concurrent/day04/"+filename)
        # elif cmd[:3] == 'put':
        #     filename = cmd.strip().split(' ')[-1]
        #     ftp.do_put("/home/tarena/Secondclass/concurrent/day04/"+filename, filename)
        elif cmd.strip() == 'quit':
            ftp.do_quit()
        else:
            print("请输入正确命令")


if __name__ == "__main__":
    main()


# def see():
#     ...
#
# def download():
#     ...
#
# def upload():
#     ...
#
