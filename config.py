#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    HOST_SERVER = 'http://localhost:5000'
    RESTAPI_KEY = os.environ.get('RESTAPI_KEY') or 'e8f06640b658cef3568974ad6438343a'
    BASE_URL = 'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100'
    SEARCH_LIST = ['백신', '치료제', 'vaccine', 'Vaccine', 'remedy', 'Remedy', '임상']

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}