import datetime
import re
import random
import time
from queue import Queue
from threading import Thread

line = '''183.60.212.153 - - [19/Feb/2013:10:23:28 +0800] "GET /o2o/media.html?menu=3 HTTP/1.1" 200 16691 "-" "Mozilla/5.0 (compatible; EasouSpider; +http://www.easou.com/search/spider.html)"'''
CHARS = set(' \'"[]')

def makekey(line:str):
    start = 0
    flag = False
    for i,c in enumerate(line):
        if c in CHARS:
            if c == '[':
                flag = True
                start = i+1
            if c == ']':
                flag = False
            if c == '"':
                flag = not flag
                if flag:
                    start = i+1
            if flag:
                continue
            if start == i:
                start = i+1
                continue
            yield line[start:i]
            start = i+1
    else:
        if start < len(line):
            yield line[start:]

# #格式转换 转lambda
# def convent_time(timestr):
#     return datetime.datetime.strptime(timestr, '%d/%b/%Y:%H:%M:%S %z')
# #request解析 转lambda
# def get_request(request:str):
#     return dict(zip(['method', 'url', 'protocol'],request.split()))

name = ('remote', '', '', 'datetime', 'request', 'status', 'length', '', 'useragent')
ops = (None, None, None, lambda timestr: datetime.datetime.strptime(timestr, '%d/%b/%Y:%H:%M:%S %z'),
       lambda request: dict(zip(['method', 'url', 'protocol'],request.split())), int, int, None, None)

def extract(line:str):
    return dict(map(lambda item:(item[0], item[2](item[1]) if item[2] is not None else item[1]),
                zip(name, makekey(line), ops)))

def load(path):
    with open(path) as f:
        for line in f:
            fields = extract(line)
            if fields:
                yield fields
            else: continue

def source(seconds=1):
    while True:
        yield {'value':random.randint(1, 100),
               'datetime':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))}
        time.sleep(seconds)

s = source()
items = (next(s) for _ in range(5))

def handler(iterable):
    return sum(map(lambda item:item['value'], iterable)) / len(iterable)

def status_handler(iterable):
    status = {}
    for item in iterable:
        key = item['status']
        status[key] = status.get(key, 0) +1
    total = len(iterable)
    return {k: status[k] / total for k,v in status.items()}

def window(iterator, handler, width:int, interval:int):
    start = datetime.datetime.strptime('20170101 000000 +0800', '%Y%m%d %H%M%S %z')
    current = datetime.datetime.strptime('20170101 010000 +0800', '%Y%m%d %H%M%S %z')
    buffer = []
    delta = datetime.timedelta(seconds=width-interval)
    while True:
        data = next(iterator)
        if data:
            buffer.append(data)
            current = data['datetime']

        if (current - start).total_seconds() >= interval:
            ret = handler(buffer)
            print('{:.2f}'.format(ret))
            start = current
            buffer =[x for x in buffer if x['datetime'] > current-delta] #清除数据

def dispatcher(src):
    handlers = []
    queues = []

    def reg(handler, width:int, interval:int):
        q = Queue()
        queues.append(q)
        h = Thread(target=window, args=(q, handler, width, interval))
        handlers.append(h)
    def run():
        for t in handlers:
            t.start()
        for item in src:
            for q in queues:
                q.put(item)
    return reg, run

if '__name__' == '__main__':
    import sys
    path = 'test.log'
    reg,run = dispatcher(load(path))
    reg(status_handler, 10, 5)
    run()










