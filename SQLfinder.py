# mySQL Bamboo build vs Github branch checker
# mika.nokka1@gmail.com

import MySQLdb
import netrc
import logging
import sys, getopt, re

__version__ = "0.1"

dbinfo="sqldb.com"
sqldb="bamboo_4"

loglevel = logging.DEBUG # Default logging level INFO, override with '-d' for logging.DEBUG
logging.basicConfig(level=loglevel) 


#check password from .netrc
# REMEMBER CHMOD 600 RIGHTS
credentials = netrc.netrc()
auth = credentials.authenticators(dbinfo)

if auth:
    user = auth[0]
    password = auth[2]
    logging.debug("---> Got netrc authentication bits OK")
else:
    logging.error( "---> ERROR: .netrc file problem EXITING!")
    sys.exit(1)

 
try:
    db = MySQLdb.connect("localhost",user,password,sqldb)
    logging.debug("---> Database logging OK")
except Exception,e:
    logging.error("Failed to connect to mySQL: %s" % e)
    sys.exit(1)


# disconnect from server
db.close()
