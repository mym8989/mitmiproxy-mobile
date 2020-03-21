from mitmproxy import http


def request(flow: http.HTTPFlow) -> None:
  # pretty_host takes the "Host" header of the request into account,
  # which is useful in transparent mode where we usually only have the IP
  # otherwise.
  blist = ["microad", "degwas", "baidu.com"]
  for bkey in blist:
    if bkey in flow.request.pretty_host:
      flow.request.url = "http://10.142.0.3/blank.html"
      
