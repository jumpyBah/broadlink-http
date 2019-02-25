#!/usr/bin/env python

import time
import BaseHTTPServer
import broadlink
import base64
import yaml
import binascii
HOST_NAME = '192.168.1.88' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8321 
BROADLINK = "192.168.1.99"
DEVICE = 10039
global y



def br_init():
  global BROADLINK
#  BROADLINK=broadlink.discover(local_ip_address="192.168.1.214")
  DEVICE = y["broadlink"]["device"]
  HOST = y["broadlink"]["host"]
  MACR = y["broadlink"]["macreverse"]
  mac = bytearray.fromhex(MACR)
  BROADLINK = broadlink.gendevice(DEVICE, (HOST, 80), mac)
  BROADLINK.auth()
  return
  
def br_send(data):
  global BROADLINK
  BROADLINK.send_data(base64.b64decode(data))
  return

def br_learn():
  global BROADLINK
  BROADLINK.enter_learning()
  ir = BROADLINK.check_data()
  while ir == None:
    ir = BROADLINK.check_data()
  return base64.b64encode(ir)

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
  def do_GET(s):
    global y
    """Respond to a GET request."""
    path = ""
    path = s.path
#    if s.path == "/learn":
#      s.send_response(200)
#      s.send_header("Content-type", "text/html")
#     s.end_headers()
#     s.wfile.write(br_learn())
#     return
    if path.split("/")[1] == "send":
      br_send(y["commands"][path.split("/")[2]])
      s.send_response(302)
      s.send_header('Location', "/")
      s.end_headers()
      return
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    s.wfile.write("<html><body>ok<br>")
    return

if __name__ == '__main__':
  with open("config.yaml", 'r') as stream:
    try:
      y = yaml.load(stream)
    except yaml.YAMLError as exc:
      print(exc)
      exit

  y["server"]["port"]
  
  br_init()
  server_class = BaseHTTPServer.HTTPServer
  httpd = server_class((y["server"]["host"], y["server"]["port"]), MyHandler)
#  print time.asctime(), "Server Starts - %s:%s" % (y["server"]["host"], y["server"]["port"])
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
    httpd.server_close()
#  print time.asctime(), "Server Stops - %s:%s" % (y["server"]["host"], y["server"]["port"])
