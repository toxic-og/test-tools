import socket
import logging
import threading
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(thread)d | %(message)s')

class ChatServer:
    def __init__(self, ip='127.0.0.1', port=9999):
        self.sock = socket.socket() #专管accept的socket
        self.addr = (ip, port)
        self.clients = {}
        self.event = threading.Event()

    def start(self):
        self.sock.bind(self.addr)
        self.sock.listen()
        threading.Thread(target=self.accept).start() #accept阻塞主线程，开启新线程

    def accept(self):
        while not self.event.is_set(): #event没有设为set（）时就会向下执行
            sock, client =  self.sock.accept() #专管与不同客户端连接的socket
            f = sock.makefile(mode='rw') #创建套接字文件
            self.clients[client] = sock
            threading.Thread(target=self.recv, args=(f, client)).start() #recv阻塞主线程，开启新线程

    def recv(self, f, client):
        while not self.event.is_set():
            try:
                data = f.readline() #按行读取数据
            except Exception as e:
                logging.error(e)
                data = 'quit' # 捕获错误信息并退出
            msg = data.strip()
            if msg == 'quit':
                self.clients.pop(client) #从字典中把客户端(ip,port)扔出去
                f.close() #关闭套接字文件
                logging.info('{} quits'.format(client))
                break
            msg = '{:%Y/%m/%d %H:%M:%S} {}:{}\n{}\n'.format(datetime.datetime.now(), *client, data)
            logging.info(msg)
            msg = msg.encode()
            for s in self.clients.values(): #直接用线程的sock不行吗？
                s.send(msg)

    def stop(self):
        for s in self.clients.values():
            s.close()  #关闭线程里的socket
        self.event.set()  # 关闭时event置为True，上面的accept和recv不会执行
        self.sock.close()  #关闭主线程socket

def main():
    cs = ChatServer()
    cs.start()
    while True:
        cmd = input('<<').strip()
        if cmd == 'quit':
            cs.stop()
            threading.Event().wait(3)
            break
        logging.info(threading.enumerate())

if __name__ == '__main__':
    main()









