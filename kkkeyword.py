import requests
from bs4 import BeautifulSoup

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

print(keywords())
    
