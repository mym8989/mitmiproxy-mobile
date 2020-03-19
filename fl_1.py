#!/usr/bin/env python3

from PIL import Image
import io, time, gzip
import brotli
from bs4 import BeautifulSoup

def response(flow):
  #print("%%%%%%%%%%%%%%%%%%%%%%%%%%")
  
  if "example_of_a_simple_html_page.htm" in flow.request.url:
    #flow.response.content = b""    # bytesタイプのascii文字
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$" + str(flow.response.content))
    print("$$$$$$$$$$$$$$$$$$$$$$$$$")
    html = BeautifulSoup(flow.response.content, "html.parser")
    if html.head:
      script = html.new_tag("script", id="mitmproxy")
      script.string = 'alert("Hello from mitmproxy!")'
      html.head.insert(0, script)
      flow.response.content = str(html).encode("utf8")

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
         print("                   image *** compressed %s percent, size = %s/%s bytes, %s to %s, %s is processed, %s sec ***" % (i, cl2, cl, ct, ct2, ru, elapsed_time))
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
             print("                   gzip *** compressed %s percent, size = %s/%s bytes, %s to %s, %s to %s, %s is processed, %s sec ***" % (i, cl2, cl, ct, ct2, ce, ce2, ru, elapsed_time))
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
             print("                   brotli *** compressed %s percent, size = %s/%s bytes, %s to %s, %s to %s, %s is processed, %s sec ***" % (i, cl2, cl, ct, ct2, ce, ce2, ru, elapsed_time))
#             return

     else:
         ce = str(flow.response.headers["content-encoding"])
         print("*** %s, %s, %s, %s is not processed ***" % (ce, ct, cl, ru))

