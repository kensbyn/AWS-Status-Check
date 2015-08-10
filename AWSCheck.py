# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 14:50:35 2015

@author: kenneths
"""
import feedparser
import argparse
import pickle

feed = ""
msg  = ""
title = ""
pubdate = ""
desc = ""
forcache = ""
class AWSCheck(object):
    aws_services = ['cloudfront','cloudsearch','cloudwatch','dynamodb','ecs','ec2','elb','emr', 'elastictranscoder','elasticache','glacier','kinesis','redshift','rds', 'route53','sns','sqs' ,'s3' ,'swf','simpledb','vpc','workdocs','workspaces','autoscaling','cloudformation','cloudhsm','cloudtrail','codedeploy','config','datapipeline','directconnect','directoryservice','elasticbeanstalk','iam','import-export','kms','management-console','storagegateway' ]
    parser = argparse.ArgumentParser(description='Current status check of AWS Service Health Dashboard')
    parser.add_argument('service', choices= aws_services)
    parser.add_argument('--region', choices = ['ap-southeast-1','ap-southeast-2','ap-northeast-1','us-east-1','us-west-1','us-west-2','us-standard','sa-east-1','sa-west-2','eu-central-1','eu-west-1'])
    args = parser.parse_args()

    if args.region == None:
        feed = args.service
    else:
        feed = args.service + '-' + args.region
    
    def collectmsg(feed):
        try:
            uri = feedparser.parse('http://status.aws.amazon.com/rss/'+feed+'.rss')
            if uri.entries:
                title = uri.entries[0]['title']
                pubdate = uri.entries[0]['published']
                desc = uri.entries[0]['description']
            elif uri['feed']['title']:
                    print 'AWS is OK: No events to display for now.'
                    exit(0)
        except KeyError:
            print 'AWS URL ERROR: Feed http://status.aws.amazon.com/rss/'+feed+'.rss cound not be parsed. Check command options.'
            exit(3)
    
        if title.startswith("Service is operating normally"):
            status = 0
            msg = "AWS is OK: "
        elif (title.startswith("Informational message") or title.startswith("Performance issues") ):
            status = 1
            msg = "AWS has WARNING: "
        elif (title.startswith("Service disruption")):
            status = 2
            msg = "AWS is CRITICAL: "
        else:
            status = 3
            msg = "AWS UNKNOWN: "
        msg += title
        forcache = msg + "\n" + pubdate + "\n" + desc
        
        try:
            oldcache = pickle.load(open(feed+"_cachemsg.p","rb"))
            if oldcache == forcache:
                print "No new event, last event message will be shown \n \n*******************"
                print oldcache
        except Exception:
            pickle.dump(forcache, open(feed+"_cachemsg.p","wb"))
            print(chr(7)+chr(7)+chr(7)+chr(7)+chr(7)+" New Event "+chr(7)+chr(7)+chr(7)+chr(7)+chr(7))
            print forcache
            print "Cached!"

    collectmsg(feed)