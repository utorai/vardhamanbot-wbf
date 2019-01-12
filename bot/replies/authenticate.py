from tools.scraper import Scraper
from tools.state import Student

def reply(activity, bot, data):
    print(data.get_entities())
    credentials = activity["message"]["text"].split(" ")
    rollno = credentials[0]
    wak = credentials[1]
    if len(wak) > 5:
        bot.send_text_activity(activity, "Please check your roll no. and web access key again.")
        bot.send_text_activity(activity, "Enter roll no. and web access key seperated by a single space.")
        return
    scraper = Scraper()
    scraper.authenticate(rollno,wak)
    if scraper.authenticated:
        student = Student()
        student_data = {}
        student_data["user_id"] = activity["sender"]["id"]
        student_data["wak"] = wak
        student_data["student_id"] = rollno
        student.insert_or_update_data(student_data)
        bot.send_text_activity(activity, "Authentication Successful!")
    else:
        bot.send_text_activity(activity, "Please check your roll no. and web access key again.")
        bot.send_text_activity(activity, "Enter roll no. and web access key seperated by a single space.")