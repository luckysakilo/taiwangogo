from flask import Flask, request, abort
from bs4 import BeautifulSoup
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

import configparser

def keywords(x):
    allresult=''
    dic={'古蹟巡禮':'31','打卡熱點':'24','生態體驗':'18','地質奇觀':'17','寺廟祈福':'22','非吃不可':'27','逛夜市':'54','單車漫遊':'26','森林步道':'40','無障礙':'34','網美必拍':'43','賞夜景':'21','親子共遊':'23','藝術':'30','鐵道旅遊':'42','觀景平台':'37'}
    keywords=dic.get(x,'none')
    url='https://www.taiwan.net.tw/m1.aspx?sNo=0000193&id='+keywords
    webpage=requests.get(url)
    webpage.encoding='UTF-8'  #抓取頁面
    soup=BeautifulSoup(webpage.text,'html.parser') #讀取網頁文字檔
    hotspots = soup.find_all('div',class_='card-wrap')
    for i in hotspots[0:10]:
        spot_name = i.find('div', 'card-title').text.strip()
        link=i.select('a',class_='card-link')[0]['href']
        tag=i.find('span',class_='target-mark color-orange').text
        allresult+='[{}]{}\nhttps://www.taiwan.net.tw/{}\n____________________\n'.format(tag, spot_name,link)
    return allresult

def search_place(x):
    allresult=''
    dic={'台北市':'0001090','新北市':'0001091','基隆市':'0001105','宜蘭縣':'0001106','桃園市':'0001107','新竹縣':'0001108','新竹市':'0001109','苗栗縣':'0001110','台中市':'0001112','彰化縣':'0001113','南投縣':'0001114','雲林縣':'0001115','嘉義縣':'0001116','嘉義市':'0001117','臺南市':'0001119','高雄市':'0001121','屏東縣':'0001122','花蓮縣':'0001124','臺東縣':'0001123','澎湖縣':'0001125','金門縣':'0001126','連江縣':'0001127'}
    city=dic.get(x,'none')
    url='https://www.taiwan.net.tw/m1.aspx?sNo='+city
    webpage=requests.get(url)
    webpage.encoding='UTF-8'  #抓取頁面
    soup=BeautifulSoup(webpage.text,'html.parser') #讀取網頁文字檔
    hotspots = soup.find_all('div', {'class':'card-wrap'})
    for i in hotspots[0:10]:
        spot_name = i.find('div', 'card-title').text.strip()
        view=i.find('p',class_='target target-like').text
        link=i.select('a',class_='card-link')[0]['href']
        hashtag=i.find('div',class_='hashtag').text
        allresult+='{}\n{}\n{}\nhttps://www.taiwan.net.tw/{}\n________________\n'.format(spot_name,view,hashtag,link)
    return allresult

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config_2.ini')
access_token = config['line-bot']['access_token']
secret = config['line-bot']['secret']

line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secret)
#--------------------------------------------------------#

app = Flask(__name__)
app.config['DEBUG'] = True

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 機器人說話

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    usersend=event.message.text
    if usersend in ['縣市','[縣市]']:
        message = TextSendMessage(text='請輸入旅遊的台灣縣市(ex.台北市):')
    elif usersend in ['[標籤]','標籤']:
        message = TextSendMessage(text='請輸入標籤(ex.打卡熱點):\n[選項]\n古蹟巡禮/打卡熱點/生態體驗/地質奇觀/寺廟祈福/非吃不可/逛夜市/單車漫遊/森林步道/無障礙/網美必拍/賞夜景/親子共遊/藝術/鐵道旅遊/觀景平台\n')
    elif usersend in ['古蹟巡禮','打卡熱點','生態體驗','地質奇觀','寺廟祈福','非吃不可','逛夜市','單車漫遊','森林步道','無障礙','網美必拍','賞夜景','親子共遊','藝術','鐵道旅遊','觀景平台']:
        message = TextSendMessage(text=keywords(usersend))
    elif usersend in ['台北市','新北市','基隆市','宜蘭縣','桃園市','新竹縣','新竹市','苗栗縣','台中市','彰化縣','南投縣','雲林縣','嘉義縣','嘉義市','臺南市','高雄市','屏東縣','花蓮縣','臺東縣','澎湖縣','金門縣','連江縣']:
        message = TextSendMessage(text=search_place(usersend))
    else:
        message = TextSendMessage(text='哈囉~請輸入要查詢：[縣市]/[標籤]?')
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    message = TextSendMessage(text='哈囉~請輸入要查詢：[縣市]/[標籤]?')
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    import os
    port=int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port)

