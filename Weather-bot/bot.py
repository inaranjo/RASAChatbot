from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings

from policy import RestaurantPolicy

#import sys
#sys.path.append('/home/arte/Documents/ProyectoChatbotISTAC/rasa_core/rasa_core/')
from rasa_core import utils
from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.events import SlotSet
from rasa_core.featurizers import (
    MaxHistoryTrackerFeaturizer,
    BinarySingleStateFeaturizer)
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.memoization import MemoizationPolicy

logger = logging.getLogger(__name__)


class RestaurantAPI(object):
    def search(self, info):
        return "papi's pizza place"


class ActionSuggest(Action):
    def name(self):
        return 'action_suggest'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("here's what I found:")
        dispatcher.utter_message(tracker.get_slot("matches"))
        dispatcher.utter_message("is it ok for you? "
                                 "hint: I'm not going to "
                                 "find anything else :)")
        return []


def train_dialogue(domain_file="weather_domain.yml",
                   model_path="models/dialogue",
                   training_data_file="data/stories.md"):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=3),
                            RestaurantPolicy()])

    training_data = agent.load_data(training_data_file)
    agent.train(
            training_data,
            epochs=400,
            batch_size=100,
            validation_split=0.2
    )

    agent.persist(model_path)
    return agent


def train_nlu():
    from rasa_nlu.training_data import load_data
    from rasa_nlu import config
    from rasa_nlu.model import Trainer

    training_data = load_data('data/nlu_train.json')
    trainer = Trainer(config.load("nlu_model_config.yml"))
    trainer.train(training_data)
    model_directory = trainer.persist('models/nlu/',
                                      fixed_model_name="current")

    return model_directory

def run(serve_forever=True):
    interpreter = RasaNLUInterpreter("models/nlu/default/model_20180529-103257")
    agent = Agent.load("models/dialogue", interpreter=interpreter)

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
    return agent

def runSlack(serve_forever=True):
    from rasa_core.channels import HttpInputChannel
    from rasa_core.channels.slack import SlackInput
    from rasa_core.agent import Agent
    from rasa_core.interpreter import RegexInterpreter

    # load your trained agent
    interpreter = RasaNLUInterpreter("models/nlu/default/model_20180529-103257")
    agent = Agent.load("models/dialogue", interpreter=interpreter)

    input_channel = SlackInput(
    slack_token = "xoxb-371047401462-369661464209-wcn44I8JzTIfJVwE6soZp6XH",  # this is the `bot_user_o_auth_access_token`
    #slack_channel = "@Bot-test"  # the name of your channel to which the bot posts (optional)
    )
    print(HttpInputChannel(5004, "/app", input_channel))

    agent.handle_channel(HttpInputChannel(5002, "/app", input_channel))

if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")

    parser = argparse.ArgumentParser(
            description='starts the bot')

    parser.add_argument(
            'task',
            choices=["train-nlu", "train-dialogue", "run", "runSlack"],
            help="what the bot should do - e.g. run or train?")
    task = parser.parse_args().task

    # decide what to do based on first parameter of the script
    if task == "train-nlu":
        train_nlu()
    elif task == "train-dialogue":
        train_dialogue()
    elif task == "run":
        run()
    elif task == "runSlack":
        runSlack()