import json
import logging
import time

from classes.loghandler import LogHandler
from classes.exporter import Exporter
 
def monitor(mconnection,dconnection,opts,duration):
    
 try:
    exporter = Exporter(mconnection,dconnection)
    starttime = mconnection.now(u'minute')
    startepoch = mconnection.nowepoch(u'minute')
    endepoch = startepoch + (int(duration) * 60)
    nowepoch = mconnection.nowepoch(u'second') 
    nowtime = mconnection.now(u'second')
    nextepoch = startepoch
    while nowepoch <= endepoch:
        exporter.export_statements(nowepoch,nowtime)
        exporter.export_activity()
        
        nextepoch = nextepoch+60    
        nowepoch = mconnection.nowepoch(u'second')
        nowtime = mconnection.now(u'second')
        time.sleep(nextepoch-nowepoch)

 except Exception as e:
    exceptionlogger = LogHandler(u'/var/log/pgwp/pgwp.log',u'[monitor] ')
    exceptionlogger.logprint(u'Unexpected error during monitoring : {}'.format(str(e)))
    return False
