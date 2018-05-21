from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RegexInterpreter


def run_restoclima(serve_forever=True):
    interpreter = RasaNLUInterpreter("models/nlu_v13/default/model_20180518-152807")
    agent = Agent.load("models/dialogue",
                       interpreter=interpreter)
                       #interpreter=RegexInterpreter())

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
    return agent


if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")
    run_restoclima()