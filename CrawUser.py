# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import re,requests,time
# 初始页面
OriginPage='https://www.dianping.com/member/133803355/'

# 存放已经爬取过的url
CHECKED_URL = []
# 存放待爬取的url
CHECKING_URL=set([])
# Key的hash去重
# 头信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
    'Cookie': 'navCtgScroll=0; showNav=#nav-tab|0|0; navCtgScroll=0; showNav=#nav-tab|0|0; _hc.v="\"28c48835-807a-422e-ba61-ad744498f777.1450593856\""; __utma=1.196682546.1450594182.1450594182.1452605452.2; __utmz=1.1452605452.2.2.utmcsr=gufensoso.com|utmccn=(referral)|utmcmd=referral|utmcct=/search/; PHOENIX_ID=0a018986-152531ce5a3-13cb4e7; s_ViewType=10; JSESSIONID=6FAF186D727AFC4CD60107EBA6D2D2D4; aburl=1; cy=1; cye=shanghai'}
# 代理
proxies = {'http': "117.175.193.42:8123",
           "https": "http://10.10.1.10:1080"}

def getResponse(url=OriginPage,headers=headers):
    #得到response
    response = requests.get(url,headers=headers)
    print response

def handleUserPage(url):
    # 处理单个用户的信息
    userInfo={}
    # 得到的response为None？
    # response=getResponse(url,headers=headers)
    # print response
    response=requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, "html.parser", from_encoding='utf-8')
    dataSoup=soup.find('div',class_='txt')
    # 抓取用户信息
    userName=dataSoup.find('h2',class_='name').text
    # 点评数目
    userInfo['reviewNum']=dataSoup.find('a',class_='col-link',href=re.compile("reviews$")).text
    # 收藏数目
    userInfo['contentNum']=dataSoup.find('a',class_='col-link',href=re.compile("wishlists$")).text
    # 签到次数
    userInfo['checkIn']=dataSoup.find('a',class_='col-link',href=re.compile("checkin$")).text
    # 图片个数
    userInfo['picNum']=dataSoup.find('a',class_='col-link',href=re.compile("album$")).text
    # 榜单数目（什么乱七八糟）
    userInfo['listNum']=dataSoup.find('a',class_='col-link',href=re.compile("mylists$")).text
    # 发帖数目
    userInfo['bbsNum']=dataSoup.find('a',class_='col-link',href=re.compile("groups$")).text

    # # 社交信息
    # socialSoup=dataSoup.find('div',class_='container-box home-container')
    # # 关注数目
    # userInfo['followNum']=socialSoup.find('a',href=re.compile("follows$"))
    # # 粉丝数目
    # userInfo['fansNum']=socialSoup.find('a',href=re.compile("fans$"))
    # # 互动数目
    # userInfo['interNum']=socialSoup.find('span',class_='col-link')


    for key in userInfo:
        print key,':',userInfo[key]
def handleFollowsPage(url):

    # 处理用户关注信息
    followUrl = url + "follows"
    response = requests.get(followUrl, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser", from_encoding='utf-8')
    followsData = soup.find('div', class_='modebox fllow-list')
    followLink = followsData.findAll('a', class_='J_card')
    for follow in followLink:
        print url
        CHECKING_URL.add(follow)

def handUserContent(url):
    contentList=[]
    # 处理用户的评论信息
    contentUrl=url+'reviews'
    response=requests.get(contentUrl,headers=headers)
    soup=BeautifulSoup(response.text, "html.parser", from_encoding='gb2312')

    # 分析用户对每家店面的评论信息
    contentData=soup.find('div',class_='modebox comm-list')
    contentMsg=contentData.findAll('div',class_='txt J_rptlist')
    for content in contentMsg:
        shopUrl=content.find('a',class_='J_rpttitle')['href']
        # print content.find('a',class_='J_rpttitle')['href']
        # print content.find('div',class_='mode-tc comm-entry').text
        shopContentInfo=getShopInfo(shopUrl)
        shopContentInfo['content']=content.find('div',class_='mode-tc comm-entry').text.encode
        contentList.append(shopContentInfo)
    return contentList
def getShopInfo(shopUrl):
    # 处理店铺的简单信息
    shopInfo={}
    response = requests.get(shopUrl, headers=headers)
    soup=BeautifulSoup(response.text, "html.parser", from_encoding='gb2312')
    # 店名
    shopName=soup.find('h1',class_='shop-name').text.split('\n')[1]
    shopInfo['shopName']=shopName
    briefinfo = soup.find('div', {'class': 'brief-info'})
    if briefinfo is None:
        return
    # 商户星级
    shopInfo['level']=briefinfo.find('span', class_="mid-rank-stars")['title'].encode('utf-8')
    # 点评数
    infos = briefinfo.findAll('span', class_='item')
    if (len(infos) == 5):
        shopInfo['commentnum'] = infos[0].text[:-3].encode('utf-8')
        # 人均消费
        shopInfo['avgCost'] = infos[1].text[3:-1].encode('utf-8')
        # 口味
        shopInfo['taste'] = infos[2].text[3:].encode('utf-8')
        # 环境
        shopInfo['env'] = infos[3].text[3:].encode('utf-8')
        # 服务
        shopInfo['service'] = infos[4].text[3:].encode('utf-8')
    elif (len(infos) == 4):
        shopInfo['commentnum'] = '0'.decode('utf-8').encode('utf-8')
        # 人均消费
        shopInfo['avgCost'] = infos[0].text[3:-1].encode('utf-8')
        # 口味
        shopInfo['avgCost'] = infos[1].text[3:].encode('utf-8')
        # 环境
        shopInfo['avgCost'] = infos[2].text[3:].encode('utf-8')
        # 服务
        shopInfo['avgCost'] = infos[3].text[3:].encode('utf-8')
    else:
        return

    return shopInfo

handleUserPage('http://www.dianping.com/member/802659774')