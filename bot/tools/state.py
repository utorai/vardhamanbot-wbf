import json
from tools.scraper import Scraper
from tinydb import TinyDB, Query

class Student:
    def __init__(self):
        self.db = TinyDB('./db.json')

    def get_data(self, user_id):
        query = Query()
        result = self.db.search(query.user_id == user_id)
        if len(result) > 0:
            return result[0]
        else:
            return False

    def insert_or_update_data(self, data):
        query = Query()
        result = (self.db.search(query.user_id == data["user_id"]))[0]
        if len(result) > 0:
            self.db.update(data, query.user_id == data["user_id"])
        else:
            self.db.insert(data)