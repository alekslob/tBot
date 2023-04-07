import telebot
from telebot import types
from db import DBClient
# import logging

token = '5803984180:AAEN7i9qdI1VDceX29Kq8MEGzgt3pPrV4es'
# options = ['1','2','3']
# counts = [0,0,0]
bot = telebot.TeleBot(token)
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)

def addLinc(option):
    dbclient = DBClient()
    options = dbclient.get_settings({})
    if option in options:
        options[option]+=1
    else: options['0']+=1
    dbclient.save_settings(options)
    return options

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id,'🤝')

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Добавить к 1', url='https://t.me/phroil_bot?start=1')
    btn2 = types.InlineKeyboardButton(text='Добавить к 2', url='https://t.me/phroil_bot?start=2')
    markup.add(btn1)
    markup.add(btn2)
    text = ""
    # print(message.text.split().pop())
    options = addLinc(message.text.split().pop())
    for option in options:
        text+=f"Перешли по ссылке {option}: {options[option]}\n"
    bot.send_message(message.from_user.id, text, reply_markup = markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id,'Ок👍')

bot.polling(none_stop=True, interval=0) 