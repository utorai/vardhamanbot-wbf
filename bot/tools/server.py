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
    
    def send_text_activity(self, activity, text):
        reply = self.create_reply_activity(activity["sender"]["id"], text)
        requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + self.access_token, data=reply)
    
    def handle_message_activity(self, activity):
        self.current_user_id = activity["sender"]["id"]
        self.message_activity_handler(activity)
    
    def start(self, action):
        self.initial_activity_handler = action
    
    def replies(self, action):
        self.message_activity_handler = action

async def handle_all_activity(request):
    data = request.json
    bot.handle_message_activity(data)
    return request.Response(code=200)
    
def start(current_bot):
    server = Application()
    server.router.add_route('/', handle_all_activity)
    server.run(debug=True)