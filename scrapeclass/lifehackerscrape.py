from scrapeclass.scrapeclass import ScrapeClass
from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urljoin
from linebot import LineBotApi
from linebot.models import (
    TemplateSendMessage, ButtonsTemplate, URITemplateAction
)

# LifeHackerの情報をLINEに送信するためのクラス
class LifeHackerScrape(ScrapeClass):
    
    # 画像のURLを取得するためのセレクター
    figure_url_sel = "div.lh-entryDetail-body img"

    def __init__(self, user_list, access_token, selector):
        super().__init__(user_list, access_token, selector)

    # LINEに送信するための情報を取得するクラス
    def scrapeWeb(self):
        # 相対URLの取得
        url_ref = self.soup_one.select_one(self.url_sel).attrs['href']
        
        # 絶対URLの生成
        self.got_page_url = urljoin(self.base_url, url_ref)
        request = requests.get(self.got_page_url)
        soup = bs(request.content, "html.parser")
        
        # Lineに送信する情報の抽出を行う。
        self.figure_url = soup.select_one(self.figure_url_sel)['data-src']
        self.title = soup.select_one(self.title_sel).text
        self.content = soup.select_one(self.contents_sel).text
    
    # LINEに情報を送信する。
    def sendToLine(self):
        button_message = TemplateSendMessage(
            alt_text=self.title[:37] + "...",
            template=ButtonsTemplate(
                thumbnail_image_url=self.figure_url,
                title=self.title[:37] + "...",
                text=self.content[:57] + "...",
                actions=[
                    URITemplateAction(
                        label='記事を見る',
                        uri=self.got_page_url
                    )
                ]
            )
        )
        for user in self.user_list:
            self.line.push_message(to=user["line_id"], messages=button_message)
