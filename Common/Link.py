# -*- coding: UTF-8 -*-
# python    :2.7.5
# @Time     :2017/8/30 10:25
# @Author   :Link
# @Contact  :wsqihoulin@gmail.com
# @FileName :Link.py

import requests
from bs4 import BeautifulSoup
from Config import CrawConfig as config

def getResonse(url,heasders=config.HEADERS):
    response=None
    try:
        response=requests.get(url,headers=heasders)
    except :
        print 'failed archive response!'
    else:
        print 'success link '+url
        return response
    return response

def getSoup(url,heasders=config.HEADERS,resolve=config.SOUP_RESOLVE,encode=config.SOUP_ENCODE):
    soup=None
    try:
        response=getResonse(url,heasders)
        soup=BeautifulSoup(response.text,resolve,encode)
    except:
        print 'failed archive soup!'
    else:
        return soup
    return soup