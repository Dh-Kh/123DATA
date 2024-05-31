# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ScrapingItem(scrapy.Item):
    url = Field()
    title = Field()
    price_usd = Field()
    odometer = Field()
    username = Field()
    phone_number = Field()
    image_url = Field()
    images_count = Field()
    car_number = Field()
    car_vin = Field()
