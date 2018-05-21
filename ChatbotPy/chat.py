from __future__ import print_function, unicode_literals
import random
import logging
import os

os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'

from textblob import TextBlob
from pattern.es import singularize, pluralize, parse, split
from config import FILTER_WORDS
import unidecode
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Sentences we'll respond with if we have no idea what the user just said
NONE_RESPONSES = [
    "Lo sentimos, tu busqueda no ha dado resultados",
]
# end

class UnacceptableUtteranceException(Exception):
    """Raise this (uncaught) exception if the response was going to trigger our blacklist"""
    pass


def chatback(sentence):
    """Main program loop: select a response for the input sentence and return it"""
    logger.info("Chat: respond to %s", sentence)
    resp = respond(sentence)
    return resp


def construct_response(query, time, place):
    """No special cases matched, so we're going to try to construct a full sentence that uses as much
    of the user's input as possible"""
    resp = []
    resp.append('\nQueries : ')
    if (len(query)>0):
        for q in query:
            resp.append(q)
    resp.append('\nTime : ')
    if (len(time)>0):
        for t in time:
            resp.append(t)
    resp.append('\nPlace : ')
    if (len(place)>0):
        for p in place:
            resp.append(p)

    return " ".join(resp)
# end


def preprocess_text(sentence):
    """Handle some weird edge cases in parsing, like accents, etc."""
    cleaned = []
    words = sentence.split(' ')
    for w in words:
        w = unidecode.unidecode(w)
        cleaned.append(w)
    return ' '.join(cleaned)

def respond(sentence):
    """Parse the user's inbound sentence and find candidate terms that make up a best-fit response"""
    cleaned = preprocess_text(sentence)
    parsed = parse(cleaned)
    
    query, time, place = find_candidate_queries(parsed)

    resp = None
    if (len(query) + len(time) + len(place) == 0):
        resp = random.choice(NONE_RESPONSES)
    else:
        resp = construct_response(query, time, place)

    # If we got through all that with nothing, use a random response
    if not resp:
        resp = random.choice(NONE_RESPONSES)

    # Check that we're not going to say anything obviously offensive
    filter_response(resp)

    return resp

def find_candidate_queries(parsed):
    """Given a parsed input, find the best query, time lapse, place to match their input.
    Returns a tuple of query, time, place any of which may be None if there was no good match"""
    query = []
    time = []
    place = []

    for w in parsed.split(' '):
        word_tag = w.split('/')
        logger.info("Palabra = %s, tag = %s", word_tag[0], word_tag[1] )
        if(word_tag[1]=='NN'):
            query.append(word_tag[0])
        if(word_tag[1]=='CD'):
            time.append(word_tag[0])
        if(word_tag[1]=='NNP'):
            place.append(word_tag[0])

    #for sent in parsed.sentences:
        #query = find_query(sent)
        #time = find_time(sent)
        #place = find_place(sent)
    logger.info("Query=%s, Time=%s, Place=%s", query, time, place)
    return query, time, place


def filter_response(resp):
    """Don't allow any words to match our filter list"""
    tokenized = resp.split(' ')
    for word in tokenized:
        if '@' in word or '#' in word or '!' in word:
            raise UnacceptableUtteranceException()
        for s in FILTER_WORDS:
            if word.lower().startswith(s):
                raise UnacceptableUtteranceException()


if __name__ == '__main__':
    import sys
    # Usage:
    # python chat.py "I am an engineer"
    if (len(sys.argv) > 1):
        saying = sys.argv[1]
        print(chatback(saying))
    else:
        print("Usage: python chat.py 'desempleo Tenerife en 2015' ")       
