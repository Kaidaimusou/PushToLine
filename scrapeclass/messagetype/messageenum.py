from enum import Enum
from linebot.models import (
    TemplateSendMessage, ButtonsTemplate, URITemplateAction
)

# めーせーじテンプレートを列挙型で定義
class MessageEnum(Enum):
    # ページに画像がある場合のメッセージテンプレート
	MESSAGE_WITH_FIGURE = lambda title, figure_url, content, got_page_url\
		: TemplateSendMessage(
            alt_text = title[:37] + "...",
            template = ButtonsTemplate(
                thumbnail_image_url = figure_url,
                title = title[:37] + "...",
                text = content[:57] + "...",
                actions = [
                    URITemplateAction(
                        label = '続きを見る',
                        uri = got_page_url
                    )
                ]
            )
        )
    # ページに画像がない場合のメッセージテンプレート
	MESSAGE_WITHOUT_FIGURE = lambda title, content, got_page_url\
		: TemplateSendMessage(
            alt_text = title[:37] + "...",
            template = ButtonsTemplate(
                title = title[:37] + "...",
                text = content[:57] + "...",
                actions = [
                    URITemplateAction(
                        label = '続きを見る',
                        uri = got_page_url
                    )
                ]
            )
        )

    MESSAGE_ERROR = TextSendMessage(
            text = "本日はメンテナンス中です。\nご迷惑をおかけしております。"
        )