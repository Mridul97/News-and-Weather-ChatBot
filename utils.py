import os
from config import api_key, project_id, mongourl
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client-secret.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = project_id

from gnewsclient import gnewsclient
from pyowm import OWM
from pymongo import MongoClient

mclient = MongoClient(mongourl)
db = mclient.get_database('weather')

API_key = api_key

owm = OWM(API_key)

client = gnewsclient.NewsClient(max_results = 3)

def get_news(parameters, session_id):
    print(parameters)
    preferences = db.preferences
    if parameters.get('news_type'):
        client.topic = parameters.get('news_type')
    elif preferences.find_one({'user_id' : session_id}) != None and preferences.find_one({'user_id' : session_id})['news_type'] != '':
        client.topic = preferences.find_one({'user_id' : session_id})['news_type']
    
    # if not parameters.get('language') and preferences.find_one({'user_id' : session_id}) != None and preferences.find_one({'user_id' : session_id})['language'] != '':
    #     client.language = list(preferences.find({'user_id' : session_id}))[0]['language']
    # else:
    #     client.language = parameters.get('language')

    if parameters.get('language') : 
        client.language = parameters.get('language')
    elif preferences.find_one({'user_id' : session_id}) != None and preferences.find_one({'user_id' : session_id})['language'] != '':
        client.language = preferences.find_one({'user_id' : session_id})['language']

    if parameters.get('geo-country'):
        client.location = parameters.get('geo-country')
    elif preferences.find_one({'user_id' : session_id}) != None and preferences.find_one({'user_id' : session_id})['country'] != '':
        client.location = preferences.find_one({'user_id' : session_id})['country']
    
    print(client.topic, client.language, client.location)
    return client.get_news()

def change_preference(parameters, session_id):
    print(parameters)
    preferences = db.preferences
    strout = ""
    if preferences.find_one({'user_id': session_id}) == None :
        print("Setting")
        if parameters.get('Parameters') == 'City':
            if parameters.get('geo-city'):
                new_preferences = {'city' : parameters.get('geo-city'), 'user_id' : session_id, 'country' : '', 'language' : '', 'news_type' : ''}
                preferences.insert_one(new_preferences)
                strout += "Preferences set successfully!"
        elif parameters.get('Parameters') == 'Country':
            if parameters.get('geo-country'):
                new_preferences = {'city' : '', 'user_id' : session_id, 'country' : parameters.get('geo-city'), 'language' : '', 'news_type' : ''}
                preferences.insert_one(new_preferences)
                strout += "Preferences set successfully!"
        elif parameters.get('Parameters') == 'Language':
            if parameters.get('language'):
                new_preferences = {'city' : '', 'user_id' : session_id, 'country' : '', 'language' : parameters.get('language'), 'news_type' : ''}
                preferences.insert_one(new_preferences)
                strout += "Preferences set successfully!"
        elif parameters.get('Parameters') == 'news_type':
            if parameters.get('news_type'):
                new_preferences = {'city' : '', 'user_id' : session_id, 'country' : '', 'language' : '', 'news_type' : parameters.get('news_type')}
                preferences.insert_one(new_preferences)
                strout += "Preferences set successfully!"
    else:
        print("Updating")
        if parameters.get('Parameters') == 'City':
            if parameters.get('geo-city'):
                updates = {'city' : parameters.get('geo-city')}
                preferences.update_one({'user_id' : session_id}, {'$set' : updates})
                strout += "Preferences changed successfully!"
        elif parameters.get('Parameters') == 'Country':
            if parameters.get('geo-country'):
                updates = {'country' : parameters.get('geo-country')}
                preferences.update_one({'user_id' : session_id}, {'$set' : updates})
                strout += "Preferences changed successfully!"
        elif parameters.get('Parameters') == 'Language':
            if parameters.get('language'):
                updates = {'language' : parameters.get('language')}
                preferences.update_one({'user_id' : session_id}, {'$set' : updates})
                strout += "Preferences changed successfully!"
        elif parameters.get('Parameters') == 'news_type':
            if parameters.get('news_type'):
                updates = {'news_type' : parameters.get('news_type')}
                preferences.update_one({'user_id' : session_id}, {'$set' : updates})
                strout += "Preferences changed successfully!"
    return strout
             
def get_weather(parameters, session_id):
    preferences = db.preferences
    print(parameters)
    if parameters.get('geo-city'):
        obs = owm.weather_at_place(parameters.get('geo-city'))
    elif preferences.find_one({'user_id' : session_id}) != None and preferences.find_one({'user_id' : session_id})['city'] != '':
        obs = owm.weather_at_place(preferences.find_one({'user_id' : session_id})['city'])
    else:
        return "No city is given to show results. Please set your preferred city to get result."

    w = obs.get_weather()
    if (parameters.get('weather_property') == 'Temperature'):
        return "Temperature :" + str(w.get_temperature()['temp']) + " K" , w.get_weather_icon_url()
    if (parameters.get('weather_property') == 'Weather Condition'):
        return  "\n" + str(w.get_detailed_status()) + "\nTemperature : " +  str(w.get_temperature()['temp']) + " K" + "\nPressure : " + str(w.get_pressure()['press']) + " mb" + "\nHumidity : " + str(w.get_humidity()) + "%" + "\nClouds Coverage : " + str(w.get_clouds()) + "%" + "\nWind : {} km/h at {} deg".format(w.get_wind()['speed'], w.get_wind()['deg']) , w.get_weather_icon_url() 

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(msg, session_id):
    response = detect_intent_from_text(msg, session_id)

    if response.intent.display_name == 'get_news':
        # return "ok I will show you news {}".format(
            # dict(response.parameters))
        news = get_news(dict(response.parameters), session_id)
        news_str = 'Here is your news:'
        for row in news:
            news_str += "\n\n{}\n\n{}\n\n".format(row['title'], row['link'])
        # print (news_str)
        return news_str
    if response.intent.display_name == 'get_weather':
        if(type(get_weather(dict(response.parameters), session_id)) == str):
            weather = get_weather(dict(response.parameters), session_id)
            weather_str = "The current conditions are : " + weather
            return weather_str
        else :
            weather , url = get_weather(dict(response.parameters), session_id)
            weather_str = "The current conditions are : " + weather
            return weather_str , url
    if response.intent.display_name == 'change_preference':
        outstr = change_preference(dict(response.parameters), session_id)
        if outstr == "":
            return "The preferences were not changed. Please try again"
        else:
            return outstr
    else:
        return response.fulfillment_text