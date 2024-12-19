import scrapy
from scrapy.spiders import SitemapSpider

from developers_parser.items import News

class DonstroiSpider(SitemapSpider):
    name = "donstroi"

    sitemap_urls = ["https://donstroy.moscow/sitemap-iblock-6.xml"]

    sitemap_rules = [
        ('/press/news/', 'parse_news'),
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36',  
    }
    
    def parse_news(self, response):
        item = News()
        item['developer_name'] = 'Донстрой'
        item['url'] = response.url
        item['date'] = response.xpath('/html/body/main/div/div[1]/div[1]/div[3]/div[1]/div/text()').get()
        item['header'] = response.xpath('/html/body/main/div/div[1]/div[1]/h1/text()').get()
        return item
