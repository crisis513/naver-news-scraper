#!/usr/bin/python
#-*- coding: utf-8 -*-

import requests
import sys
import urllib
import json
import bs4
import re
from time import sleep
from config import config
from flask import Flask, render_template, redirect, url_for, request

reload(sys)
sys.setdefaultencoding('utf-8')
        
def send_text(access_token, title, body, link) :
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
                "title": "웹으로 보기",
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
                result = send_text(f_a.read(), title, body, link)
                print(result)
                f_a.close()

                print("Title: " + title)
                print("Body: " + body)
                print("Link: " + link)
                print("Time: " + time)
                print("\n")

                return "Success scrap()!"

app = Flask(__name__)

if __name__ == '__main__':
    app.config.from_object(config['default'])
    config['default'].init_app(app)

    while True:
        sleep(10)
        result = scrap()
        print(result)

# # url = 'https://kauth.kakao.com/oauth/authorize?client_id=e8f06640b658cef3568974ad6438343a&redirect_uri=http://localhost:5000/oauth&response_type=code&scope=talk_message'
# url = 'https://kauth.kakao.com/oauth/token'
# headers = {
#     'Content-Type': "application/x-www-form-urlencoded",
#     'Cache-Control': "no-cache",
# }
# data = dict({
#     'grant_type': 'refresh_token', 
#     'client_id': 'e8f06640b658cef3568974ad6438343a', 
#     'refresh_token': 's-duBiRHMJljhCiIev6OYJ7K5MbcbISc_tedfwo9c5sAAAFxFiQOJw',
# })

# resp = requests.post(url, headers=headers, data=data)

# resp_json = json.loads(((resp.text).encode('utf-8')))
# print(resp_json['access_token'])
# # print("response status:\n%d" % resp.status_code)
# # print("response headers:\n%s" % resp.headers)
# # print("response body:\n%s" % resp.json)