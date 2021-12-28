import requests
from bs4 import BeautifulSoup

#inputans=str(input('請輸入台灣縣市(ex.台北市)：')) 
#輸入程式

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
print(search_place())
