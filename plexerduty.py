#!/usr/bin/env python2 
from datetime import datetime, timedelta
from pygerduty import PagerDuty
import json
import time
import urllib2
import argparse
import ConfigParser
import os

defaults = {
    "cronInterval":"30",
    "plexApiUrl": "http://127.0.0.1:3005/jsonrpc", 
    "pagerdutyHost": "",
    "pagerdutyApiKey": "",
    "notificationDelay":"5",
    "triggeredOnly":"true",
}

config = ConfigParser.ConfigParser(defaults)
config.read(os.path.expanduser("~/.pygerrc"))

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Increase output verbosity.", action="store_true")
          
args = parser.parse_args()
        
if args.verbose:
    print "Connecting to PagerDuty..."

pager = PagerDuty(config.get("settings","pagerdutyHost"),config.get("settings","pagerdutyApiKey"))

currentTime = datetime.now()
cronInterval = config.getint("settings","cronInterval")
pastTime = currentTime - timedelta(minutes=cronInterval)

currentTimeStr = currentTime.strftime('%Y-%m-%dT%X')
pastTimeStr= pastTime.strftime('%Y-%m-%dT%X')

argList = {}
argList['since'] = pastTimeStr
argList['until'] = currentTimeStr
if config.getboolean("settings","triggeredOnly"):
    argList['status'] = 'triggered'

if args.verbose:
    print "Fetching incidents..."
    print argList
incidents = pager.incidents.list(**argList)

if args.verbose:
    print "Looping incidents..."
for incident in incidents:
    incident_json = incident.trigger_summary_data.to_json()
    subject = incident.service.name
    message = " - ".join(item[1] for item in incident_json.items())
    if args.verbose:
        print "Sending incident popup (%s - %s)" % (subject,message)
    data = {"id":1,"jsonrpc":"2.0","method":"GUI.ShowNotification","params":{"title":subject,"message":message}}
    req = urllib2.Request(config.get("settings","plexApiUrl"))
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data))
    time.sleep(config.getfloat("settings","notificationDelay"))

