FROM python:latest
USER root

RUN apt-get update
RUN apt-get upgrade -y python3
#RUN apt-get -y install locales && \
#    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
#ENV LANG ja_JP.UTF-8
#ENV LANGUAGE ja_JP:ja
#ENV LC_ALL ja_JP.UTF-8
#ENV TZ JST-9
#ENV TERM xterm

RUN apt-get install -y nano less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
#RUN pip install mitmproxy
RUN pip install mitmproxy pillow-simd brotli pillow beautifulsoup4 lxml

#RUN /usr/local/bin/mitmdump --ssl-insecure -s /data/fl.py --set stream_large_bodies=10m --ignore-hosts '(mzstatic.com|apple.com|icloud.com|mobilesuica.com|crashlytics.com|google-analytics.com|tokyo-ame2.jwa.or.jp)' --anticomp --set block_global=false --set flow_detail=2

EXPOSE 8080

#ENTRYPOINT ["/bin/bash"] 

