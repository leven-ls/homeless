# -*- coding: utf-8 -*-
# @Author: levenls
# @Date:   2016-09-29 17:40:30
# @Last Modified by:   leven-ls
# @Last Modified time: 2016-10-06 17:15:20

from bs4 import BeautifulSoup

s = u"<div class='div-cun'>9513<span>元/平</span></div>"

soup = BeautifulSoup(s, "lxml")

for i in soup.strings:
	print i

print soup.strings.next()
	