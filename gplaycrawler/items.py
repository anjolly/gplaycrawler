# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GplaycrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = scrapy.Field()
    Description = scrapy.Field()
    DeveloperName = scrapy.Field()
    Genre = scrapy.Field()
    Price = scrapy.Field()
    Ratings = scrapy.Field()
    FiveStarRatings = scrapy.Field()
    FourStarRatings = scrapy.Field()
    ThreeStarRatings = scrapy.Field()
    TwoStarRatings = scrapy.Field()
    OneStarRatings = scrapy.Field()
    ReviewsAverage = scrapy.Field()
    ContentRating = scrapy.Field()
    WhatsNew = scrapy.Field()
    LastUpdated = scrapy.Field()
    Downloads = scrapy.Field()
    CurrentVersion = scrapy.Field()
    AndroidVersion = scrapy.Field()
    DeveloperWebsite = scrapy.Field()
    DeveloperEmail = scrapy.Field()
    DeveloperAddress = scrapy.Field()
    PrivacyPolicyLink = scrapy.Field()
    pass
