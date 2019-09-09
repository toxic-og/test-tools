import datetime

pattern = '''(?P<remote>[\d\.]{7,})\s-\s-\s\[(?P<datetime>[^\[\]]+)\]\s\
"(?P<method>.*)\s(?P<url>.*)\s(?P<protocol>.*)"\s(?P<status>\d{3})\s(?P<length>\d+)\s"[^"]"\s\
"(?P<useragent>[^"]+)"'''

line = '''183.60.212.153 - - [19/Feb/2013:10:23:28 +0800] "GET /o2o/media.html?menu=3 HTTP/1.1" 200 16691 "-" "Mozilla/5.0 (compatible; EasouSpider; +http://www.easou.com/search/spider.html)"'''

ops = {
        'datetime':lambda timestr: datetime.datetime.strptime(timestr, '%d/%b/%Y:%H:%M:%S %z'),
        'status':int,
        'length':int
        }


ip, port = '127.0.0.1', '9999'
print(ip, port)
