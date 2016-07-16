import sys
sys.path.append("packages")
import iron_mq
from iron_worker import *
from video_download import *
from image_extract import *
from upload_s3 import *

payload = IronWorker.payload()
print 'payload: %s' % payload 
url = payload['url']

print "url:", url

#downloaded_file_path = convert_embed_url_and_download(url)
#print "download file path:", downloaded_file_path 
downloaded_file_path = "test_video.mp4"
upload_s3(downloaded_file_path)

#images = extract_images("./test_video.mp4")
print 'Here is the task_id: %s' %  IronWorker.task_id()
