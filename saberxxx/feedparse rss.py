# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 15:01:58 2015

@author: benedicki
"""

gen = None
import threading
import feedparser as fe

def checktitle(x):
    if "[RESOLVED]" in x.title:
        msg = "AWS RESOLVED: "    
    elif x.title.startswith("Service is operating normally"):
        msg = "AWS OK: "
    elif (x.title.startswith("Informational message") or x.title.startswith("Performance issues") ):
        msg = "AWS WARNING: "
    elif (x.title.startswith("Service disruption")):
        msg = "AWS CRITICAL: "
    else:
        msg = "AWS UNKNOWN: "
    return msg
def getcheck():
    global gen 
    threading.Timer(2.0, getcheck).start()

    f = fe.parse('http://status.aws.amazon.com/rss/all.rss')

    if gen is None:
        print("null")
        gen = [x for x in f.entries]
        for x in gen:
            msg = checktitle(x)
            print (msg+x.title+" "+x.published+" : "+x.description+"\n")
    else:  
        print("ekse")
        for x in f.entries:
            for y in gen:
                if x == y:
                    break
            else:        
                msg = checktitle(x)
                gen.append(x)
                print (msg+x.title+" "+x.published+" : "+x.description+"\n")
                print (chr(7))
                print("meron "+x.published)
        
        

getcheck()