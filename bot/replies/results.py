import random
from tools.scraper import Scraper
from tools.state import State

def convert(roman):
    if roman == "VI":
        return '5'
    elif roman == 'IV':
        return '3'
    elif roman == 'VIII':
        return '7'

def reply(activity, bot, data):
    state = State()
    result = state.getStudent(activity["sender"]["id"])
    scraper = Scraper()
    if result:
        rollno = str(result['RollNumber'])
        wak = str(result['wak'])
        #Find the exam Code.
        #BT3R15NOV17
        current = "BT" + convert(str(result["Semester"])) + "R15" + "NOV18"
        print(current)
        try:
            subjects, cred, gpa = scraper.getResults(rollno,wak)
        except Exception:
            bot.send_text_activity(activity, "Not Yet! Hold your horses.")
            return
        response = ""
        for i in subjects:
            for j in i:
                response += j
                response += "\t"
            response += "\n"
        bot.send_text_activity(activity, response)
        bot.send_text_activity(activity, "Total Credits: " + str(cred))
        bot.send_text_activity(activity, "Gpa: " + str(gpa))
    else:
        bot.send_text_activity(activity, "Authentication failed. Please message your rollno and web access key again.")
        bot.send_text_activity(activity, "Enter roll no. and web access key seperated by a single space.")