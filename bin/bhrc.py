#!/usr/bin/env python

import time
import BaseHTTPServer
import broadlink
import base64
import yaml
import binascii
import sys

# default parameters
HOST_NAME = '192.168.1.88'  # 
PORT_NUMBER = 8321 
BROADLINK = "192.168.1.99"  #
DEVICE = 10039              # 0x2737 hex
global y



def br_init():
  global BROADLINK
  DEVICE = y[config]["device"]
  HOST = y[config]["RMhost"]
  MACR = y[config]["macreverse"]
  mac = bytearray.fromhex(MACR)
  BROADLINK = broadlink.gendevice(DEVICE, (HOST, 80), mac)
  BROADLINK.auth()
  return
  
def br_send(data):
  global BROADLINK
  BROADLINK.send_data(base64.b64decode(data))
  return

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
############################################## 
	 
  try:
     config = sys.argv[2]
  except:
     config = "broadlink"
  print time.asctime(), "device ", config
  br_init()
  server_class = BaseHTTPServer.HTTPServer
  httpd = server_class((y[config]["host"], y[config]["port"]), MyHandler)
  print time.asctime(), "Server Starts - %s:%s" % (y[config]["host"], y[config]["port"])
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
    httpd.server_close()
  print time.asctime(), "Server Stops - %s:%s" % (y[config]["host"], y[config]["port"])
