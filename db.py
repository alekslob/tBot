import sqlite3

class DBClient:
    def __init__(self, dbname:str="data.db", urls:list=[]) -> None:
        self.urls = urls
        self.connect = sqlite3.connect(dbname)
        self.cursor = self.connect.cursor()
        self.__check_db()
        
    def __check_db(self):
        response = self.cursor.execute("select name from sqlite_master where name = 'urls'")
        if response.fetchone() is None: self.__create_db
        # таблицы не существует
        
        self.cursor.execute("select count(id) from urls;")
        response = self.cursor.fetchall()
        if response[0][0] == 0: self.__create_urls()
        # записей не существует

    def __create_db(self):
        prepare_command = "create table if not exists urls (id INTEGER primary key autoincrement NOT NULL UNIQUE, name varchar(225), urlid varchar(225) UNIQUE, count int);"
        self.cursor.execute(prepare_command)

    def __create_urls(self):
        url={"name": "Не по ссылке", "urlid": "-", "count": 0}
        self.save_urls(url)
        for url in self.urls:
            name = url["name"]
            urlid = url["urlid"]
            self.save_urls({"name": name, "urlid": urlid, "count": 0})
                           
    def get_url(self, urlid:str): 
        self.cursor.execute(f"select * from urls where urlid = '{urlid}';")
        response = self.cursor.fetchall()
        if response != []:
            res = response[0]
            name = res[1]
            urlid = res[2]
            count = res[3]
            return {"name": name, "urlid": urlid, "count": count}
        else: return {"name": None, "urlid": urlid, "count": 0}
    
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
    def get_urlsid(self):
        self.cursor.execute("select urlid from urls;")
        response = self.cursor.fetchall()
        urlsid = []
        for i in range(1,len(response)):
            urlsid.append(response[i][0])
        return urlsid

    def save_url(self, url) -> None:
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
