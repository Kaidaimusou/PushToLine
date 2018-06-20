from scrapeclass.scrapeclass import ScrapeClass
from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urljoin

# LifeHackerの情報をLINEに送信するためのクラス
class LifeHackerScrape(ScrapeClass):

    # 画像のURLを取得するためのセレクター
    figure_url_sel = "div.lh-entryDetail-body img"

    def __init__(self, scrape_data):
        super().__init__(scrape_data)

    # LINEに送信するための情報を取得するクラス
    def scrapeWeb(self):
        # 相対URLの取得
        url_ref = self.soup_one.select_one(self.url_sel).attrs['href']

        # 絶対URLの生成
        self.got_page_url = urljoin(self.base_url, url_ref)
        print(self.got_page_url)
        request = requests.get(self.got_page_url)
        soup = bs(request.content, "html.parser")

        # Lineに送信する情報の抽出を行う。
        try:
            self.figure_url = soup.select_one(self.figure_url_sel)['data-src']

        except AttributeError:
            self.figure_url = None

        self.title = soup.select_one(self.title_sel).text
        self.content = soup.select_one(self.contents_sel).text
