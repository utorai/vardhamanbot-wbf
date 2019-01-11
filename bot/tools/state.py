import azure
import json
from tools.scraper import Scraper
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from azure.storage.common.retry import (
    LinearRetry,
    ExponentialRetry
)


class State:
    def __init__(self):
        with open('./vardhamanbot/bot/config/app.json') as app_config_file:
            app_config = json.load(app_config_file)
        self.tableservice = TableService(app_config["ats_name"], app_config["ats_key"])
        self.tableservice.retry = ExponentialRetry(initial_backoff=30, increment_base=2, max_attempts=20).retry

    def getStudent(self, userId):
        try:
            #Try to get the user data based on his year
            return self.tableservice.get_entity('vbotusers', "VMEG", userId)
        except azure.common.AzureMissingResourceHttpError:
            return {}

    def insertOrUpdateStudent(self, studentdata):
        #Partition the Data Based on Year
        studentdata["PartitionKey"] = "VMEG"
        self.tableservice.insert_or_replace_entity("vbotusers", studentdata)

