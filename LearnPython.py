# -*- coding: UTF-8 -*-
# python    :2.7.5
# @Time     :2017/8/30 16:25
# @Author   :Link
# @Contact  :wsqihoulin@gmail.com
# @FileName :Link.py
# from ConfigPackage import CrawConfig as config
#
# print config.HEADERS

# tuple=[1,2]
#
# for i in tuple:
#     print i
#     tuple.append(i)

# print 3 == True
# import os
# path='D:\qhl1139\PycharmProjects\Data'
# if os.path.exists(path) is False:
#     os.makedirs(path)
# fileName='ababa'
# # filePath=path+'\\'+fileName
# filePath=os.path.join((path+fileName))
# print filePath
# fp=open(filePath,'a')
# fp.write('aaa')


# print f
# filePath=os.path.join(path,filename)
# with open(filePath,'a') as out:
#     out.write('aaaa')

from bs4 import BeautifulSoup
import requests
from Config  import  CrawConfig as config

def getResponse(url,headers):
    response=requests.get(url,headers=headers)

url='https://www.dianping.com/member/133803355'
getResponse(url,config.HEADERS)