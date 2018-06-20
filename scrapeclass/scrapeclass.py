from linebot import LineBotApi
import requests
from bs4 import BeautifulSoup as bs

class ScrapeClass:
    
    def __init__(self, user_list, access_token, scrape_data):
        self.user_list = user_list
        self.line = LineBotApi(channel_access_token=access_token)
        self.base_url = scrape_data['url']
        self.url_sel = scrape_data['url_selector']
        self.title_sel = scrape_data['title_selector']
        self.contents_sel = scrape_data['contents_selector']
        self.res_one = requests.get(self.base_url)
        content_type_encoding = self.res_one.encoding if self.res_one.encoding != 'ISO-8859-1' else None
        self.soup_one = bs(self.res_one.content, "html.parser", from_encoding=content_type_encoding)
    
    def scrapeWeb(self):
        pass
    
    def sendToLine(self):
        pass