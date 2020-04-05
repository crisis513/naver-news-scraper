#!/usr/bin/python
#-*- coding: utf-8 -*-

import json

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

def send_kakaotalk_message(access_token, title, body, link):
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