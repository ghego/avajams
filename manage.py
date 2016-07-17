import flask, os, signal, sys, argparse, logging
from flask_script import Manager, Shell, Server
from app import app

manager = Manager(app)


def log_messages(app, port):
  print "Server is running at http://0.0.0.0:{}/".format(port)
  print "Flask version: {}".format(flask.__version__)
  print "DEBUG: {}".format(app.config["DEBUG"])


@manager.command
@manager.option('-p', '--port', help='Port to run host on')
@manager.option('-r', '--noreload', help='Debug setting')
def dev(port=5000, noreload=False):
  port = int(port)
  debug = not noreload
  log_messages(app, port)
  app.run(host='0.0.0.0', port=port, debug=debug, threaded=True)


@manager.command
def gevent():
  ### At top
  # from gevent import monkey; monkey.patch_all()
  port = 5000
  from gevent.pywsgi import WSGIServer
  log_messages(app, port)
  http_server = WSGIServer(('0.0.0.0',5000), app)
  http_server.serve_forever()

@manager.command
def shell():
  console_handler = logging.StreamHandler(sys.stdout)
  console_handler.setLevel(logging.DEBUG)
  root = logging.getLogger()
  root.setLevel(logging.DEBUG)
  root.addHandler(console_handler)

  
  Shell(make_context=lambda: 
    dict( app=app,
          GenderClassifier=GenderClassifier
    )
  ).run(no_ipython=False, no_bpython=False)


if __name__ == '__main__':
  signal.signal(signal.SIGINT, lambda *_: sys.exit(0))  # Properly handle Control+C
  manager.run()

