import psycopg2
import os

from classes.loghandler import LogHandler
from helpers.pgwputils import get_installbase

class Exporter:
    
    def __init__(self, mconnection, dconnection):
        self.mconnection = mconnection
        self.dconnection = dconnection
        
    def export_statements(self,nowepoch,nowtime):
      try:
        self.dconnection.logger.log("Export Statements Started")
        mcursor = self.mconnection.connection.cursor()
        dcursor = self.dconnection.connection.cursor()
        mcursor.execute(u"SELECT column_name FROM information_schema.columns"+\
                        u" where table_name = 'pg_stat_statements' ORDER BY column_name ASC")
        crows = mcursor.fetchall()
        cols = []
        for c in crows:
            cols.append(c[0])
        mcolstring = ','.join(cols)
        mcursor.execute(u"SELECT {} FROM pg_stat_statements LIMIT 1000".format(mcolstring))
        srows = mcursor.fetchall()
        for s in srows:
            vals = []
            for i in range(0,len(s)):
                value = str(s[i]).replace("'","''")
                vals.append(u"'{}'".format(value))
            dcolstring = mcolstring  + ',mtime_epoch,mtime'
            valstring = ','.join(map(str,vals))
            valstring = valstring + u",'{}','{}'".format(str(nowepoch),str(nowtime))
            dquery = u"INSERT INTO pgwp.statements ({}) values ({})".format(dcolstring,str(valstring))
            dcursor.execute(dquery)

        mcursor.close()
        dcursor.close()
        self.dconnection.connection.commit()
        self.mconnection.connection.commit()
        self.dconnection.logger.log("Export Statements Complete Success")
        
      except (Exception, psycopg2.Error) as error:                
        self.dconnection.logger.log(u"Export Statements Complete Failure : {}".format(str(error)))
        
        
    def export_activity(self):
        pass
        
    def __str__(self):
        return str(self.__dict__)
 
# Special Helpers
 

