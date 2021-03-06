from gplaycrawler.items import GplaycrawlerItem
from gplaycrawler.gplayapi.googleplay import GooglePlayAPI
from gplaycrawler.gplayapi.config import *
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import urlparse


class ScrapySpider(CrawlSpider):
    name = "scrapy"
    allowed_domains = [ "play.google.com" ]
    start_urls = [ "https://play.google.com/store/apps/" ]
    rules = (
        Rule(LinkExtractor(allow=('/store/apps/details\?')),follow=True,callback='parse_link'),
        Rule(LinkExtractor(allow=('/store/apps',)),follow=True),
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
        sel = Selector(response)
        titles = sel.xpath('/html')

        #download apk
        api = GooglePlayAPI(ANDROID_ID)
        api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
        packageName = response.url.split('=')
        fileName = "%s.apk" % (packageName[1])
        data = api.download(packageName[1])
        with open("apks\%s" % (fileName), "wb") as f:
            f.write(data)

        items = []
        for titles in titles:
            item = GplaycrawlerItem()
            item["Title"] = titles.xpath("//div[@class='id-app-title']/text()").extract()
            item["Url"] = response.url
            item["Description"] = titles.xpath("//div[@itemprop='description']/div/text()").extract()
            item["DeveloperName"] = titles.xpath("//span[@itemprop='name']/text()").extract()
            item["Genre"] = titles.xpath("//span[@itemprop='genre']/text()").extract()
            item["Price"] = titles.xpath("//meta[@itemprop='price']/@content").extract()
            item["Ratings"] = titles.xpath("//span[@class='reviews-num']/text()").extract()
            item["FiveStarRatings"] = titles.xpath("//div[@class='rating-bar-container five']/span[@class='bar-number']/text()").extract()
            item["FourStarRatings"] = titles.xpath("//div[@class='rating-bar-container four']/span[@class='bar-number']/text()").extract()
            item["ThreeStarRatings"] = titles.xpath("//div[@class='rating-bar-container three']/span[@class='bar-number']/text()").extract()
            item["TwoStarRatings"] = titles.xpath("//div[@class='rating-bar-container two']/span[@class='bar-number']/text()").extract()
            item["OneStarRatings"] = titles.xpath("//div[@class='rating-bar-container one']/span[@class='bar-number']/text()").extract()
            item["ReviewsAverage"] = titles.xpath("//div[@class='score']/text()").extract()
            item["ContentRating"] = titles.xpath("//div[@itemprop='contentRating']/text()").extract()
            item["WhatsNew"] = titles.xpath("//div[@class='details-section whatsnew']//div[@class='recent-change']/text()").extract()
            item["LastUpdated"] = titles.xpath("//div[@itemprop='datePublished']/text()").extract()
            item["FileSize"] = titles.xpath("//div[@itemprop='fileSize']/text()").extract()
            item["Downloads"] = titles.xpath("//div[@itemprop='numDownloads']/text()").extract()
            item["CurrentVersion"] = titles.xpath("//div[@itemprop='softwareVersion']/text()").extract()
            item["AndroidVersion"] = titles.xpath("//div[@itemprop='operatingSystems']/text()").extract()
            item["DeveloperWebsite"] = titles.xpath("//a[@class='dev-link'][contains(text(), 'Visit website')]/@href").extract()
            item["DeveloperEmail"] = titles.xpath("substring(//a[contains(@href, 'mailto')]/text(), 8)").extract()
            item["DeveloperAddress"] = titles.xpath("//div[@class='content physical-address']/text()").extract()
            item["PrivacyPolicyLink"] = titles.xpath("//a[@class='dev-link'][contains(text(), 'Privacy Policy')]/@href").extract()
            items.append(item)

        return items
