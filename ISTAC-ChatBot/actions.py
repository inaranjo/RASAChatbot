from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
from rasa_core.events import Restarted
from termcolor import colored
from variables import locations, dates, indexes
import unidecode
import sys  
import difflib


reload(sys)  
sys.setdefaultencoding('utf8')

locations_lower = [unidecode.unidecode(unicode(x.lower(), "utf-8"))  for x in locations]
dates_lower = [unidecode.unidecode(unicode(x.lower(), "utf-8"))  for x in dates]
indexes_lower = [unidecode.unidecode(unicode(x.lower(), "utf-8"))  for x in indexes]

class ActionShow(Action):
    def name(self):
        return 'action_show'

    def run(self, dispatcher, tracker, domain):
        Loc = tracker.get_slot("var_Loc")
        Date = tracker.get_slot("var_Date")
        What = tracker.get_slot("var_What")
   
        foundLoc = False
        foundDate = False 
        foundWhat = False

        if(Loc != None): foundLoc = (unidecode.unidecode(Loc.lower()) in locations_lower)
        if(Date != None): foundDate = (unidecode.unidecode(Date.lower()) in dates_lower) 
        if(What != None): foundWhat = (unidecode.unidecode(What.lower()) in indexes_lower)

        foundAll = foundLoc and foundDate and foundWhat

        if (foundAll):    
            DBIndex = indexes[indexes_lower.index(unidecode.unidecode(What.lower()))]
            DBDate = dates[dates_lower.index(unidecode.unidecode(Date.lower()))]
            DBLoc = locations[locations_lower.index(unidecode.unidecode(Loc.lower()))]
            dispatcher.utter_message("\n")
            dispatcher.utter_message("Encontrado : {} en {} durante {}: AAAAA".format(
                colored(DBIndex, 'green'), 
                colored(DBLoc, 'yellow'),
                colored(DBDate, 'cyan') 
                ))
            dispatcher.utter_message("\n")
            dispatcher.utter_message("Te gustaria conocer el {} en {} de otra localidad?".format(
                colored(DBIndex, 'green'), 
                colored(DBDate, 'cyan')))
            dispatcher.utter_message("Te gustaria conocer el {} de {} en otra fecha?".format(
                colored(DBIndex, 'green'), 
                colored(DBLoc, 'yellow')))
            dispatcher.utter_message("Te gustaria conocer otra informacion de {} en {}?".format(
                colored(DBLoc, 'yellow'), 
                colored(DBDate, 'cyan')))
        else:
            dispatcher.utter_message("\n")
            dispatcher.utter_message("Tratando de encontrar : {} en {} durante {}".format(
                colored(What, 'green'), 
                colored(Loc, 'yellow'),
                colored(Date, 'cyan') 
                ))
            dispatcher.utter_message("No encontre esta informacion en la DB :")
            if (not foundLoc):
                dispatcher.utter_message("Localidad {} no encontrada en nuestra DB".format(colored(Loc, 'yellow')))
                # Check posible answers if slot is not empty
                if(Loc == None): return []
                dispatcher.utter_message("Querias decir alguna de las siguientes localidades?")
                matchDict = {}
                for (token, token2) in zip(locations_lower,locations):
                    matchDict[token2] = difflib.SequenceMatcher(None, Loc.lower(), token).ratio()
                for i in range(10):
                    dispatcher.utter_message("{}".format(colored(sorted(matchDict, key=matchDict.get, reverse=True)[i],'yellow')))
            if (not foundDate):
                dispatcher.utter_message("Fecha {} no encontrada en nuestra DB".format(colored(Date, 'cyan')))
                # Check posible answers if slot is not empty
                if(Date == None): return []
                dispatcher.utter_message("Querias decir alguna de las siguientes fechas?")
                matchDict = {}
                for token in dates_lower:
                    matchDict[token] = difflib.SequenceMatcher(None, Date.lower(), token).ratio()
                for i in range(10):
                    dispatcher.utter_message("{}".format(colored(sorted(matchDict, key=matchDict.get, reverse=True)[i],'cyan')))          
            if (not foundWhat):
                dispatcher.utter_message("Indice {} no encontrado en nuestra DB".format(colored(What, 'green')))
                # Check posible answers if slot is not empty
                if(What == None): return []
                dispatcher.utter_message("Querias buscar alguno de los siguientes indices?")
                matchDict = {}
                for (token, token2) in zip(indexes_lower,indexes):
                    matchDict[token2] = difflib.SequenceMatcher(None, What.lower(), token).ratio() 
                for i in range(len(indexes)):
                    dispatcher.utter_message("{}".format(colored(sorted(matchDict, key=matchDict.get, reverse=True)[i],'green')))      
        return []       

class ActionAskHowCanHelp(Action):
    def name(self):
        return 'action_ask_howcanhelp'

    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_message("Hola! En que te puedo ayudar?")

        return [Restarted()]