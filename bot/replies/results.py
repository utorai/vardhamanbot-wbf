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
            subjects, cred, gpa = scraper.getResults(rollno,wak,current)
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
        
        if gpa >= 9.5:
            responses = ["iamgonnacry", "really", "hurtmyfeelings", "Clapping", "telugu1"]
        elif gpa >= 9.0:
            responses = ["Winner", "genius", "mindblown", "youaretheman", "awesomesauce", "minions", "badass", "proud", "meeru", "mahesh"]
        elif gpa >= 8.0:
            responses = ["Woah", "whosawesome", "WOW", "fantastic", "Mogambo", "superabba", "intelli"]
        elif gpa >= 7.0:
            responses = ["goodjob", "groot", "betterluck", "deserve", "control"]
        elif gpa >= 6.0:
            responses = ["barelysurviving", "sarsarle", "apnatimeaayega"]
        elif gpa >= 5.0:
            responses = ["iknowthatfeel", "iknowtfeel", "baymax", "nextsem", "rightinthefeels"]
        elif gpa >= 4.0:
            responses = ["doyouthink", "laughing", "howamisupposedtolive", "tearsineyes", "doomed", "feels", "subject"]
        elif gpa < 4.0:
            responses = ["ohdear", "mkalaadla", "gfather", "hug", "crying", "ritf", "balayya"]
        reply = random.choice(responses)
        bot.send_rich_activity(activity, "https://www.utorai.com/assets/gifs/" + reply + ".gif")
    else:
        bot.send_text_activity(activity, "Authentication failed. Please message your rollno and web access key again.")
        bot.send_text_activity(activity, "Enter roll no. and web access key seperated by a single space.")
