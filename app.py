import requests
import re
import random
import configparser
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient
from random import randrange

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

"""from linebot.models import (
    ImageCarouselTemplate, ImageCarouselColumn
)"""


app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])
client_id = config['imgur_api']['Client_ID']
client_secret = config['imgur_api']['Client_Secret']
# album_id = config['imgur_api']['Album_ID']
API_Get_Image = config['other_api']['API_Get_Image']

album_id = random.choice(['CTHOg', 'DydG5', 'R77q1'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'


def ptt_hot():
    target_url = 'http://disp.cc/b/PttHot'
    print('Start parsing pttHot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for data in soup.select('#list div.row2 div span.listTitle'):
        title = data.text
        link = "http://disp.cc/b/" + data.find('a')['href']
        if data.find('a')['href'] == "796-59l9":
            break
        content += '{}\n{}\n\n'.format(title, link)
    return content


def movie():
    target_url = 'http://www.atmovies.com.tw/movie/next/0/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('ul.filmNextListAll a')):
        if index == 20:
            return content
        title = data.text.replace('\t', '').replace('\r', '')
        link = "http://www.atmovies.com.tw" + data['href']
        content += '{}\n{}\n'.format(title, link)
    return content


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)

    if event.message.text.lower() == "pick" or event.message.text == "抽":
        album_id = random.choice(['CTHOg', 'DydG5', 'R77q1', '8rwr1', 'qcXCJ', 'TnnUK', 'tQ7uZ', '8otXg', 'cIZ63', ',x5Wzd', '729rZ', 'XGXEV', 'LLGww', 'xsVtq', 'veIy2'])
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images(album_id)
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0

    if event.message.text.lower() == "test":
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='目錄 template',
                template=ButtonsTemplate(
                    title='Template-樣板介紹',
                    text='Template分為四種，也就是以下四種：',
                    thumbnail_image_url='圖片網址',
                    actions=[
                        MessageTemplateAction(
                            label='Buttons Template',
                            text='Buttons Template'
                        ),
                        MessageTemplateAction(
                            label='Confirm template',
                            text='Confirm template'
                        ),
                        MessageTemplateAction(
                            label='Carousel template',
                            text='Carousel template'
                        ),
                        MessageTemplateAction(
                            label='Image Carousel',
                            text='Image Carousel'
                        )
                    ]
                )
            )
        )
        return 0

    if event.message.text.lower() == "pp" or event.message.text == "抽男":
        album_id = random.choice(['eAmGJ'])
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images(album_id)
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0

    """if event.message.text.lower() == "test":
        line_bot_api.reply_message(
            event.reply_token,
            ImagemapSendMessage(

                base_url='https://i.imgur.com/ctNbzlw.jpg',
                alt_text='this is an imagemap',
                base_size=BaseSize(height=1040, width=1040),
                actions=[
                    MessageImagemapAction(
                        text='hello',
                        area=ImagemapArea(
                            x=520, y=0, width=520, height=1040
                        )
                    )
                ]


            )
        )
        return 0"""

    """if event.message.text.lower() == "test":
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://example.com/item1.jpg',
                            title='this is menu1',
                            text='description1',
                            actions=[
                                PostbackTemplateAction(
                                    label='postback1',
                                    text='postback text1',
                                    data='action=buy&itemid=1'
                                ),
                                MessageTemplateAction(
                                    label='message1',
                                    text='message text1'
                                ),
                                URITemplateAction(
                                    label='uri1',
                                    uri='http://example.com/1'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://example.com/item2.jpg',
                            title='this is menu2',
                            text='description2',
                            actions=[
                                PostbackTemplateAction(
                                    label='postback2',
                                    text='postback text2',
                                    data='action=buy&itemid=2'
                                ),
                                MessageTemplateAction(
                                    label='message2',
                                    text='message text2'
                                ),
                                URITemplateAction(
                                    label='uri2',
                                    uri='http://example.com/2'
                                )
                            ]
                        )
                    ]
                )
            )
        )
        return 0"""




    """if ("pick" in event.message.text.lower() and len(event.message.text) > 4) or (
                "抽" in event.message.text and len(event.message.text) > 2):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="要打'pick'或者'抽'我才會提供圖喔!"))
            return 0"""

    """if event.message.text.lower() == "test":
        album_id = random.choice(['CTHOg', 'DydG5', 'R77q1', '8rwr1', 'qcXCJ','TnnUK'])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(type='text',text=album_id))"""

    """if event.message.text.lower() == "test":
        album_id = random.choice(['CTHOg', 'DydG5', 'R77q1', '8rwr1', 'qcXCJ'])
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images(album_id)
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        line_bot_api.reply_message(event.reply_token, TextSendMessage(type='text', text=url))
        return 0"""

    if event.message.text.lower() == "小魯自我介紹":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="哈囉~大家好，我是小魯，我專門為大家帶來美女圖提振大家的精神~~\n1. 打'pick'或者'抽'可以抽一張美女圖\n2. 打'movie'或'熱門電影'可以取得最新的熱門電影資訊\n3. 要跟我對話請在內容加上'小魯'or'洨魯'or'LL'(Little Lu的簡稱，大小寫都可)這樣我才會回!\n4. 在群組中，除了關鍵字外我也會偶爾貼個美女圖或者一段簡短回話刷一下存在感A___A (此功能暫時關閉)\n5. 小魯爸不會收集對話內容(沒這麼閒)，請放心使用\n6. 打'pp'或者'抽男'可以抽一張帥哥圖\n7. 要顯示此段說明請打'小魯自我介紹'"))
        return 0

    if event.message.text.lower() == "movie" or event.message.text == "熱門電影":
        content = movie()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="近期上映的電影:\n" + content))
        return 0

    """if ("小魯" in event.message.text or "洨魯" in event.message.text or "ll" in event.message.text.lower()) and (
            "a" in event.message.text.lower() or "色" in event.message.text or "18" in event.message.text or "sex" in event.message.text):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="沒有A圖 快將圖庫提供給我爸!"))
        return 0"""

    if ("小魯" in event.message.text or "洨魯" in event.message.text) and (
            "爸" in event.message.text and "誰" in event.message.text):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=random.choice(
            ["我爸就是小魯爸阿", "我爸是帥哥", "我爸是魯魯 所以才會生小魯", "我爸?請上網google'金城武'", "別問我爸是誰 你會怕", "我爸就金城武阿不是說很多次了"])))
        return 0

    if "jizz" == event.message.text.lower() or "射了" == event.message.text or "身寸" in event.message.text or "插" == event.message.text or "米分" in event.message.text or "想舔" in event.message.text or "想趴" in event.message.text or "%%" in event.message.text or "想幹" in event.message.text or "ininder" in event.message.text.strip() or "硬了" in event.message.text.strip() or "石更" in event.message.text.strip() or "女乃" in event.message.text.strip() or "豆頁" in event.message.text.strip():
        album_id = 'Q2Bfm'
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images(album_id)
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0

    if ("小魯" in event.message.text and "小魯哥" not in event.message.text) or "洨魯" in event.message.text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=random.choice(
                ["所以呢?", "阿不就好棒棒", "幹嘛?你在想色色的事情對不對?", "笑點呢?", "看什麼看?你是不是想幹人家?", "好啦聽我說 其實我覺得你今天蠻帥的",
                 "cue我幹嘛?剛剛傳給你那麼多A圖還不夠?", "再玩我我就要被玩壞拉!!", "不要玩我啊～～～", "先別說這個了 你昨天私敲我說終於突破3秒是真的嗎?", "不要亂cue我", "關我P事",
                 "在說啥呢傻逼～", "怎麼了?又要嫌我的圖醜嗎?", "叫我幹嘛?我給的圖拿去尻尻了沒?", "不准說我跟我爸壞話!", "帥哥你好 叫我嗎?", "樓上的每天私下跟我抽幾十張不膩嗎?", "汪汪！",
                 "再亂cue我 我就要翹起來囉 我是說翹中指", "是是是 你最棒", "大哥你是對的"])))
        return 0

    if "fuck" in event.message.text or "幹他媽" in event.message.text or "三小" in event.message.text or "啥小" in event.message.text or "靠北" in event.message.text or "幹" == event.message.text or "操" == event.message.text or "他媽的" in event.message.text.lower() or "馬的" in event.message.text.lower() or "幹你娘" in event.message.text.lower() or "機掰" in event.message.text.lower() or "機歪" in event.message.text.lower() or "靠杯" in event.message.text.lower() or "靠背" in event.message.text.lower() or "靠邀" in event.message.text.lower():
        if (random.randint(0, 2)) >= 0:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text=random.choice(
                    ["別亂罵髒話啦", "好啦別生氣～～", "好兇喔～～", "這麼兇 倫家會怕怕", "別生氣了　等等傳給你好看的", "誰讓你生氣了叫他出乃面對", "欸你怎麼這樣說話！"])))
        return 0

    if "又囉" in event.message.text:
        image_message = ImageSendMessage(
            original_content_url='https://i.imgur.com/ptDWQCN.jpg',
            preview_image_url='https://i.imgur.com/ptDWQCN.jpg'
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0

    if random.randint(0, 30) == 0:
        if (random.randint(0, 1)) > 2:
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text=random.choice(
                                           ["提醒大家要跟我對話一定要加上'小魯' or '洨魯' or 'LL' 我才會回你喔", "笑點呢?", "沒錯沒錯", "就是這樣~", "ㄎㄎ",
                                            "ㄏㄏ", "嘻嘻"])))
        else:
            album_id = random.choice(['CTHOg', 'DydG5', 'R77q1', '8rwr1', 'qcXCJ', 'TnnUK', 'tQ7uZ', '8otXg', 'cIZ63', ',x5Wzd', '729rZ', 'XGXEV', 'LLGww', 'xsVtq', 'veIy2'])
            client = ImgurClient(client_id, client_secret)
            images = client.get_album_images(album_id)
            index = random.randint(0, len(images) - 1)
            url = images[index].link
            image_message = ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )
            line_bot_api.reply_message(
                event.reply_token, image_message)
            return 0


if __name__ == '__main__':
    app.run()