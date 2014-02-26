#!/usr/bin/env python2 
from datetime import datetime, timedelta
from pygerduty import PagerDuty
import json
import time
import urllib2
import argparse
import ConfigParser
import os

class Plexerduty:
    def __init__(self, confFile="~/.pygerrc"):
        self.defaults = {
            "cronInterval":"30",
            "plexApiUrl": "http://127.0.0.1:3005/jsonrpc", 
            "pagerdutyHost": "",
            "pagerdutyApiKey": "",
            "notificationDelay":"5",
            "triggeredOnly":"true",
        }
        self.config = self.getConfig(confFile)
        self.args = self.getArgs()

    def run(self):
        self.checkForPages()

    def getArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose", help="Increase output verbosity.", action="store_true")
              
        args = parser.parse_args()
        return args

    def getConfig(self,confFile):
        config = ConfigParser.ConfigParser(self.defaults)
        config.read(os.path.expanduser(confFile))
        return config

    def checkForPages(self):        
        if self.args.verbose:
            print "Connecting to PagerDuty..."

        pager = PagerDuty(self.config.get("settings","pagerdutyHost"),self.config.get("settings","pagerdutyApiKey"))

        currentTime = datetime.utcnow()
        cronInterval = self.config.getint("settings","cronInterval")
        pastTime = currentTime - timedelta(minutes=cronInterval)

        currentTimeStr = currentTime.strftime('%Y-%m-%dT%X')
        pastTimeStr= pastTime.strftime('%Y-%m-%dT%X')

        argList = {}
        argList['since'] = pastTimeStr
        argList['until'] = currentTimeStr
        if self.config.getboolean("settings","triggeredOnly"):
            argList['status'] = 'triggered'

        if self.args.verbose:
            print "Fetching incidents..."
            print argList
        incidents = pager.incidents.list(**argList)

        if self.args.verbose:
            print "Looping incidents..."
        for incident in incidents:
            incident_json = incident.trigger_summary_data.to_json()
            subject = incident.service.name
            message = " - ".join(item[1] for item in incident_json.items())

            if incident.status != 'triggered':
                message = incident.last_status_change_by.name + " " + incident.status + " " + message
            self.sendIncident(subject,message)
            time.sleep(self.config.getfloat("settings","notificationDelay"))

    def sendIncident(self,subject,message):
        if self.args.verbose:
            print "Sending incident popup (%s - %s)" % (subject,message)
        data = {"id":1,"jsonrpc":"2.0","method":"GUI.ShowNotification","params":{"title":subject,"message":message}}
        req = urllib2.Request(config.get("settings","plexApiUrl"))
        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')

        response = urllib2.urlopen(req, json.dumps(data))

if __name__ == '__main__':
    Plexerduty().run()