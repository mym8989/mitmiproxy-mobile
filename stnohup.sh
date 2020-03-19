nohup mitmdump --ssl-insecure -s /data/fl_1.py --set stream_large_bodies=10m \
--ignore-hosts '(.*.twitter.com|.*.twimg.com|.*.yahoo.co.jp|.*.yahooapis.jp|.*.yimg.jp|.*.jorte.com|.*.jorte.net|dummyKaigyou\
|.*.live.com|.*.live.net|.*.onedrive.com|.*.microsoft.com|.*oneclient.sfx.ms|dummyKaigyou\
|slack.com|.*.slack.com|.*.connectivitycheck.gstatic.com|dummyKaigyou\
|.*.amazon.co.jp|.*.amazon.com|.*.media-amazon.com|.*.ssl-images-amazon.com|.*amazonvideo.com|.*.amazonaws.com|.*.amazon-adsystem.com|.*.a2z.com|dummyKaigyou\
|.*.aliexpress.com|.*.alibaba.com|.*.alicdn.com|.*.alibabausercontent.com|dummyKaigyou\
|.*.cookpad.com|.*.cpcdn.com|dummyKaigyou\
|.*.googleapis.com|.*.google.com|.*.googleusercontent.com|.*.ggpht.com|.*.accounts.google.co.jp|moneyforward.com)'\
 --anticomp --set block_global=false --set flow_detail=1

#tail -f nohup.out
