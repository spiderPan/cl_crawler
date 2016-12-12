import scrapy
from datetime import datetime
from scrapy.loader import ItemLoader
from cl_1024.items import CLItem


class CLSpider(scrapy.Spider):
    name = "cl"
    allowed_domains = ['t66y.com']
    start_urls = [
        'http://www.t66y.com/thread0806.php?fid=16',
    ]

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                 errback=self.errback,
                                 dont_filter=True)

    def parse(self, response):
        for item in response.css('#ajaxtable tr.tr3'):
            viewNum = item.xpath('.//td[4]/text()').extract_first()
            publishDate = item.xpath('.//td[3]/div/text()').extract_first()
            articleLink = item.xpath('.//td[1]/a/@href').extract_first()
            if viewNum is None or publishDate is None or articleLink is None:
                continue

            try:
                d = datetime.strptime(publishDate, "%Y-%m-%d")
            except ValueError:
                d = datetime.strptime('1990-10-03', "%Y-%m-%d")
            if int(viewNum) > 30 and (publishDate is 'top-mark' or (datetime.now() - d).days < 2):
                articleLink = response.urljoin(articleLink)
                yield scrapy.Request(articleLink, callback=self.parse_item)

    def parse_item(self, response):
        il = ItemLoader(item=CLItem(), response=response)
        il.add_xpath('image_urls', '//input[@type="image"]/@src')
        return il.load_item()

    def errback(self, failure):
        pass
