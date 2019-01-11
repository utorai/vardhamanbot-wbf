import requests
from japronto import Application

bot = None


class Bot:
    def __init__(self, access_token):
        self.access_token = access_token
        self.initial_activity_handler = None
        self.message_activity_handler = None

    def create_reply_activity(self, recipient_id, text):
        message_dict = {
            "messaging_type": "RESPONSE",
            "recipient": {
                "id": str(recipient_id)
            },
            "message": {
                "text": text
            }
        }
        return message_dict

    def create_quick_reply_activity(self, recipient_id, message, text):
        message_dict = {
            "recipient": {
                "id": str(recipient_id)
            },
            "message": {
                "text": message,
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": text,
                        "payload": text
                    }
                ]
            }
        }
        return message_dict

    def create_rich_activity(self, recipient_id, media_url):
        message_dict = {
            "messaging_type": "RESPONSE",
            "recipient": {
                "id": str(recipient_id)
            },
            "message": {
                "attachment": {
                    "type": "image",
                    "payload": {
                        "url": media_url,
                        "is_reusable": True
                    }
                }
            }
        }
        return message_dict

    def send_text_activity(self, activity, text):
        reply = self.create_reply_activity(activity["sender"]["id"], text)
        request = requests.post(
            "https://graph.facebook.com/v2.6/me/messages?access_token=" + self.access_token, json=reply)
        print(request.text)
        if 'error' in request.json():
            raise Exception

    def send_quick_reply_activity(self, activity, message, text):
        reply = self.create_quick_reply_activity(
            activity["sender"]["id"], message, text)
        request = requests.post(
            "https://graph.facebook.com/v2.6/me/messages?access_token=" + self.access_token, json=reply)
        print(request.text)
        if 'error' in request.json():
            raise Exception

    def send_rich_activity(self, activity, media_url):
        reply = self.create_rich_activity(activity["sender"]["id"], media_url)
        request = requests.post(
            "https://graph.facebook.com/v2.6/me/messages?access_token=" + self.access_token, json=reply)
        print(request.text)
        if 'error' in request.json():
            raise Exception

    def send_typing_activity(self, activity):
        reply = {
            "recipient": {
                "id": activity["sender"]["id"]
            },
            "sender_action": "typing_on"
        }
        request = requests.post(
            "https://graph.facebook.com/v2.6/me/messages?access_token=" + self.access_token, json=reply)
        print(request.text)
        if 'error' in request.json():
            raise Exception
        

    def handle_message_activity(self, activity):
        print(activity)
        self.current_user_id = activity["sender"]["id"]
        self.message_activity_handler(activity)

    def start(self, action):
        self.initial_activity_handler = action

    def replies(self, action):
        self.message_activity_handler = action


async def handle_all_activity(request):
    global bot
    if request.method == 'GET':
        if request.query['hub.mode'] == 'subscribe' and request.query['hub.verify_token'] == 'hello_world':
            return request.Response(request.query['hub.challenge'], code=200)
        else:
            return request.Response(code=404)
    elif request.method == 'POST':
        data = (request.json)["entry"][0]["messaging"][0]
        if 'postback' in data:
            data["message"] = {}
            data["message"]["text"] = data["postback"]["payload"]
        bot.handle_message_activity(data)
        return request.Response(code=200)
    else:
        return request.Response(code=404)


def start(current_bot):
    global bot
    bot = current_bot
    server = Application()
    server.router.add_route('/', handle_all_activity)
    server.run(debug=True)
