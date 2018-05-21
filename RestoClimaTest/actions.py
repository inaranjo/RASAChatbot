from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet


class ActionSearchConcerts(Action):
    def name(self):
        return 'action_search_concerts'

    def run(self, dispatcher, tracker, domain):
        concerts = [
            {"artist": "Foo Fighters", "reviews": 4.5},
            {"artist": "Katy Perry", "reviews": 5.}
        ]
        description = ", ".join([c["artist"] for c in concerts])
        dispatcher.utter_message("{}".format(description))
        return [SlotSet("concerts", concerts)]


class ActionSearchVenues(Action):
    def name(self):
        return 'action_search_venues'

    def run(self, dispatcher, tracker, domain):
        venues = [
            {"name": "Big Arena", "reviews": 4.5},
            {"name": "Rock Cellar", "reviews": 5.}
        ]
        dispatcher.utter_message("here are some venues I found")
        description = ", ".join([c["name"] for c in venues])
        dispatcher.utter_message("{}".format(description))
        return [SlotSet("venues", venues)]


class ActionShowConcertReviews(Action):
    def name(self):
        return 'action_show_concert_reviews'

    def run(self, dispatcher, tracker, domain):
        concerts = tracker.get_slot("concerts")
        dispatcher.utter_message("concerts from slots: {}".format(concerts))
        return []


class ActionShowVenueReviews(Action):
    def name(self):
        return 'action_show_venue_reviews'

    def run(self, dispatcher, tracker, domain):
        venues = tracker.get_slot("venues")
        dispatcher.utter_message("venues from slots: {}".format(venues))
        return []

class ActionShowWeather(Action):
    def name(self):
        return 'action_show_weather'

    def run(self, dispatcher, tracker, domain):
        city = tracker.get_slot("city")
        weatherDate = tracker.get_slot("weatherDate")
        dispatcher.utter_message("el clima {} en {} es de 24 grados ;-)".format(weatherDate, city))
        return []

class ActionShowRestaurant(Action):
    def name(self):
        return 'action_show_restaurant'

    def run(self, dispatcher, tracker, domain):
        restaurantLoc = tracker.get_slot("restaurantLoc")
        restaurantDate = tracker.get_slot("restaurantDate")
        restaurantPeople = tracker.get_slot("restaurantPeople")
        dispatcher.utter_message("reserva de restaurante para {} en el {} para el {} confirmada ;-)".format(restaurantPeople, restaurantLoc, restaurantDate))
        return []