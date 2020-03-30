#!/usr/bin/python
#-*- coding: utf-8 -*-

from config import config
from flask import Flask, render_template, redirect, url_for, request
from logging.handlers import RotatingFileHandler
from time import sleep
import os
import logging
import requests
import threading
import urllib
import json
import bs4
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

LOG_FILENAME = 'server.log'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/oauth')
def oauth():
    code = str(request.args.get('code'))
    res_token = get_token(app.config['RESTAPI_KEY'], str(code))
    
    f_a = open('filedb/access_token', 'wt')
    f_a.write(res_token['access_token'])
    f_a.close()

    f_r = open('filedb/refresh_token', 'wt')
    f_r.write(res_token['refresh_token'])
    f_r.close()

    return "success! \n\n" + str(res_token)

@app.route('/goto')
def goto():
    url = str(request.args.get('goto'))
    return redirect(url, code=200)
    
def get_token(client_id, code): 
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code"
    payload += "&client_id=" + client_id
    payload += "&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Foauth&code=" + code
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    response_json = json.loads(((response.text).encode('utf-8')))
    return response_json 

def send_text(access_token, title, body, link):
    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
    payload_dict = dict({
        "object_type": "feed",
        "content":{
            "title": title,
            "description": body,
            "image_url": "http://k.kakaocdn.net/14/dn/btqCSg7rP0f/mTkd9xrRtbOkjZssTxz7Ek/o.jpg",
            "link": {
                "mobile_web_url": link,
                "web_url": link
            }
        },
        "buttons":[
            {
                "title": "Redirect Page",
                "link": {
                    "mobile_web_url": link,
                    "web_url": link
                }
            }
        ]
    })
    
    payload = 'template_object=' + str(json.dumps(payload_dict))
    headers = {
        'Content-Type' : "application/x-www-form-urlencoded",
        'Cache-Control' : "no-cache",
        'Authorization' : "Bearer " + access_token,
    }

    reponse = requests.request("POST", url, data=payload, headers=headers)
    response_json = json.loads(((reponse.text).encode('utf-8')))
    return response_json

def scrap():
    resp = requests.get(app.config['BASE_URL'])
    resp.raise_for_status()
    soup = bs4.BeautifulSoup(resp.text, "html.parser")

    all_ul = soup.find("ul", {"class":"type06_headline"})
    all = all_ul.find_all("li")

    for item in all:
        writer = item.find("span", {"class":"writing"}).text # 뉴스 작성자
        title = item.find("dt", "").find("a").text.strip("\n\t\r ") # 뉴스 제목
        link = app.config['HOST_SERVER']
        link += '/goto?goto=' + item.find("dt", "").find("a").get("href") # 뉴스 링크
        body = item.find("span", {"class":"lede"}).text # 뉴스 내용 요약
        time = item.find("span", {"class":"date"}).text # 뉴스 업로드된 시간
        # img = item.find("dt", {"class":"photo"})
        # img_src = img.find("img").attrs["src"]
        # if not img_src:
        #     img_src = 'http://k.kakaocdn.net/14/dn/btqCSg7rP0f/mTkd9xrRtbOkjZssTxz7Ek/o.jpg'
        
        for search in app.config['SEARCH_LIST']:
            if search in title or search in body:
                # if re.search('\S+초전', time) or re.search('1분전', time):
                app.logger.warning("Title: " + title)
                
                f_a = open('filedb/access_token', 'rt')
                # if not f_a.read().strip():
                #     return "Can't read access_token!"
                result = send_text(f_a.read(), str(title), str(body), "link")
                print(result)
                f_a.close()

                print("Title: " + title)
                print("Body: " + body)
                print("Link: " + link)
                print("Time: " + time)
                print("\n")


def scraper_thread(name, sec):
    while True:
        sleep(sec)
        scrap()
        

def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    return app


if __name__ == '__main__':
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler(LOG_FILENAME, maxBytes=10000000, backupCount=5)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    t = threading.Thread(target=scraper_thread, args=("NN-SCRAPER Thread", 20))
    t.start()

    app = create_app('default')
    app.run(port=5000, debug=True)
