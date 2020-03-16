import random
import string
import json

import cherrypy


@cherrypy.expose
class WordCounterWebService(object):
    def __init__(self):
        self.worldCounter = dict()

    @cherrypy.tools.accept(media='application/json')
    def GET(self, word):
        lowerWord = word.lower()
        response = {"word": lowerWord, "counter": 0}
        if lowerWord in self.worldCounter.keys():
            response["counter"] = self.worldCounter[lowerWord]
        return json.dumps(response).encode('utf8')

    def POST(self, word):
        lowerWord = word.lower()
        if lowerWord in self.worldCounter.keys():
            self.worldCounter[lowerWord] = self.worldCounter[lowerWord] + 1
        else:
            self.worldCounter[lowerWord] = 1
        return json.dumps({"response": "OK"}).encode('utf8')

    def DELETE(self, word):
        lowerWord = word.lower()
        if lowerWord in self.worldCounter.keys():
            del self.worldCounter[lowerWord]
            return json.dumps({"response": "OK"}).encode('utf8')
        else:
            raise cherrypy.HTTPError(status=400, message="Word not present in counter")


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        }
    }

    cherrypy.quickstart(WordCounterWebService(), '/word', conf)