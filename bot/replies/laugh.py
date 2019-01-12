import random

def reply(activity, bot, data):
    responses = [
        "😂😂 Glad you liked it",
        "😂😂",
        "I love to put a smile on people's faces 😄",
        "🤣🤣😎",
        "I know right!"
    ]
    response = random.choice(responses)
    bot.send_text_activity(activity, response)