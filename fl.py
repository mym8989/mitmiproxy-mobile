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

print("################### init ######################")
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
    #print("delete ads:" + flow.request.url)
    charset = 'utf8'
    if '=' in content_type:
      charset = content_type.split('=')[1]
    #htmltxt = flow.response.content
    #html = BeautifulSoup(flow.response.text, "html.parser")
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

    '''
    RULES_PATH = '/data/280blocker_adblock_nanj_supp.txt'
    with open(RULES_PATH, 'r') as f:
      lines = f.read().splitlines()

    # get elemhide rules (prefixed by ##) and create a CSSSelector for each of them
    rules = [CSSSelector(line[2:]) for line in lines if line[:2] == '##']
    print("rules=")
    print(rules)
    def remove_ads(tree):
      for rule in rules:
          for matched in rule(tree):
              matched.getparent().remove(matched)

    doc = html.document_fromstring(str(flow.response.content))
    #remove_ads(doc)
    
    flow.response.content = str(doc.tostring)
    '''
  
  if "content-type" in flow.response.headers and "content-length" in flow.response.headers:
    ru = str(flow.request.url)
    ae = str(flow.request.headers["accept-encoding"])
    ct = str(flow.response.headers["content-type"])
    cl = int(flow.response.headers["content-length"])
    s = io.BytesIO(flow.response.content)
    s2 = io.BytesIO()
    if (cl) > 100:

     # 画像を jpeg quality 10/100 に変換する
     if (ct) [0:6] == ("image/") and (cl) > 1000 and (ct) [0:9] != ("image/svg"):
         start = time.time()
         if (ct) [0:9] == ("image/png"):
           img = Image.open(s)
           if img.mode == 'RGBA' or "transparency" in img.info:
             img.save(s2, "png", optimize=True, bits=8)
           else:
             img = Image.open(s).convert("RGB")
             img.save(s2, "jpeg", quality=10, optimize=True, progressive=True)
             flow.response.headers["content-type"] = "image/jpeg"
         else:
           img = Image.open(s).convert("RGB")
           img.save(s2, "jpeg", quality=10, optimize=True, progressive=True)
           flow.response.headers["content-type"] = "image/jpeg"
         flow.response.content = s2.getvalue()
         ct2 = str(flow.response.headers["content-type"])
         cl2  = int(flow.response.headers["content-length"])
         i = int(cl2 /cl * 100)
         elapsed_time = time.time() - start
         print("                   image *** compressed %s percent, size = %s/%s bytes, %s to %s, %s is processed, %s sec ***" % (i, cl2, cl, ct, ct2, ru, str(round(elapsed_time, 1))))
         return

     # スキームが http のテキストを gzip 圧縮する
     elif flow.request.scheme == "http" and not "content-encoding" in flow.response.headers:
         flow.response.headers["content-encoding"] = "none"     
         if (ct) [0:5] == ("text/") or (ct) [0:12] == ("application/") or (ct) [0:9] == ("image/svg"):
             start = time.time()
             gz = gzip.GzipFile(fileobj=s2, mode='w')
             gz.write(flow.response.content)
             gz.close()
             flow.response.content = s2.getvalue()
             ce = str(flow.response.headers["content-encoding"])
             flow.response.headers["content-encoding"] = "gzip"
             ct2 = str(flow.response.headers["content-type"])
             cl2 = int(flow.response.headers["content-length"])
             ce2 = str(flow.response.headers["content-encoding"])
             i = int(cl2 / cl * 100)
             elapsed_time = time.time() - start
             print("                   gzip *** compressed %s percent, size = %s/%s bytes, %s to %s, %s to %s, %s is processed, %s sec ***" % (i, cl2, cl, ct, ct2, ce, ce2, ru, str(round(elapsed_time, 1))))
#             return

     # スキームが https のテキストを brotli 圧縮する
     elif flow.request.scheme == "https" and not "content-encoding" in flow.response.headers:
         flow.response.headers["content-encoding"] = "none"
         if (ct) [0:5] == ("text/") and (ct) [0:10] != ("text/plain") and (ct) [0:9] != ("text/html") or (ct) [0:12] == ("application/") and (ct) [0:16] != ("application/json") or (ct) [0:9] == ("image/svg"):
             start = time.time()
             s2 = flow.response.content
             s3 = brotli.compress(s2, quality=10)
             flow.response.content = s3
             ce = str(flow.response.headers["content-encoding"])
             flow.response.headers["content-encoding"] = "br"
             ct2 = str(flow.response.headers["content-type"])
             cl2 = int(flow.response.headers["content-length"])
             ce2 = str(flow.response.headers["content-encoding"])
             i = int(cl2 / cl * 100)
             elapsed_time = time.time() - start
             print("                   brotli *** compressed %s percent, size = %s/%s bytes, %s to %s, %s to %s, %s is processed, %s sec ***" % (i, cl2, cl, ct, ct2, ce, ce2, ru, str(round(elapsed_time, 1))))
#             return

     else:
         ce = str(flow.response.headers["content-encoding"])
         print("*** %s, %s, %s, %s is not processed ***" % (ce, ct, cl, ru))

