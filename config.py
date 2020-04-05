#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Default Configuration
    HOST_SERVER = 'http://localhost:5000'
    BASE_URL = 'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100'
    SEARCH_LIST = ['백신', '치료제', 'vaccine', 'Vaccine', 'remedy', 'Remedy', '임상', '코로나']

    # Bot Configuration
    USE_BOT = 'telegram' # kakaotalk / telegram
    RESTAPI_KEY = os.environ.get('RESTAPI_KEY') or 'e8f06640b658cef3568974ad6438343a'
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN') or 'TOKEN'

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