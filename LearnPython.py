# -*- coding: UTF-8 -*-
# encoding:utf-8
# from ConfigPackage import CrawConfig as config
#
# print config.HEADERS

# http='http://www.dianping.com/shop/69498877'
# urlSplit=http.split('/')
# # for s in str:
# #     print s,
#
# httpUrl= urlSplit[0] + '//' + urlSplit[1] + urlSplit[2] + '/' + urlSplit[3] + '/' + urlSplit[4]
# print httpUrl

# dic={'a':'aaaaa',
#      'b':'bbbbb'}
# print type(dic.keys())
#
# for key in dic.keys():
#     print key

# dic={1:'aaaa',
#      2:'bbbbb'}
# dic[2]='cccc'
# for key in dic.keys():
#     print dic[key]

# JSON TEST
import json
import os
import codecs
path='Data/tex'
dic1={1:'哈哈',
      2:'bbbbb'}
# for key in dic1.keys():
#     print dic1.get(key)
dic2={3:'ccccc',
      4:'ddddd'}
dic3={'e':dic1,
      'f':dic2}
jsonstr=json.dumps(dic3,ensure_ascii=False)
print jsonstr
# file_path='Data/TestPath'
# if os.path.exists(file_path) == False:
#     os.makedirs(file_path)
# file_name='test.txt'
# fullPath=os.path.join(file_path,file_name)
# fp=codecs.open(fullPath,'w','UTF_8')


# with open(fullPath,'a') as out:
#     out.write(jsonstr+'\n')
#     out.write(jsonstr)

# 递归
# cons=[]
# def func(contents,count=0):
#     if (count < 5):
#         contents.append(str(count))
#         count=count+1
#         func(contents,count)
#     return contents
# for content in func(cons,0):
#     print content