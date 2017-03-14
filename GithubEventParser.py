# Flask server to parse Github PullRqeust events
# -finding out origination branch
#
# mika.nokka1@gmail.com
# added for PR testing
# second added line


from __future__ import unicode_literals
from getpass import getpass
from pprint import pprint
import xmlrpclib, sys, getopt

from datetime import datetime
import sys, getopt, re
import netrc
import argparse
import logging
import os,platform
import json

from SQLfinder import SQLChecker 

__version__ = "0.1"

from flask import Flask, request
#import request   # pip install flask
from jira import JIRA # pip install jira

app = Flask(__name__)

jira = None
confluence = None
token = None
confFile="RELEASE_NOTES.conf" #yep

def main(argv):
    global jira, confluence, token
    global JiraProject, jiraAddress
    global confluenceSpace
    global confluencePage
    global confFile
    global ConfDictionary
    
    user=''
    host=''
#    jiraAddress=''
#    confluenceAddress=''
#    confluenceSpace=''
#    confluencePage=''
    JiraProject=''
    ConfDictionary={}
    
    
    loglevel = logging.INFO # Default logging level, override with '-d' for logging.DEBUG
    parser = argparse.ArgumentParser(usage="""
    {1}    Version:{0}
    
   TBD 
 
 
    """.format(__version__,sys.argv[0]))

    #parser.add_argument('-u','--user', help='<User>')
   # parser.add_argument('-j','--jira', help='<Jira address')
   # parser.add_argument('-c','--confluence', help='<Confluence address>')
   # parser.add_argument('-s','--space', help='<Existing Confluence space name>')
    parser.add_argument('-v','--version', help='<Version>', action='store_true')
    parser.add_argument('-d','--debug', help='<Debug info>', action='store_true')
    
    args = parser.parse_args()
        
    if args.version:
        print 'Tool version: %s'  % __version__
        sys.exit(2)    
    
    if args.debug:
        loglevel = logging.DEBUG
            
 #   jiraAddress = args.jira or ''
  #  confluenceAddress = args.confluence or ''
  #  confluenceSpace = args.space or ''
      
    logging.basicConfig(level=loglevel)    
                 

                 
    # quick old-school way to check needed parameters
#    if (jiraAddress=='' or  confluenceAddress=='' or confluenceSpace==''):
#        parser.print_help()
#        sys.exit(2)
            
    os_info=os.name+"  "+platform.system()
    logging.info ("OS info: %s" %os_info)
   
   
    logging.info("----> Flask server %s is starting running" % __version__)
    #app.run(debug=True)
    app.run(host='82.118.195.16', debug=True) # 
    
 
@app.route("/", methods=["GET", "POST"])
def webhook():
   
    
    
    if request.method == "GET":
        return "GithubPullRequestBambooBuilder reporting back (GET): OK"
    elif request.method == "POST":
        data = request.get_json() #(force=True)
        logging.info( "--> Received data")
        #logging.info( "%s" % pprint(data))
        branch="No branch information found. Maybe this was not PullRequest creation event" #default message
        
        logging.debug('**********************************************')
        logging.debug('JSON Headers: %s', request.headers) 
        logging.debug('JSON Body: %s', request.get_data())
        logging.debug('**********************************************')

        if data.get('pull_request'): # pull request event
            action=data['action']
            if (action=="opened"):  # "action": "opened", category must be "create the pull request"
                logging.info('---Processing Pull Request payload----')
                logging.info('USERINFO:%s' ,  data['pull_request']['user']['login'])
                logging.info('TITLE:%s' , data['pull_request']['title'])
                logging.info('ORIGINATING BRANCH:%s' , data['pull_request']['head']['ref'])
                branch=(data['pull_request']['head']['ref'])
            
    return "GithubPullRequestBambooBuilder reporting back (PUT) Originating branch is: {0}".format(branch)

    
if __name__ == "__main__":
   main(sys.argv[1:])
