import requests
import json

def getName(psid):
    with open('./vardhamanbot/bot/config/app.json') as app_config_file:
        app_config = json.load(app_config_file)
    accesstoken = app_config["access_token"]
    url =  str.format("https://graph.facebook.com/{0}?fields=first_name,last_name&access_token={1}",psid,accesstoken)
    response = requests.Session().get(url)
    result = json.loads(response.text)
    return result["first_name"]


