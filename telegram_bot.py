#!/usr/bin/python
#-*- coding: utf-8 -*-

import telegram
from telegram.error import NetworkError, Unauthorized

def send_telegram_message(title, body, link):
    bot = telegram.Bot('TOKEN')

    chat_id = bot.getUpdates()[-1].message.chat.id
    #print(chat_id)

    message = "[Title]\n" + title + "\n\n[Body]\n" + body + "\n\n[Link]\n" + link

    bot.send_message(chat_id=chat_id, text=message)