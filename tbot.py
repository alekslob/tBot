import json
import telebot
from telebot import types
from db import DBClient

def load_json(name):
    file = open("data.json")
    data = json.load(file)
    return data[name]

def add_url(urlid):
    dbclient = DBClient(load_json('URLS'))
    url = dbclient.get_url(urlid)
    if url is None:
        url = dbclient.get_url("-")
    url['count']+=1
    dbclient.save_urls(url)

def get_urls():
    dbclient = DBClient(load_json('URLS'))
    return dbclient.get_urls()




textBtnStatistics = "Показать статистику"
token = load_json('API_TOKEN')
namebot = load_json('NAME_BOT')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    parametres = message.text.split()
    if len(parametres) > 1: urlid = parametres[1]
    else: urlid = " "
    add_url(urlid)

    urls = load_json('URLS')
    bot.send_message(message.from_user.id,'🤝')
    text = "Сюда можно попасть по ссылкам:\n"
    for url in urls:
        text += f"{url['name']} https://t.me/{namebot}?start={url['urlid']} \n"
    
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
    text = "Статистика открытия этого диалога\n"
    text += "=============================\n"
    for url in urlsbd:
        text += f"{url['name']}: {url['count']}\n"
    bot.send_message(message.from_user.id, text)


bot.polling(none_stop=True, interval=0) 

