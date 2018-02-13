# encoding: utf-8
# copy from https://github.com/UniSerj/BiliBili
import sys
import struct
import requests
import json
import re
import random
import xml.dom.minidom
import socket
import threading
import time
import string
import urllib
from liveutils import log

ChatPort=788
protocolVersion=1
ChatHost='livecmt-1.bilibili.com'
showDanmakuLog=True

class Client():
	def __init__(self, room_id, danmaku_filename):
		self.sock = None
		self.room_id = room_id
		self.f = open(danmaku_filename, 'w')
		self.f.write('<?xml version="1.0" encoding="UTF-8"?><i><chatserver>chat.bilibili.com</chatserver><chatid>' + str(self.room_id) + '</chatid><mission>0</mission><maxlimit>233233233</maxlimit><state>0</state><realname>0</realname><source>k-v</source>')
		self.start_time = time.time()
		self.started = False

	def handle_data(self, data):
		data_length=len(data)
		if data_length < 16:
			log("broken data. reconnecting...")
			self.connect()
		else:
			info=struct.unpack("!ihhii" + str(data_length - 16) + "s", data)
			length=info[0]

			if length > 16 and length == data_length:
				action = info[3] - 1
				if action == 4:
					msg_str = info[5].decode("utf-8",'ignore')
					msg_json = json.loads(msg_str, encoding='utf-8')
					msg_type = msg_json['cmd']
					
					if msg_type == "DANMU_MSG":
						user_name = msg_json['info'][2][1]
						comment = msg_json['info'][1]
						if showDanmakuLog:
							log('[%d] [DANMAKU] %s: %s' % (self.room_id, user_name, comment))
						self.f.write('<d p="%.5f,%d,%d,%d,%d,%d,%s,2332332332">%s</d>' % (time.time()-self.start_time, msg_json['info'][0][1], msg_json['info'][0][2],msg_json['info'][0][3],msg_json['info'][0][4],msg_json['info'][0][6],msg_json['info'][0][7],msg_json['info'][1]))
						self.f.flush()
						
			elif 16 < length < data_length:
				single_data=data[0:length]
				threading.Thread(target=self.handle_data, args=(single_data,)).start()
				remain_data=data[length:data_length]
				threading.Thread(target=self.handle_data, args=(remain_data,)).start()


	def connect(self):
		log("connecting to danmaku server...")
		uid= (int)(100000000000000.0 + 200000000000000.0*random.random())
		body='{"roomid":%s,"uid":%s}' % (self.room_id, uid)

		bytearr = body.encode('utf-8')
		log('danmaku server login: ' + str(body))
		packetlength = len(bytearr)+16
		sendbytes = struct.pack('!IHHII', packetlength, 16, protocolVersion, 7, 1)
		if len(bytearr) != 0:
		    sendbytes = sendbytes + bytearr

		self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((ChatHost, ChatPort))
		self.sock.send(sendbytes)

	def send_heart_beat_msg(self):
		while self.started:
			time.sleep(20)
			sendBytes = struct.pack('!IHHII', 16, 16, protocolVersion, 2, 1)
			self.sock.send(sendBytes)

	def recv_msg_loop(self):
		while self.started:
			try:
				recv_data=self.sock.recv(1024000)
			except:
				self.sock.close()
				self.connect()
			self.handle_data(recv_data)
	
	def stop(self):
		self.started = False
		self.sock.close()
		self.f.write('</i>')
		self.f.close()

	def start(self):
		self.started = True
		self.connect()
		threading.Thread(target=self.send_heart_beat_msg).start()
		threading.Thread(target=self.recv_msg_loop).start()


if __name__=='__main__':
	# test
	b = Client(5096, '123.xml')
	b.connect()
	b.recv_msg_loop()