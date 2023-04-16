import json
from tbot import Tbot
from db import DBClient

def load_json(name):
    file = open("data.json")
    data = json.load(file)
    return data[name]

if __name__ == "__main__":
    token = load_json('API_TOKEN')
    urls = load_json('URLS')
    db = DBClient(urls=urls)
    tbot = Tbot(token, db)
    tbot.work()
