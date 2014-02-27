#!/usr/bin/env python2 
from pygermeister import PygerMeister

class PlexerDuty(PygerMeister):
    def __init__(self, confFile="~/.pygerrc"):
        PygerMeister.__init__(self,confFile)
        self.defaults['plexApiUrl'] = "http://127.0.0.1:3005/jsonrpc"
    def sendIncident(self,subject,message):
        data = {"id":1,"jsonrpc":"2.0","method":"GUI.ShowNotification","params":{"title":subject,"message":message}}
        req = urllib2.Request(self.config.get("settings","plexApiUrl"))
        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')

        response = urllib2.urlopen(req, json.dumps(data))

if __name__ == '__main__':
    PlexerDuty().run()


