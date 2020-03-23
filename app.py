from flask import Flask, render_template, redirect, url_for, request
#!/usr/bin/python
#-*- coding: utf-8 -*-

import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/oauth')
def oauth():
    code = str(request.args.get('code'))
    resToken = getAccessToken("e8f06640b658cef3568974ad6438343a".str(code))
    return 'code=' + str(code) + '<br/>response for token=' + str(resToken)

def getAccessToken(clientId, code): 
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code"
    payload += "&client_id=" + clientId
    payload += "&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Foauth&code=" + code
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    access_token = json.loads(((response.text).encode('utf-8')))
    return access_token 
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)