# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from Config import CrawConfig as config
import re,requests,time,os,json,sys
reload(sys)
sys.setdefaultencoding('utf8')
# 初始页面
OriginPage=config.ORIGIN_PAGE

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
    userHome = url.split('/')[0] + '//' + url.split('/')[2] + '/' + url.split('/')[3] + '/' + url.split('/')[4]
    userInfo={}
    userContents=[]
    # 得到的response为None？
    # response=getResponse(url,headers=headers)
    # print response

    # time.sleep(config.SLEEP_TIME)
    response=requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, "html.parser", from_encoding='utf-8')
    dataSoup=soup.find('div',class_='txt')
    # 抓取用户信息
    userName=dataSoup.find('h2',class_='name').text.encode('utf-8')
    userInfo['userName']=userName.encode('utf-8')
    userInfo['userHome']=userHome.encode('utf-8')
    # 点评数目
    userInfo['reviewNum']=soup.find('a',class_='col-link',href=re.compile("reviews$")).text.encode('utf-8')
    # 收藏数目
    userInfo['contentNum']=soup.find('a',class_='col-link',href=re.compile("wishlists$")).text.encode('utf-8')
    # 签到次数
    userInfo['checkIn']=soup.find('a',class_='col-link',href=re.compile("checkin$")).text.encode('utf-8')
    # 图片个数
    userInfo['picNum']=soup.find('a',class_='col-link',href=re.compile("album$")).text.encode('utf-8')
    # 榜单数目（什么乱七八糟）
    userInfo['listNum']=soup.find('a',class_='col-link',href=re.compile("mylists$")).text.encode('utf-8')
    # 发帖数目
    userInfo['bbsNum']=soup.find('a',class_='col-link',href=re.compile("groups$")).text.encode('utf-8')

    # 社交信息
    socialSoup=soup.find('div',class_='container-box home-container')
    # 关注数目
    userInfo['followNum']=socialSoup.find('a',href=re.compile("follows$")).text.encode('utf-8')
    # 粉丝数目
    userInfo['fansNum']=socialSoup.find('a',href=re.compile("fans$")).text.encode('utf-8')
    # 互动数目
    userInfo['interNum']=socialSoup.find('span',class_='col-link').text.encode('utf-8')


    # 用户的评论信息
    userContentUrl = userHome + '/reviews'
    print userContentUrl
    handUserContent(userContentUrl,userContents)
    # 用户信息持久化
    userInfo_json=json.dumps(userInfo,ensure_ascii=False).encode('utf-8')
    outFolder=config.USERINFO_FOLDER
    if os.path.exists(outFolder) == False:
        os.makedirs(outFolder)
    outFileName=url.split('/')[4]
    filePath=os.path.join(outFolder,outFileName)

    with open(filePath,'a') as outFile:
        # print '正在写入'+userName+'的数据'
        outFile.write(userInfo_json+'\n')
        for content in userContents:
            outFile.write(json.dumps(content,ensure_ascii=False).encode('utf-8')+'\n')

def handleFollowsPage(url):
    userHome = url.split('/')[0] + '//' + url.split('/')[2] + '/' + url.split('/')[3] + '/' + url.split('/')[4]
    # 处理用户关注信息
    # time.sleep(config.SLEEP_TIME)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser", from_encoding='utf-8')
    # print soup.prettify()
    followsData = soup.find('div', class_='modebox fllow-list')
    # 判断用户是否公开了自己的关注
    if followsData is not None:
        followLink = followsData.findAll('a', class_='J_card')
        for follow in followLink:
            # 用户是否爬取过
            if follow['href'].split('/')[2] in CHECKED_USER:
                continue
            else:
                CHECKED_USER.append(follow['href'].split('/')[2])
                CHECKING_USER.append(config.HOME + follow['href'])
                print config.HOME + follow['href']

def handUserContent(url,contentsList):
    userHome=url.split('/')[0]+'//'+url.split('/')[2]+'/'+url.split('/')[3]+'/'+url.split('/')[4]
    # 处理用户的评论信息
    # time.sleep(config.SLEEP_TIME)
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.text, "html.parser", from_encoding='gb2312')

    # print soup.prettify()

    # 分析用户对每家店面的评论信息
    contentData = soup.find('div', class_='modebox comm-list')
    if contentData is not None:
        contentMsg=contentData.findAll('div',class_='txt J_rptlist')
        for content in contentMsg:
            shopContentInfo = {}
            shopUrl=content.find('a',class_='J_rpttitle')['href']
            # shopContentInfo=getShopInfo(shopUrl)
            shopContentInfo['content']=content.find('div',class_='mode-tc comm-entry').text.encode('utf-8')
            contentsList.append(shopContentInfo)
    else :
        print 'content None'

    # 翻页
    pageIndex=soup.find('div',class_='pages-num')
    if pageIndex is not None:
        if pageIndex.find('a',class_='page-next') is not None:
            netxContentPageUrl=userHome+'/reviews'+pageIndex.find('a',class_='page-next')['href']
            handUserContent(netxContentPageUrl,contentsList)
        else:
            return
    else:
        return
    return contentsList

def getShopInfo(shopUrl):
    urlSplit=shopUrl.split('/')
    shopHome=urlSplit[0] + '//' + urlSplit[1] + urlSplit[2] + '/' + urlSplit[3] + '/' + urlSplit[4]
    shopID=urlSplit[4]
    if shopID in CHECKING_SHOP.keys():
        return CHECKING_SHOP.get(shopID)
    else:
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
            shopInfo=None
        CHECKING_SHOP[shopID]=shopInfo
    return shopInfo

# handleUserPage('https://www.dianping.com/member/135910734')
# contents=[]
# handUserContent('https://www.dianping.com/member/1094091/reviews',contents)
# print contents
# handleFollowsPage('https://www.dianping.com/member/819235579/follows')
handleFollowsPage('https://www.dianping.com/member/21718585/follows')
