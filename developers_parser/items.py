# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class News(scrapy.Item):
    developer_name = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    header = scrapy.Field()
    
