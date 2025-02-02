# -*- coding: utf-8 -*-
from scrapy import FormRequest
import re
from newscrapy.items import NewscrapyItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from newscrapy.tools import dateGen
from urllib import parse


class mySpider(CrawlSpider):
    name = "mudanwanbao"
    newspapers = "牡丹晚报"
    allowed_domains = ['epaper.hezeribao.com']

    def start_requests(self):
        dates = dateGen(self.start, self.end, "%Y%m%d")
        template = "http://www.heze.cn/mdwb/pc/layout/{date}/node_A01.html"
        for d in dates:
            yield FormRequest(template.format(date = d))

    rules = (
        Rule(LinkExtractor(allow=('mdwb/\d+/vA\w+.shtml'))),
        Rule(LinkExtractor(allow=('mdwb/\d+/\w+.shtml')), callback="parse_item")
    )

    def parse_item(self, response):
        try:
            title = response.xpath("//*[@id='content']//h1").xpath('string(.)').get()
            content = response.xpath("//div[@class='para").xpath('string(.)').get()
            url = response.url
            # date = re.search("pc/c/(\d+/\d+)/", url).group(1)
            # date = '-'.join([date[0:4], date[4:6], date[7:9]])
            imgs = response.xpath("//div[id='article_img_marquee']//img/@src").getall()
            imgs = [parse.urljoin(url, imgurl) for imgurl in imgs]
            html = response.text
        except Exception as e:
            return

        item = NewscrapyItem()
        item['title'] = title
        item['content'] = content
        # item['date'] = date
        item['imgs'] = imgs
        item['url'] = response.url
        item['newspaper'] = self.newspapers
        item['html'] = html
        yield item