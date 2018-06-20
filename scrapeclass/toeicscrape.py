from scrapeclass.scrapeclass import ScrapeClass
import requests
from bs4 import BeautifulSoup as bs

from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urljoin
from linebot import LineBotApi
from linebot.models import TextSendMessage

# TOEIC日替わり問題を送信するためのクラス
class ToeicScrape(ScrapeClass):

    def __init__(self, user_list, access_token, selector):
       super().__init__(user_list, access_token, selector)

    # LINEに送信する情報を取得する
    def scrapeWeb(self):
        self.title = self.soup_one.select_one(self.title_sel).text
        content = self.soup_one.select_one(self.contents_sel).text
        self.content = content[:content.find("あなたの答え") - 4] +\
             content[content.find("正解：")]

    # LINEに情報を送信する
    def sendToLine(self):
        print(self.title)
        print()
        print(self.content)
        text_message = TextSendMessage(
            text = self.title + self.content
        )
        for user in self.user_list:
            self.line.push_message(to=user["line_id"], messages=text_message)