from scrapeclass.scrapeclass import ScrapeClass
from bs4 import BeautifulSoup as bs
import requests
from linebot import LineBotApi
from linebot.models import (
    TemplateSendMessage, ButtonsTemplate, URITemplateAction
)

# YahooNewsの情報を送信するクラス
class YahooScrape(ScrapeClass):
    continue_sel = ".newsLink"
    figure_url_sel = "div.thumb img"

    def __init__(self, user_list, access_token, selector):
        super().__init__(user_list, access_token, selector)

    # LINEに送信する情報を取得する
    def scrapeWeb(self):
        got_url = self.soup_one.select_one(self.url_sel).attrs["href"]
        
        res_two = requests.get(got_url)
        soup_two = bs(res_two.content, "html.parser")

        if soup_two.select_one(self.continue_sel):
            self.got_page_url = soup_two.select_one(self.continue_sel).attrs["href"]
            print(self.got_page_url)
            res_three = requests.get(self.got_page_url)
            soup_three = bs(res_three.content, "html.parser")

        self.figure_url = soup_three.select_one(self.figure_url_sel).attrs['src']
        self.title = soup_three.select_one("h1").text
        self.content = soup_three.select_one("p.ynDetailText").text

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
