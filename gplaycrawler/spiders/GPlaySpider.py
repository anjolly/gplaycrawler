from gplaycrawler.items import GplaycrawlerItem
from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import urlparse


class GPlaySpider(CrawlSpider):
    name = "gplay"
    allowed_domains = [ "play.google.com" ]
    start_urls = [ "https://play.google.com/store/apps/" ]
    rules = (
        Rule(LinkExtractor(allow=('/store/apps',)),follow=True),
        Rule(LinkExtractor(allow=('/store/apps/details\?')),follow=True,callback='parse_link'),
    )

    def abs_url(url, response):
        """Return absolute link"""
        base = response.xpath('//head/base/@href').extract()
        if base:
            base = base[0]
        else:
            base = response.url
        return urlparse.urljoin(base, url)

    def parse_link(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select('/html')
        items = []
        for titles in titles:
            item = GplaycrawlerItem()
            item["Name"] = titles.xpath("//div[@class='id-app-title']/text()").extract_first()
            item["Description"] = titles.xpath("//div[@itemprop='description']/div/text()").extract_first()
            item["Developer"] = titles.xpath("//span[@itemprop='name']/text()").extract_first()
            item["Ratings"] = titles.xpath("//span[@class='rating-count']/text()").extract_first()
            items.append(item)
        return items
