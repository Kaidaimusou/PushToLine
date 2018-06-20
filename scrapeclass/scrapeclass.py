from linebot import LineBotApi
import requests
from bs4 import BeautifulSoup as bs

class ScrapeClass:

    def __init__(self, scrape_data):
        self.base_url = scrape_data['url']
        self.url_sel = scrape_data['url_selector']
        self.title_sel = scrape_data['title_selector']
        self.contents_sel = scrape_data['contents_selector']
        self.res_one = requests.get(self.base_url)
        self.soup_one = bs(self.res_one.content, "html.parser", from_encoding=content_type_encoding)

    def scrapeWeb(self):
        pass

    def returnSendMessage(self):
        pass