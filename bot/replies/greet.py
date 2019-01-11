import random
from tools.facebook import getName
def reply(activity, bot, data):
    name = getName(activity["sender"]["id"])
    responses = [
        "Hi", 
        "Hi there!", 
        "Hello", 
        "Hey there!"
    ]
    response = random.choice(responses)
    bot.send_text_activity(activity, response + " " + name)