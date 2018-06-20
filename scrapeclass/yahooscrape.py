from scrapeclass.scrapeclass import ScrapeClass
from bs4 import BeautifulSoup as bs
import requests

# YahooNewsの情報を送信するクラス
class YahooScrape(ScrapeClass):
    continue_sel = ".newsLink"
    figure_url_sel = "div.thumb img"

    def __init__(self, scrape_data):
        super().__init__(scrape_data)

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
        else:
            soup_three = soup_two

        try:
            self.figure_url = soup_three.select_one(self.figure_url_sel).attrs['src']
        except AttributeError:
            self.figure_url = None

        self.title = soup_three.select_one("h1").text
        self.content = soup_three.select_one("p.ynDetailText").text
