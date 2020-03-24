#!/usr/bin/python
#-*- coding: utf-8 -*-

from config import config
from flask import Flask, render_template, redirect, url_for, request
from logging.handlers import RotatingFileHandler
from time import sleep
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
    resToken = getAccessToken(app.config['RESTAPI_KEY'], str(code))
    sendText(resToken['access_token'])
    return 'code = ' + str(code) + '<br/>response for token=' + str(resToken)

def getAccessToken(client_id, code): 
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code"
    payload += "&client_id=" + client_id
    payload += "&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Foauth&code=" + code
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    access_token = json.loads(((response.text).encode('utf-8')))
    return access_token 

def def scraper_thread(name, sec):
    while True:
        sleep(sec)
        scrap()(accessToken) :
    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
    payloadDict = dict({
        "object_type" : "text",
        "text" :u"이것은 테스트".encode("utf-8"),
        "link" : {
            "web_url" : "http://crisis513.github.io",
            "mobile_web_url" : "http://crisis513.github.io"
            },
        "button_title" : u"방문".encode("utf-8"),
    })
    
    payload = 'template_object=' + str(json.dumps(payloadDict))
    headers = {
        'Content-Type' : "application/x-www-form-urlencoded",
        'Cache-Control' : "no-cache",
        'Authorization' : "Bearer " + accessToken,
    }

    reponse = requests.request("POST",url,data=payload, headers=headers)
    access_token = json.loads(((reponse.text).encode('utf-8')))
    return access_token

def scrap():
    resp = requests.get(app.config['BASE_URL'])
    resp.raise_for_status()
    soup = bs4.BeautifulSoup(resp.text, "html.parser")

    all_ul = soup.find("ul", {"class":"type06_headline"})
    all = all_ul.find_all("li")

    for item in all:
        try:
            #img = item.find("dt", {"class":"photo"})
            #img2 = img.find("img")["src"]
            #writer = item.find("span", {"class":"writing"}).text # 뉴스 작성자
            title = item.find("dt", "").find("a").text.strip("\n\t\r ") # 뉴스 제목
            link = item.find("dt", "").find("a").get("href") # 뉴스 링크
            body = item.find("span", {"class":"lede"}).text # 뉴스 내용 요약
            time = item.find("span", {"class":"date"}).text # 뉴스 업로드된 시간
            
            for search in app.config['SEARCH_LIST']:
                if search in title or search in body:
                    # if re.search('\S+초전', time) or re.search('\S+분전', time):
                    app.logger.warning("Title: " + title)
                    print("Title: " + title)
                    print("Body: " + body)
                    print("Link: " + link)
                    print("Time: " + time)
                    print("\n")

        except Exception as e:
            logging.exception(e, exc_info=True)

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

    t = threading.Thread(target=scraper_thread, args=("Thread-1", 60))
    t.start()

    app = create_app('default')
    app.run(port = 5000, debug = True)

    try:
        while True:
            sleep(2)
    except KeyboardInterrupt:
        t.join()
