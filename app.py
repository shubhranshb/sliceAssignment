import random
import string
import json

import cherrypy


@cherrypy.expose
class WordCounterWebService(object):
    def __init__(self):
        self.worldCounter = dict()

    @cherrypy.tools.accept(media='application/json')
    def GET(self, word=""):
        response = {"status": True, "message": "", "result": ""}
        if not word:
            response["status"] = False
            response["message"] = "Empty Request"

        else:
            lowerWord = (word.lower()).strip()
            response["result"] = {"word": lowerWord, "counter": 0}
            if lowerWord in self.worldCounter.keys():
                response["result"]["counter"] = self.worldCounter[lowerWord]

        return json.dumps(response).encode('utf8')

    def POST(self, word=""):
        response = {"status": True, "message": "", "result": ""}

        if not word:
            response["status"] = False
            response["message"] = "Empty Request"

        else:
            lowerWord = (word.lower()).strip()
            if lowerWord in self.worldCounter.keys():
                self.worldCounter[lowerWord] = self.worldCounter[lowerWord] + 1
            else:
                self.worldCounter[lowerWord] = 1
            response["message"] = "word added " + lowerWord + "successfully"

        return json.dumps(response).encode('utf8')

    def DELETE(self, word=""):
        response = {"status": True, "message": "", "result": ""}

        if not word:
            response["status"] = False
            response["message"] = "Empty Request"
        else:
            lowerWord = (word.lower()).strip()
            if lowerWord in self.worldCounter.keys():
                del self.worldCounter[lowerWord]
                response["message"] = "word removed successfully"
            else:
                response["status"] = False
                response["message"] = "word not present"

        return json.dumps(response).encode('utf8')



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