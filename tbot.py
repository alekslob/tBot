import asyncio
from db import DBClient
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, Updater
from telegram.ext import CommandHandler, MessageHandler, filters

class Tbot:
    def __init__(self, token:str, db:DBClient) -> None:
        self.textBtnStatistics = "Показать статистику"
        self.token = token
        self.db = db

    def work(self):
        application = ApplicationBuilder().token(self.token).build()
        application.add_handler(CommandHandler('start', self.__start))
        application.add_handler(CommandHandler('statistics', self.__get_statisics))
        application.add_handler(MessageHandler(filters.TEXT, self.__get_text))
        application.run_polling()
    
    def __add_url(self, urlid:str):
        url = self.db.get_url(urlid)
        if url['name'] is None:
            url['name'] = urlid
        url['count']+=1
        self.db.save_url(url)
    
    def __get_urlsid(self):
        return self.db.get_urlsid()
    def __get_urls(self):
        return self.db.get_urls()
        

    async def __start(self,update, context):
        await update.message.reply_text('🤝')
        parametrs = update.message.text.split()
        if len(parametrs) > 1: urlid = parametrs[1]
        else: urlid = "-"
        self.__add_url(urlid)
        
        text = "Сюда можно попасть по ссылкам:\n"
        urlsid = self.__get_urlsid()
        for urlid in urlsid:
            text += f"{update.get_bot().link}?start={urlid} \n"
        await update.message.reply_text(text)
        
    async def __get_text(self, update, context):
        await update.message.reply_text('Ок👍')
        if update.message.text == self.textBtnStatistics:
            await self.__get_statisics(update, context)
        
    async def __get_statisics(self, update, context):
        urlsbd = self.__get_urls()
        text = "Статистика открытия этого диалога\n"
        text += "=============================\n"
        for url in urlsbd:
            text += f"{url['name']}: {url['count']}\n"
        await update.message.reply_text(text)
