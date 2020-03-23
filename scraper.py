#!/usr/bin/python
#-*- coding: utf-8 -*-

import requests
import bs4
import logging
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

base_url = 'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100'
search_list = ['백신', '치료제', 'vaccine', 'Vaccine', 'remedy', 'Remedy', '코로나']

def scrap():
    resp = requests.get(base_url)
    resp.raise_for_status()
    soup = bs4.BeautifulSoup(resp.text, "html.parser")

    all_ul = soup.find("ul", {"class":"type06_headline"})
    all = all_ul.find_all("li")

    for item in all:
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
                    print("Title: " + title)
                    print("Body: " + body)
                    print("Link: " + link)
                    print("Time: " + time)
                    print("\n")

        except Exception as e:
            logging.exception(e, exc_info=True);


scrap()
