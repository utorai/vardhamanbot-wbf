import random

def reply(activity, bot, data):
    responses = [
        "Hi", 
        "Hi there!", 
        "Hello", 
        "Hey there!"
    ]
    response = random.choice(responses)
    bot.send_rich_activity(activity, "https://media.giphy.com/media/T4gMNMn9qF5wQ/giphy.gif")