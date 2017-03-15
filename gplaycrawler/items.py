# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class GplaycrawlerItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = Field()
    Url = Field()
    Description = Field()
    DeveloperName = Field()
    Genre = Field()
    Price = Field()
    Preregister = Field()
    Ratings = Field()
    FiveStarRatings = Field()
    FourStarRatings = Field()
    ThreeStarRatings = Field()
    TwoStarRatings = Field()
    OneStarRatings = Field()
    ReviewsAverage = Field()
    ContentRating = Field()
    WhatsNew = Field()
    LastUpdated = Field()
    Downloads = Field()
    CurrentVersion = Field()
    AndroidVersion = Field()
    DeveloperWebsite = Field()
    DeveloperEmail = Field()
    DeveloperAddress = Field()
    PrivacyPolicyLink = Field()
    Permissions = Field()
    pass
