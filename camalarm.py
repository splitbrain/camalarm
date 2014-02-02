#!/usr/bin/python2

import os
import subprocess
import json
import datetime
import time
import urllib2
import base64
import sys
import signal

def main():
    global conf

    # load config
    cfg = os.path.splitext(__file__)[0]+'.json';
    print "loading config from %s" % cfg
    with open(cfg, 'r') as conffile:
        conf = conffile.read();
    conf = json.loads(conf);

    # catch ctrl-c
    signal.signal(signal.SIGINT, shutdown)

    # monitor alarm state
    alarm = None
    while True:
        toalarm = shouldbearmed()
        if (toalarm != alarm):
            if toalarm:
                setalarm(True)
                alarm = True
            else:
                setalarm(False)
                alarm = False
        time.sleep(conf['checkminutes'] * 60)

def shutdown(signal, frame):
    print "Shutting down. Please wait..."
    setalarm(True)
    sys.exit(0)

def setalarm(enable):
    global conf

    if(enable):
        url1 = "http://%s/set_alarm.cgi?motion_armed=1" % conf['camera']
        url2 = "http://%s/set_misc.cgi?led_mode=1" % conf['camera']
        print "%s enabling alarm" % datetime.datetime.today()
    else:
        url1 = "http://%s/set_alarm.cgi?motion_armed=0" % conf['camera']
        url2 = "http://%s/set_misc.cgi?led_mode=2" % conf['camera']
        print "%s disabling alarm" % datetime.datetime.today()

    auth = base64.standard_b64encode('%s:%s' % (conf['user'], conf['pass']))

    # alarm
    req = urllib2.Request(url1)
    req.add_header('Authorization', 'Basic %s' % auth)
    res = urllib2.urlopen(req)
    #print res.read()

    # led
    req = urllib2.Request(url2)
    req.add_header('Authorization', 'Basic %s' % auth)
    res = urllib2.urlopen(req)
    #print res.read()


def shouldbearmed():
    global conf

    # check if anyone is at home - if not, arm immeadiately
    anyonehome = False
    for host in conf['athome']:
        if ping(host):
            anyonehome = True
            break
    if not anyonehome:
        return True

    # is it sleepy time? if not, no alarm
    t = conf['waketime'][weekday()][0]          # asleep til
    f = conf['waketime'][weekday()][1]          # asleep from
    n = time.strftime('%H%M', time.localtime()) # current time
    if(n > t and n < f):
        return False

    # is someone still awake, despite sleepy time? no alarm then
    anyoneawake = False
    for host in conf['awake']:
        if ping(host):
            anyoneawake = True
            break
    if not anyoneawake:
        return False

    # it's sleepy time and noone is awake, set alarm
    return True

def weekday():
    days = ['mon','tue','wed','thu','fri','sat','sun'];
    return days[datetime.datetime.today().weekday()]

def ping(host):
    FNULL = open(os.devnull, 'w');
    status = subprocess.call(['ping', '-c', '1', host], stdout=FNULL, stderr=FNULL)
    if status == 0:
        return True
    else:
        return False



if __name__ == "__main__":
    main()
