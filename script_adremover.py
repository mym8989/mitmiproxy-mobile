#!/usr/bin/env python3
#thank you! -> https://qiita.com/tongari0/items/ffa3297630547c3bb712
from PIL import Image
import io, time, gzip
import brotli
from bs4 import BeautifulSoup
from lxml import html
from lxml.cssselect import CSSSelector
import requests
import cgi
import time

print("################### init script_adremover.py ######################")
url = "https://280blocker.net/files/280blocker_adblock_nanj_supp.txt"
blist_txt = requests.get(url).text
blist = []
for line in blist_txt.split("\r\n"):
  if line[:2] == '##':
    blist.append(line[2:])

print(blist)



def response(flow):
  content_type = flow.response.headers.get('Content-Type', '')
  if content_type.startswith('text/html'):
    charset = 'utf8'
    if '=' in content_type:
      charset = content_type.split('=')[1]
    print("delete ads:" + content_type + "->" + charset + ": " + flow.request.url)
    t1 = time.time()
    html = BeautifulSoup(flow.response.content, "html.parser", from_encoding=charset )
    print("           BeautifulSoup:" + str(round(time.time()-t1, 1)) + "sec")
    if html.head:
      delcount = 0
      t1 = time.time()
      for bkey in blist:
        for col in html.select(bkey):
          col.extract()
          delcount+=1
      flow.response.content = str(html).encode(charset)
      print("           " + str(round(time.time()-t1, 1)) + "sec: delcount=" + str(delcount))
