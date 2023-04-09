import sqlite3
import random as rnd
import numpy as np

class DBClient:
    def __init__(self,urls,dbname:str="data.db") -> None:
        self.connect = sqlite3.connect(dbname)
        self.cursor = self.connect.cursor()
        self.check_urls(urls)
        
    def create_urls(self, urls):
        url={"name": "Не по ссылке", "urlid": "-", "count": 0}
        self.save_urls(url)
        for url in urls:
            name = url["name"]
            urlid = url["urlid"]
            self.save_urls({"name": name, "urlid": urlid, "count": 0})

    def check_urls(self, urls):
        response = self.cursor.execute("select name from sqlite_master where name = 'urls'")
        if response.fetchone() is None: self.create_urls(urls)
        # таблицы не существует
        
        self.cursor.execute("select count(id) from urls;")
        response = self.cursor.fetchall()
        if response[0][0] == 0: self.create_urls(urls)
        # записей не существует

        self.cursor.execute("select urlid from urls;")
        response = self.cursor.fetchall()
        urlsid = np.array(response).transpose()[0]
        for url in urls:
            if not (url["urlid"] in urlsid):
                name = url["name"]
                urlid = url["urlid"]
                self.save_urls({"name": name, "urlid": urlid, "count": 0})
    
    def get_url(self, urlid):
        self.cursor.execute(f"select * from urls where urlid = '{urlid}';")
        response = self.cursor.fetchall()
        if response != []:
            res = response[0]
            name = res[1]
            urlid = res[2]
            count = res[3]
            return {"name": name, "urlid": urlid, "count": count}
        else: return None

    def get_urls(self):
        self.cursor.execute("select * from urls;")
        response = self.cursor.fetchall()
        urls = []
        for res in response:
            name = res[1]
            urlid = res[2]
            count = res[3]
            urls.append({"name": name, "urlid": urlid, "count": count})
        return urls
    
    def save_urls(self, url) -> None:
        prepare_command = "create table if not exists urls (id INTEGER primary key autoincrement NOT NULL UNIQUE, name varchar(225), urlid varchar(225) UNIQUE, count int);"
        self.cursor.execute(prepare_command)
        name = url["name"]
        urlid = url["urlid"]
        count = url["count"]
        self.cursor.execute(f"select id from urls where urlid = '{urlid}';")
        response = self.cursor.fetchall()
        if response == []:
            command = f"insert or replace into urls (name, urlid, count) values ('{name}', '{urlid}', {count});"
        else:
            id = response[0][0]
            command = f"insert or replace into urls (id,name, urlid, count) values ({id},'{name}', '{urlid}', {count});"
        self.cursor.execute(command)
        self.connect.commit()
