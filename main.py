from sqlconn.mysqlconn import MySQLConn
from scrapeclass.lifehackerscrape import LifeHackerScrape
from scrapeclass.toeicscrape import ToeicScrape
from scrapeclass.yahooscrape import YahooScrape
from linebot import LineBotApi

account = {
    "db": "webapp",
    "host": "localhost",
    "user": "root",
    "passwd": "rootroot"
}

# 登録してあるWEBサイトの数
WEB_SITE_N = 3

# LINEのMessaging APIに接続するためのチャンネルアクセストークン
ACCESS_TOKEN = "0GKT3HsJjvy59nx185ZwloyKRx7+FvvUBpCZ+zfm78KNGzas+pZT//FJblg965j4GRUB8kA8FGkdaQFYAMqM+340xSRFTfcOoWbrLi5xRVoWIn86LJEKfLaW6V+NQFKk0i1VSh0VnzOa9Re7I4I6xAdB04t89/1O/w1cDnyilFU="

# url, userの情報を取得するためのqueryのテンプレート
URL_QUERY = "SELECT * FROM url WHERE id = %d"
USER_QUERY = "SELECT * FROM user WHERE url_id = %d"

# サイトごとのidの割り当て
YAHOO = 1
TOEIC = 2
LIFEHACK = 3

# 波田のテスト用LINE ID
LINE_TEST_ID = "Uf4910c7b2fb5ea0275dc87660fd07c37"

# LINEに接続する。
LINE = LineBotApi(channel_access_token=ACCESS_TOKEN)

with MySQLConn(account) as connect:
    cursor = connect.cursor(dictionary=True)

    for url_id in range(1, WEB_SITE_N + 1):

        # url_idごとにユーザーのリストを取得する。
        cursor.execute(USER_QUERY % url_id)
        user_list = cursor.fetchall()

        # 送信するユーザーがいなければスキップ
        if(len(user_list) == 0):
            continue

        # サイトをスクレイピングする情報を取得する。
        cursor.execute(URL_QUERY % url_id)
        scrape_data = cursor.fetchone()

        # idによって呼び出すクラスを切り替える。
        if(url_id == YAHOO):
            print("1")
            SC = YahooScrape(scrape_data)
        elif(url_id == TOEIC):
            continue
            print("2")
            SC = ToeicScrape(scrape_data)
        elif(url_id == LIFEHACK):
            print("3")
            SC = LifeHackerScrape(scrape_data)

        # 各サイトからスクレイピングを行いLINEに情報を送信する。
        SC.scrapeWeb()
        send_message = SC.sendToLine()
        for user in user_list:
            line.push_message(to=user["line_id"], messages=send_message)

    cursor.close()