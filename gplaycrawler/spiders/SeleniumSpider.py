from gplaycrawler.items import GplaycrawlerItem
from scrapy import signals
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import urlparse


class SeleniumSpider(CrawlSpider):

    name = "selenium"

    def __init__(self):
        super(SeleniumSpider, self).__init__()
        self.allowed_domains = [ "play.google.com" ]
        self.start_urls = [ "https://play.google.com/store/apps/" ]
        self.rules = (
            Rule(LinkExtractor(allow=('/store/apps/collection/',))),
            Rule(LinkExtractor(allow=('/store/apps/category/',))),
            Rule(LinkExtractor(allow=('/store/apps/details\?')),callback='parse_link'),
        )
        #self.driver = webdriver.PhantomJS()
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver.maximize_window()
        super(SeleniumSpider, self)._compile_rules()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SeleniumSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        self.driver.close()

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
        self.driver.get(response.url)
        #self.state['items_count'] = self.state.get('items_count', 0) + 1
        #titles = self.driver.find_elements_by_xpath("/html")
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

            preregButton = self.driver.find_elements_by_xpath("//button[contains(@class,'preregistration')]")
            if len(preregButton) > 0:
                item["Preregister"] = "1"
            else:
                item["Preregister"] = "0"

            # Reviews
            if len(preregButton) == 0:
                reviewList = []
                wait = WebDriverWait(self.driver, 5)
                #while len(self.driver.find_elements_by_xpath("//div[@class='details-section reviews']//button[@aria-label='See More']")) > 0:
                #    if len(self.driver.find_elements_by_xpath("//div[@class='expand-loading']")) > 0:
                #        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='details-section reviews']//button[@aria-label='See More']")))
                #    self.driver.find_element_by_xpath("//div[@class='details-section reviews']//button[@aria-label='See More']").click()
                #    sleep(0.1)
                #wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='review-text']")))
                reviews = self.driver.find_elements_by_xpath("//div[@class='review-text']")
                for review in reviews:
                    reviewList.append(review.text)
                item["UserReviews"] = reviewList
            else:
                item["UserReviews"] = "PreRegister apps have no reviews."

            # Permissions
            if len(preregButton) == 0:
                try:
                    permList = []
                    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'permissions')]")))
                    self.driver.find_element_by_xpath("//button[contains(@class,'permissions')]").click()
                    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='permission-buckets id-permission-buckets']")))
                    permissions = self.driver.find_elements_by_xpath("//ul[@class='bucket-description']//li")
                    for permission in permissions:
                        permList.append(permission.text)
                    item["Permissions"] = permList
                except NoSuchElementException:
                    item["Permissions"] = "No permission link found"
                    print "[ERROR] No permission link found."
                except TimeoutException:
                    item["Permissions"] = "Timed out waiting for permission modal to load"
                    print "[ERROR] Timed out waiting for permission modal to load."
            else:
                item["Permissions"] = "PreRegister apps have no permissions"

            #item["PermissionCategories"] = titles.xpath("//div[@class='permissions-container bucket-style']//jsl[not(contains(@style, 'display:none'))]/span/text()").extract()
            items.append(item)
        return items
