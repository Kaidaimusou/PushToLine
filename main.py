import os
from dotenv import load_dotenv

from linebot import LineBotApi

from sqlconn.mysqlconn import MySQLConn
from scrapeclass.lifehackerscrape import LifeHackerScrape
from scrapeclass.toeicscrape import ToeicScrape
from scrapeclass.yahooscrape import YahooScrape
from scrapeclass.messagetype.messageenum import MessageEnum

# DBにアクセスするための情報
account = {
    "db": "webapp",
    "host": "localhost",
    "user": "root",
    "passwd": "rootroot"
}

# 登録してあるWEBサイトの数
WEB_SITE_N = 3

# LINEのMessaging APIに接続するためのチャンネルアクセストークン
load_dotenv("./.env")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")

# url, userの情報を取得するためのqueryのテンプレート
URL_QUERY = "SELECT * FROM url WHERE id = %d"
USER_QUERY = "SELECT * FROM user WHERE url_id = %d"

# サイトごとのidの割り当て
YAHOO = 1
TOEIC = 2
LIFEHACK = 3

# LINEに接続する。
LINE = LineBotApi(channel_access_token=ACCESS_TOKEN)

# MYSQLに接続し情報を取得する。
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
            print("2")
            SC = ToeicScrape(scrape_data)
        elif(url_id == LIFEHACK):
            print("3")
            SC = LifeHackerScrape(scrape_data)

        # 各サイトからスクレイピングを行いLINEに情報を送信する。
        try:
            SC.scrapeWeb()
            send_message = SC.returnSendMessage()
        except:
            send_message = MessageEnum.MESSAGE_ERROR

        for user in user_list:
            LINE.push_message(to=user["line_id"], messages=send_message)

    cursor.close()