import telebot
from telebot import types
from db import DBClient
# import logging

token = '5803984180:AAEN7i9qdI1VDceX29Kq8MEGzgt3pPrV4es'
# options = ['1','2','3']
# counts = [0,0,0]
bot = telebot.TeleBot(token)
count_linc = 2
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)

def addLinc(option):
    dbclient = DBClient()
    options = dbclient.get_settings(count_linc)
    try:
        int_option = int(option)
        if int_option>0 and int_option<=count_linc:
            options[int_option][1]+=1
        else: raise ValueError()
    except ValueError:
        options[0][1]+=1
    finally:
        dbclient.save_settings(options)
        return options

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id,'🤝')
    text = "Сюда можно попасть по ссылкам:\n"
    text += "Ссылка 1 https://t.me/phroil_bot?source=1\n"
    text += "Ссылка 1 https://t.me/phroil_bot?source=2\n"
    # print(message.text.split().pop())
    # options = addLinc(message.text.split().pop())
    # print(options)
    # for option in options:
    #     text+=f"Перешли {option[0]}: {option[1]}\n"
    bot.send_message(message.from_user.id, text)

    keyboard = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton(text="Показать статистику")
    keyboard.add(button_1)
    message.answer(text, reply_markup=keyboard)
didit=False
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id,'Ок👍')
    if didit: bot.send_message(message.from_user.id, 'Было')


@bot.message_handler(commands=['source'])
def source(message):
    didit=True
bot.polling(none_stop=True, interval=0) 