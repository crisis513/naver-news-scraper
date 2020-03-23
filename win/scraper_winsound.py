#!usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import bs4
import winsound
import re

base_url = 'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100'
search_list = ['백신', '치료제', 'vaccine', 'Vaccine', 'remedy', 'Remedy', '총선']

def playAudio():
    winsound.PlaySound('sound.wav', winsound.SND_FILENAME)

def scrap():
    resp = requests.get(base_url)

    resp.raise_for_status()
    resp.encoding='euc-kr'
    soup = bs4.BeautifulSoup(resp.text, "html.parser")

    all = soup.find("ul", {"class":"type06_headline"})
    all2 = all.find_all("li")

    for item in all2:
        try:
            #img = item.find("dt", {"class":"photo"})
            #img2 = img.find("img")["src"]
            title = item.find("dt", "").find("a").text.strip("\n\t\r ") # 뉴스 제목
            link = item.find("dt", "").find("a").get("href") # 뉴스 링크
            body = item.find("span", {"class":"lede"}).text # 뉴스 내용 요약
            #writer = item.find("span", {"class":"writing"}).text # 뉴스 제공자
            time = item.find("span", {"class":"date"}).text # 뉴스 업로드된 시간

            for search in search_list:
                if search in title or search in body:
                    if re.search('\S+초전', time) or re.search('1분전', time):
                        print("Title: " + title)
                        print("Body: " + body)
                        print("Link: " + link)
                        print("Time: " + time)
                        print("\n")

        except:
            print("No image")

scrap()
playAudio()
