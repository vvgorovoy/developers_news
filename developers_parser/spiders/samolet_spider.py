import scrapy
from scrapy.spiders import SitemapSpider

from developers_parser.items import News

class PikSpider(SitemapSpider):
    name = "samolet"

    sitemap_urls = ["https://samolet.ru/sitemap-base.xml"]

    sitemap_rules = [
        ('/news/', 'parse_news'),
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36',  
    }
    
    def parse_news(self, response):
        item = News()
        item['developer_name'] = 'Самолет'
        item['url'] = response.url
        item['date'] = response.xpath('/html/body/main/div/div[2]/div[1]/div[1]/text()').get()
        item['header'] = response.xpath('/html/body/main/div/div[2]/div[1]/h1/text()').get()
        return item
