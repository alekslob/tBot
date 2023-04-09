import json
import telebot
from telebot import types
from db import DBClient

def load_json(name):
    file = open("data.json")
    data = json.load(file)
    return data[name]

def add_url(urlid):
    dbclient = DBClient()
    urlsbd = dbclient.get_settings(urls)
    for i in range(1,len(urlsbd)):
        if urlid == urlsbd[i]["urlid"]: 
            urlsbd[i]["count"]+=1
            break
    if i == len(urlsbd)-1:
        urlsbd[0]["count"]+=1
    for url in urlsbd:
        dbclient.save_settings(url)

def get_urls():
    dbclient = DBClient()
    return dbclient.get_settings(urls)

textBtnStatistics = "Показать статистику"
token = load_json('API_TOKEN')
urls = load_json('URLS')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    parametres = message.text.split()
    if len(parametres) > 1: urlid = parametres[1]
    else: urlid = ""
    add_url(urlid)
    
    bot.send_message(message.from_user.id,'🤝')
    text = "Сюда можно попасть по ссылкам:\n"
    for url in urls:
        text += f"{url['name']} https://t.me/phroil_bot?start={url['urlid']} \n"
    
    keyboard =  types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text=textBtnStatistics)
    keyboard.add(btn1)
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)
    

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id,'Ок👍')
    if message.text == textBtnStatistics: get_statistics(message)

@bot.message_handler(commands=['statistics'])
def get_statistics(message):
    urlsbd = get_urls()
    text = "Статистика открытия этого бота\n"
    text += "============================\n"
    for url in urlsbd:
        text += f"{url['name']}: {url['count']}\n"
    bot.send_message(message.from_user.id, text)


bot.polling(none_stop=True, interval=0) 

