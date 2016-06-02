#coding:utf-8
from flask import Flask, render_template, request, redirect, url_for
import time 
import os
import requests
import shutil
import sys
import types

TEXT_ENCODING = "utf-8"
#Number of picture
NumberOfPic = 1
app = Flask(__name__)
class GetPic:

	def __init__(self,username,password):
		#set Microsoft Azure Marketplace Username, Password
		self.MS_USER = username
		self.MS_ACCTKEY = password

	def bing_get_pic(self,query):
		urlList = []
		#set URL
		bing_url = 'https://api.datamarket.azure.com/Bing/Search/Image'
		#set parameter
		payload = { '$format': 'json','Query': "'"+query+"'",}

		#GET request
		r = requests.get(bing_url, params=payload, auth=(self.MS_USER,self.MS_ACCTKEY))

		#count the number of pictures
		count = 1
	
		#make directory to save pictures
		dirname = "./%s"%query
	 
		for item in r.json()['d']['results']:
			time.sleep(3)
			image_url = item['MediaUrl']

			root,ext = os.path.splitext(image_url)

			if ext.lower() == '.jpg':    

				urlList.append(image_url)
				if urlList[0].find('wikipedia') == -1:
					count += 1
					if count >= NumberOfPic:
						break		
				else:
					urlList.pop()
		return urlList

	def bing_search(self, word):
		l = []
		url = ""
		l = self.bing_get_pic(word)
		for i in range(len(l)):
			url += l[i]
			if i != len(l)-1:
				url += ","
		return url

@app.route('/entry/<string:txt>')
def index(txt):
	url = ""
        txt = txt.encode(TEXT_ENCODING)
	url = gp.bing_search(txt)
	return url	

if __name__ == '__main__':
	username = input(' Microsoft_Azure UserName > ')
	password = input(' Microsoft_Azure PassWord > ')
	
	gp = GetPic(username,password)
	app.run(host='0.0.0.0')
