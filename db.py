import sqlite3

class DBClient:
    def __init__(self, dbname:str="data.db") -> None:
        self.connect = sqlite3.connect(dbname)
        self.cursor = self.connect.cursor()

    def get_settings(self, settings):
        response = self.cursor.execute("select name from sqlite_master")
        if response.fetchone() is None: return settings
        # таблицы не существует
        
        self.cursor.execute("select count(id) from settings;")
        response = self.cursor.fetchall()
        if response[0][0] == 0: return settings
        # записей не существует

        self.cursor.execute("select * from settings;")
        response = self.cursor.fetchall()
        print(response)
        for res in response:
            settings[f"{res[0]}"] = res[1]
        return settings
    
    def save_settings(self, settings) -> None:
        prepare_command = "create table if not exists settings (id int primary key, name  count int);"
        self.cursor.execute(prepare_command)
        for _ in settings:
            command = f"insert or replace into settings (id, count) values ({_}, {settings[_]});"
            self.cursor.execute(command)
        self.connect.commit()

if __name__ == '__main__':
    dbclient = DBClient()
    settings = {'0': 0, '1': 0, '2':0}
    dbclient.save_settings(settings)
    print(dbclient.get_settings({}))