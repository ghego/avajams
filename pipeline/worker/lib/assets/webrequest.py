from urllib import urlopen, unquote
from urlparse import parse_qs, urlparse
import urllib2
import urllib
import time
import socket
import concurrent.futures
import json
import random
import datetime
from lib.assets.decorators import retry


class WebRequest:
  
  USER_AGENTS = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17', 'Mozilla/5.0 (Linux; U; Android 2.2; fr-fr; Desire_A8181 Build/FRF91) App3leWebKit/53.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.1.4322; PeoplePal 6.2)', 'Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1', 'Opera/9.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.01', 'Mozilla/5.0 (Windows NT 5.1; rv:5.0.1) Gecko/20100101 Firefox/5.0.1', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 3.5.30729)']

  @classmethod
  @retry((urllib2.URLError, socket.timeout), tries=1, delay=1, backoff=1)
  def get(self, uri, headers=[], data=None, timeout=10):
    request = urllib2.Request(uri)
    request.add_header('User-Agent', random.choice(self.USER_AGENTS))
    for header in headers:
      request.add_header(*header)

    if data and type(data) != str:
      data = json.dumps(data)

    urlfile = urllib2.urlopen(request, timeout=timeout, data=data)
    response = urlfile.read()
    urlfile.close()
    try:
      data = json.loads(response)
    except:
      return response
    return data

  @classmethod
  def multi_request(self, uris, max_workers=10, request_func='get'):
    request_func = getattr(self, request_func)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
      # Start the load operations and mark each future with its uri
      jobs = {executor.submit(request_func, uri): i for i, uri in enumerate(uris)}
      
      results = {}
      for future in concurrent.futures.as_completed(jobs):
        index = jobs[future]
        try:
          data = future.result()
          results[index] = data
        except Exception as exc:
          print('%r generated an exception: %s' % (uris[index], exc))
          results[index] = {}
        # else:
          # print index
    return results



if __name__ == '__main__':
  uri = 'http://www.clipconverter.cc/check.php'
  input_url = 'https://www.youtube.com/watch?v=N9hazmsUxrM'
  
  headers = [('Accept', "application/json"), ('Referer', "http://www.clipconverter.cc/"), ('Origin', 'http://www.clipconverter.cc'), ('Content-Type', 'application/x-www-form-urlencoded')]
  data = 'mediaurl=' + input_url +'&filename=&filetype=&format=&audiovol=0&audiochannel=2&audiobr=128&videobr=224&videores=352x288&videoaspect=&customres=320x240&timefrom-start=1&timeto-end=1&id3-artist=&id3-title=&id3-album=ClipConverter.cc&auto=0&hash=&image=&org-filename=&videoid=&pattern=&server=&serverinterface=&service=&ref=&lang=en&client_urlmap=none&ipv6=false&addon_urlmap=&cookie=&addon_cookie=&addon_title=&ablock=1&clientside=0&addon_page=none&verify=&addon_browser=&addon_version='
  response = WebRequest.get(uri, headers=headers, data=data, timeout=30)
  video_items = sorted([r for r in response['url'] if r['filetype'] == 'MP4'], key=lambda x: x['size'])
  for v in video_items:
    print v['url'], "SIZE:", v['size']

  print;print
  print v