from rasa_core.channels import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_slack_connector import SlackInput


#nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/weathernlu')
nlu_interpreter = RasaNLUInterpreter("models/nlu/default/model_20180529-103257")
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter)

input_channel = SlackInput('xoxp-323477913479-323485125591-371645106850-dbe0993955d947777f252bc8e1974d84', #app verification token
							'xoxb-323477913479-372692497543-oapwh0sjBGeLL0EP2amERnMg', # bot verification token
							'dTIzwLYyD0MiKScpM3ptgCGS', # slack verification token
							False)

agent.handle_channel(HttpInputChannel(5004, '/', input_channel))