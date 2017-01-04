# Bamboo build starter
# mika.nokka1@gmail.com

import MySQLdb
import netrc
import logging
import sys, getopt, re
import requests,netrc


def main(argv):
    BambooSteps("https://bamboo.almdemo.fi","GITHUBINT-SGF")

################################################################
# server=Bamboo server
# branch=Bamboo build plan to be build
#

def BambooSteps(server,theplan):

    #check password from .netrc
    # REMEMBER CHMOD 600 RIGHTS
    credentials = netrc.netrc()
    auth = credentials.authenticators(server)
    
    if auth:
        user = auth[0]
        password = auth[2]
        logging.debug("---> Got netrc authentication bits OK")
    else:
        logging.error( "---> ERROR: .netrc file problem EXITING!")
        sys.exit(1)
    
    
    
    
    data = {
      'Default Stage': '',
      'ExecuteAllStages': ''
    }
    
    URL="{0}/rest/api/latest/queue/{1}".format(server,theplan)
    #requests.post('https://bamboo.almdemo.fi/rest/api/latest/queue/GITHUBINT-SGF', data=data, auth=(user, password))
    requests.post(URL, data=data, auth=(user, password))
    #''http://bamboo.almdemo.fi/rest/api/latest/queue/GITHUBINT-SGF'

if __name__ == "__main__":
        main(sys.argv[1:])

