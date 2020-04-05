#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import logging
import requests
import urllib
import bs4
import re
import sys
from time import sleep
from config import config
from flask import Flask, render_template, redirect, url_for, request
from logging.handlers import RotatingFileHandler
from apscheduler.schedulers.background import BackgroundScheduler
from telegram_bot import send_telegram_message
from kakaotalk_bot import send_kakaotalk_message, get_token
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig()
LOG_FILENAME = 'server.log'

app = Flask(__name__)

@app.route('/')
def index():
    if app.config['USE_BOT'] == 'telegram':
        return "use telegram bot.."
    elif app.config['USE_BOT'] == 'kakaotalk':
        return render_template('index.html')
    else:
        return "error!"

@app.route('/oauth')
def oauth():
    code = str(request.args.get('code'))
    res_token = get_token(app.config['RESTAPI_KEY'], str(code))
    
    access_file = open('filedb/access_token', 'wt')
    access_file.write(res_token['access_token'])
    access_file.close()

    refresh_file = open('filedb/refresh_token', 'wt')
    refresh_file.write(res_token['refresh_token'])
    refresh_file.close()

    return "success! \n\n" + str(res_token)

@app.route('/goto')
def goto():
    url = str(request.args.get('goto'))
    return redirect(url, code=200)

def start_scrap():
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
                if app.config['USE_BOT'] == 'telegram':
                    send_telegram_message(str(title), str(body), str(link))
                elif app.config['USE_BOT'] == 'kakaotalk':
                    f_a = open('filedb/access_token', 'rt')
                    send_kakaotalk_message(f_a.read(), str(title), str(body), "link")
                    f_a.close()
                else:
                    print("error!")

                app.logger.warning("Send to " + app.config['USE_BOT'] + "-> Title: " + title + ", Body: " + body  + ", Link: " + link + ", Time: " + time)

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

    sched = BackgroundScheduler()
    sched.start()
    sched.add_job(start_scrap, 'interval', seconds=30, id="nn-scraper")

    app = create_app('default')
    app.run(port=5000, debug=True)
