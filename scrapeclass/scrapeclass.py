from linebot import LineBotApi
import requests
from bs4 import BeautifulSoup as bs
from scrapeclass.messagetype.messageenum import MessageEnum

class ScrapeClass:
    # LINEのメッセージオブジェクト作成に関するデータ
    title = ""
    figure_url = ""
    content = ""
    got_page_url = ""

    # 共通で使うスクレイピングのデータを格納する。
    def __init__(self, scrape_data):
        self.base_url = scrape_data['url']
        self.url_sel = scrape_data['url_selector']
        self.title_sel = scrape_data['title_selector']
        self.contents_sel = scrape_data['contents_selector']
        self.res_one = requests.get(self.base_url)
        self.soup_one = bs(self.res_one.content, "html.parser")

    def scrapeWeb(self):
        pass

    # LINEに送信する情報を成形する。
    def returnSendMessage(self):
        # ページに画像が存在するかでメッセージテンプレートを選択する。
        if self.figure_url:
            message = MessageEnum.MESSAGE_WITH_FIGURE(self.title, self.figure_url, self.content, self.got_page_url)
        else:
            message = MessageEnum.MESSAGE_WITHOUT_FIGURE(self.title, self.content, self.got_page_url)
        return message