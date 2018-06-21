import requests
from bs4 import BeautifulSoup as bs

from scrapeclass.scrapeclass import ScrapeClass

# YahooNewsの情報を送信するクラス
class YahooScrape(ScrapeClass):
    # 続きを読むボタンのセレクター
    continue_sel = ".newsLink"

    #　詳細ページの画像URLを取得するためのセレクター
    figure_url_sel = "div.thumb img"

    # 一覧ページから取得する番号,0が一番上を表す。
    hiera = 0

    # コンストラクタ、親クラスに情報を渡し、スクレイピングするための情報をフィールドに格納する。
    def __init__(self, scrape_data):
        super().__init__(scrape_data)

    # LINEに送信する情報を取得する
    def scrapeWeb(self):
        got_url = self.soup_one.select(self.url_sel)[self.hiera].attrs["href"]

        res_two = requests.get(got_url)
        soup_two = bs(res_two.content, "html.parser")

        # 続きを読むボタンが存在すれば、さらに詳細ページを取得する。
        if soup_two.select_one(self.continue_sel):
            self.got_page_url = soup_two.select_one(self.continue_sel).attrs["href"]
            print(self.got_page_url)
            res_three = requests.get(self.got_page_url)
            soup_three = bs(res_three.content, "html.parser")
        else:
            soup_three = soup_two

        # 画像がなかった場合、画像をなしのメッセージテンプレートを選択する。
        try:
            self.figure_url = soup_three.select_one(self.figure_url_sel).attrs['src']
        except AttributeError:
            self.figure_url = None

        # 情報が取得できなかった場合、ページ構造が異なると仮定し、一つ下のページを取得する。
        try:
            self.title = soup_three.select_one("h1").text
            self.content = soup_three.select_one("p.ynDetailText").text
        except AttributeError:
            self.hiera += 1
            if self.hiera == 3:
                return
            self.scrapeWeb()
            return
