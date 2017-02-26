#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'bird'

# 时间：2017年2月25日15:46:02
# 使用方法：输入酒店ID，获取评论数据，每一个酒店的数据保存为一个文件夹

from urllib import request,parse
from urllib.request import urlopen
import re
import csv

# 根据输入的酒店ID获取指定酒店的评论信息
def byId(hotelId):
    #hotelId = input('请输入酒店的ID：')
    hotelId = str(hotelId)

    # 先获取酒店概况 https://hotel.jd.com/detail/16248.html酒店介绍
    hotelUrl = 'https://hotel.jd.com/detail/{}.html'.format(hotelId)
    hotelHtml = urlopen(hotelUrl).read().decode('utf-8')
    try:
        cityId = re.findall('cityId: \'(.*?)\',', hotelHtml)[0]
        poiArr = re.findall('poiArr: \'(.*?)\',', hotelHtml)[0]
        hotelTitle = re.findall('hotelTitle: \'(.*?)\',', hotelHtml)[0]
    except:
        return

    # 创建CSV文件
    column = ['酒店ID', '城市ID', '酒店名称', '酒店坐标', '客户地址', '结账天数', '结账时间', '房间类型', '星级', '评论标签', '评论内容', '客户端', 'VIP类型']
    filename = '京东酒店' + hotelId + hotelTitle + '.csv'
    with open(filename, "a+", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        csvwriter.writerow(column)


    # 抓取特定hotelID的酒店评论
    #  https://hotel.jd.com/comment/invokeComment.action?callback=comment&level=0&hotelId=290000&pageSize=10&curPage=1

    # 获取评论总数,评论页数
    preUrl = 'https://hotel.jd.com/comment/invokeComment.action?callback=comment&level=0&hotelId='
    pageUrl = '&pageSize=10&curPage='
    totalUrl = preUrl + hotelId + pageUrl + '1'
    totleHtml = urlopen(totalUrl).read().decode('utf-8')
    totleComment = re.findall('"total":(.*?)}',totleHtml)[0]
    totlePage = int(totleComment)/10 + 1
    print(totlePage)
    # 这里的page不一定是整数，可能是小数。所有的页数小于page+1

    #分别爬取每一页的评论
    page = 1
    while page < totlePage:
        if totleComment==0:
            print('该酒店无评论数据')
            break
        else :
            pass
        commentUrl = preUrl + hotelId + pageUrl + str(page)
        commentHtml = urlopen(commentUrl).read().decode('utf-8')
        adress = re.findall('"adress":"(.*?)",',commentHtml)
        checkoutDay = re.findall('"checkoutDay":(.*?),', commentHtml)
        checkoutTime = re.findall('"checkoutTime":"(.*?)",', commentHtml)
        descr = re.findall('"descr":"(.*?)",', commentHtml)
        roomType = re.findall('"roomType":"(.*?)",', commentHtml)
        source = re.findall('"source":"(.*?)",', commentHtml)
        star = re.findall('"star":(.*?),', commentHtml)
        tags = re.findall('"tags":"(.*?)",', commentHtml)
        vipType = re.findall('"vipType":"(.*?)"},', commentHtml)

        # 把获取到的信息写入CSV文件
        length = len(adress)
        i = 0
        while i < length:
            row = []
            try:
                row.append(hotelId)
            except:
                row.append('null')
            try:
                row.append(cityId)
            except:
                row.append('null')
            try:
                row.append(hotelTitle)
            except:
                row.append('null')
            try:
                row.append(poiArr)
            except:
                row.append('null')
            try:
                row.append(adress[i])
            except:
                row.append('null')
            try:
                row.append(checkoutDay[i])
            except:
                row.append('null')
            try:
                row.append(checkoutTime[i])
            except:
                row.append('null')
            try:
                row.append(roomType[i])
            except:
                row.append('null')
            try:
                row.append(star[i])
            except:
                row.append('null')
            try:
                row.append(tags[i])
            except:
                row.append('null')
            try:
                row.append(descr[i])
            except:
                row.append('null')
            try:
                row.append(source[i])
            except:
                row.append('null')
            try:
                row.append(vipType[i])
            except:
                row.append('null')

            with open(filename,'a+',newline = '',encoding='gb18030') as datacsv:
                csvwriter = csv.writer(datacsv, dialect=("excel"))
                csvwriter.writerow(row)

            i = i + 1
        print('第{}页评论保存完毕，进行下一页。。。。。'.format(page))
        page = page + 1



#批量根据hotelID获取酒店评论数据
def byIds():
    startHotelID = input('请输入起始ID：')
    hotelNum = input('请输入酒店数量：')

    num = 0
    while num <= int(hotelNum):
        hotelID = num + int(startHotelID)
        byId(hotelID)
        num = num + 1


if __name__=='__main__':
    byIds()
