# News-and-Weather-ChatBot

News and Weather ChatBot made using Twilio, Dialogflow, and Flask.

The chatbot has four Dialogflow intents : get_weather, get_news, change_preferences and show_preferences

The get_news intent has three entities, news_type, geo-country and language. Some sample queries are 'Give entertainment news from India', 'Show me sports news from Australia' etc. MongoDB is used so that user's preferences can be stored. You can set your preferred news_type, language and country. So if you want news from India you can set your preferred country to India then you won't have to write India in every query, Simmilarly, you can do this with the language, if you set your preferred language to spanish, then all the news will come in spanish if no language is specified.
   
The get_weather intent has two entities, geo-city and weather_property. Some sample queries are 'Tell temperature in New Delhi', "Weather in London", "Tell humidity in Los Angeles" etc. Here also user's preferred city is stored, you can set your preferred city and then you can just write 'Tell weather' and you will get weather of your preferred city. You can also ask for any particular property also like cloud coverage, wind etc. 
    
The change_preferences intent has one entity, parameter. Some sample queries are 'Set my preferred city to New Delhi', 'Change my preferred country to India' etc.

The show_preferences intent has no entity. Some sample queries are 'Show preferences', "Show me my preferences", "Tell me my preferences" etc.
   
MongoDB has been integrated to store user preferences, so the preferences can be used while responding. For example, "Tell weather" will tell weather of your preferred city. Similarly tell news will give news of your preferred topic from your preferred country in your preferred language. 
    
## Hosted on : https://news-and-weather-chatbot.herokuapp.com/

## To interact with the bot

   Send a WhatsApp message to +14155238886 with code join men-home.
