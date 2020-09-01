#-*- codeing=utf-8 -*-
from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import urllib.parse
import xlwt
import sqlite3
import datetime
import pandas as pd

def main():
    today=datetime.date.today()
    today=str(today)
    baseURL = 'http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b341_c513'
    print(today)
    data = getData(baseURL)
    savepath='.\\BaiduNews'+today+'.xlsx'
    saveexcel(savepath,data)


findTitle = re.compile(r'<a class="list-title.*>(.*?)</a>')
findRank = re.compile(r'<span class="num.*>(.*?)</span>')
findLink = re.compile(r'href="(.*?)".*>新闻</a>')

def askURL(url):
    request = urllib.request.Request(url)
    html = ''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('GB2312')
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
    
    return html

def getData(url):
    datalist=[]
    html = askURL(url)
    soup = BeautifulSoup(html,'html.parser')
    # print(soup)
    # list1=['hideline','']
    
    for item in soup.find_all('tr'):
        # print(item)
        # a=input('continue?')
        data=[]
        item = str(item)
        try:
            Rank = re.findall(findRank,item)[0]
            data.append(Rank)

            Title = re.findall(findTitle,item)[0]          
            data.append(Title)

            Link = re.findall(findLink,item)[0]
            Link = Link.replace('amp;','')
            data.append(Link)
            datalist.append(data)
        except IndexError:
            1
        
    return datalist

def saveexcel(savepath,datalist):
    df = pd.DataFrame(datalist)
    df.columns=['Rank','Title','Link']
    df.to_excel(savepath,index=False)

if __name__=='__main__':
    main()
