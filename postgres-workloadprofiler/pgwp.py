import time
import datetime
import logging
import os


from pgwp_menu import *
from pgwp_process import *

from classes.defaults import CommandDefaults
from classes.connection import Connection
from helpers.pgwputils import get_installbase

defaults_file = os.path.join(get_installbase(),u"resources/configuration/pgwp.conf")
logfilename = u"/var/log/pgwp/pgwp.log"

logging.basicConfig(filename = logfilename, level=logging.WARN,
                    format=u'%(asctime)s[%(module)-5s:%(funcName)-5s] (%(processName)-5s) %(message)s',
                    )

if __name__ == u"__main__":

    valid_selection = False
    
    defaults = CommandDefaults(defaults_file)
    opts, args = options(defaults)
    monitorconnection = Connection(opts.monitorconnection)
    if not monitorconnection.valid:
            print(u"pgwp: Cannot process monitor connection info [{}] reason [{}]".format(opts.monitorconnection,monitorconnection.failurereason))
            sys.exit(1)
    else:
        if not monitorconnection.testQuery(u"SELECT query, calls, total_time FROM pg_stat_statements",limit=1):
            print(u"pgwp: Monitoring failure - No access to pg_stat_statements [{}]".format(opts.monitorconnection))
            monitorconnection.connection.close()
            sys.exit(1)
          
    dashboardconnection = Connection(opts.dashboardconnection)  
    if not dashboardconnection.valid:
            print(u"pgwp: Cannot process dashboard connection info [{}] reason [{}]".format(opts.dashboardconnection,dashboardconnection.failurereason))
            sys.exit(1)
    else:
        if not dashboardconnection.testQuery(u"SELECT * FROM pgwp.statements",limit=1):
            print(u"pgwp: Dashboarding failure - No schema - creating...".format(opts.dashboardconnection))
            process_dashboardcreateschema(dashboardconnection,args,opts)
            if not dashboardconnection.testQuery(u"SELECT * FROM  pgwp.statements",limit=1):
                print(u"pgwp: Dashboarding failure - failed to create schema".format(opts.dashboardconnection))
                dashboardconnection.connection.close()
                sys.exit(1)                  
            
    if len(args) == 0: 
        print(u"pgwp: Cannot process command - please supply a command")
        sys.exit(1)
    
    if args[0] == u"monitor":
        valid_selection = process_monitor(monitorconnection,dashboardconnection,args,opts)
        
    elif args[0] == u"dashboard" and args[1] == u"createschema":
        valid_selection = process_dashboardcreateschema(dashboardconnection,args,opts)
 


    if not valid_selection:
       print(u"pgwp: Command not recognised")
       
