# News-and-Weather-ChatBot

News and Weather ChatBot made using Twilio, Dialogflow, and Flask.

The chatbot has three Dialogflow intents : the get_weather, get_news, and change_preferences.

The get_news has three entities, news_type, geo-country and language. Some sample queries are 'Give entertainment news from India', 'Show me sports news from Australia' etc.
    MongoDB is used so that user's preferences can be stored. You can set your preferred news_type, language and country. So if you want news from India you can set your preferred country to India then you won't have to write India in every query,
    Simmilarly, you can do this with the language, if you set your preferred language to spanish, then all news will come in spanish if not specified specifically.
   
The get_weather has two entities, geo-city and weather_property. Some sample queries are 'Tell temperature in New Delhi', "Weather in London", etc.
    Here also user's preferred city is stored, you can set your preferred city and then you can just write 'Tell weather' and you will get weather of your preferred city.
    
The change_preferences has one entity, parameter. Some sample queries are 'Change my preferred city to New Delhi', 'Change my preferred country to India' etc.
   
MongoDB has been integrated to store user preferences, so the preferences can be used while responding. For example, "Tell weather" will tell weather of your preferred city. 
    Simmilarly tell news will give news of your preferred topic from your preferred country in your preferred language. 
    
## Hosted on : https://news-and-weather-chatbot.herokuapp.com/

## To interact with the bot

   Send a WhatsApp message to +14155238886 with code join men-home.
