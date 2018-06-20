from scrapeclass.scrapeclass import ScrapeClass
from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urljoin
from linebot.models import TextSendMessage

# TOEIC日替わり問題を送信するためのクラス
class ToeicScrape(ScrapeClass):

    def __init__(self, user_list, access_token, scrape_data):
       super().__init__(scrape_data)

    # LINEに送信する情報を取得する
    def scrapeWeb(self):
        self.title = self.soup_one.select_one(self.title_sel).text
        content = self.soup_one.select_one(self.contents_sel).text
        self.content = content[:content.find("あなたの答え") - 4] +\
             content[content.find("正解：")]

    # LINEに送信する情報を成形する。
    def returnSendMessage(self):
        text_message = TextSendMessage(
            text = self.title + self.content
        )

        return text_message