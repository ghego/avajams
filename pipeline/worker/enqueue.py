# Here is how to queue tasks from Python.
from iron_worker import *

import csv
dr = csv.DictReader(open("input.csv"))

worker = IronWorker(project_id=your_project_id, token=your_project_token)

for row in dr:
	url = row['urls']	
	task = worker.queue(code_name="hello", payload={"url": url })
	print url
	print task.id
