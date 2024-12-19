import scrapy
from scrapy.spiders import SitemapSpider

from developers_parser.items import News

class LsrSpider(SitemapSpider):
    name = "lsr"

    sitemap_urls = ["https://www.lsr.ru/sitemap_msk.xml"]

    sitemap_rules = [
        ('/novosti/', 'parse_news'),
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36',  
    }
    
    def parse_news(self, response):
        item = News()
        item['developer_name'] = 'ЛСР'
        item['url'] = response.url
        item['date'] = response.xpath('/html/body/div[2]/main/div/section[2]/div/div/div/div/div[1]/span/text()').get()
        item['date'] = item['date'].replace('января', '01').replace('февраля', '02').replace('марта', '03')
        item['date'] = item['date'].replace('апреля', '04').replace('мая', '05').replace('июня', '06')
        item['date'] = item['date'].replace('июля', '07').replace('августа', '08').replace('сентября', '09')
        item['date'] = item['date'].replace('октября', '10').replace('ноября', '11').replace('декабря', '12')
        item['date'] = item['date'].replace(' ', '.')
        item['header'] = response.xpath('/html/body/div[2]/main/div/section[2]/div/div/div/div/div[2]/h1/text()').get()
        return item
