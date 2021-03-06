import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from linebot.models import TextSendMessage

from scrapeclass.scrapeclass import ScrapeClass

# TOEIC日替わり問題を送信するためのクラス
class ToeicScrape(ScrapeClass):

    # コンストラクタ、親クラスに情報を渡し、スクレイピングするための情報をフィールドに格納する。
    def __init__(self, scrape_data):
       super().__init__(scrape_data)

    # LINEに送信する情報を取得する
    def scrapeWeb(self):
        self.title = self.soup_one.select_one(self.title_sel).text
        content = self.soup_one.select_one(self.contents_sel).text
        self.content = content[:content.find("あなたの答え") - 4] +\
             "\n\n\n\n\n" + content[content.find("正解："):]

    # LINEに送信する情報を成形する。
    def returnSendMessage(self):
        text_message = TextSendMessage(
            text = self.title + "\n" + self.content
        )

        return text_message