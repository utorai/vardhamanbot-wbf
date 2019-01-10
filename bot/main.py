import tools.server
import tools.nlu
import json
import replies

try:
    with open('./vardhamanbot/bot/config/app.json') as app_config_file:
        app_config = json.load(app_config_file)
except FileNotFoundError:
    app_config = {}
    app_config["access_token"] = ""

bot = tools.server.Bot(access_token = app_config["access_token"])
engine = tools.nlu.Engine()

@bot.start
def start(activity):
    replies.start.reply(activity, bot, {})

@bot.replies
def reply(activity):
    bot.send_typing_activity(activity)
    data = engine.parse(activity["message"]["text"])
    intent = data.get_intent()
    entities = data.get_entities()
    print(intent)
    print(entities)
    try:
        intent_handler = getattr(replies, intent)
        intent_handler.reply(activity, bot, data)
    except Exception:
        replies.default.reply(activity, bot, data)

tools.server.start(bot)