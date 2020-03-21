mitmdump --ssl-insecure -s /data/fl.py -s request.py --set stream_large_bodies=10m \
 --anticomp --set block_global=false --set flow_detail=1

#tail -f nohup.out
