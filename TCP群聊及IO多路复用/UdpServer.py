import threading
import socket
import datetime
import logging

FORMAT = '%(asctime)s %(thread)d %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

class ChatUdpServer:
    def __init__(self, ip='127.0.0.1', port=9999, interval=10):
        self.sock = socket.socket(type=socket.SOCK_DGRAM) #创建udp对象需要指明类型
        self.addr = ip, port
        #self.clients = set() #因为udp是无连接协议，所以只需要对端地址，集合就能搞定
        self.clients = {} #引进心跳机制就要用到字典，raddr与time是一对
        self.event = threading.Event()
        self.interval = interval

    def start(self):
        self.sock.bind(self.addr)
        threading.Thread(target=self.recv, name='recv1').start()

    def recv(self):
        while not self.event.is_set():
            localset = set()
            data, raddr = self.sock.recvfrom(1024)
            current = datetime.datetime.now().timestamp()
            if data.strip() == b'^hb^':
                print('^^^^^^this is my hb', raddr)
                self.clients[raddr] = current #记录下来存活时间
                # stamp = current #心跳时间
            if data.strip() == b'quit':
                self.clients.pop(raddr, None) #有可能发来数据的不是clients中的
                logging.info('{} leaving'.format(raddr))
                continue
            self.clients[raddr] = current #更新时间
            msg = '{} from {}:{}'.format(data.decode(), *raddr)
            logging.info(msg)
            msg = msg.encode()
            for c,stamp in self.clients.items():
                print(0,current)
                print(1,stamp)
                print(2,c)
                print(localset)
                if current - stamp > self.interval:
                    localset.add(c)
                    print(localset)
                else:
                    self.sock.sendto(msg, c)  #指定发给谁
            for c in localset:
                self.clients.pop(c)

    def stop(self):
        for c in self.clients:
            self.sock.sendto(b'bye', c)
        self.sock.close()
        self.event.set()

def main():
    cs = ChatUdpServer()
    cs.start()
    while True:
        cmd = '>>>'
        if cmd.strip() == 'quit':
            cs.stop()
            threading.Event().wait(3)
            break
        #logging.info(threading.enumerate())
        #logging.info(cs.clients)

if __name__ == '__main__':
    main()

