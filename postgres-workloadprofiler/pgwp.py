import time
import datetime
import logging
import os


from pgwp_menu import *
from pgwp_process import *

from classes.defaults import CommandDefaults
from helpers.cbutils import get_installbase,process_timeperiod
import commands 
import daemons



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
    if not connection.valid:
            print(u"pgwp: Cannot process connection info [{}]".format(opts.monitorconnection))
            sys.exit(1)
    else:
        if not monitorconnection.testQuery(u"SELECT query, calls, total_time FROM pg_stat_statements"):
            print(u"pgwp: Monitoring failure - No access to pg_stat_statements [{}]".format(opts.monitorconnection))
            monitorconnection.close()
            sys.exit(1)
          
                        
            
    if len(args) == 0: 
        print(u"pgwp: Cannot process command - please supply a command")
        sys.exit(1)
    
    if args[0] == u"monitor":
        valid_selection = process_monitor(monitorconnection,args,opts)
 


    if not valid_selection:
       print(u"pgwp: Command not recognised")
       
