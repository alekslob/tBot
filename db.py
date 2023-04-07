import sqlite3
import random as rnd

class DBClient:
    def __init__(self, count:int=1,dbname:str="data.db") -> None:
        self.connect = sqlite3.connect(dbname)
        self.cursor = self.connect.cursor()
        self.clear_settings(count)
        
    def clear_settings(self, count:int=1):
        settings=[['не по ссылке',0, 0]]
        for i in range(1,count+1,1):
            settings.append([f"по ссылке {i}",i, 0])
        return settings
    
    def get_settings(self, count:int=1):
        settings = self.clear_settings(count)
        response = self.cursor.execute("select name from sqlite_master")
        if response.fetchone() is None: return settings
        # таблицы не существует
        
        self.cursor.execute("select count(id) from settings;")
        response = self.cursor.fetchall()
        if response[0][0] == 0: return settings
        # записей не существует

        self.cursor.execute("select * from settings;")
        response = self.cursor.fetchall()
        # print(response)
        settings = []
        for res in response:
            settings.append([res[1],res[2], res[3]])
        return settings
    
    def save_settings(self, settings) -> None:
        prepare_command = "create table if not exists settings (id int primary key, name varchar(225), option int, count int);"
        self.cursor.execute(prepare_command)
        for i in range(len(settings)):
            command = f"insert or replace into settings (id,name, option, count) values ({i},'{settings[i][0]}',{settings[i][1]}, {settings[i][2]});"
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