# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from ConfigPackage import CrawConfig as config
import re,requests,time
# 初始页面
OriginPage='https://www.dianping.com/member/133803355/'

# 存放已经爬取过的url
CHECKED_USER =[]
# 存放待爬取的url
CHECKING_USER =[]
# 存放已经爬取过的店面
CHECKING_SHOP={}
# 头部信息
headers = config.HEADERS
# 代理
proxies = config.PROXIES

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
    print soup
    dataSoup=soup.find('div',class_='txt')
    # 抓取用户信息
    userName=dataSoup.find('h2',class_='name').text
    userInfo['userName']=userName
    # 点评数目
    userInfo['reviewNum']=soup.find('a',class_='col-link',href=re.compile("reviews$")).text
    # 收藏数目
    userInfo['contentNum']=soup.find('a',class_='col-link',href=re.compile("wishlists$")).text
    # 签到次数
    userInfo['checkIn']=soup.find('a',class_='col-link',href=re.compile("checkin$")).text
    # 图片个数
    userInfo['picNum']=soup.find('a',class_='col-link',href=re.compile("album$")).text
    # 榜单数目（什么乱七八糟）
    userInfo['listNum']=soup.find('a',class_='col-link',href=re.compile("mylists$")).text
    # 发帖数目
    userInfo['bbsNum']=soup.find('a',class_='col-link',href=re.compile("groups$")).text

    # 社交信息
    socialSoup=soup.find('div',class_='container-box home-container')
    # 关注数目
    userInfo['followNum']=socialSoup.find('a',href=re.compile("follows$")).text
    # 粉丝数目
    userInfo['fansNum']=socialSoup.find('a',href=re.compile("fans$")).text
    # 互动数目
    userInfo['interNum']=socialSoup.find('span',class_='col-link').text

    # for key in userInfo:
    #     print key,":",userInfo[key]

def handleFollowsPage(url):
    userHome = url.split('/')[0] + '//' + url.split('/')[2] + '/' + url.split('/')[3] + '/' + url.split('/')[4]
    # 处理用户关注信息
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser", from_encoding='utf-8')
    # print soup.prettify()
    followsData = soup.find('div', class_='modebox fllow-list')
    followLink = followsData.findAll('a', class_='J_card')
    for follow in followLink:
        # print config.HOME+follow['href']
        print follow['href'].split('/')[2]

        # 用户是否爬取过
        if follow['href'].split('/')[2] in CHECKED_USER:
            continue
        else:
            CHECKED_USER.append(follow['href'].split('/')[2])
            CHECKING_USER.append(config.HOME + follow['href'])

def handUserContent(url):
    userHome=url.split('/')[0]+'//'+url.split('/')[2]+'/'+url.split('/')[3]+'/'+url.split('/')[4]
    contentList=[]
    # 处理用户的评论信息
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.text, "html.parser", from_encoding='gb2312')

    # print soup.prettify()

    # 分析用户对每家店面的评论信息
    contentData = soup.find('div', class_='modebox comm-list')
    if contentData is not None:
        contentMsg=contentData.findAll('div',class_='txt J_rptlist')
        for content in contentMsg:
            shopUrl=content.find('a',class_='J_rpttitle')['href']
            print content.find('div',class_='mode-tc comm-entry').text

            # shopContentInfo=getShopInfo(shopUrl)
            # shopContentInfo['content']=content.find('div',class_='mode-tc comm-entry').text.encode('utf-8')
            # contentList.append(shopContentInfo)
    else :
        print 'content None'
    # 翻页

    pageIndex=soup.find('div',class_='pages-num')
    if pageIndex is not None:
        # print 'now page:'+pageIndex.find('span',class_='cur').text
        netxContentPageUrl=userHome+'/reviews'+pageIndex.find('a',class_='page-next')['href']
        handUserContent(netxContentPageUrl)
    return contentList
def getShopInfo(shopUrl):
    shopID=shopUrl.split('/')
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

# handleUserPage('https://www.dianping.com/member/1175663717')
handUserContent('https://www.dianping.com/member/1094091/reviews')
# handleFollowsPage('https://www.dianping.com/member/819235579/follows')
