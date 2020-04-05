import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from dempP.items import DemppItem

class MySpider(scrapy.Spider):
    name = 'dempP'
    allowed_domains = ['a514a.com']
    bash_url = 'http://www.a514a.com/aa514.com/'
    bashurl  = '.aspx'
    baseUrl = 'http://www.a514a.com'

    def start_requests(self):
        for i in range(14,15):
            url = self.bash_url + str(i) + self.bashurl
            yield Request(url, self.parse)

    def parse(self, response):
        max_num = BeautifulSoup(response.text, 'lxml').find('a', class_= 'end').get_text()
        bashurl = str(response.url)[:-5]
        print(bashurl, max_num)
        max_num = 2
        for num in range(1, int(max_num) + 1):
            url = bashurl + '/' + str(num) + self.bashurl
            print('---' + url + '---')
            yield Request(url, self.handle_novelList)
    
    def handle_novelList(self, response):
        contextList = BeautifulSoup(response.text, 'lxml').find('div', class_='box list channel').find_all('li') 
        contextList = contextList[4:] # 去掉前4个广告 :)
        for index, context in enumerate(contextList):
            if index >= 1:
                break;
            novelurl  = self.baseUrl + context.find('a')['href']
            novelname = context.find('a').get_text()[5:]
            yield Request(novelurl, self.handle_novel, meta = {'name': novelname, 'url': novelurl})

    def handle_novel(self, response):
        novelContext = BeautifulSoup(response.text, 'lxml').find('div', class_='pics')
        item = DemppItem()
        item['storyTitle'] = response.meta['name']
        item['storyContext'] = novelContext.get_text()
        item['storyUrl'] = response.meta['url']