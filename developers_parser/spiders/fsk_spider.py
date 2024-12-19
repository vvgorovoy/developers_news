import scrapy
from scrapy.spiders import SitemapSpider

from developers_parser.items import News

class FskSpider(SitemapSpider):
    name = "fsk"

    sitemap_urls = ["https://fsk.ru/sitemap/news.xml"]

    sitemap_rules = [
        ('/about/news/', 'parse_news'),
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36',  
    }
    
    def parse_news(self, response):
        item = News()
        item['developer_name'] = 'ФСК'
        item['url'] = response.url
        item['date'] = response.xpath('//*[@id="__layout"]/div/main/div/article/div/div/div[2]/time/text()').get()
        item['date'] = item['date'].replace('января', '01').replace('февраля', '02').replace('марта', '03')
        item['date'] = item['date'].replace('апреля', '04').replace('мая', '05').replace('июня', '06')
        item['date'] = item['date'].replace('июля', '07').replace('августа', '08').replace('сентября', '09')
        item['date'] = item['date'].replace('октября', '10').replace('ноября', '11').replace('декабря', '12')
        item['date'] = item['date'].replace(' ', '.')
        item['header'] = response.xpath('//*[@id="__layout"]/div/main/div/article/div/div/div[1]/h1/text()').get()
        return item
