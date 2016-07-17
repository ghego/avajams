from app import app
from flask import render_template, jsonify, request, url_for, redirect, session
from pipeline.worker.image_extract import *
from werkzeug.utils import secure_filename
from mashup.compile import *
from train.recommend import main as recommend

@app.route('/')
def index():
  return render_template('index.html', msg="Hello world")


@app.route('/upload_forms')
def upload_forms():
  return render_template('upload_forms.html', msg="Hello world")


@app.route('/upload', methods=['POST'])
def upload():
  app.logger.info(request.files)
  upload_file = request.files['file']
  if upload_file:
    filename = secure_filename(upload_file.filename)
    destination_path = os.path.join(app.config['STATIC_VIDEO_FOLDER'], filename)
    print upload_file.save(destination_path)
    try:
      os.makedirs("".join(destination_path.split(".")[:-1]))
    except:
      pass
    static_video_url = "static/video/%s"%(filename)
    extract_images(destination_path)

    image_match, video_match = recommend("".join(destination_path.split(".")[:-1]) + "/20.jpg")
    video_id = image_match[0].split("_")[-1]

  embed_url = 'https://www.youtube.com/embed/%s'%(video_id)
  

  matched_video_path = app.config['STATIC_VIDEO_FOLDER'] + "/video_%s.mp4"%(video_id)
  out_path = app.config['STATIC_VIDEO_FOLDER'] + "/chopped_video_%s.webm"%(video_id)
  compile_clips(destination_path, matched_video_path, out_path=out_path)


  chopped_static_url = "static/video/chopped_video_%s.webm"%(video_id)

  return jsonify(msg='test', embed_url=embed_url, static_video_url=static_video_url, chopped_static_url=chopped_static_url)


@app.route('/api/ping')
def ping():
  app.logger.info(jsonify(msg="success"))
  return jsonify(msg="success")