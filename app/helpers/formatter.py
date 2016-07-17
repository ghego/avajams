import datetime
import time
import pytz
import json
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
  
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      timeLocal = pytz.utc.localize(obj).astimezone(pytz.timezone('US/Pacific-New'))
      return timeLocal.strftime('%Y-%m-%d %I:%M:%S %p %Z')
    elif isinstance(obj, datetime.time):
      return obj.strftime("%H:%M:%S")
    elif hasattr(obj, 'serialize'):
      return obj.serialize
    else:
      return JSONEncoder.default(self,obj)

def custom_jsonify(obj):
  return json.dumps(obj, cls=CustomJSONEncoder) 