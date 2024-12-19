import pandas as pd
import scrapy 
from scrapy.crawler import CrawlerProcess
from developers_parser.spiders.pik_spider import PikSpider
from developers_parser.spiders.lsr_spider import LsrSpider
from developers_parser.spiders.fsk_spider import FskSpider
from developers_parser.spiders.donstroi_spider import DonstroiSpider

process = CrawlerProcess({
    'USER_AGENT': 
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36'
})

def parse_developer(developer):
    if developer == 'pik':
        process.crawl(PikSpider)
    elif developer == 'lsr':
        process.crawl(LsrSpider)
    elif developer == 'fsk':
        process.crawl(FskSpider)
    elif developer == 'donstroi':
        process.crawl(DonstroiSpider)
    
    process.start()
    
def read_json(developer_small_name, end_date):
    data = pd.read_json(f'developers_parser/result_{developer_small_name}.json')
    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')
    #if end_date is None or end_date == '' or data['date'].max() < end_date :
    #    parse_developer(developer_small_name)
    #    data = pd.read_json(f'developers_parser/result_{developer_small_name}.json')
    #    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')
    return data
    
def get_data(developers, start_date=None, end_date=None):
    if 'ПИК' in developers:
        data_pik = read_json('pik', end_date)
    else:
        data_pik = None
    if 'ЛСР' in developers:
        data_lsr = read_json('lsr', end_date)
    else:
        data_lsr = None
    if 'ФСК' in developers:
        data_fsk = read_json('fsk', end_date)
    else:
        data_fsk = None
    if 'Донстрой' in developers:
        data_donstroi = read_json('donstroi', end_date)
    else:
        data_donstroi = None
        
    data = pd.concat([data_pik, data_lsr, data_fsk, data_donstroi], ignore_index=True)
    if start_date is None or start_date == '':
        start_date = data['date'].min()
    if end_date is None or end_date == '':
        end_date = data['date'].max()
        
    data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    return data
    
