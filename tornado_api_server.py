import tornado.ioloop
import tornado.web
import tornado.concurrent
import json
import base64
import os
import uuid
import numpy as np
import time
from datetime import datetime
import random, string, pytz

MAX_PROCESS=1 

class TextHandler(tornado.web.RequestHandler):
  def post(self, *args, **kwargs):
    param = self.request.headers['time']
    message = self.request.arguments['msg'][0].decode()
    print("[{}-RECV] param:{}, message: {}".format(self.__class__.__name__,param, message))
    return self.write(bytes(json.dumps({"type":"TextHandler", "result":"ok", "data":param}), 'UTF-8'))

class ImageHandler(tornado.web.RequestHandler):
  def upload_file(self, file, f_name):
    with open(f_name, 'wb') as save_file:
      save_file.write(file['body'])

  def post(self, *args, **kwargs):
    ret = "ok"
    param = self.request.headers['time']
    request_file = self.request.files['uploadFile'][0]
    print("[{}-RECV] param: {}".format(self.__class__.__name__,param))
    
    if request_file:
      ret = "ok"
      file_name = request_file.filename
      self.upload_file(request_file, file_name)
      with open(file_name, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
      print("  file write: {}".format(file_name))
    else:
      ret = "fail"
      data = ""

    return self.write(bytes(json.dumps({'type':'ImageHandler', "result":ret, "data":data}), 'UTF-8'))

def configure_app():
  return tornado.web.Application([
    ("/ImageHandler", ImageHandler),
    ("/TextHandler", TextHandler),
  ])

if __name__ == "__main__":
  app = configure_app()
  server = tornado.httpserver.HTTPServer(app)
  server.bind(8888)
  server.start(MAX_PROCESS) # forks one process per cpu 0
  tornado.ioloop.IOLoop.current().start()

