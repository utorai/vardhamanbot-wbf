import random

def reply(activity, bot, data):
    responses = [
        "Your time!", 
        "For formality's sake 'nothing much'", 
        "My lawyer says I don't have to answer that question",
        "Ironing my blazer, Shaadi nahi hain meri, NBA Inspection hai. Pata nahi kya kya karna padta hai.",
        "Relishing Hyderabad's Biryani!, I just love it.",
        "Figuring out how to save Stark from space",
        "'Chilling' in front of a fireplace, It's really cold these days",
        "Watching The Mentalist on Amazon Prime Video, Patrick Jane is really awesome!",
        "Watching videos of Lionel Messi slaying Real Madrid, they are so satisfying! ",
        "Watching India conquer Australia at their home! Its always a pleasure watching MSD and Virat.",
        "Kisi ki keh ke leraha hoon!",
        "Waiting in my gallery, hoping that my order from Swiggy arrives soon!"

    ]
    response = random.choice(responses)
    bot.send_text_activity(activity, response)