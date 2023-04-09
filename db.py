import sqlite3
import random as rnd
import numpy as np

class DBClient:
    def __init__(self,dbname:str="data.db") -> None:
        self.connect = sqlite3.connect(dbname)
        self.cursor = self.connect.cursor()
        
    def create_settings(self, urls):
        settings={"name": "Не по ссылке", "urlid": "-", "count": 0}
        self.save_settings(settings)
        for url in urls:
            name = url["name"]
            urlid = url["urlid"]
            # settings.append({"name": name, "urlid": urlid, "count": 0})
            self.save_settings({"name": name, "urlid": urlid, "count": 0})

    def check_settings(self, response, urls):
        names = np.array(response).transpose()[1]
        for url in urls:
            if not (url["name"] in names):
                name = url["name"]
                urlid = url["urlid"]
                self.save_settings({"name": name, "urlid": urlid, "count": 0})

    def get_settings(self, urls):
        response = self.cursor.execute("select name from sqlite_master")
        if response.fetchone() is None: self.create_settings(urls) # settings
        # таблицы не существует
        
        self.cursor.execute("select count(id) from settings;")
        response = self.cursor.fetchall()
        if response[0][0] == 0: self.create_settings(urls) # settings
        # записей не существует
        
        self.cursor.execute("select * from settings;")
        response = self.cursor.fetchall()
        self.check_settings(response, urls)
        # обновляется статистика если есть новые url

        self.cursor.execute("select * from settings;")
        response = self.cursor.fetchall()
        # print(response)
        settings = []
        for res in response:
            name = res[1]
            urlid = res[2]
            count = res[3]
            settings.append({"name": name, "urlid": urlid, "count": count})

        return settings
    
    def save_settings(self, settings) -> None:
        prepare_command = "create table if not exists settings (id INTEGER primary key autoincrement NOT NULL UNIQUE, name varchar(225), urlid varchar(225) UNIQUE, count int);"
        self.cursor.execute(prepare_command)
        command = ""
        # for i in range(len(settings)):
        name = settings["name"]
        urlid = settings["urlid"]
        count = settings["count"]
        command += f"insert or replace into settings (name, urlid, count) values ('{name}', '{urlid}', {count});"
        self.cursor.execute(command)
        self.connect.commit()

# if __name__ == '__main__':
#     dbclient = DBClient()
#     set = dbclient.clear_settings(2)
    # print(rnd.randint(1e5,1e6))
    # if int(op)>0 and int(op)<len(set): print(True)
    # else: print(False)
    # settings = {'0': 0, '1': 0, '2':0}
    # dbclient.save_settings(set)
    # print(dbclient.get_settings())