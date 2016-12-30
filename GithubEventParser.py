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

__version__ = "0.1"

from flask import Flask, request   # pip install flask
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
    app.run(debug=True)
      
    
 
@app.route("/<version_id_projectKey>", methods=["GET", "POST"])
def webhook(version_id_projectKey):
   
    global ConfDictionary
    logging.info("---> Hook entry:%s" % version_id_projectKey)
    
   
    
    if request.method == "GET":
        return "GithubPullRequestBambooBuilder reporting back: OK"
    else:   # Do the release notes generation
        data = request.get_json() #(force=True)
        logging.info( "--> Received data")
        logging.info( "%s" % pprint(data))
       
        logging.debug('JSON Headers: %s', request.headers) 
        logging.debug('JSON Body: %s', request.get_data())
        
        

@app.route('/')
def hello_world():  
    return "Hello World! Flask server here!"

if __name__ == "__main__":
   main(sys.argv[1:])
