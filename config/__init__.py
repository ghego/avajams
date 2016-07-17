import os
from dotenv import load_dotenv
load_dotenv(os.environ['PROJECT_ROOT']+'/.env')


PROPOGATE_EXCEPTIONS = True
# UPLOAD_FOLDER = os.environ['PROJECT_ROOT'] + "/app/data/uploads"
STATIC_VIDEO_FOLDER = os.environ['PROJECT_ROOT'] + "/app/static/video"