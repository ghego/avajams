import sys
sys.path.append("packages")
import iron_mq
from iron_worker import *
from video_download import *


payload = IronWorker.payload()
print 'payload: %s' % payload 
url = payload['url']

print url
downloaded_file_path = convert_embed_url_and_download(url)
print downloaded_file_path 
print 'Here is the task_id: %s' %  IronWorker.task_id()
