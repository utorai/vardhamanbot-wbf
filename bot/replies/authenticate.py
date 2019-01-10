from tinydb import TinyDB, Query
from tools.scraper import Scraper
from tools.state import State

def reply(activity, bot, data):
    print(data.get_entities())
    credentials = activity.text.split(" ")
    rollno = credentials[0]
    wak = credentials[1]
    if len(wak) > 5:
        await bot.send_text_activity(activity, "Please check your roll no. and web access key again.")
        await bot.send_text_activity(activity, "Enter roll no. and web access key seperated by a single space.")
        return
    scraper = Scraper()
    scraper.authenticate(rollno,wak)
    if scraper.authenticated:
        state = State()
        studentdata = scraper.get_studentdata()
        studentdata["wak"] = wak
        studentdata["RowKey"] = activity.from_property.id
        print(studentdata.items())
        state.insertOrUpdateStudent(studentdata)
        await bot.send_text_activity(activity, "Authentication Successful!")
    else:
        await bot.send_text_activity(activity, "Please check your roll no. and web access key again.")
        await bot.send_text_activity(activity, "Enter roll no. and web access key seperated by a single space.")