# mySQL Bamboo build vs Github branch checker
# mika.nokka1@gmail.com

import MySQLdb
import netrc
import logging
import sys, getopt, re

__version__ = "0.1"
thisFile = __file__

    
def main(argv):
    
    dbinfo="sqldb.com"
    sqldb="bamboo_4"
    heavy=False

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


    

    branch="new_feature_V3"
    cursor=db.cursor()

    sql = """SELECT p.full_key, p.BUILD_ID, b.full_key, b.title, b.master_id 
      FROM BUILD p 
      JOIN BUILD b ON p.build_id = b.master_id 
      WHERE b.title="{0}" 
      ORDER BY 1 DESC""".format(branch) 
      #sql2="SELECT VERSION()"
 
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        logging.debug("---------------------------------------------------------")
        logging.debug( "Full query results: {0}".format(results))

        for row in results:
           logging.debug("---------------------------------------------------------")
           logging.debug(row)
           build=row[0]  
           gitbranch=row[3] 
           logging.info( "--> Bamboo build:%s" %build)
           logging.info( "------> Builds Github branch:%s" %gitbranch)

    except (MySQLdb.Error, MySQLdb.Warning) as e:
       logging.error("SQL query error:{0}".format(e))
        
    db.close()




if __name__ == "__main__":
        main(sys.argv[1:])


