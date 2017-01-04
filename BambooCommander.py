# Bamboo build starter
# mika.nokka1@gmail.com

import MySQLdb
import netrc
import logging
import sys, getopt, re
import requests,netrc
import logging

def main(argv):
    BambooSteps("https://bamboo.almdemo.fi","GITHUBINT-SGF","DEBUG")

################################################################
# server=Bamboo server
# branch=Bamboo build plan to be build
#

def BambooSteps(server,theplan,debuglevel):


    if (debuglevel=="DEBUG"):
        loglevel = logging.DEBUG # Default logging level INFO, override with '-d' for logging.DEBUG
    elif (debuglevel=="INFO"):
        loglevel = logging.INFO # Default logging level INFO, override with '-d' for logging.DEBUG
    logging.basicConfig(level=loglevel)

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
    r=requests.post(URL, data=data, auth=(user, password))
    #''http://bamboo.almdemo.fi/rest/api/latest/queue/GITHUBINT-SGF'
    
    logging.debug("Bamboo feedback:")
    logging.debug(r.status_code)
    logging.debug(r.headers)
    if (r.status_code==requests.codes.ok):
        logging.info("---> Bamboo build:{0} commanded OK to be built".format(theplan))
    else:
        logging.info("---> ERROR: Bamboo build:{0} commanding error:{1}".format(theplan,r.status_code))

if __name__ == "__main__":
        main(sys.argv[1:])

