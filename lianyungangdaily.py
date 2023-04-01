# -*- coding: utf-8 -*-
from scrapy import FormRequest
import re
from newscrapy.items import NewscrapyItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from newscrapy.tools import dateGen
from urllib import parse


class mySpider(CrawlSpider):
    name = "lianyungangdaily"
    newspapers = "连云港日报"
    allowed_domains = ['lygrbepaper.lygfb.cn']

    def start_requests(self):
        dates = dateGen(self.start, self.end, "%Y-%m-%d")
        template = "http://lygrbepaper.lygfb.cn/Media/lygrb/{date}"
        for d in dates:
            yield FormRequest(template.format(date = d))

    rules = (
        Rule(LinkExtractor(allow=('/Page/index/pageid/\w+.html'))),
        Rule(LinkExtractor(allow=('/Article/index/aid/\w+.html')), callback="parse_item")
    )

    def parse_item(self, response):
        try:
            title = response.xpath("//div[@class='title']").xpath("string(.)").get()
            content = response.xpath("//div[@class='article-cont']").xpath("string(.)").get()
            url = response.url
            # date = re.search('html/(\d+-\d+-\d+)/Qpaper', url).group(1)
            # date = '-'.join([date[0:4], date[5:7], date[8:10]])
            imgs = response.xpath("//p[@align='center']//img/@src").getall()
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