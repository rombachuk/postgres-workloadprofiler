import os
import subprocess
import datetime

class LogHandler:

    def __init__(self,logfile,prefix,silent=False):
        self.logfile = logfile
        self.prefix = prefix
        self.printsilent = silent
        if not os.path.exists(self.logfile):
         subprocess.call([u"touch",self.logfile])

        
    def setSilent(self,silent):
        self.printsilent = silent
    
    def log(self,istring):
        if os.path.exists(self.logfile):
         now_pretty = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S.%f")
         lf = open(self.logfile,u'a')
         lf.write(u'{},{} {}\n'.format(str(now_pretty),self.prefix,str(istring)))
         lf.flush()
         lf.close()
         
    def logprint(self,istring):
        if os.path.exists(self.logfile):
         now_pretty = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S.%f")
         lf = open(self.logfile,u'a')        
         lf.write(u'{},{} {}\n'.format(str(now_pretty),self.prefix, str(istring)))
         if not self.printsilent:
             print(str(istring))
         lf.flush()
         lf.close()        
         

