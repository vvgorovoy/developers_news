import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class NewsSpider(scrapy.Spider):
    name = 'mr'
    start_urls = ['https://www.mr-group.ru/news/']  

    def __init__(self, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36',  
    }

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(2)  

        while True:
            # Извлекаем данные
            news_blocks = self.driver.find_elements(By.CSS_SELECTOR, '#root > div > main > div._mainContainer_u91q2_8.container > div.row') 
            for block in news_blocks:
                date = block.find_element(By.CSS_SELECTOR, 'a > div._itemCardContent_1zasx_1291 > div > time').text  
                header = block.find_element(By.CSS_SELECTOR, 'a > div._itemCardContent_1zasx_1291 > div > div').text 
                url = block.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

                yield {
                    'developer_name': 'MR Group',
                    'date': date,
                    'header': header,
                    'url': url,
                }

            try:
                load_more_button = self.driver.find_element(By.CSS_SELECTOR, '#root > div > main > div._mainContainer_u91q2_8.container > button')  
                load_more_button.click()
                time.sleep(2)  
            except Exception as e:
                self.logger.info("Больше нет блоков для загрузки.")
                break

    def closed(self, reason):
        self.driver.quit()