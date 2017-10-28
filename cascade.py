import datetime

import mysql.connector

config = {
  'user': 'ruchir',
  'password': 'TnKYH1yV',
  'host': 'sunapee.cs.dartmouth.edu',
  'database': 'ruchir_db',
  'raise_on_warnings': True,
}



class Cas(object):
    def __init__(self):
        self.check = False

    def cascade_exec(self, a, b):
        # returns two string. Which can be passed to executor in main file
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        cursor.execute(a, b)
        for e in cursor:
            print e
        cnx.commit()
        cursor.close()
        cnx.close()

    def sql_return(self, a, b):
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        cursor.execute(a, b)
        l = []
        for e in cursor:
            l.append(e)
        return l
