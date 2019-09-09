import socket
import threading
import datetime
import logging

FORMAT = '%(asctime)s %(threadName)s %(thread)d %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

class ChatUdpClient:
    def __init__(self, rip='127.0.0.1', rport=9999):
        self.sock = socket.socket(type=socket.SOCK_DGRAM)
        self.raddr = rip, rport
        self.event = threading.Event()

    def start(self):
        self.sock.connect(self.raddr)
        threading.Thread(target=self.recv, name='recv').start()
        threading.Thread(target=self._sendhb, name='heartbeat').start()

    def _sendhb(self):
        while not self.event.wait(5):
            self.send('^hb^') #event事件等5秒，等不到返回false

    def recv(self):
        while not self.event.is_set():
            data, raddr = self.sock.recvfrom(1024)
            msg = '{}.from{}:{}'.format(data.decode(), *raddr)
            logging.info(msg)

    def send(self, msg:str):
        self.sock.sendto(msg.encode(), self.raddr)

    def stop(self):
        self.sock.close()
        self.event.set()

def main():
    cc1 = ChatUdpClient()
    cc2 = ChatUdpClient()
    cc1.start()
    cc2.start()
    print(cc1)
    print(cc2)

    while True:
        mad = '>>>'
        if mad.strip() == 'quit':
             cc1.stop()
             cc2.stop()
             break
        # cc1.send(mad)
        # cc2.send(mad)

if __name__ == '__main__':
    main()



