import sys
sys.path.append("packages")
import iron_mq
from iron_worker import *
from video_download import *


downloaded_file_path = convert_embed_url_and_download('https://www.youtube.com/embed/fDrTbLXHKu8')
print downloaded_file_path 
print 'Hello %s' %  IronWorker.payload()['name']
print
print 'Here is the payload: %s' %  IronWorker.payload()
print 'Here is the task_id: %s' %  IronWorker.task_id()
