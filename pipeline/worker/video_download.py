import os
import csv
import sys
from lib.assets.webrequest import WebRequest
from urllib import urlopen, unquote
from urlparse import parse_qs, urlparse
import argparse
import urllib2

def convert_embed_to_watch(url):
  components = url.replace('embed', 'watch').split("/")
  root = "/".join(components[:-1])
  video_id = components[-1]
  video_url = root +"?v="+video_id
  return video_url, video_id

def download_file(url, video_id):
  print video_id 
  content = urlopen(url).read()
  fpath = os.path.join(os.environ['PROJECT_ROOT'], "data") 
  os.makedirs(fpath)
  fname = os.path.join(fpath, "video_" + video_id+'.mp4')
  print fname
  f = open(fname, 'wb')
  f.write(content)
  f.close()
  return fname


## Core Function to send to workers
def convert_embed_url_and_download(embed_url):
  uri = 'http://www.clipconverter.cc/check.php'
  headers = [('Accept', "application/json"), ('Referer', "http://www.clipconverter.cc/"), ('Origin', 'http://www.clipconverter.cc'), ('Content-Type', 'application/x-www-form-urlencoded')]
  video_url, video_id = convert_embed_to_watch(embed_url)
  print video_url

  data = 'mediaurl=' + video_url +'&filename=&filetype=&format=&audiovol=0&audiochannel=2&audiobr=128&videobr=224&videores=352x288&videoaspect=&customres=320x240&timefrom-start=1&timeto-end=1&id3-artist=&id3-title=&id3-album=ClipConverter.cc&auto=0&hash=&image=&org-filename=&videoid=&pattern=&server=&serverinterface=&service=&ref=&lang=en&client_urlmap=none&ipv6=false&addon_urlmap=&cookie=&addon_cookie=&addon_title=&ablock=1&clientside=0&addon_page=none&verify=&addon_browser=&addon_version='
  print uri

  #response = WebRequest.get(uri, headers=headers, data=data, timeout=30)
  
  import urllib2
  import json

  response = urllib2.urlopen('http://www.clipconverter.cc/check.php', timeout=20, data=data).read()
  response = json.loads(response)
  if response.get('redirect'):
    raise Exception("Captcha validation requested |{}|".format(response))
  try:
    video_items = sorted([r for r in response['url'] if r['filetype'] == 'MP4' and r.get('checked')], key=lambda x: x['size'])
  except:
    print response
    raise
  
  if len(video_items):
    v = video_items[0]
  else:
    video_items = sorted([r for r in response['url'] if r['filetype'] == 'MP4'], key=lambda x: x['size'])
    v = video_items[0]
  
  # print video_url, v['url'][:], v['size']
  filename = download_file(v['url'], video_id)
  return filename

### Usage
#downloaded_file_path = convert_embed_url_and_download('https://www.youtube.com/embed/fDrTbLXHKu8')
