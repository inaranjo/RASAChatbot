from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
from rasa_core.events import Restarted
from termcolor import colored
import unidecode
import sys  
import difflib
from apixu.client import ApixuClient
from rasa_core.events import SlotSet

class ActionShow(Action):
    def name(self):
        return 'action_show'

    def run(self, dispatcher, tracker, domain):

        api_key = 'bc28bfb2026a474f808213126182805' #your apixu key
        client = ApixuClient(api_key)
		
        city = tracker.get_slot("city")

        current = client.getCurrentWeather(q=city)
        country = current['location']['country']
        city = current['location']['name']
        condition = current['current']['condition']['text']
        temperature_c = current['current']['temp_c']
        humidity = current['current']['humidity']
        wind_kph = current['current']['wind_kph']		
        wind_dir = current['current']['wind_dir']		
        cloud = current['current']['cloud']		
        feelslike_c = current['current']['feelslike_c']		
        response = """It is currently {} in {}, {} at the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} kph coming from the {}. Cloud covering is {}% and thermal sensation is {} degrees.""".format(
            condition, 
            city, 
            country, 
            temperature_c, 
            humidity, 
            wind_kph,
            wind_dir,
            cloud,
            feelslike_c)
						
        dispatcher.utter_message(response)
        return [SlotSet('city',city)]

