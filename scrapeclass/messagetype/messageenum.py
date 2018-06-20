from enum import Enum
from linebot.models import (
    TemplateSendMessage, ButtonsTemplate, URITemplateAction
)

class MessageEnum(Enum):
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
	MESSAGE_WITHOUT_FIGURE = lambda title, content, got_page_url\
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