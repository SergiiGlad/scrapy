import scrapy
from scrapy.http import Request
from urllib.parse import urljoin, unquote
from urllib.request import install_opener, URLopener
import os


class SpiderkubeconSpider(scrapy.Spider):
    name = 'spiderkubecon'
    allowed_domains = ['events.linuxfoundation.org','sched.com']
    start_urls = ['https://kccncna2022.sched.com/?iframe=no']
    num = 1
    file_download = False

    def start_requests(self):
        return [Request(url='https://kccncna2022.sched.com/?iframe=no',callback=self.parse)]

    def parse(self, response):
        events=response.xpath('//*[contains(@href,"event/")]/@href').extract()
        for event in events:
            yield Request(url=urljoin(response.url,event), callback=self.parse_event )

    def parse_event(self, response):
        # link with file uploaded
        link = response.xpath('//*[contains(@class,"file-uploaded")]/@href').extract() 
        # event name
        name = response.xpath('//*[contains(@class,"name")]/text()').extract()
        # event type
        con_type = response.xpath('//*[contains(@href,"type/")]/text()').extract()
        # level
        company_level = response.xpath('//*[contains(@href,"company/")]/text()').extract()

        # if link has file uploaded
        if len(link) != 0:
            filename = unquote(os.path.basename(link[0]))
            print(self.num)
            print(name[0].rstrip())
            print("url: " + response.url)
            print(con_type[0]) if len(con_type) == 1 else print(con_type[0] + "," + con_type[1])
            print(company_level[0]) if len(company_level) > 0 else print("Any")
            print(link)
            print(filename)
            self.num += 1
            if self.file_download :
                opener = URLopener()
                opener.addheaders = [('User-Agent', 'MyApp/1.0')]
                install_opener(opener)
                filename, headers = opener.retrieve(link[0], filename)




             
