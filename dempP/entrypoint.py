# Scrapy默认是不能在IDE中调试的
from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'dempP'])