import scrapy
from scrapy.spiders import SitemapSpider

from developers_parser.items import News

class PikSpider(SitemapSpider):
    name = "pik"

    sitemap_urls = ["https://cdn.pik.ru/sitemap/pik/news.xml"]

    def parse(self, response):
        item = News()
        item['developer_name'] = 'ПИК'
        item['url'] = response.url
        item['date'] = response.xpath('//*[@id="__next"]/div[3]/div/div/div[1]/div[2]/text()').get()
        item['date'] = item['date'].replace('января', '01').replace('февраля', '02').replace('марта', '03')
        item['date'] = item['date'].replace('апреля', '04').replace('мая', '05').replace('июня', '06')
        item['date'] = item['date'].replace('июля', '07').replace('августа', '08').replace('сентября', '09')
        item['date'] = item['date'].replace('октября', '10').replace('ноября', '11').replace('декабря', '12')
        item['date'] = item['date'].replace(' ', '.')
        item['header'] = response.xpath('//*[@id="__next"]/div[3]/div/div/div[2]/h1/text()').get()
        return item
