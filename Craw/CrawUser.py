# -*- coding: UTF-8 -*-
# python    :2.7.5
# @Time     :2017/8/30 10:25
# @Author   :Link
# @Contact  :wsqihoulin@gmail.com
# @FileName :Link.py

from bs4 import BeautifulSoup
from Config import CrawConfig as config
from Common import Link
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

def handleUserPage(url):
    # 处理单个用户的信息
    userHome = url.split('/')[0] + '//' + url.split('/')[2] + '/' + url.split('/')[3] + '/' + url.split('/')[4]
    userInfo={}
    userContents=[]
    # 得到的response为None？
    # response=getResponse(url,headers=headers)
    # print response

    if config.SLEEP_SWITCH == True:
        time.sleep(config.SLEEP_TIME)
    # response=requests.get(url,headers=headers)
    response=Link.getResonse(url,headers)
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
    handUserContent(userContentUrl,userContents)
    # 用户信息持久化
    userInfo_json=json.dumps(userInfo,ensure_ascii=False).encode('utf-8')

    # 使用相对路径
    # outFolder=config.USERINFO_FOLDER

    # 使用绝对路径
    outFolder=config.USERINFO_ABS_FOLDER
    if os.path.exists(outFolder) == False:
        os.makedirs(outFolder)
    outFileName=url.split('/')[4]

    # 相对路径的文件夹与文件连接方式
    # filePath=os.path.join(outFolder,outFileName)

    # 绝对路径的文件连接方式
    filePath=outFolder+'\\'+outFileName
    with open(filePath,'a') as outFile:
        # print '正在写入'+userName+'的数据'
        outFile.write(userInfo_json+'\n')
        for content in userContents:
            outFile.write(json.dumps(content,ensure_ascii=False).encode('utf-8')+'\n')
            
    # 处理用户的粉丝信息
    userFollowsUrl=userHome+'/follows'
    handleFollowsPage(userFollowsUrl)
def handleFollowsPage(url):
    userHome = url.split('/')[0] + '//' + url.split('/')[2] + '/' + url.split('/')[3] + '/' + url.split('/')[4]
    # 处理用户关注信息
    if config.SLEEP_SWITCH == True:
        time.sleep(config.SLEEP_TIME)
    response = Link.getResonse(url, headers)
    soup = BeautifulSoup(response.text, "html.parser", from_encoding='utf-8')
    followsData = soup.find('div', class_='modebox fllow-list')
    # 判断用户是否公开了自己的关注
    if followsData is not None:
        followLink = followsData.findAll('a', class_='J_card')
        for follow in followLink:
            # 用户是否爬取过
            if follow['href'].split('/')[2] in CHECKED_USER:
                # print 'User Has benen CRAWED!'
                continue
            else:
                CHECKED_USER.append(follow['href'].split('/')[2])
                CHECKING_USER.append(config.HOME + follow['href'])

def handUserContent(url,contentsList):
    userHome=url.split('/')[0]+'//'+url.split('/')[2]+'/'+url.split('/')[3]+'/'+url.split('/')[4]
    # 处理用户的评论信息
    if config.SLEEP_SWITCH == True:
        time.sleep(config.SLEEP_TIME)
    response = Link.getResonse(url, headers)
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
            try:
                shopContentInfo['content']=content.find('div',class_='mode-tc comm-entry').text.encode('utf-8')
            except TypeError:
                print TabError.message
                print shopUrl
            contentsList.append(shopContentInfo)

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
    # 由于此函数调用之后，会产生大量的response，触发点评的反扒机制，需在配置代理IP之后调用，或者单独封装爬取点评的店面信息
    urlSplit=shopUrl.split('/')
    shopHome=urlSplit[0] + '//' + urlSplit[1] + urlSplit[2] + '/' + urlSplit[3] + '/' + urlSplit[4]
    shopID=urlSplit[4]
    if shopID in CHECKING_SHOP.keys():
        return CHECKING_SHOP.get(shopID)
    else:
        # 处理店铺的简单信息
        shopInfo={}
        if config.SLEEP_SWITCH == True:
            time.sleep(config.SLEEP_TIME)
        # response = requests.get(shopUrl, headers=headers)
        response = Link.getResonse(shopUrl, headers)
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

CHECKING_USER.append(config.ORIGIN_PAGE)
for userUrl in CHECKING_USER:
    handleUserPage(userUrl)