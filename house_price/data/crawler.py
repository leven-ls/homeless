# -*- coding: utf-8 -*-
# @Author: levenls
# @Date:   2016-09-29 17:27:41
# @Last Modified by:   levenls
# @Last Modified time: 2016-10-04 16:12:03


import pickle
import os.path
import datetime
import time
import random


import requests
from bs4 import BeautifulSoup


from model import TradedHouse


grabedPool = {}


def before_grab(func):
    def wapper(*args, **kwargs):
        if os.path.exists("grabedPool.set"):
            with open("grabedPool.set", "rb") as f:
                grabedPool["data"] = pickle.load(f)
        else:
            grabedPool["data"] = set([])

        func(*args, **kwargs)
    return wapper


def after_grab(func):
    def wapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception, e:
            raise
        finally:
            with open("grabedPool.set" , "wb") as f:
                pickle.dump(grabedPool["data"], f)
    return wapper


@before_grab
def start():
    print grabedPool["data"]
    for i in xrange(1, 101):
        page = "http://cq.lianjia.com/chengjiao/pg{0}/".format(str(i))
        grab(page)
        break


@after_grab
def grab(url):
    print "try to grab page ",url 
    r = requests.get(url, timeout= 5)
    soup = BeautifulSoup(r.content, "lxml")

    tradedHoustList = soup.find("ul", class_="clinch-list").find_all('li')
    for item in tradedHoustList:
        try:
            xiaoqu, houseType, square = (item.find("h2").a.string.split(" "))
        except Exception, e:
            xiaoqu, houseType, square = ('Nav', 'Nav', 'Nav')

        
        houseUrl = item.find("h2").a["href"]

        try:
            orientation = item.find("div", class_="con").string.split("/")[0]
            floor = item.find("div", class_="con").string.split("/")[1].strip()
            buildInfo = item.find("div", class_="con").string.split("/")[2].strip()
        except Exception, e:
            orientation, floor, buildInfo = ('', '', '')

        try:
            dateStr = item.find_all("div", class_="div-cun")[0].get_text()
            tradeDate = datetime.datetime.strptime(dateStr, '%Y.%m.%d')
            perSquarePrice = item.find_all("div", class_="div-cun")[1].get_text()
            totalPrice = item.find_all("div", class_="div-cun")[2].get_text()
        except Exception, e:
            print 'go fuck yourself'
        


        if houseUrl in grabedPool["data"]:
            print houseUrl, " 已经存在，跳过，开始抓取下一个"
            continue

        tradeItem = TradedHouse(
                                xiaoqu = xiaoqu,
                                houseType = houseType,
                                square = square,
                                houseUrl = houseUrl,
                                orientation = orientation,
                                floor = floor,
                                buildInfo = buildInfo,
                                tradeDate = tradeDate,
                                perSquarePrice = perSquarePrice,
                                totalPrice = totalPrice,
                                )


        tradeItem.save()
        grabedPool["data"].add(houseUrl)

        """
        print xiaoqu
        print houseType
        print square
        print houseUrl
        print orientation
        print floor
        print buildInfo
        print tradeDate
        print perSquarePrice
        print totalPrice
        """
        

    # 抓取完成后，休息几秒钟，避免给对方服务器造成大负担
    time.sleep(random.randint(10,30))


start()
