# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 11:27:08 2015

@author: kenneths
"""

import feedparser
import pickle

AsiaPac = {'cloudfront':"http://status.aws.amazon.com/rss/cloudfront.rss",
'cloudsearchSG':"http://status.aws.amazon.com/rss/cloudsearch-ap-southeast-1.rss",
'cloudsearchSydn':"http://status.aws.amazon.com/rss/cloudsearch-ap-southeast-2.rss"}


print AsiaPac.keys()
ServiceSelected = raw_input("Select Service: ")
print AsiaPac[ServiceSelected]

try:
  query = feedparser.parse(AsiaPac[ServiceSelected])
  if query.entries:
    title = query.entries[0]['title']
    pubdate = query.entries[0]['published']
    dsc = query.entries[0]['description']
  elif query['feed']['title']:
    print 'AWS OK: No events to display.'
    exit(0)
except KeyError:
  print "error"
  exit(3)

if title.startswith("Service is operating normally"):
  status = 0
  msg = "AWS OK: \n"
elif (title.startswith("Informational message") or title.startswith("Performance issues") ):
  status = 1
  msg = "AWS WARNING: "
elif (title.startswith("Service disruption")):
  status = 2
  msg = "AWS CRITICAL: "
else:
  status = 3
  msg = "AWS UNKNOWN: "
  
msg += title
print pubdate
print msg
print dsc

exit(status)