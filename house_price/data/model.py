# -*- coding: utf-8 -*-
# @Author: levenls
# @Date:   2016-10-04 11:52:18
# @Last Modified by:   levenls
# @Last Modified time: 2016-10-04 13:54:54

from peewee import SqliteDatabase, Model, CharField, DateTimeField


db = SqliteDatabase('house_price/data/houseprice.db')

class TradedHouse(Model):
	xiaoqu = CharField()
	houseType = CharField()
	square = CharField()
	houseUrl = CharField()
	orientation = CharField()
	floor = CharField()
	buildInfo = CharField()
	tradeDate = DateTimeField()
	perSquarePrice = CharField()
	totalPrice = CharField()

	class Meta:
		database = db


def create_table():
	db.create_tables([TradedHouse])


