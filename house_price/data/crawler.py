# -*- coding: utf-8 -*-
# @Author: levenls
# @Date:   2016-09-29 17:27:41
# @Last Modified by:   leven-ls
# @Last Modified time: 2016-10-07 17:07:15


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
        


@after_grab
def grab(url):
    print "try to grab page ", url 
    r = requests.get(url, timeout= 30)
    soup = BeautifulSoup(r.content, "lxml")

    tradedHoustList = soup.find("ul", class_="clinch-list").find_all('li')

    if not tradedHoustList:
        return 

    for item in tradedHoustList:

        # 房屋详情链接，唯一标识符
        houseUrl = item.find("h2").a["href"] or ''


        if houseUrl in grabedPool["data"]:
            print houseUrl, " 已经存在，跳过，开始抓取下一个"
            continue

        print '开始抓取' , houseUrl


        # 抓取 小区，户型，面积
        title = item.find("h2").a
        if title:
            xiaoqu, houseType, square = (item.find("h2").a.string.split(" "))
        else:
            xiaoqu, houseType, square = ('Nav', 'Nav', 'Nav')


        # 成交时间，朝向，楼层
        houseInfo = item.find("div", class_="con").string

        if houseInfo:
            if len(houseInfo.split("/")) == 2:
                orientation, floor = ([x.strip() for x in houseInfo.split("/")])
                buildInfo = 'Nav'
            if len(houseInfo.split("/")) == 3:
                orientation, floor, buildInfo = ([x.strip() for x in houseInfo.split("/")])

        div_cuns =  item.find_all("div", class_="div-cun")

        if div_cuns:
            tradeData = datetime.datetime.strptime(div_cuns[0].get_text(), '%Y.%m.%d') or datetime.datetime(1990, 1, 1)
            perSquarePrice = div_cuns[1].strings.next() or 'Nav'
            totalPrice = div_cuns[2].strings.next() or 'Nav'
        

        # 通过 ORM 存储到 sqlite
        tradeItem = TradedHouse(
                                xiaoqu = xiaoqu,
                                houseType = houseType,
                                square = square,
                                houseUrl = houseUrl,
                                orientation = orientation,
                                floor = floor,
                                buildInfo = buildInfo,
                                tradeDate = tradeData,
                                perSquarePrice = perSquarePrice,
                                totalPrice = totalPrice,
                                )


        tradeItem.save()

        # 添加到已经抓取的池
        grabedPool["data"].add(houseUrl)
        

    # 抓取完成后，休息几秒钟，避免给对方服务器造成大负担
    time.sleep(random.randint(10,30))


if __name__== "__main__":
    start()
