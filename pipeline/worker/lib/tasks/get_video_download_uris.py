import os
import csv
import sys
from lib.assets.webrequest import WebRequest
from urllib import urlopen, unquote
from urlparse import parse_qs, urlparse
import argparse

def convert_embed_to_watch(url):
  components = url.replace('embed', 'watch').split("/")
  root = "/".join(components[:-1])
  video_id = components[-1]
  video_url = root +"?v="+video_id
  return video_url, video_id

def download_file(url, video_id):
  content = urlopen(url).read()
  fname = os.environ['PROJECT_ROOT'] + "/data/video_" + video_id+'.mp4'
  print fname
  f = open(fname, 'wb')
  f.write(content)
  f.close()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--data", help="Input data file", type=str)
  parser.add_argument("--startindex", help="Test a saved classifier", type=int, default=0)
  parser.add_argument("--endindex", help="Test a saved classifier", type=int, default=-1)
  args = parser.parse_args()

  file_path = os.path.join(os.environ['PROJECT_ROOT'], args.data)
  print "Reading file from: |{}|".format(file_path);print
  dr = csv.DictReader(open(file_path))

  rows = [r for r in dr]
  uri = 'http://www.clipconverter.cc/check.php'
  headers = [('Accept', "application/json"), ('Referer', "http://www.clipconverter.cc/"), ('Origin', 'http://www.clipconverter.cc'), ('Content-Type', 'application/x-www-form-urlencoded')]

  with open(os.environ['PROJECT_ROOT'] + "/data/video_download_urls.csv", 'w') as csvfile:
    fieldnames = ['url', 'size']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
  
    out_data = []
    for r in rows[args.startindex:args.endindex]:
      video_url, video_id = convert_embed_to_watch(r['urls'])

      data = 'mediaurl=' + video_url +'&filename=&filetype=&format=&audiovol=0&audiochannel=2&audiobr=128&videobr=224&videores=352x288&videoaspect=&customres=320x240&timefrom-start=1&timeto-end=1&id3-artist=&id3-title=&id3-album=ClipConverter.cc&auto=0&hash=&image=&org-filename=&videoid=&pattern=&server=&serverinterface=&service=&ref=&lang=en&client_urlmap=none&ipv6=false&addon_urlmap=&cookie=&addon_cookie=&addon_title=&ablock=1&clientside=0&addon_page=none&verify=&addon_browser=&addon_version='
      response = WebRequest.get(uri, headers=headers, data=data, timeout=30)
      if response.get('redirect'):
        raise Exception("Captcha validation requested |{}|".format(response))
      
      video_items = sorted([r for r in response['url'] if r['filetype'] == 'MP4' and r.get('checked')], key=lambda x: x['size'])
      
      if len(video_items):
        v = video_items[0]
      else:
        video_items = sorted([r for r in response['url'] if r['filetype'] == 'MP4'], key=lambda x: x['size'])
        v = video_items[0]
      
      print video_url, v['url'][:20], v['size']
      out = {}
      out['url'] = v['url']
      out['size'] = v['size']
      writer.writerow(out)

      # download_file(v['url'], video_id)

